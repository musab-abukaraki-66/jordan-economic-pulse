"""M05: INDEPENDENT baseline KPIs. Reads raw WB zips and raw CBJ xlsx directly (own code path, not staging). Output: docs/validation/baseline_kpis.csv"""
import zipfile, glob, io, re, os, pandas as pd, numpy as np
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
RAW=str(REPO / "data" / "raw")
OUT=str(REPO / "docs" / "validation" / "baseline_kpis.csv")
def wb(code):
    z=glob.glob(RAW+f"/worldbank\WB_{code}_all_countries_csv.zip")[0]
    with zipfile.ZipFile(z) as f: d=pd.read_csv(f.open([n for n in f.namelist() if n.startswith("API_")][0]),skiprows=4)
    r=d[d["Country Code"]=="JOR"].iloc[0]; return {int(c):r[c] for c in d.columns if c.isdigit() and pd.notna(r[c])}
W={k:wb(k) for k in ["NY.GDP.MKTP.CD","NY.GDP.MKTP.KD.ZG","NY.GDP.PCAP.CD","FP.CPI.TOTL.ZG","SL.UEM.TOTL.ZS","SP.POP.TOTL","TX.VAL.MRCH.CD.WT","TM.VAL.MRCH.CD.WT","BN.GSR.GNFS.CD","BN.CAB.XOKA.CD","BN.CAB.XOKA.GD.ZS","BX.TRF.PWKR.CD.DT","BX.KLT.DINV.CD.WD","FI.RES.TOTL.CD"]}
def cbj_row(fname,year,cols):
    d=pd.read_excel(RAW+f"/cbj\{fname}",header=None)
    yc=None
    for j in range(d.shape[1]):
        m=d[j].astype(str).str.strip().str.replace(r"^\(\d\)\s*","",regex=True).str.replace(r"\.0$","",regex=True)
        if (m==str(year)).sum()==1 and d.index[m==str(year)][0]>10: yc=j; ri=d.index[m==str(year)][0]; 
    # year column = the rightmost column that holds the label; validate by reading positions from excel letters
    return d,ri,yc
def cbj_vals(fname,year,letters,ycol_letter):
    from openpyxl.utils import column_index_from_string as ci
    d=pd.read_excel(RAW+f"/cbj\{fname}",header=None)
    yj=ci(ycol_letter)-1
    lab=d[yj].astype(str).str.strip().str.replace(r"^\(\d\)\s*","",regex=True).str.replace(r"\.0$","",regex=True)
    idx=d.index[lab==str(year)]; assert len(idx)>=1,(fname,year)
    r=idx[0]; return {l:float(d.iloc[r,ci(l)-1]) for l in letters}
CAT=dict(zip("CDEFGHIJKL",["Other","MiscManuf","Machinery","ManufGoods","Chemicals","OilsFats","Fuels","Crude","BevTob","Food"]))
imp=lambda y: cbj_vals("imports_by_commodity_according_to_s.i.t.c..xlsx",y,list(CAT),"O")
exp=lambda y: cbj_vals("domestic_exports_by_commodity_according_to_s.i.t.c..xlsx",y,list(CAT),"O")
GEO=dict(zip("CDEFGHIJ",["OtherCountries","Japan","India","China","USA","OtherEurope","EU","Arab"]))
gexp=lambda y: cbj_vals("geographic_distribution_of_exports.xlsx",y,list(GEO),"M")
gimp=lambda y: cbj_vals("geographic_distribution_of_imports.xlsx",y,list(GEO),"M")
Y=2024; rows=[]
def add(i,name,yr,val,unit,defn): rows.append(dict(ID=i,KPI=name,Year=yr,Value=val,Unit=unit,Definition=defn))
g=lambda k,y: W[k][y]
add("B01","GDP",Y,g("NY.GDP.MKTP.CD",Y),"USD","WB NY.GDP.MKTP.CD")
add("B02","Real GDP growth",Y,g("NY.GDP.MKTP.KD.ZG",Y),"%","WB NY.GDP.MKTP.KD.ZG")
add("B03","GDP per capita",Y,g("NY.GDP.PCAP.CD",Y),"USD","WB NY.GDP.PCAP.CD")
add("B04","CPI inflation",Y,g("FP.CPI.TOTL.ZG",Y),"%","WB FP.CPI.TOTL.ZG")
add("B05","Unemployment",Y,g("SL.UEM.TOTL.ZS",Y),"%","WB SL.UEM.TOTL.ZS (ILO modelled)")
add("B06","Population",Y,g("SP.POP.TOTL",Y),"persons","WB SP.POP.TOTL")
add("B07","Population growth",Y,(g("SP.POP.TOTL",Y)/g("SP.POP.TOTL",Y-1)-1)*100,"%","pop(t)/pop(t-1)-1")
xe,mi=g("TX.VAL.MRCH.CD.WT",Y),g("TM.VAL.MRCH.CD.WT",Y)
add("B08","Merchandise exports (total)",Y,xe,"USD","WB TX.VAL.MRCH.CD.WT (incl. re-exports)")
add("B09","Merchandise imports",Y,mi,"USD","WB TM.VAL.MRCH.CD.WT")
add("B10","Merchandise trade balance",Y,xe-mi,"USD","exports - imports")
add("B11","Trade balance % GDP",Y,(xe-mi)/g("NY.GDP.MKTP.CD",Y)*100,"%","balance / GDP")
add("B12","Export coverage of imports",Y,xe/mi*100,"%","exports / imports")
add("B13","Net goods & services (BoP)",Y,g("BN.GSR.GNFS.CD",Y),"USD","WB BN.GSR.GNFS.CD")
add("B14","Current account",Y,g("BN.CAB.XOKA.CD",Y),"USD","WB BN.CAB.XOKA.CD")
add("B15","Current account % GDP",Y,g("BN.CAB.XOKA.GD.ZS",Y),"%","WB BN.CAB.XOKA.GD.ZS")
add("B16","Remittances received",Y,g("BX.TRF.PWKR.CD.DT",Y),"USD","WB BX.TRF.PWKR.CD.DT")
add("B17","FDI net inflows",Y,g("BX.KLT.DINV.CD.WD",Y),"USD","WB BX.KLT.DINV.CD.WD")
add("B18","Total reserves incl. gold",Y,g("FI.RES.TOTL.CD",Y),"USD","WB FI.RES.TOTL.CD")
add("B19","Import coverage (months)",Y,g("FI.RES.TOTL.CD",Y)/mi*12,"months","reserves / merch imports * 12 (derived)")
add("B20","Remittances + FDI as % of merchandise deficit",Y,(g("BX.TRF.PWKR.CD.DT",Y)+g("BX.KLT.DINV.CD.WD",Y))/(mi-xe)*100,"%","context ratio, NOT an identity")
add("B21","Reserve change",Y,g("FI.RES.TOTL.CD",Y)-g("FI.RES.TOTL.CD",Y-1),"USD","reserves(t)-reserves(t-1); includes valuation effects")
add("B22","Avg real GDP growth 2010-2024","2010-2024",np.mean([W["NY.GDP.MKTP.KD.ZG"][y] for y in range(2010,2025)]),"%","simple mean of annual growth")
add("B23","Cumulative remittances 2015-2024","2015-2024",sum(W["BX.TRF.PWKR.CD.DT"][y] for y in range(2015,2025)),"USD","sum")
add("B24","Avg trade deficit % GDP 1990-2024","1990-2024",np.mean([(W["TX.VAL.MRCH.CD.WT"][y]-W["TM.VAL.MRCH.CD.WT"][y])/W["NY.GDP.MKTP.CD"][y]*100 for y in range(1990,2025)]),"%","simple mean of annual ratios")
add("B25","Peak unemployment 1991-2025","1991-2025",max(v for y,v in W["SL.UEM.TOTL.ZS"].items() if y>=1991),"%","max")
add("B26","Merchandise trade balance 2025 (provisional)",2025,W["TX.VAL.MRCH.CD.WT"][2025]-W["TM.VAL.MRCH.CD.WT"][2025],"USD","WB 2025")
# CBJ (JD thousand), 2022
Yc=2022; I=imp(Yc); E=exp(Yc); GX=gexp(Yc); GM=gimp(Yc)
add("C01","CBJ imports total (sum of commodity groups)",Yc,sum(I.values()),"JD thousand","sum of 10 SITC groups")
add("C02","CBJ domestic exports total (sum of commodity groups)",Yc,sum(E.values()),"JD thousand","sum of 10 SITC groups")
add("C03","Fuel share of imports",Yc,I["I"]/sum(I.values())*100,"%","Mineral fuels / total imports")
add("C04","Food share of imports",Yc,I["L"]/sum(I.values())*100,"%","Food & live animals / total imports")
add("C05","Arab share of domestic exports",Yc,GX["J"]/sum(GX.values())*100,"%","Arab / sum of partner groups")
add("C06","EU share of imports",Yc,GM["I"]/sum(GM.values())*100,"%","EU / sum of partner groups")
add("C07","Domestic export coverage of imports (CBJ)",Yc,sum(E.values())/sum(I.values())*100,"%","domestic exports / imports")
add("C08","Chemicals share of domestic exports",Yc,E["G"]/sum(E.values())*100,"%","Chemicals / total domestic exports")
add("C09","China share of imports",Yc,GM["F"]/sum(GM.values())*100,"%","China / sum of partner groups")
add("C10","Fuel share of imports 2000",2000,imp(2000)["I"]/sum(imp(2000).values())*100,"%","Mineral fuels / total imports")
add("C11","Imports total 2012 via partner table",2012,sum(gimp(2012).values()),"JD thousand","commodity 2012 unavailable (source copy error)")
add("C12","CBJ imports total 2010",2010,sum(imp(2010).values()),"JD thousand","sum")
out=pd.DataFrame(rows); out.to_csv(OUT,index=False,encoding="utf-8")
pd.set_option("display.width",220); pd.set_option("display.float_format",lambda v:f"{v:,.4f}")
print(out[["ID","KPI","Year","Value","Unit"]].to_string(index=False))
