
import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Landscaping",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "Final_Horticulture_Dataset.xlsx"


@st.cache_data
def load_data():
    return pd.read_excel(DATA_PATH)


data = load_data()


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Plant",
    "Soil",
    "Sunlight",
    "Water_Freq",
    "Maint_Cost",
    "Aesthetic",
    "Success_Score",
    "Success_Category",
    "Survival_Rate"
]

missing_columns = [
    column for column in required_columns
    if column not in data.columns
]

if missing_columns:
    st.error(
        "Missing columns: " + ", ".join(missing_columns)
    )
    st.stop()


# ============================================================
# BASIC METRICS
# ============================================================

total_records = len(data)

unique_plants = data["Plant"].nunique()

average_success = round(
    data["Success_Score"].mean(),
    2
)

excellent_count = int(
    (data["Success_Category"] == "Excellent").sum()
)

minimum_success = round(
    data["Success_Score"].min(),
    2
)

maximum_success = round(
    data["Success_Score"].max(),
    2
)

median_success = round(
    data["Success_Score"].median(),
    2
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F4F7F3;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #12372A 0%,
            #1F5C45 55%,
            #2E7D5B 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    h1, h2, h3 {
        color: #12372A !important;
    }

    p {
        color: #42564B;
        line-height: 1.7;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #DCE7E0;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: #60746A !important;
    }

    div[data-testid="stMetricValue"] {
        color: #12372A !important;
        font-weight: 800;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(
            135deg,
            #1F5C45,
            #2E7D5B
        );
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 20px;
        font-size: 16px;
        font-weight: 700;
    }

    .stButton > button:hover {
        background: #12372A;
        color: white;
    }

    div[data-baseweb="select"] > div {
        border-radius: 10px;
        border-color: #CBD9D0;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 15px;
        overflow: hidden;
    }

    hr {
        border-color: #D8E3DC;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌿 Smart Landscaping")

    st.caption(
        "Data-Driven Plant Recommendation System"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📊 EDA Dashboard",
            "⭐ Success Score",
            "🌱 Plant Recommendation"
        ]
    )

    st.divider()

    st.metric(
        "Dataset Records",
        total_records
    )

    st.metric(
        "Plant Entries",
        unique_plants
    )


# ============================================================
# MAIN TITLE
# ============================================================

st.title("🌿 Smart Landscaping")

st.write(
    "Intelligent Plant Recommendation System for "
    "smarter, data-driven and sustainable garden planning."
)

st.divider()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🌱 Horticulture Records",
        total_records,
        "Survey responses collected"
    )

with col2:

    st.metric(
        "🌿 Plant Entries",
        unique_plants,
        "Unique plant entries"
    )

with col3:

    st.metric(
        "⭐ Average Success",
        average_success,
        "Overall Success Score"
    )

with col4:

    st.metric(
        "🏆 Excellent Plants",
        excellent_count,
        "Score ≥ 80"
    )


# ============================================================
# HOME PAGE
# ============================================================

if page == "🏠 Home":

    st.header("🌿 About the Project")

    st.write(
        "Smart Landscaping is a data-driven plant selection "
        "system designed to support better landscaping decisions. "
        "The system uses horticulture survey data to calculate "
        "a plant Success Score and recommend plants according "
        "to user requirements."
    )

    st.subheader("🎯 Project Objective")

    st.info(
        "The main objective is to use horticultural information "
        "such as survival rate, growth, lifespan, watering, "
        "maintenance cost and popularity to identify plants "
        "with better overall landscaping performance."
    )

    st.write(
        "The system also provides personalized plant "
        "recommendations based on soil, sunlight, watering "
        "frequency, maintenance budget and aesthetic purpose."
    )

    st.header("🔄 Project Workflow")

    process1, process2, process3, process4 = st.columns(4)

    with process1:

        st.subheader("1️⃣ Data Collection")

        st.write(
            "Horticulture responses were collected "
            "through a structured survey."
        )

    with process2:

        st.subheader("2️⃣ Data Preparation")

        st.write(
            "The collected data was cleaned, "
            "standardized and prepared for analysis."
        )

    with process3:

        st.subheader("3️⃣ Success Score")

        st.write(
            "Important plant performance factors "
            "were converted into weighted scores."
        )

    with process4:

        st.subheader("4️⃣ Recommendation")

        st.write(
            "Suitable plants are recommended according "
            "to the user's selected requirements."
        )

    st.header("⭐ Two Important Scores")

    score1, score2 = st.columns(2)

    with score1:

        st.subheader("⭐ Success Score")

        st.metric(
            "Meaning",
            "Overall Plant Performance"
        )

        st.write(
            "Measures the overall performance of a plant "
            "using survival rate, growth, lifespan, "
            "water requirement, maintenance cost and popularity."
        )

        st.write(
            "A higher Success Score indicates better "
            "overall landscaping performance according "
            "to the designed scoring framework."
        )

    with score2:

        st.subheader("🌱 Recommendation Score")

        st.metric(
            "Meaning",
            "User-Specific Plant Fit"
        )

        st.write(
            "Measures how well a plant matches the "
            "requirements selected by the user."
        )

        st.write(
            "Soil, sunlight, water, maintenance, "
            "aesthetic purpose and Success Score "
            "are considered."
        )

    st.success(
        "The current recommendation system is a "
        "rule-based weighted scoring system, not a trained "
        "machine-learning prediction model."
    )


# ============================================================
# EDA DASHBOARD
# ============================================================

elif page == "📊 EDA Dashboard":

    st.header("📊 Exploratory Data Analysis")

    st.write(
        "Explore the major characteristics and patterns "
        "present in the horticulture dataset."
    )

    # --------------------------------------------------------
    # SUCCESS CATEGORY
    # --------------------------------------------------------

    st.subheader("⭐ Success Category Distribution")

    category_counts = (
        data["Success_Category"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = [
        "Success Category",
        "Count"
    ]

    fig = px.bar(
        category_counts,
        x="Success Category",
        y="Count",
        text="Count",
        title="Distribution of Plant Success Categories"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#12372A"),
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # TOP 10 PLANTS
    # --------------------------------------------------------

    st.subheader("🏆 Top 10 Plants by Success Score")

    top10 = (
        data[
            [
                "Plant",
                "Success_Score"
            ]
        ]
        .sort_values(
            "Success_Score",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top10,
        x="Success_Score",
        y="Plant",
        orientation="h",
        text="Success_Score",
        title="Top 10 Plants by Success Score"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        yaxis=dict(
            categoryorder="total ascending"
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#12372A"),
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # SURVIVAL RATE
    # --------------------------------------------------------

    st.subheader("🌿 Survival Rate Distribution")

    survival_counts = (
        data["Survival_Rate"]
        .value_counts()
        .reset_index()
    )

    survival_counts.columns = [
        "Survival Rate",
        "Count"
    ]

    fig = px.bar(
        survival_counts,
        x="Survival Rate",
        y="Count",
        text="Count",
        title="Distribution of Survival Rate"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#12372A"),
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # SOIL AND SUNLIGHT
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🌱 Soil Type")

        soil_counts = (
            data["Soil"]
            .value_counts()
            .reset_index()
        )

        soil_counts.columns = [
            "Soil",
            "Count"
        ]

        fig = px.pie(
            soil_counts,
            names="Soil",
            values="Count",
            title="Soil Distribution"
        )

        fig.update_layout(
            paper_bgcolor="white",
            font=dict(color="#12372A"),
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("☀️ Sunlight Requirement")

        sunlight_counts = (
            data["Sunlight"]
            .value_counts()
            .reset_index()
        )

        sunlight_counts.columns = [
            "Sunlight",
            "Count"
        ]

        fig = px.bar(
            sunlight_counts,
            x="Sunlight",
            y="Count",
            text="Count",
            title="Sunlight Distribution"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#12372A"),
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # WATER AND AESTHETIC
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("💧 Water Frequency")

        water_counts = (
            data["Water_Freq"]
            .value_counts()
            .reset_index()
        )

        water_counts.columns = [
            "Water Frequency",
            "Count"
        ]

        fig = px.bar(
            water_counts,
            x="Water Frequency",
            y="Count",
            text="Count",
            title="Watering Frequency Distribution"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#12372A"),
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("🌸 Aesthetic Purpose")

        aesthetic_counts = (
            data["Aesthetic"]
            .value_counts()
            .reset_index()
        )

        aesthetic_counts.columns = [
            "Aesthetic",
            "Count"
        ]

        fig = px.pie(
            aesthetic_counts,
            names="Aesthetic",
            values="Count",
            title="Aesthetic Purpose Distribution"
        )

        fig.update_layout(
            paper_bgcolor="white",
            font=dict(color="#12372A"),
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # DATASET OVERVIEW
    # --------------------------------------------------------

    st.header("📋 Dataset Overview")

    d1, d2, d3, d4 = st.columns(4)

    with d1:

        st.metric(
            "Rows",
            data.shape[0]
        )

    with d2:

        st.metric(
            "Columns",
            data.shape[1]
        )

    with d3:

        st.metric(
            "Minimum Success Score",
            minimum_success
        )

    with d4:

        st.metric(
            "Maximum Success Score",
            maximum_success
        )


# ============================================================
# SUCCESS SCORE PAGE
# ============================================================

elif page == "⭐ Success Score":

    st.header("⭐ Plant Success Score")

    st.write(
        "The Success Score is a weighted index designed "
        "to summarize overall plant performance using "
        "multiple horticultural factors."
    )

    st.info(
        "The Success Score is a designed weighted index. "
        "It is not a machine-learning prediction."
    )

    st.subheader("🧮 Success Score Factors")

    factor1, factor2, factor3 = st.columns(3)

    with factor1:

        st.metric(
            "🌿 Survival Rate",
            "30%"
        )

        st.write(
            "Higher survival rate receives a higher score. "
            "Survival is given the largest weight because "
            "successful establishment is important in landscaping."
        )

    with factor2:

        st.metric(
            "📈 Growth Rate",
            "15%"
        )

        st.write(
            "Faster growth receives a higher score "
            "within the defined growth categories."
        )

    with factor3:

        st.metric(
            "🌳 Lifespan",
            "10%"
        )

        st.write(
            "Plants with longer expected lifespan "
            "receive higher scores."
        )

    factor4, factor5, factor6 = st.columns(3)

    with factor4:

        st.metric(
            "💧 Water Requirement",
            "15%"
        )

        st.write(
            "Less frequent watering receives a higher "
            "water-efficiency score."
        )

    with factor5:

        st.metric(
            "💰 Maintenance Cost",
            "15%"
        )

        st.write(
            "Lower maintenance cost receives a higher score."
        )

    with factor6:

        st.metric(
            "⭐ Popularity",
            "15%"
        )

        st.write(
            "More popular plants receive higher scores "
            "within the defined popularity categories."
        )

    st.subheader("📐 Success Score Formula")

    st.code(
        """
Success Score =
    (Survival Score / 4 × 30)
  + (Growth Score / 3 × 15)
  + (Lifespan Score / 4 × 10)
  + (Water Score / 4 × 15)
  + (Maintenance Score / 4 × 15)
  + (Popularity Score / 4 × 15)
        """,
        language="text"
    )

    st.subheader("📊 Score Summary")

    summary1, summary2, summary3, summary4 = st.columns(4)

    with summary1:

        st.metric(
            "Average",
            average_success
        )

    with summary2:

        st.metric(
            "Minimum",
            minimum_success
        )

    with summary3:

        st.metric(
            "Median",
            median_success
        )

    with summary4:

        st.metric(
            "Maximum",
            maximum_success
        )

    st.subheader("📌 Success Category Classification")

    category_definition = pd.DataFrame(
        {
            "Category": [
                "Excellent",
                "Good",
                "Average",
                "Low"
            ],
            "Score Range": [
                "80 – 100",
                "60 – 79.99",
                "40 – 59.99",
                "Below 40"
            ],
            "Meaning": [
                "Very strong overall performance",
                "Good overall performance",
                "Moderate overall performance",
                "Lower overall performance"
            ]
        }
    )

    st.dataframe(
        category_definition,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🏆 Top 10 Plants")

    top_plants = (
        data[
            [
                "Plant",
                "Success_Score",
                "Success_Category"
            ]
        ]
        .sort_values(
            "Success_Score",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_plants,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PLANT RECOMMENDATION PAGE
# ============================================================

elif page == "🌱 Plant Recommendation":

    st.header("🌱 Personalized Plant Recommendation")

    st.write(
        "Select your landscaping requirements below. "
        "The system will calculate a Recommendation Score "
        "and show plants that best match your selected criteria."
    )

    st.subheader("🎯 Select Your Requirements")

    requirement1, requirement2 = st.columns(2)

    with requirement1:

        soil = st.selectbox(
            "🌱 Soil Type",
            sorted(
                data["Soil"]
                .dropna()
                .unique()
                .tolist()
            )
        )

        sunlight = st.selectbox(
            "☀️ Sunlight Requirement",
            sorted(
                data["Sunlight"]
                .dropna()
                .unique()
                .tolist()
            )
        )

        water = st.selectbox(
            "💧 Watering Frequency",
            sorted(
                data["Water_Freq"]
                .dropna()
                .unique()
                .tolist()
            )
        )

    with requirement2:

        maintenance = st.selectbox(
            "💰 Maintenance Cost",
            sorted(
                data["Maint_Cost"]
                .dropna()
                .unique()
                .tolist()
            )
        )

        aesthetic = st.selectbox(
            "🌸 Aesthetic Purpose",
            sorted(
                data["Aesthetic"]
                .dropna()
                .unique()
                .tolist()
            )
        )

        top_n = st.slider(
            "🌿 Number of Recommendations",
            min_value=3,
            max_value=10,
            value=5
        )

    st.divider()

    # --------------------------------------------------------
    # RECOMMENDATION SCORE FUNCTION
    # --------------------------------------------------------

    def calculate_recommendation_score(
        row,
        selected_soil,
        selected_sunlight,
        selected_water,
        selected_maintenance,
        selected_aesthetic
    ):

        score = 0

        if row["Soil"] == selected_soil:
            score += 25

        if row["Sunlight"] == selected_sunlight:
            score += 20

        if row["Water_Freq"] == selected_water:
            score += 20

        if row["Maint_Cost"] == selected_maintenance:
            score += 15

        if row["Aesthetic"] == selected_aesthetic:
            score += 10

        score += (
            row["Success_Score"] / 100
        ) * 10

        return round(
            score,
            2
        )

    # --------------------------------------------------------
    # EXPLANATION FUNCTION
    # --------------------------------------------------------

    def explain_recommendation(
        row,
        selected_soil,
        selected_sunlight,
        selected_water,
        selected_maintenance,
        selected_aesthetic
    ):

        reasons = []

        if row["Soil"] == selected_soil:
            reasons.append(
                "🌱 Suitable for selected soil"
            )

        if row["Sunlight"] == selected_sunlight:
            reasons.append(
                "☀️ Matches sunlight requirement"
            )

        if row["Water_Freq"] == selected_water:
            reasons.append(
                "💧 Matches watering requirement"
            )

        if row["Maint_Cost"] == selected_maintenance:
            reasons.append(
                "💰 Matches maintenance budget"
            )

        if row["Aesthetic"] == selected_aesthetic:
            reasons.append(
                "🌸 Matches selected purpose"
            )

        if row["Success_Score"] >= 80:
            reasons.append(
                "⭐ High overall Success Score"
            )

        if not reasons:
            reasons.append(
                "📌 Selected based on the overall weighted score"
            )

        return reasons

    # --------------------------------------------------------
    # RECOMMENDATION BUTTON
    # --------------------------------------------------------

    # ============================================================
# RECOMMENDATION BUTTON
# ============================================================

if st.button(
    "🌿 Find Suitable Plants",
    use_container_width=True
):

    # --------------------------------------------------------
    # STRICT AESTHETIC FILTER
    # --------------------------------------------------------

    recommendations = data[
        data["Aesthetic"] == aesthetic
    ].copy()

    # --------------------------------------------------------
    # CHECK WHETHER PLANTS ARE AVAILABLE
    # --------------------------------------------------------

    if recommendations.empty:

        st.warning(
            f"No plants were found for the selected aesthetic: {aesthetic}"
        )

    else:

        # ----------------------------------------------------
        # CALCULATE RECOMMENDATION SCORE
        # ----------------------------------------------------

        recommendations[
            "Recommendation_Score"
        ] = recommendations.apply(
            lambda row:
                calculate_recommendation_score(
                    row,
                    soil,
                    sunlight,
                    water,
                    maintenance,
                    aesthetic
                ),
            axis=1
        )

        # ----------------------------------------------------
        # SORT BY RECOMMENDATION SCORE
        # ----------------------------------------------------

        recommendations = (
            recommendations
            .sort_values(
                "Recommendation_Score",
                ascending=False
            )
            .head(top_n)
        )

        st.success(
            f"{len(recommendations)} suitable {aesthetic} "
            "plants have been identified based on your requirements."
        )

        st.subheader("🌿 Recommended Plants")

        # ----------------------------------------------------
        # DISPLAY RECOMMENDED PLANTS
        # ----------------------------------------------------

        for rank, (_, row) in enumerate(
            recommendations.iterrows(),
            start=1
        ):

            st.markdown("---")

            st.subheader(
                f"#{rank} 🌿 {row['Plant']}"
            )

            score1, score2, score3 = st.columns(3)

            with score1:

                st.metric(
                    "Recommendation Score",
                    f"{row['Recommendation_Score']}/100"
                )

            with score2:

                st.metric(
                    "Success Score",
                    row["Success_Score"]
                )

            with score3:

                st.metric(
                    "Category",
                    row["Success_Category"]
                )

            detail1, detail2, detail3 = st.columns(3)

            with detail1:

                st.write(
                    f"🌱 **Soil:** {row['Soil']}"
                )

                st.write(
                    f"☀️ **Sunlight:** {row['Sunlight']}"
                )

            with detail2:

                st.write(
                    f"💧 **Water:** {row['Water_Freq']}"
                )

                st.write(
                    f"💰 **Maintenance:** {row['Maint_Cost']}"
                )

            with detail3:

                st.write(
                    f"🌸 **Aesthetic:** {row['Aesthetic']}"
                )

                st.write(
                    f"🌿 **Survival:** {row['Survival_Rate']}"
                )

            # ------------------------------------------------
            # WHY THIS PLANT?
            # ------------------------------------------------

            reasons = explain_recommendation(
                row,
                soil,
                sunlight,
                water,
                maintenance,
                aesthetic
            )

            st.write(
                "💡 **Why this plant?**"
            )

            for reason in reasons:

                st.write(
                    reason
                )

        # ----------------------------------------------------
        # RECOMMENDATION CHART
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "📊 Recommendation Score Comparison"
        )

        recommendation_chart = recommendations[
            [
                "Plant",
                "Recommendation_Score"
            ]
        ].copy()

        recommendation_chart = (
            recommendation_chart
            .sort_values(
                "Recommendation_Score",
                ascending=True
            )
        )

        fig = px.bar(
            recommendation_chart,
            x="Recommendation_Score",
            y="Plant",
            orientation="h",
            text="Recommendation_Score",
            title="Recommended Plants by Recommendation Score"
        )

        fig.update_traces(
            textposition="outside"
        )

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#12372A"),
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.info(
        "👆 Select your requirements and click "
        "'Find Suitable Plants' to generate recommendations."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌿 Smart Landscaping Recommendation System | "
    "MSc Data Science Project"
)

st.caption(
    "Python • Pandas • Plotly • Streamlit | "
    "Data-Driven Plant Selection for Smarter Landscaping"
)