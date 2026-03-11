"""
============================================================
Basketo — Online Grocery Shopping Analytics Dashboard
============================================================
Author      : Keerthi Housure Srinivas
Description : Interactive Plotly Dash dashboard analyzing
              user behavior, purchase trends, delivery
              performance, and funnel drop-offs for the
              Basketo grocery platform prototype.
============================================================
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import os

# ── Load Data ──────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "..", "data")

sessions_df = pd.read_csv(os.path.join(DATA, "user_sessions.csv"))
orders_df   = pd.read_csv(os.path.join(DATA, "orders.csv"))
items_df    = pd.read_csv(os.path.join(DATA, "order_items.csv"))
funnel_df   = pd.read_csv(os.path.join(DATA, "funnel.csv"))

sessions_df["date"] = pd.to_datetime(sessions_df["date"])
orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

# ── KPIs ───────────────────────────────────────────────────
total_sessions   = len(sessions_df)
total_orders     = len(orders_df)
conversion_rate  = round(total_orders / total_sessions * 100, 1)
avg_order_value  = round(orders_df["subtotal_usd"].mean(), 2)
on_time_rate     = round(orders_df["on_time"].mean() * 100, 1)
top_pain_point   = sessions_df[sessions_df["converted"] == 0]["last_stage"].mode()[0]

FUNNEL_ORDER = ["Landing", "Browse", "Product View", "Add to Cart",
                "Checkout Start", "Payment", "Order Confirmed"]

# ── App ────────────────────────────────────────────────────
app = Dash(__name__)
app.title = "Basketo Analytics Dashboard"

COLORS = {
    "bg"       : "#F8FAF5",
    "card"     : "#FFFFFF",
    "green"    : "#2E7D32",
    "light_green": "#66BB6A",
    "accent"   : "#FF6F00",
    "text"     : "#1A1A2E",
    "subtext"  : "#666666",
    "border"   : "#E8F5E9"
}

def kpi_card(title, value, subtitle="", color=COLORS["green"]):
    return html.Div([
        html.P(title, style={"margin": "0", "fontSize": "12px",
                              "color": COLORS["subtext"], "fontWeight": "600",
                              "textTransform": "uppercase", "letterSpacing": "0.5px"}),
        html.H2(str(value), style={"margin": "4px 0", "fontSize": "28px",
                                    "color": color, "fontWeight": "800"}),
        html.P(subtitle, style={"margin": "0", "fontSize": "11px",
                                 "color": COLORS["subtext"]})
    ], style={
        "background": COLORS["card"], "borderRadius": "12px",
        "padding": "20px 24px", "flex": "1",
        "borderLeft": f"4px solid {color}",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"
    })

app.layout = html.Div([

    # Header
    html.Div([
        html.Div([
            html.H1("🛒 Basketo", style={"margin": "0", "fontSize": "28px",
                                          "color": COLORS["green"], "fontWeight": "900"}),
            html.P("Grocery Platform Analytics Dashboard · Sep – Nov 2024",
                   style={"margin": "2px 0 0", "color": COLORS["subtext"], "fontSize": "13px"})
        ]),
        html.Div([
            html.Label("Filter by Device:", style={"fontSize": "12px",
                                                    "color": COLORS["subtext"],
                                                    "marginRight": "8px"}),
            dcc.Dropdown(
                id="device-filter",
                options=[{"label": "All Devices", "value": "All"}] +
                        [{"label": d, "value": d} for d in sessions_df["device"].unique()],
                value="All",
                clearable=False,
                style={"width": "160px", "fontSize": "13px"}
            )
        ], style={"display": "flex", "alignItems": "center"})
    ], style={
        "display": "flex", "justifyContent": "space-between", "alignItems": "center",
        "background": COLORS["card"], "padding": "20px 32px",
        "borderBottom": f"2px solid {COLORS['border']}",
        "boxShadow": "0 2px 8px rgba(0,0,0,0.04)"
    }),

    html.Div([

        # KPI Row
        html.Div([
            kpi_card("Total Sessions",    total_sessions,  "Sep–Nov 2024"),
            kpi_card("Orders Placed",     total_orders,    "Converted sessions"),
            kpi_card("Conversion Rate",   f"{conversion_rate}%", "Sessions → Orders", COLORS["accent"]),
            kpi_card("Avg Order Value",   f"${avg_order_value}", "Per completed order"),
            kpi_card("On-Time Delivery",  f"{on_time_rate}%",   "Of all deliveries"),
            kpi_card("Top Drop-off Stage",top_pain_point,  "Biggest funnel leak", "#C62828"),
        ], style={"display": "flex", "gap": "16px", "marginBottom": "24px",
                  "flexWrap": "wrap"}),

        # Row 1: Funnel + User Behavior
        html.Div([
            html.Div([
                html.H3("Conversion Funnel",
                        style={"margin": "0 0 16px", "fontSize": "15px",
                               "color": COLORS["text"], "fontWeight": "700"}),
                dcc.Graph(id="funnel-chart", style={"height": "320px"})
            ], style={"background": COLORS["card"], "borderRadius": "12px",
                      "padding": "20px", "flex": "1",
                      "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),

            html.Div([
                html.H3("Sessions by Device Over Time",
                        style={"margin": "0 0 16px", "fontSize": "15px",
                               "color": COLORS["text"], "fontWeight": "700"}),
                dcc.Graph(id="sessions-trend", style={"height": "320px"})
            ], style={"background": COLORS["card"], "borderRadius": "12px",
                      "padding": "20px", "flex": "2",
                      "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"})
        ], style={"display": "flex", "gap": "16px", "marginBottom": "24px"}),

        # Row 2: Purchase Trends + Delivery
        html.Div([
            html.Div([
                html.H3("Top Categories by Revenue",
                        style={"margin": "0 0 16px", "fontSize": "15px",
                               "color": COLORS["text"], "fontWeight": "700"}),
                dcc.Graph(id="category-revenue", style={"height": "300px"})
            ], style={"background": COLORS["card"], "borderRadius": "12px",
                      "padding": "20px", "flex": "1",
                      "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),

            html.Div([
                html.H3("Delivery Performance",
                        style={"margin": "0 0 16px", "fontSize": "15px",
                               "color": COLORS["text"], "fontWeight": "700"}),
                dcc.Graph(id="delivery-chart", style={"height": "300px"})
            ], style={"background": COLORS["card"], "borderRadius": "12px",
                      "padding": "20px", "flex": "1",
                      "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"})
        ], style={"display": "flex", "gap": "16px", "marginBottom": "24px"}),

        # Row 3: Top Products Table
        html.Div([
            html.H3("Top 10 Products by Units Sold",
                    style={"margin": "0 0 16px", "fontSize": "15px",
                           "color": COLORS["text"], "fontWeight": "700"}),
            html.Div(id="top-products-table")
        ], style={"background": COLORS["card"], "borderRadius": "12px",
                  "padding": "20px", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"})

    ], style={"padding": "24px 32px", "background": COLORS["bg"], "minHeight": "100vh"})

], style={"fontFamily": "'Segoe UI', Arial, sans-serif", "background": COLORS["bg"]})


# ── Callbacks ──────────────────────────────────────────────

@app.callback(
    Output("funnel-chart", "figure"),
    Output("sessions-trend", "figure"),
    Output("category-revenue", "figure"),
    Output("delivery-chart", "figure"),
    Output("top-products-table", "children"),
    Input("device-filter", "value")
)
def update_dashboard(device):

    # Filter
    sess = sessions_df if device == "All" else sessions_df[sessions_df["device"] == device]
    ords = orders_df   if device == "All" else orders_df[orders_df["device"] == device]
    ord_ids = ords["order_id"].tolist()
    itms = items_df[items_df["order_id"].isin(ord_ids)]

    # 1. Funnel
    funnel_counts = []
    for stage in FUNNEL_ORDER:
        idx = FUNNEL_ORDER.index(stage)
        count = sess[sess["last_stage"].apply(
            lambda x: FUNNEL_ORDER.index(x) >= idx if x in FUNNEL_ORDER else False
        )].shape[0]
        funnel_counts.append(count)

    funnel_fig = go.Figure(go.Funnel(
        y=FUNNEL_ORDER, x=funnel_counts,
        textinfo="value+percent initial",
        marker={"color": ["#2E7D32","#388E3C","#43A047","#66BB6A",
                          "#FF8F00","#F57C00","#E65100"]},
        connector={"line": {"color": "#E8F5E9", "width": 2}}
    ))
    funnel_fig.update_layout(margin=dict(l=0,r=0,t=0,b=0),
                              paper_bgcolor="white", plot_bgcolor="white")

    # 2. Sessions trend
    trend = sess.groupby([sess["date"].dt.to_period("W").astype(str),
                          "device"]).size().reset_index(name="sessions")
    trend_fig = px.line(trend, x="date", y="sessions", color="device",
                        color_discrete_map={"Mobile":"#2E7D32","Desktop":"#FF8F00","Tablet":"#1565C0"},
                        markers=True)
    trend_fig.update_layout(margin=dict(l=0,r=0,t=0,b=0),
                             paper_bgcolor="white", plot_bgcolor="white",
                             legend=dict(orientation="h", y=-0.2),
                             xaxis_title="", yaxis_title="Sessions")

    # 3. Category revenue
    cat_rev = itms.groupby("category")["line_total"].sum().reset_index()
    cat_rev = cat_rev.sort_values("line_total", ascending=True)
    cat_fig = px.bar(cat_rev, x="line_total", y="category", orientation="h",
                     color="line_total",
                     color_continuous_scale=["#C8E6C9","#2E7D32"])
    cat_fig.update_layout(margin=dict(l=0,r=0,t=0,b=0),
                           paper_bgcolor="white", plot_bgcolor="white",
                           showlegend=False, coloraxis_showscale=False,
                           xaxis_title="Revenue (USD)", yaxis_title="")

    # 4. Delivery
    delivery = ords.groupby("delivery_window").agg(
        total=("order_id","count"),
        on_time=("on_time","sum")
    ).reset_index()
    delivery["late"] = delivery["total"] - delivery["on_time"]
    del_fig = go.Figure()
    del_fig.add_trace(go.Bar(name="On Time", x=delivery["delivery_window"],
                             y=delivery["on_time"], marker_color="#2E7D32"))
    del_fig.add_trace(go.Bar(name="Late", x=delivery["delivery_window"],
                             y=delivery["late"], marker_color="#C62828"))
    del_fig.update_layout(barmode="stack", margin=dict(l=0,r=0,t=0,b=0),
                           paper_bgcolor="white", plot_bgcolor="white",
                           legend=dict(orientation="h", y=-0.2),
                           xaxis_title="Delivery Window", yaxis_title="Orders")

    # 5. Top products table
    top_prods = itms.groupby(["product","category"]).agg(
        units_sold=("quantity","sum"),
        revenue=("line_total","sum")
    ).reset_index().sort_values("units_sold", ascending=False).head(10)
    top_prods["revenue"] = top_prods["revenue"].apply(lambda x: f"${x:,.2f}")

    table = dash_table.DataTable(
        data=top_prods.to_dict("records"),
        columns=[{"name": c.replace("_"," ").title(), "id": c}
                 for c in top_prods.columns],
        style_header={"backgroundColor": "#2E7D32", "color": "white",
                       "fontWeight": "700", "fontSize": "13px"},
        style_cell={"padding": "10px 14px", "fontSize": "13px",
                    "fontFamily": "Segoe UI, Arial, sans-serif"},
        style_data_conditional=[
            {"if": {"row_index": "odd"},
             "backgroundColor": "#F1F8F1"}
        ],
        page_size=10
    )

    return funnel_fig, trend_fig, cat_fig, del_fig, table


if __name__ == "__main__":
    app.run(debug=True)
