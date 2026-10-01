"""M04: curate the in-scope model tables (Power Query loads these CSVs). Reads staging produced by m03_build_tidy.py."""
import pandas as pd, os
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
R=str(REPO)
S=R+"/data/staging"; C=R+"/data/curated"; os.makedirs(C,exist_ok=True)
Y0,Y1=1990,2025
wb=pd.read_csv(S+"/wb_long.csv"); wb=wb[(wb["Country Code"]=="JOR")&wb.Year.between(Y0,Y1)]
MAP={"NY.GDP.MKTP.CD":"GDP_USD","NY.GDP.MKTP.KD.ZG":"GDP_Growth_Pct","NY.GDP.PCAP.CD":"GDP_PerCapita_USD","FP.CPI.TOTL.ZG":"Inflation_Pct",
     "SL.UEM.TOTL.ZS":"Unemployment_Pct","SP.POP.TOTL":"Population","TX.VAL.MRCH.CD.WT":"MerchExports_USD","TM.VAL.MRCH.CD.WT":"MerchImports_USD",
     "BN.GSR.GNFS.CD":"NetGoodsServices_USD","BN.CAB.XOKA.CD":"CurrentAccount_USD","BN.CAB.XOKA.GD.ZS":"CurrentAccount_PctGDP",
     "BX.TRF.PWKR.CD.DT":"Remittances_USD","BX.KLT.DINV.CD.WD":"FDI_USD","FI.RES.TOTL.CD":"Reserves_USD"}
eco=wb[wb.IndicatorCode.isin(MAP)].pivot(index="Year",columns="IndicatorCode",values="Value").rename(columns=MAP)
eco=eco.reindex(range(Y0,Y1+1))[list(MAP.values())]; eco.index.name="Year"
assert eco.shape[1]==14
eco.reset_index().to_csv(C+"/FactEconomy.csv",index=False)
dy=pd.DataFrame({"Year":range(Y0,Y1+1)}); dy["Decade"]=(dy.Year//10*10).astype(str)+"s"; dy["IsProvisional"]=(dy.Year==2025)
dy.to_csv(C+"/DimYear.csv",index=False)
COMM=["Food & Live Animals","Beverages & Tobacco","Crude Materials (Inedible)","Mineral Fuels & Lubricants","Animal & Vegetable Oils & Fats","Chemicals","Manufactured Goods (by Material)","Machinery & Transport Equipment","Misc. Manufactured Articles","Other"]
PART=["Arab Countries","European Union","Other European Countries","U.S.A.","China","India","Japan","Other Countries"]
dc=pd.DataFrame({"CommodityKey":range(1,11),"Commodity":COMM,"SortOrder":range(1,11)})
SHORT={"Crude Materials (Inedible)":"Crude materials","Animal & Vegetable Oils & Fats":"Oils & fats","Manufactured Goods (by Material)":"Manufactured goods","Machinery & Transport Equipment":"Machinery & transport","Misc. Manufactured Articles":"Misc. manufactured","Food & Live Animals":"Food & live animals","Beverages & Tobacco":"Beverages & tobacco"}
dc_out=dc.copy(); dc_out["Commodity"]=dc_out["Commodity"].replace(SHORT); dc_out.to_csv(C+"/DimCommodity.csv",index=False)
dp=pd.DataFrame({"PartnerKey":range(1,9),"Partner":PART,"SortOrder":range(1,9)}); dp.to_csv(C+"/DimPartner.csv",index=False)
df=pd.DataFrame({"FlowKey":[1,2],"Flow":["Imports","Domestic exports"]}); df.to_csv(C+"/DimFlow.csv",index=False)
def load(t,flowkey,col,dim,keycol,lab):
    x=pd.read_csv(S+f"/cbj_{t}_long.csv"); x=x[x.Year.between(Y0,2022)].dropna(subset=["ValueJDk"])
    k=dict(zip(dim[lab],dim[keycol])); x[keycol]=x.Category.map(k); assert x[keycol].notna().all(),t
    x["FlowKey"]=flowkey; return x[["Year","FlowKey",keycol,"ValueJDk"]]
fc=pd.concat([load("imports_commodity",1,"","CommodityKey" and dc,"CommodityKey","Commodity"),load("exports_commodity",2,"",dc,"CommodityKey","Commodity")]).sort_values(["Year","FlowKey","CommodityKey"])
fp=pd.concat([load("imports_geo",1,"",dp,"PartnerKey","Partner"),load("exports_geo",2,"",dp,"PartnerKey","Partner")]).sort_values(["Year","FlowKey","PartnerKey"])
for n,x,k in (("FactTradeCommodity",fc,["Year","FlowKey","CommodityKey"]),("FactTradePartner",fp,["Year","FlowKey","PartnerKey"])):
    assert not x.duplicated(k).any(); x.to_csv(C+f"/{n}.csv",index=False); print(n,len(x),"rows; years",x.Year.min(),x.Year.max(),"; 2012 imports rows:",len(x[(x.Year==2012)&(x.FlowKey==1)]))
print("FactEconomy",eco.shape,"; nulls per column:\n",eco.isna().sum()[eco.isna().sum()>0].to_dict())
print(eco.loc[[1990,2000,2010,2020,2024,2025]].round(2).T.to_string())
