from __future__ import annotations

import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "cleaned_hr_dataset.csv"
IMPORTANCE_PATH = ROOT / "data" / "feature_importance.csv"
PERFORMANCE_PATH = ROOT / "data" / "model_performance.csv"
FEATURES_PATH = ROOT / "models" / "feature_columns.json"
MODEL_PATH = ROOT / "models" / "best_model.pkl"
SCALER_PATH = ROOT / "models" / "scaler.pkl"
METADATA_PATH = ROOT / "models" / "model_metadata.json"

PINK = "#ff39d4"
MAGENTA = "#d946ef"
CYAN = "#38e8ff"
ORANGE = "#ff685d"
LIME = "#c9ff47"
INK = "#0d0a24"
MUTED = "#aaa2d1"
GRID = "rgba(157, 117, 255, 0.18)"


st.set_page_config(
    page_title="People Pulse | IBM HR Analytics",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict, list[str]]:
    employees = pd.read_csv(DATA_PATH)
    importance = pd.read_csv(IMPORTANCE_PATH)
    performance = pd.read_csv(PERFORMANCE_PATH)
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    features = json.loads(FEATURES_PATH.read_text(encoding="utf-8"))
    return employees, importance, performance, metadata, features


@st.cache_resource
def load_model():
    with MODEL_PATH.open("rb") as model_file:
        model = pickle.load(model_file)
    with SCALER_PATH.open("rb") as scaler_file:
        scaler = pickle.load(scaler_file)
    return model, scaler


def inject_style() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        :root {
            --ink: #0d0a24;
            --panel: #171238;
            --panel-light: #21194b;
            --text: #f7f4ff;
            --muted: #aaa2d1;
            --pink: #ff39d4;
            --cyan: #38e8ff;
            --orange: #ff685d;
            --lime: #c9ff47;
        }
        .stApp {
            background: radial-gradient(circle at 78% 5%, rgba(126, 44, 154, 0.28), transparent 24rem),
                        radial-gradient(circle at 8% 50%, rgba(34, 117, 179, 0.13), transparent 22rem),
                        var(--ink);
            color: var(--text);
            font-family: 'Space Grotesk', sans-serif;
        }
        .block-container { max-width: 1480px; padding: 2.1rem 3.2rem 4rem; }
        [data-testid="stSidebar"] { background: #110d2c; border-right: 1px solid rgba(255,255,255,.08); }
        [data-testid="stSidebar"] .block-container { padding: 2rem 1.4rem; }
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: var(--muted) !important; }
        [data-testid="stSidebar"] h3 { color: white; font-size: 0.75rem; letter-spacing: .16em; text-transform: uppercase; }
        [data-testid="stMetric"] { background: linear-gradient(145deg, rgba(36, 25, 76, .92), rgba(19, 14, 48, .95)); border: 1px solid rgba(255,255,255,.08); border-radius: 18px; padding: 1.1rem 1.2rem; min-height: 126px; }
        [data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: .76rem; letter-spacing: .12em; text-transform: uppercase; }
        [data-testid="stMetricValue"] { color: white !important; font-size: 2rem; font-weight: 600; }
        [data-testid="stMetricDelta"] { font-family: 'DM Mono', monospace; }
        .hero { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 1.8rem; gap: 1rem; }
        .eyebrow { color: var(--pink); font: 500 .72rem 'DM Mono', monospace; letter-spacing: .22em; text-transform: uppercase; margin-bottom: .6rem; }
        .hero h1 { color: white; font-size: clamp(2.2rem, 5vw, 4.7rem); line-height: .93; letter-spacing: -.06em; margin: 0; font-weight: 600; }
        .hero h1 span { color: var(--cyan); }
        .hero-copy { color: var(--muted); max-width: 410px; font-size: .95rem; line-height: 1.55; text-align: right; }
        .status { color: var(--lime); border: 1px solid rgba(201,255,71,.5); border-radius: 99px; padding: .45rem .7rem; font: 500 .67rem 'DM Mono', monospace; letter-spacing: .09em; white-space: nowrap; }
        .section-label { display: flex; justify-content: space-between; align-items: center; color: var(--muted); font: 500 .7rem 'DM Mono', monospace; letter-spacing: .17em; text-transform: uppercase; margin: 1.7rem 0 .7rem; }
        .section-label b { color: var(--pink); font-weight: 500; }
        .panel-head { color: white; font-size: 1.1rem; font-weight: 600; margin: 0 0 .2rem; }
        .panel-sub { color: var(--muted); font-size: .78rem; margin: 0 0 .8rem; }
        .insight { background: linear-gradient(135deg, rgba(255,57,212,.13), rgba(56,232,255,.07)); border: 1px solid rgba(255,57,212,.28); border-radius: 16px; padding: 1rem 1.1rem; color: #f5edff; line-height: 1.5; font-size: .87rem; min-height: 95px; }
        .insight b { color: var(--pink); font: 500 .7rem 'DM Mono', monospace; letter-spacing: .12em; display: block; margin-bottom: .4rem; }
        .model-badge { display: inline-block; border-radius: 99px; padding: .34rem .65rem; color: var(--ink); background: var(--lime); font: 500 .7rem 'DM Mono', monospace; }
        .risk-card { border: 1px solid rgba(255,104,93,.42); background: linear-gradient(135deg, rgba(255,104,93,.19), rgba(255,57,212,.08)); border-radius: 18px; padding: 1.4rem; text-align: center; }
        .risk-number { color: var(--orange); font-size: 3.4rem; line-height: 1; font-weight: 600; }
        .risk-label { color: var(--muted); font: 500 .7rem 'DM Mono', monospace; letter-spacing: .13em; text-transform: uppercase; margin-top: .5rem; }
        .small-note { color: var(--muted); font-size: .75rem; line-height: 1.45; }
        div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { background: #1b1540; border-color: rgba(255,255,255,.12); }
        .stTabs [data-baseweb="tab-list"] { gap: .45rem; border-bottom: 1px solid rgba(255,255,255,.1); }
        .stTabs [data-baseweb="tab"] { color: var(--muted); font: 500 .75rem 'DM Mono', monospace; letter-spacing: .08em; text-transform: uppercase; padding: .75rem 1rem; }
        .stTabs [aria-selected="true"] { color: var(--pink); }
        .stDownloadButton button, .stButton button { border-radius: 10px; border: 1px solid rgba(255,57,212,.48); color: white; background: rgba(255,57,212,.12); }
        .stDataFrame { border: 1px solid rgba(255,255,255,.1); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def chart_layout(fig: go.Figure, height: int = 320) -> go.Figure:
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Space Grotesk, sans-serif", "color": "#f7f4ff", "size": 12},
        margin={"l": 8, "r": 8, "t": 16, "b": 8},
        legend={"bgcolor": "rgba(0,0,0,0)", "font": {"color": MUTED, "size": 11}},
        hoverlabel={"bgcolor": "#21194b", "font": {"color": "white"}},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, color=MUTED, tickfont={"size": 10})
    fig.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, color=MUTED, tickfont={"size": 10})
    return fig


def filtered_data(data: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.markdown("### View filters")
    departments = st.sidebar.multiselect("Department", sorted(data["Department"].unique()), default=sorted(data["Department"].unique()))
    outcomes = st.sidebar.multiselect("Attrition status", ["No", "Yes"], default=["No", "Yes"])
    overtime = st.sidebar.multiselect("Overtime", ["No", "Yes"], default=["No", "Yes"])
    age_min, age_max = int(data["Age"].min()), int(data["Age"].max())
    age_range = st.sidebar.slider("Age range", age_min, age_max, (age_min, age_max))
    roles = st.sidebar.multiselect("Job role", sorted(data["JobRole"].unique()), default=[])
    filtered = data[
        data["Department"].isin(departments)
        & data["Attrition"].isin(outcomes)
        & data["OverTime"].isin(overtime)
        & data["Age"].between(age_range[0], age_range[1])
    ].copy()
    if roles:
        filtered = filtered[filtered["JobRole"].isin(roles)]
    st.sidebar.divider()
    st.sidebar.markdown('<span class="small-note">Use the filters to recalculate every view. The simulator is independent.</span>', unsafe_allow_html=True)
    return filtered


def render_overview(data: pd.DataFrame, importance: pd.DataFrame, metadata: dict) -> None:
    total = len(data)
    leavers = int(data["Attrition_Binary"].sum())
    rate = leavers / total * 100 if total else 0
    avg_income = data["MonthlyIncome"].mean() if total else 0
    overtime_rate = data.loc[data["OverTime"].eq("Yes"), "Attrition_Binary"].mean() * 100 if data["OverTime"].eq("Yes").any() else 0
    st.markdown('<div class="section-label"><span>01 / workforce pulse</span><b>live slice</b></div>', unsafe_allow_html=True)
    kpis = st.columns(4)
    kpis[0].metric("Employees in view", f"{total:,}", f"{total / 1470 * 100:.0f}% of workforce")
    kpis[1].metric("Attrition rate", f"{rate:.1f}%", f"{leavers:,} employees left")
    kpis[2].metric("Avg monthly income", f"${avg_income:,.0f}", "filtered population")
    kpis[3].metric("Overtime attrition", f"{overtime_rate:.1f}%", "overtime employees")

    left, right = st.columns([1.02, 1.48], gap="large")
    with left:
        st.markdown('<div class="section-label"><span>Attrition mix</span><b>01</b></div>', unsafe_allow_html=True)
        counts = data["Attrition"].value_counts().reindex(["No", "Yes"], fill_value=0)
        pie = go.Figure(go.Pie(labels=["Stayed", "Left"], values=counts.values, hole=.74, marker_colors=[CYAN, PINK], textinfo="none", hovertemplate="%{label}: %{value:,}<extra></extra>"))
        pie.add_annotation(text=f"{rate:.1f}%<br><span style='font-size:11px'>ATTRITION</span>", x=.5, y=.5, showarrow=False, font={"size": 25, "color": "white"})
        st.plotly_chart(chart_layout(pie, 315), use_container_width=True, config={"displayModeBar": False})
    with right:
        st.markdown('<div class="section-label"><span>Department signal</span><b>02</b></div>', unsafe_allow_html=True)
        department = data.groupby("Department", as_index=False).agg(Attrition_Rate=("Attrition_Binary", "mean"), Employees=("Attrition_Binary", "size"))
        department["Attrition_Rate"] *= 100
        department = department.sort_values("Attrition_Rate")
        bars = px.bar(department, x="Attrition_Rate", y="Department", orientation="h", text="Attrition_Rate", color="Attrition_Rate", color_continuous_scale=[[0, CYAN], [.55, MAGENTA], [1, ORANGE]])
        bars.update_traces(texttemplate="%{text:.1f}%", textposition="outside", cliponaxis=False, hovertemplate="%{y}<br>%{x:.1f}% attrition<extra></extra>")
        bars.update_coloraxes(showscale=False)
        st.plotly_chart(chart_layout(bars, 315), use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-label"><span>Signals worth acting on</span><b>03</b></div>', unsafe_allow_html=True)
    strongest = importance.iloc[0]["Feature"]
    single_rate = data.loc[data["MaritalStatus"].eq("Single"), "Attrition_Binary"].mean() * 100 if data["MaritalStatus"].eq("Single").any() else 0
    income_gap = data.loc[data["Attrition"].eq("No"), "MonthlyIncome"].mean() - data.loc[data["Attrition"].eq("Yes"), "MonthlyIncome"].mean()
    cards = st.columns(3)
    cards[0].markdown(f'<div class="insight"><b>TOP DRIVER / {strongest.upper()}</b>Overtime carries the highest positive model coefficient. The filtered view shows <strong>{overtime_rate:.1f}%</strong> attrition among overtime employees.</div>', unsafe_allow_html=True)
    cards[1].markdown(f'<div class="insight"><b>COMPENSATION GAP</b>Employees who stay earn <strong>${income_gap:,.0f}</strong> more per month on average in this filtered population.</div>', unsafe_allow_html=True)
    cards[2].markdown(f'<div class="insight"><b>RETENTION WATCH</b>Single employees in view show <strong>{single_rate:.1f}%</strong> attrition. Pair this signal with role and tenure before acting.</div>', unsafe_allow_html=True)


def render_drivers(data: pd.DataFrame, importance: pd.DataFrame) -> None:
    st.markdown('<div class="section-label"><span>02 / driver intelligence</span><b>model coefficients</b></div>', unsafe_allow_html=True)
    left, right = st.columns([1.25, .75], gap="large")
    with left:
        top = importance.head(12).sort_values("Coefficient")
        top["Direction"] = np.where(top["Coefficient"] > 0, "Higher attrition risk", "Lower attrition risk")
        fig = px.bar(top, x="Coefficient", y="Feature", orientation="h", color="Direction", color_discrete_map={"Higher attrition risk": ORANGE, "Lower attrition risk": CYAN}, text="Coefficient")
        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside", cliponaxis=False, hovertemplate="%{y}<br>Coefficient: %{x:.3f}<extra></extra>")
        st.plotly_chart(chart_layout(fig, 500), use_container_width=True, config={"displayModeBar": False})
    with right:
        st.markdown('<div class="panel-head">Attrition by tenure</div><div class="panel-sub">Observed rate across years at company</div>', unsafe_allow_html=True)
        tenure = data.copy()
        tenure["Tenure band"] = pd.cut(tenure["YearsAtCompany"], bins=[-1, 1, 3, 5, 10, 50], labels=["0-1", "2-3", "4-5", "6-10", "11+"])
        tenure_view = tenure.groupby("Tenure band", observed=False, as_index=False).agg(Attrition=("Attrition_Binary", "mean"), Employees=("Attrition_Binary", "size"))
        tenure_view["Attrition"] *= 100
        line = px.line(tenure_view, x="Tenure band", y="Attrition", markers=True, text="Attrition")
        line.update_traces(line_color=PINK, marker_color=LIME, marker_size=10, texttemplate="%{text:.1f}%", textposition="top center", hovertemplate="%{x} years<br>%{y:.1f}% attrition<extra></extra>")
        st.plotly_chart(chart_layout(line, 250), use_container_width=True, config={"displayModeBar": False})
        role_view = data.groupby("JobRole", as_index=False).agg(Attrition=("Attrition_Binary", "mean"), Employees=("Attrition_Binary", "size"))
        role_view["Attrition"] *= 100
        role_view = role_view.sort_values("Attrition", ascending=True)
        role_fig = px.bar(role_view, x="Attrition", y="JobRole", orientation="h", color_discrete_sequence=[MAGENTA])
        role_fig.update_traces(hovertemplate="%{y}<br>%{x:.1f}% attrition<extra></extra>")
        st.plotly_chart(chart_layout(role_fig, 300), use_container_width=True, config={"displayModeBar": False})


def render_model(performance: pd.DataFrame, metadata: dict) -> None:
    st.markdown('<div class="section-label"><span>03 / model lab</span><b>validation snapshot</b></div>', unsafe_allow_html=True)
    st.markdown(f'<span class="model-badge">BEST MODEL / {metadata["best_model"].upper()}</span>', unsafe_allow_html=True)
    st.caption(f"Trained on {metadata['training_samples']:,} records and evaluated on {metadata['test_samples']:,} held-out records. Scores are from the exported project artifacts.")
    left, right = st.columns([1.2, .8], gap="large")
    with left:
        metric_cols = ["Accuracy", "Precision", "Recall", "F1 Score", "AUC-ROC"]
        long = performance.melt(id_vars=["Model"], value_vars=metric_cols, var_name="Metric", value_name="Score")
        chart = px.bar(long, x="Metric", y="Score", color="Model", barmode="group", color_discrete_sequence=[PINK, CYAN, ORANGE, LIME])
        chart.update_traces(hovertemplate="%{fullData.name}<br>%{x}: %{y:.3f}<extra></extra>")
        chart.update_yaxes(range=[0, 1])
        st.plotly_chart(chart_layout(chart, 400), use_container_width=True, config={"displayModeBar": False})
    with right:
        st.markdown('<div class="panel-head">Read the trade-off</div><div class="panel-sub">The selected model is accurate, but recall remains the pressure point.</div>', unsafe_allow_html=True)
        st.metric("AUC-ROC", f"{metadata['auc_roc']:.3f}")
        st.metric("Precision", f"{metadata['precision']:.3f}")
        st.metric("Recall", f"{metadata['recall']:.3f}")
        st.markdown('<div class="small-note">Use the simulator as a prioritization signal, not a standalone employment decision. Investigate the underlying experience before taking action.</div>', unsafe_allow_html=True)


def render_explorer(data: pd.DataFrame) -> None:
    st.markdown('<div class="section-label"><span>04 / employee explorer</span><b>filtered records</b></div>', unsafe_allow_html=True)
    search = st.text_input("Search role, department, or travel pattern", placeholder="Try: Sales Executive")
    view = data.copy()
    if search:
        mask = view.astype(str).apply(lambda column: column.str.contains(search, case=False, na=False)).any(axis=1)
        view = view[mask]
    columns = ["EmployeeNumber", "Age", "Department", "JobRole", "OverTime", "MonthlyIncome", "YearsAtCompany", "Attrition"]
    st.dataframe(view[columns].sort_values("EmployeeNumber"), use_container_width=True, hide_index=True, height=430, column_config={"MonthlyIncome": st.column_config.NumberColumn("Monthly income", format="$%d"), "Attrition": st.column_config.TextColumn("Attrition")})
    st.download_button("Download filtered employees", view.to_csv(index=False).encode("utf-8"), "filtered_hr_employees.csv", "text/csv")


def render_simulator(data: pd.DataFrame, features: list[str]) -> None:
    st.markdown('<div class="section-label"><span>05 / risk simulator</span><b>what-if scenario</b></div>', unsafe_allow_html=True)
    st.caption("Adjust the most actionable employee signals. Unedited model inputs use the dataset median or most common value, while categorical values follow the original notebook's LabelEncoder mapping.")
    left, right = st.columns([1.18, .82], gap="large")
    with left:
        c1, c2, c3 = st.columns(3)
        age = c1.slider("Age", int(data["Age"].min()), int(data["Age"].max()), 35)
        income = c2.number_input("Monthly income", min_value=1000, max_value=25000, value=5000, step=250)
        distance = c3.slider("Distance from home", 1, 30, 5)
        c4, c5, c6 = st.columns(3)
        department = c4.selectbox("Department", sorted(data["Department"].unique()), index=2)
        role = c5.selectbox("Job role", sorted(data["JobRole"].unique()), index=5)
        overtime = c6.selectbox("Overtime", ["No", "Yes"], index=1)
        c7, c8, c9 = st.columns(3)
        job_satisfaction = c7.slider("Job satisfaction", 1, 4, 3)
        environment = c8.slider("Environment satisfaction", 1, 4, 3)
        years_company = c9.slider("Years at company", 0, 40, 5)
        c10, c11, c12 = st.columns(3)
        travel = c10.selectbox("Business travel", sorted(data["BusinessTravel"].unique()), index=2)
        marital = c11.selectbox("Marital status", sorted(data["MaritalStatus"].unique()), index=2)
        level = c12.slider("Job level", 1, 5, 2)
        run_prediction = st.button("Run risk signal", use_container_width=True, type="primary")
    with right:
        if run_prediction or "prediction" not in st.session_state:
            model, scaler = load_model()
            model_frame = data.drop(columns=["Attrition", "Attrition_Binary", "EmployeeCount", "EmployeeNumber", "Over18", "StandardHours"])
            defaults = {}
            for column in model_frame.columns:
                if pd.api.types.is_numeric_dtype(model_frame[column]):
                    defaults[column] = model_frame[column].median()
                else:
                    defaults[column] = model_frame[column].mode().iloc[0]
            row = pd.DataFrame([defaults])
            scenario = {"Age": age, "BusinessTravel": travel, "Department": department, "DistanceFromHome": distance, "EnvironmentSatisfaction": environment, "JobLevel": level, "JobRole": role, "JobSatisfaction": job_satisfaction, "MaritalStatus": marital, "MonthlyIncome": income, "OverTime": overtime, "YearsAtCompany": years_company}
            for column, value in scenario.items():
                row.at[0, column] = value
            categorical = [column for column in features if not pd.api.types.is_numeric_dtype(data[column])]
            for column in categorical:
                labels = {value: index for index, value in enumerate(sorted(data[column].dropna().unique()))}
                row[column] = row[column].map(labels)
            values = row[features].astype(float)
            probability = float(model.predict_proba(scaler.transform(values))[:, 1][0])
            st.session_state["prediction"] = probability
        probability = st.session_state["prediction"]
        color = ORANGE if probability >= .5 else LIME
        label = "HIGHER RISK" if probability >= .5 else "LOWER RISK"
        st.markdown(f'<div class="risk-card"><div class="risk-number" style="color:{color}">{probability * 100:.1f}%</div><div class="risk-label">Predicted attrition probability / {label}</div></div>', unsafe_allow_html=True)
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=probability * 100, number={"suffix": "%", "font": {"color": "white", "size": 26}}, gauge={"axis": {"range": [0, 100], "tickcolor": MUTED}, "bar": {"color": color}, "bgcolor": "#21194b", "borderwidth": 0, "steps": [{"range": [0, 30], "color": "rgba(56,232,255,.16)"}, {"range": [30, 60], "color": "rgba(255,57,212,.16)"}, {"range": [60, 100], "color": "rgba(255,104,93,.18)"}]}))
        st.plotly_chart(chart_layout(gauge, 220), use_container_width=True, config={"displayModeBar": False})


def main() -> None:
    inject_style()
    employees, importance, performance, metadata, features = load_data()
    view = filtered_data(employees)
    st.markdown('<div class="hero"><div><div class="eyebrow">IBM HR ANALYTICS / PEOPLE PULSE</div><h1>Know your <span>people.</span></h1></div><div class="hero-copy"><span class="status">● MODEL ONLINE</span><br><br>Decision-ready workforce intelligence for retention, engagement, and responsible action.</div></div>', unsafe_allow_html=True)
    tabs = st.tabs(["Overview", "Drivers", "Model lab", "Employee explorer", "Risk simulator"])
    with tabs[0]:
        render_overview(view, importance, metadata)
    with tabs[1]:
        render_drivers(view, importance)
    with tabs[2]:
        render_model(performance, metadata)
    with tabs[3]:
        render_explorer(view)
    with tabs[4]:
        render_simulator(employees, features)
    st.markdown('<div class="section-label"><span>People Pulse / IBM HR Analytics</span><span>last updated 06 SEP 2026</span></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()