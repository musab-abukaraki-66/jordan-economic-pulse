"""Generates the Jordan Economic Pulse report (theme, canvas image, report.json, pages) from the design-system spec in pbir_lib.py.
Run: python build_report.py   (close Desktop first; reopen the .pbip afterwards)"""
import os, sys, json, shutil
sys.path.insert(0, os.path.dirname(__file__))
from pbir_lib import *
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.environ.get("JP_OUT") or str(__import__("pathlib").Path(__file__).resolve().parents[2] / "powerbi")
REP = os.path.join(ROOT, "JordanPulse.Report")
RES = os.path.join(REP, "StaticResources", "RegisteredResources")
os.makedirs(RES, exist_ok=True)
D = DS

# ------------------------------------------------------------ canvas image (soft cool tonal field; glass panels sit on it)
def make_canvas(path):
    W, H = 1440, 900
    base = Image.new("RGB", (W, H), (237, 241, 243))
    for (cx, cy, rx, ry, col, a) in [(120, 40, 560, 420, (196, 224, 226), 150), (1300, 30, 560, 420, (208, 221, 238), 140),
                                       (700, 900, 640, 380, (206, 231, 226), 110), (1330, 860, 420, 300, (240, 228, 200), 120)]:
        layer = Image.new("L", (W, H), 0)
        ImageDraw.Draw(layer).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=a)
        layer = layer.filter(ImageFilter.GaussianBlur(120))
        base.paste(Image.new("RGB", (W, H), col), (0, 0), layer)
    base.save(path, optimize=True)
make_canvas(os.path.join(RES, "bg_canvas.png"))

# ------------------------------------------------------------ theme
def T(c): return {"solid": {"color": c}}
theme = {
    "name": "Jordan Pulse Glass",
    "$schema": "https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.143.json",
    "dataColors": [D["petrol"], D["slate"], D["amber"], "#5E9EA3", "#A8B7C8", "#D3B575", "#3F7C82", "#8AA0B8"],
    "foreground": D["ink"], "foregroundNeutralSecondary": D["mute"], "foregroundNeutralTertiary": D["faint"], "foregroundLight": D["white"],
    "background": D["white"], "backgroundLight": "#F5F8F9", "backgroundNeutral": D["hair"], "secondaryBackground": "#F5F8F9",
    "tableAccent": D["petrol"], "good": D["petrol"], "neutral": D["slate"], "bad": D["amber"],
    "maximum": D["petrol"], "center": "#A8B7C8", "minimum": "#EAF0F2", "null": D["faint"], "hyperlink": D["petrol"], "visitedHyperlink": D["slate"],
    "textClasses": {k: {"fontFace": f, "fontSize": s, "color": c} for k, (f, s, c) in {
        "callout": (D["font_sb"], 28, D["ink"]), "title": (D["font_sb"], 12, D["ink"]), "header": (D["font_sb"], 10, D["ink"]),
        "label": (D["font"], 9, D["mute"]), "largeTitle": (D["font_sb"], 18, D["ink"]), "largeLabel": (D["font"], 10, D["mute"]),
        "semiboldLabel": (D["font_sb"], 9, D["ink"]), "smallLabel": (D["font"], 8, D["faint"]), "lightLabel": (D["font"], 9, D["mute"]),
        "boldLabel": (D["font_sb"], 9, D["ink"])}.items()},
    "visualStyles": {"*": {"*": {
        "background": [{"show": False}], "border": [{"show": False}], "dropShadow": [{"show": False}],
        "title": [{"show": False}], "subTitle": [{"show": False}],
        "categoryAxis": [{"fontFamily": D["font"], "fontSize": 9, "labelColor": T(D["mute"]), "gridlineShow": False}],
        "valueAxis": [{"fontFamily": D["font"], "fontSize": 9, "labelColor": T(D["mute"]), "gridlineColor": T(D["hair"])}],
        "legend": [{"fontFamily": D["font"], "fontSize": 9, "labelColor": T(D["mute"]), "showTitle": False}],
        "labels": [{"show": False}], "plotArea": [{"transparency": 100}]}},
        "lineChart": {"*": {"lineStyles": [{"strokeWidth": 2.25, "showMarker": False, "lineStyle": "solid", "lineChartType": "linear"}]}},
        "areaChart": {"*": {"lineStyles": [{"strokeWidth": 2.25, "lineChartType": "linear"}]}},
        "stackedAreaChart": {"*": {"lineStyles": [{"strokeWidth": 2.25, "lineChartType": "linear"}]}}},
}
write_json(os.path.join(RES, "JordanPulseGlass.json"), theme)

# ------------------------------------------------------------ report.json
report = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.3.0/schema.json",
    "themeCollection": {
        "baseTheme": {"name": "Fluent2-CY26SU09", "reportVersionAtImport": {"visual": "2.13.0", "report": "3.4.0", "page": "2.3.1"}, "type": "SharedResources"},
        "customTheme": {"name": "JordanPulseGlass.json", "reportVersionAtImport": {"visual": "2.13.0", "report": "3.4.0", "page": "2.3.1"}, "type": "RegisteredResources"}},
    "objects": {"outspacePane": [{"properties": {"expanded": lit("false"), "visible": lit("true")}}]},
    "resourcePackages": [
        {"name": "SharedResources", "type": "SharedResources", "items": [{"name": "Fluent2-CY26SU09", "path": "BaseThemes/Fluent2-CY26SU09.json", "type": "BaseTheme"}]},
        {"name": "RegisteredResources", "type": "RegisteredResources", "items": [
            {"name": "JordanPulseGlass.json", "path": "JordanPulseGlass.json", "type": "CustomTheme"},
            {"name": "bg_canvas.png", "path": "bg_canvas.png", "type": "Image"}]}],
    "settings": {"useStylableVisualContainerHeader": True, "defaultFilterActionIsDataFilter": True, "useEnhancedTooltips": True, "useDefaultAggregateDisplayName": True},
}
write_json(os.path.join(REP, "definition", "report.json"), report)

PAGES = [("p01Pulse", "Executive Pulse", "Pulse"), ("p02Growth", "Growth & Prices", "Growth & Prices"),
         ("p03External", "External Position", "External Position"), ("p04Trade", "Trade Structure", "Trade Structure")]
shutil.rmtree(os.path.join(REP, "definition", "pages"), ignore_errors=True)
write_json(os.path.join(REP, "definition", "pages", "pages.json"), {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
    "pageOrder": [p[0] for p in PAGES], "activePageName": "p01Pulse"})

# ------------------------------------------------------------ shared: rail + header
def rail(active):
    v = []
    v.append(glass("railGlass", 24, 24, 232, 852, 1000, radius=22, tr=48))
    v.append(solid("logoMark", 48, 50, 30, 30, 1010, D["petrol"], radius=9))
    v.append(text("logoLetter", 48, 52, 30, 26, 1020, [("J", 13, D["font_sb"], D["white"])], align="center"))
    v.append(text("brand", 86, 47, 160, 40, 1020, None, lines=[[("Jordan Economic", 10.5, D["font_sb"], D["ink"])], [("Pulse", 10.5, D["font_sb"], D["ink"])]]))
    v.append(text("railKicker", 48, 122, 160, 18, 1020, [("REPORT", 7.5, D["font_sb"], D["faint"])]))
    for i, (pid, disp, label) in enumerate(PAGES):
        y = 150 + i * 46
        if i == active:
            v.append(glass(f"navActive{i}", 40, y, 200, 38, 1030, radius=12, tr=8, shadow=False))
            v.append(solid(f"navBar{i}", 40, y + 9, 3, 20, 1040, D["petrol"], radius=2))
        v.append(solid(f"navDot{i}", 56, y + 14, 10, 10, 1050, D["petrol"] if i == active else D["faint"], tr=0 if i == active else 45, shape="ellipse"))
        v.append(button(f"nav{i}", 40, y, 200, 38, 1060, label, pid, active=(i == active), size=10.5))
    v.append(text("yearLabel", 48, 736, 170, 18, 1020, [("REFERENCE YEAR", 7.5, D["font_sb"], D["faint"])]))
    v.append(slicer_year("yearSlicer", 48, 758, 172, 40, 1070))
    v.append(text("railSource", 48, 812, 190, 44, 1020, None, lines=[[("World Bank WDI · CBJ", 8, D["font"], D["faint"])], [("Annual, current US$", 8, D["font"], D["faint"])]]))
    return v

def header(title, sub):
    return [text("pageTitle", 284, 26, 800, 44, 1020, [(title, 20, D["font_sb"], D["ink"])]),
            text("pageSub", 284, 68, 900, 24, 1020, [(sub, 9.5, D["font"], D["mute"])])]

TIME_SERIES = []   # names of visuals not filtered by the year slicer

def kpi(i, label, measure, cap, color, spark=None, spark_color=None):
    x, y, w, h = 288 + i * 286, 112, 270, 122
    v = [glass(f"kpiGlass{i}", x, y, w, h, 1100, radius=18),
         text(f"kpiLabel{i}", x + 16, y + 12, 200, 18, 1110, [(label, 7.5, D["font_sb"], D["mute"])]),
         card(f"kpiValue{i}", x + 12, y + 34, 150, 50, 1110, measure, size=20, color=color),
         card(f"kpiCap{i}", x + 12, y + 76, 236, 48, 1110, cap, size=9, font=D["font"], color=D["mute"])]
    if spark:
        c = chart(f"kpiSpark{i}", x + 154, y + 24, 112, 84, 1120, "lineChart", [spark], show_cat_axis=False, show_val_axis=False, gridlines=False,
                  objects={"dataPoint": [{"properties": {"fill": COL(spark_color or color)}}]}, axis_units=None)
        v.append(c); TIME_SERIES.append(c["name"])
    return v

def panel_title(name, x, y, title, sub, z=1110):
    return [text(name + "T", x, y, 420, 26, z, [(title, 12.5, D["font_sb"], D["ink"])]),
            text(name + "S", x, y + 24, 420, 20, z, [(sub, 9, D["font"], D["mute"])])]

# ------------------------------------------------------------ PAGE 1
def page1():
    v = rail(0) + header("Executive Pulse", "Growth, prices and the external gap · Jordan, 1990–2024 · reference year set on the left")
    v += kpi(0, "MERCHANDISE DEFICIT", "KPI Trade Balance", "Cap Deficit", D["amber"], spark="Trade balance ($bn)")
    v += kpi(1, "EXPORT COVERAGE", "KPI Export Coverage", "Cap Coverage", D["ink"])
    v += kpi(2, "CURRENT ACCOUNT", "KPI Current Account", "Cap Current Account", D["ink"], spark="Current account ($bn)", spark_color=D["slate"])
    v += kpi(3, "RESERVES", "KPI Reserves", "Cap Reserves", D["petrol"], spark="Reserves ($bn)")
    # hero
    v.append(glass("heroGlass", 288, 250, 730, 392, 1100, radius=22))
    v += panel_title("hero", 312, 268, "Exports vs imports", "Total merchandise, US$ bn · the shaded band is the gap")
    area = chart("heroArea", 300, 304, 706, 322, 1110, "stackedAreaChart", ["Exports ($bn)", "Gap ($bn)"], vmin=0, vmax=30, legend=False, gridlines=False,
                 objects={"dataPoint": [{"properties": {"fill": COL("#F7F9FA")}, "selector": {"metadata": "_Measures.Exports ($bn)"}},
                                        {"properties": {"fill": COL("#EEE3CB")}, "selector": {"metadata": "_Measures.Gap ($bn)"}}]})
    line = chart("heroLines", 300, 304, 706, 322, 1120, "lineChart", ["Imports ($bn)", "Exports ($bn)"], vmin=0, vmax=30, legend=False, gridlines=True, tip=["Gap ($bn)", "Export Coverage of Imports (%)", "Current account ($bn)", "Remittances ($bn)", "Reserves ($bn)"],
                 objects={"dataPoint": [{"properties": {"fill": COL(D["slate"])}, "selector": {"metadata": "_Measures.Imports ($bn)"}},
                                        {"properties": {"fill": COL(D["petrol"])}, "selector": {"metadata": "_Measures.Exports ($bn)"}}]})
    v += [area, line]; TIME_SERIES.extend(["heroArea", "heroLines"])
    v.append(card("heroCallout", 330, 336, 330, 44, 1130, "Cap Gap Callout", size=10.5, font=D["font_sb"], color=D["amber"]))
    for k, (lab, col, xx) in enumerate([("Imports", D["slate"], 768), ("Exports", D["petrol"], 846), ("Gap", "#D9C28F", 922)]):
        v.append(solid(f"heroLegDot{k}", xx, 275, 10, 10, 1130, col, shape="ellipse"))
        v.append(text(f"heroLegTxt{k}", xx + 14, 268, 70, 22, 1130, [(lab, 9, D["font"], D["mute"])]))
    # inflows
    v.append(glass("flowGlass", 1034, 250, 382, 392, 1100, radius=22))
    v += panel_title("flow", 1058, 268, "Inflows in context", "Remittances and FDI, US$ bn")
    flow = chart("flowChart", 1046, 304, 358, 282, 1110, "lineChart", ["Remittances ($bn)", "FDI ($bn)"], vmin=None, legend=True,
                 objects={"dataPoint": [{"properties": {"fill": COL(D["petrol"])}, "selector": {"metadata": "_Measures.Remittances ($bn)"}},
                                        {"properties": {"fill": COL(D["slate"])}, "selector": {"metadata": "_Measures.FDI ($bn)"}}]})
    v.append(flow); TIME_SERIES.append("flowChart")
    v.append(card("flowCap", 1058, 572, 340, 48, 1110, "Cap Remittances FDI", size=9, font=D["font_sb"], color=D["mute"]))
    v.append(text("flowNote", 1058, 612, 340, 20, 1110, [("Shown for context — not an accounting identity", 8, D["font"], D["faint"])]))
    # bottom row
    pw = 365
    xs = [288, 669, 1051]
    titles = ["GDP growth, %", "Inflation and unemployment, %", "Reserves, US$ bn"]
    for i, (x, t) in enumerate(zip(xs, titles)):
        v.append(glass(f"botGlass{i}", x, 658, pw, 218, 1100, radius=20))
        v.append(text(f"botT{i}", x + 20, 672, 330, 24, 1110, [(t, 11, D["font_sb"], D["ink"])]))
    g = chart("botGrowth", 300, 700, 341, 140, 1110, "columnChart", ["Growth, +", "Growth, -"], axis_units=None, legend=False,
              objects={"dataPoint": [{"properties": {"fill": COL(D["petrol"])}, "selector": {"metadata": "_Measures.Growth, +"}},
                                     {"properties": {"fill": COL(D["amber"])}, "selector": {"metadata": "_Measures.Growth, -"}}]})
    pj = chart("botPrices", 681, 700, 341, 140, 1110, "lineChart", ["Inflation, %", "Unemployment, %"], axis_units=None, legend=False, vmin=0, vmax=22,
               objects={"dataPoint": [{"properties": {"fill": COL(D["slate"])}, "selector": {"metadata": "_Measures.Inflation, %"}},
                                      {"properties": {"fill": COL(D["amber"])}, "selector": {"metadata": "_Measures.Unemployment, %"}}]})
    rs = chart("botReserves", 1063, 700, 341, 140, 1110, "areaChart", ["Reserves ($bn)"], vmin=0, legend=False)
    v += [g, pj, rs]; TIME_SERIES.extend(["botGrowth", "botPrices", "botReserves"])
    v.append(card("botCap0", 308, 824, 330, 48, 1110, "Cap Growth", size=9, font=D["font_sb"], color=D["mute"]))
    v.append(card("botCap1", 689, 824, 330, 48, 1110, "Cap Prices Jobs", size=9, font=D["font_sb"], color=D["mute"]))
    v.append(card("botCap2", 1071, 824, 330, 48, 1110, "Cap Reserves Line", size=9, font=D["font_sb"], color=D["petrol"]))
    inter = [{"source": "yearSlicer", "target": n, "type": "NoFilter"} for n in TIME_SERIES]
    write_page(REP, "p01Pulse", "Executive Pulse", v, "bg_canvas.png", inter)

def bottom_panel(i, title, chart_v, cap=None, cap_color=None, static_cap=None):
    xs = [288, 669, 1051]; x = xs[i]
    v = [glass(f"botGlass{i}", x, 658, 365, 218, 1100, radius=20), text(f"botT{i}", x + 20, 672, 330, 24, 1110, [(title, 11, D["font_sb"], D["ink"])])]
    v.append(chart_v)
    if cap: v.append(card(f"botCap{i}", x + 20, 824, 330, 48, 1110, cap, size=9, font=D["font_sb"], color=cap_color or D["mute"]))
    if static_cap: v.append(text(f"botCapS{i}", x + 20, 842, 330, 24, 1110, [(static_cap, 9, D["font"], D["mute"])]))
    return v

def bchart(i, name, vtype, measures, **kw):
    xs = [288, 669, 1051]; x = xs[i]
    c = chart(name, x + 12, 700, 341, 140, 1110, vtype, measures, **kw); TIME_SERIES.append(name); return c

def colors(m):   # series colour selectors
    return {"dataPoint": [{"properties": {"fill": COL(col)}, "selector": {"metadata": "_Measures." + name}} for name, col in m]}

def finish(pid, disp, v):
    inter = [{"source": "yearSlicer", "target": n, "type": "NoFilter"} for n in TIME_SERIES]
    write_page(REP, pid, disp, v, "bg_canvas.png", inter)

def legend(v, items, y=268):
    for k, (lab, col, xx) in enumerate(items):
        v.append(solid(f"heroLegDot{k}", xx, y + 7, 10, 10, 1130, col, shape="ellipse"))
        v.append(text(f"heroLegTxt{k}", xx + 14, y, 140, 22, 1130, [(lab, 9, D["font"], D["mute"])]))

def page2():
    TIME_SERIES.clear()
    v = rail(1) + header("Growth & Prices", "Real growth, prices and jobs · Jordan, 1990–2024 · reference year set on the left")
    v += kpi(0, "NOMINAL GDP", "KPI GDP", "Cap GDP", D["ink"], spark="GDP (USD)", spark_color=D["petrol"])
    v += kpi(1, "REAL GDP GROWTH", "KPI GDP Growth", "Cap GDP Growth", D["petrol"], spark="GDP, growth, %")
    v += kpi(2, "CPI INFLATION", "KPI Inflation", "Cap Inflation", D["ink"], spark="Inflation, %", spark_color=D["slate"])
    v += kpi(3, "UNEMPLOYMENT", "KPI Unemployment", "Cap Unemployment", D["amber"], spark="Unemployment, %", spark_color=D["amber"])
    v.append(glass("heroGlass", 288, 250, 730, 392, 1100, radius=22))
    v += panel_title("hero", 312, 268, "Is output outpacing population?", "Real GDP growth vs population growth, % per year")
    legend(v, [("Real GDP growth", D["petrol"], 790), ("Population growth", D["slate"], 900)])
    hero = chart("heroChart", 300, 304, 706, 290, 1110, "lineChart", tip=["GDP per capita ($)", "Inflation, %", "Unemployment, %"], measures=["GDP, growth, %", "Pop Growth, %"], axis_units=None, legend=False,
                 objects=colors([("GDP, growth, %", D["petrol"]), ("Pop Growth, %", D["slate"])])); TIME_SERIES.append("heroChart")
    v += [hero, card("heroCap", 312, 584, 690, 48, 1110, "Cap GDP Growth Chart", size=9, font=D["font_sb"], color=D["mute"])]
    v.append(glass("sideGlass", 1034, 250, 382, 392, 1100, radius=22))
    v += panel_title("side", 1058, 268, "GDP per capita", "Current US$")
    side = chart("sideChart", 1046, 304, 358, 290, 1110, "areaChart", ["GDP per capita ($)"], vmin=0, legend=False); TIME_SERIES.append("sideChart")
    v += [side, card("sideCap", 1058, 584, 340, 48, 1110, "Cap Per Capita", size=9, font=D["font_sb"], color=D["petrol"])]
    v += bottom_panel(0, "Inflation, %", bchart(0, "botInfl", "lineChart", ["Inflation, %"], axis_units=None, legend=False, objects=colors([("Inflation, %", D["slate"])])), static_cap="Consumer prices, annual % change")
    v += bottom_panel(1, "Unemployment, %", bchart(1, "botUnemp", "lineChart", ["Unemployment, %"], axis_units=None, legend=False, vmin=0, objects=colors([("Unemployment, %", D["amber"])])), static_cap="ILO modelled estimate; series starts 1991")
    v += bottom_panel(2, "Population, m", bchart(2, "botPop", "areaChart", ["Population (m)"], axis_units=None, vmin=0, legend=False), cap="Cap Population", cap_color=D["petrol"])
    finish("p02Growth", "Growth & Prices", v)

def page3():
    TIME_SERIES.clear()
    v = rail(2) + header("External Position", "The external gap and what sits around it · Jordan, 1990–2024 · reference year set on the left")
    v += kpi(0, "CURRENT ACCOUNT", "KPI Current Account", "Cap Current Account", D["amber"], spark="Current account ($bn)", spark_color=D["amber"])
    v += kpi(1, "REMITTANCES RECEIVED", "KPI Remittances", "Cap Remittances", D["petrol"], spark="Remittances ($bn)")
    v += kpi(2, "FDI, NET INFLOWS", "KPI FDI", "Cap FDI", D["ink"], spark="FDI ($bn)", spark_color=D["slate"])
    v += kpi(3, "IMPORT COVERAGE, MONTHS", "KPI Import Coverage", "Cap Import Coverage", D["petrol"], spark="Import coverage, months")
    v.append(glass("heroGlass", 288, 250, 730, 392, 1100, radius=22))
    v += panel_title("hero", 312, 268, "Three measures of the external gap", "US$ bn · merchandise only vs goods and services vs the full current account")
    legend(v, [("Merchandise", D["amber"], 700), ("Goods & services", D["slate"], 800), ("Current account", D["petrol"], 915)])
    hero = chart("heroChart", 300, 304, 706, 290, 1110, "lineChart", tip=["Remittances ($bn)", "FDI ($bn)", "Reserves ($bn)", "Import coverage, months"], measures=["Trade balance ($bn)", "Net goods & services ($bn)", "Current account ($bn)"], axis_units=None, legend=False,
                 objects=colors([("Trade balance ($bn)", D["amber"]), ("Net goods & services ($bn)", D["slate"]), ("Current account ($bn)", D["petrol"])])); TIME_SERIES.append("heroChart")
    v += [hero, card("heroCap", 312, 584, 690, 48, 1110, "Cap Gap Line", size=9, font=D["font_sb"], color=D["mute"])]
    v.append(glass("sideGlass", 1034, 250, 382, 392, 1100, radius=22))
    v += panel_title("side", 1058, 268, "Reserves", "Total reserves incl. gold, US$ bn")
    side = chart("sideChart", 1046, 304, 358, 290, 1110, "areaChart", ["Reserves ($bn)"], vmin=0, legend=False); TIME_SERIES.append("sideChart")
    v += [side, card("sideCap", 1058, 584, 340, 48, 1110, "Cap Reserves Line", size=9, font=D["font_sb"], color=D["petrol"])]
    v += bottom_panel(0, "Remittances, % of GDP", bchart(0, "botRem", "lineChart", ["Remittances, % GDP"], axis_units=None, vmin=0, legend=False, objects=colors([("Remittances, % GDP", D["petrol"])])), cap="Cap Remittances", cap_color=D["petrol"])
    v += bottom_panel(1, "FDI, % of GDP", bchart(1, "botFdi", "lineChart", ["FDI, % GDP"], axis_units=None, legend=False, objects=colors([("FDI, % GDP", D["slate"])])), cap="Cap FDI")
    v += bottom_panel(2, "Change in reserves, US$ bn", bchart(2, "botRes", "columnChart", ["Reserves change ($bn)"], axis_units=None, legend=False, objects=colors([("Reserves change ($bn)", D["petrol"])])), cap="Cap Reserve Change")
    finish("p03External", "External Position", v)

def page4():
    TIME_SERIES.clear()
    v = rail(3) + header("Trade Structure", "What Jordan imports and sells abroad, and to whom · CBJ Annual Statistical Bulletin, JD")
    v.append(card("pageNote", 284, 76, 1000, 44, 1020, "Cap CBJ Year", size=9, font=D["font"], color=D["amber"]))
    v += kpi(0, "IMPORTS", "KPI CBJ Imports", "Cap CBJ Imports", D["ink"])
    v += kpi(1, "DOMESTIC EXPORTS", "KPI CBJ Domestic Exports", "Cap CBJ Domestic Exports", D["petrol"])
    v += kpi(2, "DOMESTIC EXPORT COVERAGE", "KPI CBJ Coverage", "Cap CBJ Coverage", D["ink"])
    v += kpi(3, "FUEL SHARE OF IMPORTS", "KPI CBJ Fuel Share", "Cap CBJ Fuel", D["amber"])
    v.append(glass("heroGlass", 288, 250, 730, 352, 1100, radius=22))
    v += panel_title("hero", 312, 268, "What Jordan buys and what it sells", "Share of imports and of domestic exports by commodity group, %")
    v.append(text("heroLblL", 312, 304, 330, 20, 1110, [("IMPORTS", 7.5, D["font_sb"], D["mute"])]))
    v.append(text("heroLblR", 670, 304, 330, 20, 1110, [("DOMESTIC EXPORTS", 7.5, D["font_sb"], D["mute"])]))
    v.append(bar("barImpComm", 300, 322, 350, 272, 1110, ("DimCommodity", "Commodity"), "Commodity Share (CBJ year)", "Imports", color=D["slate"], fmt_max=26))
    v.append(bar("barExpComm", 660, 322, 350, 272, 1110, ("DimCommodity", "Commodity"), "Commodity Share (CBJ year)", "Domestic exports", color=D["petrol"], fmt_max=42))
    v.append(glass("sideGlass", 1034, 250, 382, 352, 1100, radius=22))
    v += panel_title("side", 1058, 268, "Do domestic exports pay for imports?", "Domestic exports ÷ imports, %")
    side = chart("sideChart", 1046, 304, 358, 250, 1110, "lineChart", ["Coverage, % (CBJ)"], axis_units=None, vmin=0, legend=False, objects=colors([("Coverage, % (CBJ)", D["petrol"])])); TIME_SERIES.append("sideChart")
    v += [side, text("sideNote", 1058, 564, 340, 24, 1110, [("CBJ domestic exports exclude re-exports", 8.5, D["font"], D["faint"])])]
    v.append(glass("botGlass0", 288, 618, 365, 258, 1100, radius=20)); v.append(text("botT0", 308, 632, 330, 24, 1110, [("Imports by partner, %", 11, D["font_sb"], D["ink"])]))
    v.append(bar("barImpPart", 300, 656, 341, 214, 1110, ("DimPartner", "Partner"), "Partner Share (CBJ year)", "Imports", color=D["slate"], fmt_max=45))
    v.append(glass("botGlass1", 669, 618, 365, 258, 1100, radius=20)); v.append(text("botT1", 689, 632, 330, 24, 1110, [("Domestic exports by partner, %", 11, D["font_sb"], D["ink"])]))
    v.append(bar("barExpPart", 681, 656, 341, 214, 1110, ("DimPartner", "Partner"), "Partner Share (CBJ year)", "Domestic exports", color=D["petrol"], fmt_max=50))
    v.append(glass("botGlass2", 1051, 618, 365, 258, 1100, radius=20))
    v.append(text("methT", 1071, 632, 330, 24, 1110, [("Definitions & sources", 11, D["font_sb"], D["ink"])]))
    lines = [[("Trade page: CBJ Annual Statistical Bulletin, JD; exports are DOMESTIC exports (no re-exports).", 8.5, D["font"], D["mute"])],
             [("Other pages: World Bank WDI, current US$; exports include re-exports.", 8.5, D["font"], D["mute"])],
             [("The two export measures are not comparable and are never mixed.", 8.5, D["font_sb"], D["ink"])],
             [("2012 commodity imports are missing in the source (a copied 2011 row was excluded); partner totals are intact.", 8.5, D["font"], D["mute"])]]
    v.append(text("methBody", 1071, 662, 330, 200, 1110, None, lines=lines))
    finish("p04Trade", "Trade Structure", v)

def tooltip_page():
    rows = [("Merchandise exports", "KPI Exports", D["petrol"]), ("Merchandise imports", "KPI Imports", D["slate"]), ("Trade balance", "KPI Trade Balance", D["amber"]),
            ("Export coverage of imports", "KPI Export Coverage", D["ink"]), ("Current account", "KPI Current Account", D["ink"]),
            ("Remittances", "KPI Remittances", D["ink"]), ("FDI, net inflows", "KPI FDI", D["ink"]), ("Reserves", "KPI Reserves", D["petrol"])]
    v = [solid("ttBar", 0, 0, 360, 4, 1000, D["petrol"]),
         text("ttKicker", 16, 12, 200, 18, 1010, [("YEAR SNAPSHOT", 7.5, D["font_sb"], D["faint"])]),
         card("ttYearVal", 12, 18, 200, 48, 1010, "KPI Year Label", size=16, color=D["ink"])]
    for i, (lab, m, col) in enumerate(rows):
        y = 70 + i * 27
        v.append(solid(f"ttRule{i}", 16, y - 1, 328, 1, 1005, D["hair"], tr=30))
        v.append(text(f"ttLab{i}", 16, y + 3, 190, 20, 1010, [(lab, 9, D["font"], D["mute"])]))
        v.append(card(f"ttVal{i}", 196, y - 9, 150, 44, 1010, m, size=10.5, color=col))
    write_tooltip_page(REP, "ttYear", "Tooltip - year snapshot", v)

page1()
page2(); page3(); page4()

print("built:", [p[0] for p in PAGES])
