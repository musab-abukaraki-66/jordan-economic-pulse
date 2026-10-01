import pandas as pd, numpy as np, os
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
ROOT=str(REPO)
S=ROOT+"/data/staging"; D=ROOT+"/docs/audit"
out=[]
def log(*a):
    s=" ".join(str(x) for x in a); out.append(s); print(s)
res=pd.read_csv(S+"/cbj_reserves_long.csv"); pv=res.pivot(index="Year",columns="Item",values="Value")
calc=pv["Gold (value)"]+pv["SDRs"]+pv["Cash, Balances & Deposits"]+pv["Bonds & Treasury Bills"]-pv["Licensed banks deposits"]
d=(calc-pv["Gross foreign reserves (JD)"]).abs()
log("Gross reserves = gold+SDR+cash+bonds-licensed banks FC deposits: max|diff|=%.2f, yrs within 0.2: %d/%d"%(d.max(),(d<0.2).sum(),len(d)))
log("Gross reserves USD / JD ratio (implied peg):", (pv["Gross foreign reserves (USD)"]/pv["Gross foreign reserves (JD)"]).describe()[["min","max"]].round(4).to_dict())
log("Import coverage months (stray check):", pv["Import coverage (months)"].loc[[1993,1994,1999,2000,2021]].to_dict())
wb=pd.read_csv(S+"/wb_long.csv"); ind=pd.read_csv(S+"/wb_indicators.csv")
jor=wb[wb["Country Code"]=="JOR"].pivot(index="Year",columns="IndicatorCode",values="Value").reindex(range(1960,2026))
log("\nJORDAN WB null classification (leading=before start, trailing=after last, interior=genuinely missing)")
rows=[]
for c in jor.columns:
    s=jor[c]; nn=s.dropna()
    if nn.empty: rows.append((c,0,66,66,0,0)); continue
    lead=int(s.index.min()<nn.index.min())*int(nn.index.min()-1960); trail=int(2025-nn.index.max()); interior=int(len(range(nn.index.min(),nn.index.max()+1))-len(nn))
    rows.append((c,len(nn),lead,trail,interior,int(nn.index.min())))
t=pd.DataFrame(rows,columns=["Indicator","NonNull","LeadingNull","TrailingNull","InteriorNull","FirstYear"]); log(t.to_string(index=False))
t.to_csv(D+"/wb_jordan_null_profile.csv",index=False)
log("\nAbnormal-value scan (Jordan)")
for c,lab in (("NY.GDP.MKTP.KD.ZG","GDP growth %"),("FP.CPI.TOTL.ZG","CPI inflation %"),("SL.UEM.TOTL.ZS","Unemployment %"),("BX.KLT.DINV.CD.WD","FDI USD"),("BN.CAB.XOKA.GD.ZS","CA % GDP"),("SP.POP.TOTL","Population")):
    s=jor[c].dropna(); log(f" {lab}: min {s.min():.2f} ({s.idxmin()}), max {s.max():.2f} ({s.idxmax()}), last {s.index.max()}={s.iloc[-1]:.2f}")
pop=jor["SP.POP.TOTL"].dropna(); ch=pop.pct_change().dropna(); log(" pop yoy>6%:",ch[ch>0.06].round(3).to_dict())
log(" negatives FDI yrs:",jor["BX.KLT.DINV.CD.WD"][jor["BX.KLT.DINV.CD.WD"]<0].index.tolist())
# identity checks WB
g=jor["NY.GDP.MKTP.CD"]; pc=jor["NY.GDP.PCAP.CD"]; pop=jor["SP.POP.TOTL"]
r=(g/pop/pc).dropna(); log(" GDP/pop vs GDP per capita: ratio min %.4f max %.4f"%(r.min(),r.max()))
tr=(jor["TX.VAL.MRCH.CD.WT"]-jor["TM.VAL.MRCH.CD.WT"]); log(" merch trade balance 2024:",round(tr.loc[2024]/1e9,2),"bn USD; 2025:",round(tr.loc[2025]/1e9,2) if not np.isnan(tr.loc[2025]) else 'NA')
cagr=jor["NY.GDP.MKTP.KD.ZG"].dropna(); 
# WB vs CBJ reserves
cb=(pv["Gross foreign reserves (USD)"]*1e6); w=jor["FI.RES.TOTL.CD"]
j=pd.concat([cb,w],axis=1,keys=["CBJ","WB"]).dropna(); j["ratio"]=j.WB/j.CBJ
log("\nWB total reserves(incl gold) / CBJ gross reserves USD: overlap %d yrs, ratio min %.3f median %.3f max %.3f"%(len(j),j.ratio.min(),j.ratio.median(),j.ratio.max()))
log(j.loc[[1995,2005,2015,2021]].round(3).to_string())
# WB 2025 / latest
log("\nJordan latest non-null year per indicator (top):"); log(t.assign(Last=[int(jor[c].dropna().index.max()) if jor[c].notna().any() else None for c in t.Indicator]).sort_values("Last").head(40).to_string(index=False))
open(D+"/m03c_wb_audit.txt","w",encoding="utf-8").write("\n".join(out))
