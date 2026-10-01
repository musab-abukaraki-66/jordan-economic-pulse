import glob, os, re, openpyxl
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]
ROOT=str(REPO / "data" / "raw" / "cbj")
yr=re.compile(r"^(19|20)\d\d$")
for f in sorted(glob.glob(ROOT+"/*.xlsx")):
    ws=openpyxl.load_workbook(f,data_only=True).worksheets[0]
    print("\n####",os.path.basename(f),ws.dimensions)
    hits=[]
    for r in ws.iter_rows():
        for c in r:
            v=c.value
            if v is None: continue
            s=str(v).strip()
            if s.endswith(".0"): s=s[:-2]
            if yr.match(s): hits.append((c.row,c.column_letter,s)); break
    if not hits: print("  no year cells"); continue
    cols={}
    for r,cl,s in hits: cols.setdefault(cl,[]).append((r,s))
    for cl,l in cols.items():
        print(f"  year col {cl}: n={len(l)} rows {l[0][0]}..{l[-1][0]} years {l[0][1]}..{l[-1][1]} first10={[x[1] for x in l[:10]]}")
    # detect year-in-header (columns)
    hdr=[]
    for r in ws.iter_rows(min_row=1,max_row=12):
        ys=[(c.column_letter,str(c.value)) for c in r if c.value is not None and yr.match(str(c.value).strip().replace('.0',''))]
        if len(ys)>3: hdr.append((r[0].row,ys[0],ys[-1],len(ys)))
    if hdr: print("  years-in-header rows:",hdr)
    # print the rows around the first hit fully
    r0=hits[0][0]
    for r in ws.iter_rows(min_row=r0,max_row=r0+2,values_only=True):
        print("   row:",[ (str(v)[:10] if v is not None else '') for v in r[:16]])
