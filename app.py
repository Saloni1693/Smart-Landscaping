%%writefile app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# SMART LANDSCAPING - PROFESSIONAL STREAMLIT APP
# ==========================================================

st.set_page_config(
    page_title="Smart Landscaping",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- DATA ----------
DATA_PATH = "Final_Horticulture_Dataset.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(DATA_PATH)
    return df

try:
    data = load_data()
except Exception:
    st.error("Dataset not found. Keep 'Final_Horticulture_Dataset.xlsx' in the same folder as app.py.")
    st.stop()

# ---------- BASIC CHECK ----------
required = [
    "Plant", "Soil", "Sunlight", "Water_Freq", "Maint_Cost",
    "Aesthetic", "Success_Score", "Success_Category", "Survival_Rate"
]

missing = [c for c in required if c not in data.columns]
if missing:
    st.error("Missing columns: " + ", ".join(missing))
    st.stop()

data = data.copy()
data["Success_Score"] = pd.to_numeric(data["Success_Score"], errors="coerce")
data = data.dropna(subset=["Success_Score"])

for c in ["Plant", "Soil", "Sunlight", "Water_Freq", "Maint_Cost",
          "Aesthetic", "Success_Category", "Survival_Rate"]:
    data[c] = data[c].astype(str).str.strip()

# ---------- PROFESSIONAL STYLE ----------
st.markdown("""
<style>
.stApp {
    background: #F5F8F5;
    color: #24342B;
    font-family: "Segoe UI", Arial, sans-serif;
}
.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#103B2A,#1D6042,#0D2E21);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}
h1,h2,h3 {
    color: #16452F !important;
}
.hero {
    background: linear-gradient(135deg,#103B2A,#28734D,#72A66E);
    border-radius: 24px;
    padding: 2.3rem 2.6rem;
    color: white;
    box-shadow: 0 12px 30px rgba(20,70,45,.16);
    margin-bottom: 1.4rem;
}
.hero h1 {
    color: white !important;
    font-size: 2.55rem;
    margin-bottom: .4rem;
}
.hero p {
    color: rgba(255,255,255,.9);
    font-size: 1.05rem;
    max-width: 850px;
    line-height: 1.6;
}
.card {
    background: white;
    border: 1px solid #DDE8DF;
    border-radius: 18px;
    padding: 1.25rem;
    box-shadow: 0 5px 18px rgba(20,50,35,.06);
    margin-bottom: 1rem;
}
.kpi {
    background: white;
    border: 1px solid #DDE8DF;
    border-radius: 18px;
    padding: 1.15rem;
    min-height: 120px;
    box-shadow: 0 5px 18px rgba(20,50,35,.06);
}
.kpi-label {
    color: #718078;
    font-size: .78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .05em;
}
.kpi-value {
    color: #17603E;
    font-size: 2rem;
    font-weight: 800;
    margin-top: .25rem;
}
.kpi-note {
    color: #87928B;
    font-size: .78rem;
}
.info {
    background: #EDF7EF;
    border-left: 5px solid #3B8B5B;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    margin: .7rem 0 1rem;
}
.dark {
    background: linear-gradient(135deg,#153E2C,#245D40);
    color: white;
    border-radius: 18px;
    padding: 1.3rem;
    box-shadow: 0 8px 22px rgba(20,60,40,.13);
}
.dark h3 { color: white !important; }
.recommend {
    background: white;
    border: 1px solid #DDE8DF;
    border-radius: 20px;
    padding: 1.35rem;
    margin: .8rem 0;
    box-shadow: 0 7px 24px rgba(20,50,35,.07);
}
.plant {
    color: #17603E;
    font-size: 1.35rem;
    font-weight: 800;
}
.score {
    color: #17603E;
    font-size: 2rem;
    font-weight: 800;
}
.reason {
    background: #F0F7F1;
    border-radius: 9px;
    padding: .42rem .65rem;
    margin: .25rem 0;
    color: #31543E;
}
.stButton > button {
    background: linear-gradient(135deg,#1C6B48,#34865C);
    color: white;
    border: none;
    border-radius: 11px;
    font-weight: 700;
    padding: .65rem 1rem;
}
.footer {
    margin-top: 3rem;
    padding: 1.2rem;
    text-align: center;
    color: #77847C;
    border-top: 1px solid #DDE6DF;
}
</style>
""", unsafe_allow_html=True)

# ---------- FUNCTIONS ----------
def kpi(label, value, note):
    return f"""
    <div class="kpi">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """

def recommendation_score(row, soil, sunlight, water, maintenance, aesthetic):
    score = 0
    if row["Soil"] == soil:
        score += 25
    if row["Sunlight"] == sunlight:
        score += 20
    if row["Water_Freq"] == water:
        score += 20
    if row["Maint_Cost"] == maintenance:
        score += 15
    if row["Aesthetic"] == aesthetic:
        score += 10

    score += (row["Success_Score"] / 100) * 10
    return round(score, 2)

def reasons(row, soil, sunlight, water, maintenance, aesthetic):
    r = []
    if row["Soil"] == soil:
        r.append("🌱 Soil requirement matched")
    if row["Sunlight"] == sunlight:
        r.append("☀️ Sunlight requirement matched")
    if row["Water_Freq"] == water:
        r.append("💧 Watering requirement matched")
    if row["Maint_Cost"] == maintenance:
        r.append("💰 Maintenance budget matched")
    if row["Aesthetic"] == aesthetic:
        r.append("🌸 Aesthetic purpose matched")
    if row["Success_Score"] >= 80:
        r.append("⭐ High overall Success Score")
    return r

# ---------- METRICS ----------
records = len(data)
plants = data["Plant"].nunique()
average = data["Success_Score"].mean()
excellent = (data["Success_Category"] == "Excellent").sum()
highest = data["Success_Score"].max()
lowest = data["Success_Score"].min()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:10px 0 20px">
        <div style="font-size:3.2rem">🌿</div>
        <div style="font-size:1.45rem;font-weight:800">Smart Landscaping</div>
        <div style="font-size:.8rem;opacity:.8">Plant Intelligence & Decision Support</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATION",
        ["🏠 Home", "📊 EDA Dashboard", "⭐ Success Score", "🌱 Plant Recommendation"]
    )

    st.markdown("---")
    st.caption("M.Sc. Data Science Research Project")
    st.caption("Current approach: Weighted Success Score + Rule-Based Recommendation")

# ==========================================================
# HOME
# ==========================================================
if page == "🏠 Home":

    st.markdown("""
    <div class="hero">
        <h1>Smart Landscaping</h1>
        <p>
        A data-driven decision support application for evaluating plant performance
        and recommending suitable plants according to landscaping requirements.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Project Overview")
    st.caption("From horticulture survey data to an interactive plant recommendation system.")

    a,b,c,d = st.columns(4)
    with a: st.markdown(kpi("Survey Records",records,"Current dataset"),unsafe_allow_html=True)
    with b: st.markdown(kpi("Plant Entries",plants,"Unique plant names"),unsafe_allow_html=True)
    with c: st.markdown(kpi("Average Success",f"{average:.2f}","Weighted score"),unsafe_allow_html=True)
    with d: st.markdown(kpi("Excellent",excellent,"Score ≥ 80"),unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    left,right = st.columns([1.15,.85])

    with left:
        st.markdown("""
        <div class="card">
        <h3>What does this application do?</h3>
        <p>
        The application analyzes horticulture survey responses and creates a
        transparent <b>Landscape Success Score</b> using survival, growth,
        lifespan, water requirement, maintenance and popularity.
        </p>
        <p>
        It also provides a <b>Plant Recommendation System</b> where users select
        soil, sunlight, watering, maintenance and aesthetic requirements.
        </p>
        <p style="margin-bottom:0">
        The current recommendation engine is <b>rule-based and weighted</b>.
        Machine learning is a future extension after collecting more data.
        </p>
        </div>
        """,unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="dark">
        <h3>Research Pipeline</h3>
        <p>01 · Data Collection</p>
        <p>02 · Data Cleaning</p>
        <p>03 · Feature Scoring</p>
        <p>04 · Weighted Success Score</p>
        <p>05 · Exploratory Data Analysis</p>
        <p>06 · Rule-Based Recommendation</p>
        <p>07 · Streamlit Application</p>
        </div>
        """,unsafe_allow_html=True)

    weights = pd.DataFrame({
        "Factor":["Survival","Growth","Lifespan","Water","Maintenance","Popularity"],
        "Weight":[30,15,10,15,15,15]
    })

    fig = px.bar(
        weights.sort_values("Weight"),
        x="Weight", y="Factor", orientation="h",
        text="Weight",
        title="Landscape Success Score – Factor Weights",
        template="simple_white"
    )
    fig.update_traces(marker_color="#2E7D57", texttemplate="%{text}%", textposition="outside")
    fig.update_layout(height=370, margin=dict(l=20,r=30,t=60,b=20))
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("""
    <div class="info">
    <b>Research note:</b> The Success Score is a project-designed weighted
    decision-support index. It is not currently a machine-learning prediction.
    </div>
    """,unsafe_allow_html=True)

# ==========================================================
# EDA
# ==========================================================
elif page == "📊 EDA Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>📊 Exploratory Data Analysis</h1>
        <p>Visual exploration of plant characteristics and Success Score patterns.</p>
    </div>
    """,unsafe_allow_html=True)

    a,b,c,d = st.columns(4)
    with a: st.markdown(kpi("Records",records,"Survey observations"),unsafe_allow_html=True)
    with b: st.markdown(kpi("Unique Plants",plants,"Plant names"),unsafe_allow_html=True)
    with c: st.markdown(kpi("Highest Score",f"{highest:.2f}","Maximum"),unsafe_allow_html=True)
    with d: st.markdown(kpi("Lowest Score",f"{lowest:.2f}","Minimum"),unsafe_allow_html=True)

    col1,col2 = st.columns(2)

    with col1:
        x=data["Success_Category"].value_counts().reindex(
            ["Excellent","Good","Average","Low"]).fillna(0).reset_index()
        x.columns=["Category","Count"]
        fig=px.bar(x,x="Category",y="Count",text="Count",
                   title="Success Category Distribution",template="simple_white")
        fig.update_traces(marker_color="#2E7D57",textposition="outside")
        fig.update_layout(height=390)
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        x=data.groupby("Plant",as_index=False)["Success_Score"].mean()
        x=x.sort_values("Success_Score",ascending=False).head(10).sort_values("Success_Score")
        fig=px.bar(x,x="Success_Score",y="Plant",orientation="h",
                   text="Success_Score",title="Top 10 Plants by Success Score",
                   template="simple_white")
        fig.update_traces(marker_color="#4F8F62",texttemplate="%{text:.2f}",textposition="outside")
        fig.update_layout(height=390)
        st.plotly_chart(fig,use_container_width=True)

    col1,col2=st.columns(2)

    with col1:
        x=data["Soil"].value_counts().reset_index()
        x.columns=["Soil","Count"]
        fig=px.pie(x,names="Soil",values="Count",hole=.48,title="Soil Distribution")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        x=data["Sunlight"].value_counts().reset_index()
        x.columns=["Sunlight","Count"]
        fig=px.pie(x,names="Sunlight",values="Count",hole=.48,title="Sunlight Distribution")
        st.plotly_chart(fig,use_container_width=True)

    col1,col2=st.columns(2)

    with col1:
        x=data["Water_Freq"].value_counts().reset_index()
        x.columns=["Water Frequency","Count"]
        fig=px.bar(x.sort_values("Count"),x="Count",y="Water Frequency",
                   orientation="h",text="Count",title="Watering Frequency",
                   template="simple_white")
        fig.update_traces(marker_color="#5C9B68",textposition="outside")
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        x=data["Aesthetic"].value_counts().reset_index()
        x.columns=["Aesthetic","Count"]
        fig=px.bar(x.sort_values("Count"),x="Count",y="Aesthetic",
                   orientation="h",text="Count",title="Aesthetic Purpose",
                   template="simple_white")
        fig.update_traces(marker_color="#3D8B5B",textposition="outside")
        st.plotly_chart(fig,use_container_width=True)

    fig=px.histogram(data,x="Success_Score",nbins=18,
                     title="Distribution of Success Scores",template="simple_white")
    fig.update_traces(marker_color="#2E7D57")
    st.plotly_chart(fig,use_container_width=True)

    with st.expander("View Dataset"):
        st.dataframe(data,use_container_width=True,height=430)

# ==========================================================
# SUCCESS SCORE
# ==========================================================
elif page == "⭐ Success Score":

    st.markdown("""
    <div class="hero">
        <h1>⭐ Landscape Success Score</h1>
        <p>
        A transparent weighted index designed to summarize plant performance
        using the factors available in the horticulture survey.
        </p>
    </div>
    """,unsafe_allow_html=True)

    st.markdown("""
    <div class="info">
    <b>Important:</b> This is a project-designed weighted index, not a trained ML prediction model.
    </div>
    """,unsafe_allow_html=True)

    left,right=st.columns([1.15,.85])

    with left:
        st.markdown("### Scoring Framework")
        table=pd.DataFrame({
            "Factor":["Survival Rate","Growth Rate","Lifespan",
                      "Water Requirement","Maintenance Cost","Popularity"],
            "Weight":["30%","15%","10%","15%","15%","15%"],
            "Higher Score Means":[
                "Higher survival",
                "Faster growth",
                "Longer lifespan",
                "Less frequent watering",
                "Lower maintenance cost",
                "Higher popularity"
            ]
        })
        st.dataframe(table,use_container_width=True,hide_index=True)

    with right:
        st.markdown("### Score Categories")
        cats=pd.DataFrame({
            "Range":["80–100","60–79","40–59","Below 40"],
            "Category":["Excellent","Good","Average","Low"]
        })
        st.dataframe(cats,use_container_width=True,hide_index=True)

        st.markdown("""
        <div class="dark">
        <h3>Interpretation</h3>
        <p>A higher score means stronger performance across the selected project factors.</p>
        </div>
        """,unsafe_allow_html=True)

    a,b,c,d=st.columns(4)
    with a: st.markdown(kpi("Average",f"{average:.2f}","Mean score"),unsafe_allow_html=True)
    with b: st.markdown(kpi("Highest",f"{highest:.2f}","Maximum score"),unsafe_allow_html=True)
    with c: st.markdown(kpi("Excellent",excellent,"Score ≥ 80"),unsafe_allow_html=True)
    with d: st.markdown(kpi("Good",(data["Success_Category"]=="Good").sum(),"Score 60–79"),unsafe_allow_html=True)

    st.markdown("### Top Plants")

    top=data.groupby(["Plant","Success_Category"],as_index=False)["Success_Score"].mean()
    top=top.sort_values("Success_Score",ascending=False).head(10)
    top["Success_Score"]=top["Success_Score"].round(2)
    st.dataframe(top,use_container_width=True,hide_index=True)

# ==========================================================
# RECOMMENDATION
# ==========================================================
else:

    # =========================================================
    # FIX: MAKE RECOMMENDATION SYSTEM LABELS BLACK & VISIBLE
    # =========================================================
    st.markdown("""
    <style>

    /* Main recommendation heading */
    div[data-testid="stMarkdownContainer"] h3 {
        color: #000000 !important;
    }

    /* Selectbox labels */
    div[data-testid="stSelectbox"] label {
        color: #000000 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    div[data-testid="stSelectbox"] label p {
        color: #000000 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* Slider label */
    div[data-testid="stSlider"] label {
        color: #000000 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    div[data-testid="stSlider"] label p {
        color: #000000 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* Selectbox selected value */
    div[data-testid="stSelectbox"] [data-baseweb="select"] span {
        color: #000000 !important;
    }

    div[data-testid="stSelectbox"] [data-baseweb="select"] p {
        color: #000000 !important;
    }

    /* Selectbox box */
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div {
        color: #000000 !important;
    }

    /* Dropdown options */
    div[data-baseweb="popover"] li {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    /* Slider numbers */
    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
        color: #000000 !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(""" 
    <div class="hero"> 
        <h1>🌱 Plant Recommendation</h1> 
        <p> 
        Select your landscaping requirements and discover plants that match 
        the selected aesthetic purpose and receive high suitability scores. 
        </p> 
    </div> 
    """, unsafe_allow_html=True) 
 
    st.markdown(""" 
    <div class="info"> 
    <b>How it works:</b> Aesthetic purpose is currently used as a strict filter. 
    Soil, sunlight, water and maintenance are matched through weighted scoring, 
    while Success Score contributes to the final ranking. 
    </div> 
    """, unsafe_allow_html=True) 
 
    st.markdown("### 1. Select Your Requirements") 
 
    c1,c2,c3=st.columns(3) 
 
    with c1: 
        soil=st.selectbox("🌱 Soil Type",sorted(data["Soil"].unique())) 
        sunlight=st.selectbox("☀️ Sunlight",sorted(data["Sunlight"].unique())) 
 
    with c2: 
        water=st.selectbox("💧 Water Frequency",sorted(data["Water_Freq"].unique())) 
        maintenance=st.selectbox("💰 Maintenance Cost",sorted(data["Maint_Cost"].unique())) 
 
    with c3: 
        aesthetic=st.selectbox("🌸 Aesthetic Purpose",sorted(data["Aesthetic"].unique())) 
        top_n=st.slider("🏆 Number of Recommendations",1,10,5)

    if st.button("🔎 Find Suitable Plants",use_container_width=True):

        # IMPORTANT: aesthetic is a strict filter
        rec=data[data["Aesthetic"]==aesthetic].copy()

        if rec.empty:
            st.warning(f"No plants found for {aesthetic}.")
            st.stop()

        rec["Recommendation_Score"]=rec.apply(
            lambda row: recommendation_score(
                row,soil,sunlight,water,maintenance,aesthetic
            ),axis=1
        )

        rec=rec.sort_values(
            ["Recommendation_Score","Success_Score"],
            ascending=False
        ).head(top_n)

        st.markdown("### 2. Recommended Plants")
        st.caption(f"Showing top {len(rec)} result(s) for {aesthetic} purpose.")

        for rank,(_,row) in enumerate(rec.iterrows(),1):

            st.markdown(f"""
            <div class="recommend">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <div style="font-size:.75rem;color:#718078;font-weight:700">
                        RANK #{rank}
                        </div>
                        <div class="plant">🌿 {row["Plant"]}</div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:.75rem;color:#718078;font-weight:700">
                        RECOMMENDATION SCORE
                        </div>
                        <div class="score">{row["Recommendation_Score"]:.2f}
                        <span style="font-size:.85rem;color:#718078">/100</span></div>
                    </div>
                </div>
                <hr style="border:none;border-top:1px solid #E6ECE7">
                <b>Success Score:</b> {row["Success_Score"]:.2f}/100
                &nbsp;&nbsp; | &nbsp;&nbsp;
                <b>Category:</b> {row["Success_Category"]}
                &nbsp;&nbsp; | &nbsp;&nbsp;
                <b>Survival:</b> {row["Survival_Rate"]}
            </div>
            """,unsafe_allow_html=True)

            a,b,c=st.columns(3)
            with a:
                st.markdown(f"""
                <div class="card">
                <b>🌱 Soil</b><br>{row["Soil"]}<br><br>
                <b>☀️ Sunlight</b><br>{row["Sunlight"]}
                </div>
                """,unsafe_allow_html=True)
            with b:
                st.markdown(f"""
                <div class="card">
                <b>💧 Water</b><br>{row["Water_Freq"]}<br><br>
                <b>💰 Maintenance</b><br>{row["Maint_Cost"]}
                </div>
                """,unsafe_allow_html=True)
            with c:
                st.markdown(f"""
                <div class="card">
                <b>🌸 Aesthetic</b><br>{row["Aesthetic"]}<br><br>
                <b>🌿 Survival</b><br>{row["Survival_Rate"]}
                </div>
                """,unsafe_allow_html=True)

            st.markdown("**Why this plant?**")
            for reason in reasons(row,soil,sunlight,water,maintenance,aesthetic):
                st.markdown(f'<div class="reason">{reason}</div>',unsafe_allow_html=True)

        chart=rec[["Plant","Recommendation_Score"]].sort_values("Recommendation_Score")
        fig=px.bar(
            chart,x="Recommendation_Score",y="Plant",orientation="h",
            text="Recommendation_Score",
            title="Recommendation Score Comparison",
            template="simple_white"
        )
        fig.update_traces(
            marker_color="#2E7D57",
            texttemplate="%{text:.2f}",
            textposition="outside"
        )
        fig.update_layout(
            height=max(380,70*len(chart)),
            xaxis_title="Recommendation Score (out of 100)",
            yaxis_title=""
        )
        st.plotly_chart(fig,use_container_width=True)

        st.markdown("""
        <div class="info">
        <b>Interpretation:</b> A higher Recommendation Score means a stronger
        match with the selected requirements under the current project rules.
        It does not mean the plant is universally the best choice.
        </div>
        """,unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="dark">
        <h3>Ready to explore?</h3>
        <p>Select your requirements above and click
        <b>Find Suitable Plants</b> to generate recommendations.</p>
        </div>
        """,unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
<b>Smart Landscaping</b> · Landscape Success Score & Plant Recommendation System<br>
M.Sc. Data Science Research Project · Python · Pandas · Plotly · Streamlit
</div>
""",unsafe_allow_html=True)
