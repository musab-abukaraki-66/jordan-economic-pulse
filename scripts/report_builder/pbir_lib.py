"""PBIR authoring helpers for the Jordan Economic Pulse report.
Every emitted structure follows patterns already proven to render in this Desktop build (2.158.1177.0):
shape / textbox / card / actionButton / column / line container objects, page background, visual header block.
Design tokens live in DS so a fix applies by class, not per visual."""
import json, os, copy

SCHEMA_VISUAL = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json"
SCHEMA_PAGE = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"

# ---------------------------------------------------------------- design tokens
DS = dict(
    canvas="#EDF1F3", ink="#16222E", mute="#5F6E7C", faint="#8A97A3",
    petrol="#0F5C63", slate="#6E86A0", amber="#B7862E", white="#FFFFFF",
    hair="#D4DDE3", panel_fill="#FFFFFF", panel_tr=38,   # % transparency of glass panels
    font="Segoe UI", font_sb="Segoe UI Semibold", font_lt="Segoe UI Light",
)

# ---------------------------------------------------------------- literal helpers
def lit(v): return {"expr": {"Literal": {"Value": v}}}
def S(x): return lit("'" + str(x).replace("'", "''") + "'")
def N(x): return lit(f"{x}D")
def B(x): return lit("true" if x else "false")
def COL(hexv): return {"solid": {"color": S(hexv)}}

HEADER_OFF = {"properties": {k: B(False) for k in [
    "showVisualInformationButton", "showVisualWarningButton", "showVisualErrorButton", "showDrillUpButton",
    "showDrillDownLevelButton", "showDrillDownExpandButton", "showDrillToggleButton", "showPinButton",
    "showFilterRestatementButton", "showFocusModeButton", "showCopyVisualImageButton", "showSeeDataLayoutToggleButton",
    "showOptionsMenu", "showCommentButton", "showTooltipButton", "showSmartNarrativeButton", "showPersonalizeVisualButton"]}}
HEADER_OFF["properties"].update({"show": B(False), "transparency": N(100)})

def container(title=None, shadow=False, link=None, bg=None, extra=None, tooltip=None):
    o = {
        "visualHeader": [copy.deepcopy(HEADER_OFF)],
        "title": [{"properties": {"show": B(False)}}],
        "subTitle": [{"properties": {"show": B(False)}}],
        "background": [{"properties": {"show": B(False)}}],
        "border": [{"properties": {"show": B(False)}}],
        "dropShadow": [{"properties": {"show": B(False)}}],
    }
    if shadow:
        o["dropShadow"] = [{"properties": {
            "show": B(True), "preset": S("Custom"), "position": S("Outer"), "color": COL(DS["ink"]),
            "transparency": N(93), "shadowBlur": N(26), "shadowDistance": N(7), "angle": N(90), "shadowSpread": N(0)}}]
    if link:
        o["visualLink"] = [{"properties": {"show": B(True), "type": S("PageNavigation"), "navigationSection": S(link[0]), "tooltip": S(link[1])}}]
    if tooltip:
        o["visualTooltip"] = [{"properties": {"show": B(True), "type": S("ReportPage"), "section": S(tooltip)}}]
    if extra: o.update(extra)
    return o

def visual(name, x, y, w, h, z, vtype, objects=None, query=None, vco=None, sort=None, filters=None):
    v = {"visualType": vtype}
    if query: v["query"] = query
    if sort and query: v["query"]["sortDefinition"] = sort
    if objects: v["objects"] = objects
    v["visualContainerObjects"] = vco if vco is not None else container()
    v["drillFilterOtherVisuals"] = True
    d = {"$schema": SCHEMA_VISUAL, "name": name, "position": {"x": x, "y": y, "z": z, "height": h, "width": w}, "visual": v}
    if filters: d["filterConfig"] = {"filters": filters}
    return d

# ---------------------------------------------------------------- primitives
def glass(name, x, y, w, h, z, radius=18, tr=None, line=True, shadow=True, fill=None):
    tr = DS["panel_tr"] if tr is None else tr
    obj = {
        "shape": [{"properties": {"tileShape": S("rectangle"), "roundEdge": N(radius)}, "selector": {"id": "default"}}],
        "fill": [{"properties": {"show": B(True)}},
                 {"properties": {"fillColor": COL(fill or DS["panel_fill"]), "transparency": N(tr)}, "selector": {"id": "default"}}],
        "outline": [{"properties": {"show": B(line)}},
                    {"properties": {"show": B(line), "lineColor": COL(DS["white"]), "transparency": N(15), "weight": N(1)}, "selector": {"id": "default"}}],
    }
    return visual(name, x, y, w, h, z, "shape", obj, vco=container(shadow=shadow))

def solid(name, x, y, w, h, z, color, tr=0, radius=0, shape="rectangle"):
    obj = {
        "shape": [{"properties": {"tileShape": S(shape), **({"roundEdge": N(radius)} if radius else {})}, "selector": {"id": "default"}}],
        "fill": [{"properties": {"show": B(True)}},
                 {"properties": {"fillColor": COL(color), "transparency": N(tr)}, "selector": {"id": "default"}}],
        "outline": [{"properties": {"show": B(False)}}, {"properties": {"show": B(False)}, "selector": {"id": "default"}}],
    }
    return visual(name, x, y, w, h, z, "shape", obj)

def text(name, x, y, w, h, z, runs, align="left", lines=None):
    """runs: list of (text, size_pt, font, color) ; lines: list of run-lists for multi-paragraph"""
    paras = []
    for rl in (lines or [runs]):
        paras.append({"textRuns": [{"value": t, "textStyle": {"fontSize": f"{sz}pt", "fontFamily": fam, "color": col}} for (t, sz, fam, col) in rl],
                      "horizontalTextAlignment": align})
    return visual(name, x, y, w, h, z, "textbox", {"general": [{"properties": {"paragraphs": paras}}]})

def field_col(entity, prop):
    return {"field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}, "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}
def field_meas(prop, entity="_Measures"):
    return {"field": {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}, "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}

def card(name, x, y, w, h, z, measure, size=26, font=None, color=None, align="left"):
    q = {"queryState": {"Values": {"projections": [field_meas(measure)]}}}
    obj = {
        "labels": [{"properties": {"color": COL(color or DS["ink"]), "fontFamily": S(font or DS["font_sb"]), "fontSize": N(size), "labelDisplayUnits": N(1), "labelPrecision": N(1)}}],
        "categoryLabels": [{"properties": {"show": B(False)}}],
        "wordWrap": [{"properties": {"show": B(False)}}],
    }
    return visual(name, x, y, w, h, z, "card", obj, query=q)

def button(name, x, y, w, h, z, label, target, active=False, size=10.5):
    obj = {
        "icon": [{"properties": {"shapeType": S("blank")}, "selector": {"id": "default"}}],
        "outline": [{"properties": {"show": B(False)}}, {"properties": {"show": B(False)}, "selector": {"id": "default"}}],
        "fill": [{"properties": {"show": B(True)}},
                 {"properties": {"fillColor": COL(DS["white"]), "transparency": N(100)}, "selector": {"id": "default"}},
                 {"properties": {"fillColor": COL(DS["white"]), "transparency": N(60)}, "selector": {"id": "hover"}}],
        "text": [{"properties": {"show": B(True)}},
                 {"properties": {"text": S(label), "fontFamily": S(DS["font_sb"] if active else DS["font"]), "fontSize": N(size),
                                 "fontColor": COL(DS["ink"] if active else DS["mute"]), "horizontalAlignment": S("left"),
                                 "verticalAlignment": S("middle"), "leftMargin": N(38)}, "selector": {"id": "default"}},
                 {"properties": {"fontColor": COL(DS["ink"])}, "selector": {"id": "hover"}}],
    }
    return visual(name, x, y, w, h, z, "actionButton", obj, vco=container(link=(target, label)))

def sort_year():
    return {"sort": [{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "DimYear"}}, "Property": "Year"}}, "direction": "Ascending"}], "isDefaultSort": True}

def chart(name, x, y, w, h, z, vtype, measures, cat=("DimYear", "Year"), objects=None, axis_units=1e9, vmin=None, vmax=None,
          legend=False, legend_pos="TopRight", show_val_axis=True, show_cat_axis=True, gridlines=True, title=None, cat_label_every=None, axis_type="Scalar", tooltip=None, tip=None):
    q = {"queryState": {"Category": {"projections": [dict(field_col(*cat), active=True)]},
                        "Y": {"projections": [field_meas(m) for m in measures]}}}
    if tip: q["queryState"]["Tooltips"] = {"projections": [field_meas(m) for m in tip]}
    o = {
        "categoryAxis": [{"properties": {"show": B(show_cat_axis), "showAxisTitle": B(False), "fontFamily": S(DS["font"]), "fontSize": N(9),
                                          "labelColor": COL(DS["mute"]), "gridlineShow": B(False), "axisType": S(axis_type),
                                          "concatenateLabels": B(False)}}],
        "valueAxis": [{"properties": {"show": B(show_val_axis), "showAxisTitle": B(False), "fontFamily": S(DS["font"]), "fontSize": N(9),
                                       "labelColor": COL(DS["mute"]), "gridlineShow": B(gridlines), "gridlineColor": COL(DS["hair"]),
                                       "gridlineThickness": N(1), "gridlineStyle": S("solid"),
                                       "labelDisplayUnits": N(1), "labelPrecision": N(0),
                                       **({"start": N(vmin)} if vmin is not None else {}), **({"end": N(vmax)} if vmax is not None else {})}}],
        "legend": [{"properties": {"show": B(legend), "position": S(legend_pos), "showTitle": B(False), "fontFamily": S(DS["font"]),
                                    "fontSize": N(9), "labelColor": COL(DS["mute"])}}],
        "labels": [{"properties": {"show": B(False)}}],
        "plotArea": [{"properties": {"transparency": N(100)}}],
    }
    if vtype in ("lineChart", "areaChart", "stackedAreaChart"):
        o["lineStyles"] = [{"properties": {"lineChartType": S("linear"), "strokeWidth": N(2.25), "showMarker": B(False)}}]
    if objects: o.update(objects)
    return visual(name, x, y, w, h, z, vtype, o, query=q, sort=sort_year(), vco=container(tooltip=tooltip))

def slicer_year(name, x, y, w, h, z, default=2024, sync="YearSync"):
    q = {"queryState": {"Values": {"projections": [dict(field_col("DimYear", "Year"), active=True)]}}}
    o = {
        "data": [{"properties": {"mode": S("Dropdown")}}],
        "selection": [{"properties": {"singleSelect": B(True), "selectAllCheckboxEnabled": B(False), "strictSingleSelect": B(False)}}],
        "header": [{"properties": {"show": B(False)}}],
        "items": [{"properties": {"fontFamily": S(DS["font_sb"]), "fontColor": COL(DS["ink"]), "background": COL(DS["white"])}}],
    }
    flt = [{
        "name": "yearDefault", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "DimYear"}}, "Property": "Year"}}, "type": "Categorical",
        "filter": {"Version": 2, "From": [{"Name": "d", "Entity": "DimYear", "Type": 0}],
                   "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "Year"}}],
                                                   "Values": [[{"Literal": {"Value": f"{default}L"}}]]}}}]},
    }]
    d = visual(name, x, y, w, h, z, "slicer", o, query=q, vco=container())
    d["visual"]["syncGroup"] = {"groupName": sync, "fieldChanges": True, "filterChanges": True}
    return d

# ---------------------------------------------------------------- page / project writers
def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def page_json(name, display, bg_image, interactions=None, tooltip=False, w=1440, h=900):
    p = {"$schema": SCHEMA_PAGE, "name": name, "displayName": display, "displayOption": "FitToPage", "width": w, "height": h}
    if tooltip: p["type"] = "Tooltip"
    obj = {}
    if bg_image:
        obj["background"] = [{"properties": {
            "image": {"image": {"name": S(bg_image), "scaling": S("Fill"),
                                "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources", "PackageType": 1, "ItemName": bg_image}}}}},
            "transparency": N(0)}}]
    else:
        obj["background"] = [{"properties": {"color": COL(DS["canvas"]), "transparency": N(0)}}]
    obj["outspace"] = [{"properties": {"color": COL(DS["canvas"])}}]
    p["objects"] = obj
    if interactions: p["visualInteractions"] = interactions
    return p

def write_page(rep_dir, name, display, visuals, bg_image, interactions=None, tooltip=False, w=1440, h=900):
    pdir = os.path.join(rep_dir, "definition", "pages", name)
    write_json(os.path.join(pdir, "page.json"), page_json(name, display, bg_image, interactions, tooltip, w, h))
    for v in visuals:
        write_json(os.path.join(pdir, "visuals", v["name"], "visual.json"), v)


def flow_filter(flow):
    return [{"name": "flowFilter", "field": {"Column": {"Expression": {"SourceRef": {"Entity": "DimFlow"}}, "Property": "Flow"}}, "type": "Categorical",
             "filter": {"Version": 2, "From": [{"Name": "f", "Entity": "DimFlow", "Type": 0}],
                        "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": "Flow"}}],
                                                        "Values": [[{"Literal": {"Value": "'" + flow + "'"}}]]}}}]}}]

def bar(name, x, y, w, h, z, cat, measure, flow, color=None, fmt_max=None):
    """Horizontal bar (clustered bar) of a share measure by a dimension column, sorted descending, flow fixed by a visual filter."""
    q = {"queryState": {"Category": {"projections": [dict(field_col(*cat), active=True)]}, "Y": {"projections": [field_meas(measure)]}},
         "sortDefinition": {"sort": [{"field": {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": measure}}, "direction": "Descending"}], "isDefaultSort": False}}
    o = {
        "categoryAxis": [{"properties": {"show": B(True), "showAxisTitle": B(False), "fontFamily": S(DS["font"]), "fontSize": N(8), "labelColor": COL(DS["ink"]),
                                          "gridlineShow": B(False), "concatenateLabels": B(False), "innerPadding": N(8)}}],
        "valueAxis": [{"properties": {"show": B(False), "showAxisTitle": B(False), "gridlineShow": B(False), **({"end": N(fmt_max)} if fmt_max else {}), "start": N(0)}}],
        "legend": [{"properties": {"show": B(False)}}],
        "labels": [{"properties": {"show": B(True), "fontFamily": S(DS["font_sb"]), "fontSize": N(8), "color": COL(DS["mute"]), "labelPrecision": N(1)}}],
        "dataPoint": [{"properties": {"fill": COL(color or DS["petrol"])}}],
        "plotArea": [{"properties": {"transparency": N(100)}}],
    }
    return visual(name, x, y, w, h, z, "clusteredBarChart", o, query=q, vco=container(), filters=flow_filter(flow))


def write_tooltip_page(rep_dir, name, display, visuals, w=360, h=300):
    pdir = os.path.join(rep_dir, "definition", "pages", name)
    p = {"$schema": SCHEMA_PAGE, "name": name, "displayName": display, "displayOption": "FitToPage", "width": w, "height": h,
         "pageBinding": {"name": name + "Binding", "type": "Tooltip", "parameters": []}, "type": "Tooltip",
         "objects": {"background": [{"properties": {"color": COL(DS["white"]), "transparency": N(0)}}],
                     "outspace": [{"properties": {"color": COL(DS["canvas"])}}]}}
    write_json(os.path.join(pdir, "page.json"), p)
    for v in visuals:
        write_json(os.path.join(pdir, "visuals", v["name"], "visual.json"), v)
