import pandas as pd
import streamlit as st

# Load dataset
df = pd.read_csv("data/Placement_Data_Full_Class.csv")

# Page configuration
st.set_page_config(
    page_title="College Placement Intelligence",
    page_icon="🎓",
    layout="wide"
)

# Title
st.title("🎓 College Placement Intelligence & Prediction System")
st.caption(
    "Business Intelligence dashboard for analyzing placement outcomes, "
    "academic performance, salary trends, and placement predictions."
)
st.write(
    "Business Intelligence dashboard for analyzing college placement outcomes."
)

# ------------------------------------------------------------
# KPI CALCULATIONS
# ------------------------------------------------------------

total_students = len(df)

placed_students = df[df["status"] == "Placed"]
placed_count = len(placed_students)

placement_rate = (placed_count / total_students) * 100

average_salary = placed_students["salary"].mean()
highest_salary = placed_students["salary"].max()

# ------------------------------------------------------------
# KPI CARDS
# ------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Students",
    total_students
)

col2.metric(
    "Placement Rate",
    f"{placement_rate:.2f}%"
)

col3.metric(
    "Average Salary",
    f"{average_salary:.2f} LPA"
)

col4.metric(
    "Highest Salary",
    f"{highest_salary:.2f} LPA"
)

# ------------------------------------------------------------
# PLACEMENT STATUS
# ------------------------------------------------------------
st.header("1. Executive Overview")
st.subheader("Placement Overview")

status_counts = df["status"].value_counts()

st.bar_chart(status_counts)

# ------------------------------------------------------------
# DATA PREVIEW
# ------------------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(df.head(10))

# ------------------------------------------------------------
# DIAGNOSTIC ANALYSIS
# ------------------------------------------------------------
st.header("2. Diagnostic Analysis")
st.subheader("Placement Rate by Work Experience")

workex_placement = pd.crosstab(
    df["workex"],
    df["status"],
    normalize="index"
) * 100

st.bar_chart(workex_placement["Placed"])


st.subheader("Placement Rate by MBA Specialization")

specialisation_placement = pd.crosstab(
    df["specialisation"],
    df["status"],
    normalize="index"
) * 100

st.bar_chart(specialisation_placement["Placed"])


st.subheader("Placement Rate by Degree Percentage")

df["degree_group"] = pd.cut(
    df["degree_p"],
    bins=[0, 60, 70, 80, 100],
    labels=["Below 60", "60-70", "70-80", "80+"]
)

degree_placement = pd.crosstab(
    df["degree_group"],
    df["status"],
    normalize="index"
) * 100

st.bar_chart(degree_placement["Placed"])

# ------------------------------------------------------------
# PLACEMENT PREDICTION
# ------------------------------------------------------------

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


st.header("3. Placement Prediction")
st.subheader("Prediction Tool")

st.write(
    "This model estimates the probability of placement based on "
    "academic performance, work experience, and other student attributes."
)

# Create target variable
ml_df = df.copy()

ml_df["placement_target"] = (
    ml_df["status"] == "Placed"
).astype(int)

# Select model features
features = [
    "gender",
    "ssc_p",
    "ssc_b",
    "hsc_p",
    "hsc_b",
    "hsc_s",
    "degree_p",
    "degree_t",
    "workex",
    "etest_p",
    "specialisation",
    "mba_p"
]

X = ml_df[features]
y = ml_df["placement_target"]

# Numerical and categorical features
numeric_features = [
    "ssc_p",
    "hsc_p",
    "degree_p",
    "etest_p",
    "mba_p"
]

categorical_features = [
    "gender",
    "ssc_b",
    "hsc_b",
    "hsc_s",
    "degree_t",
    "workex",
    "specialisation"
]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numeric_features
        ),
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)

# Logistic Regression model
prediction_model = Pipeline([
    ("preprocessor", preprocessor),
    (
        "classifier",
        LogisticRegression(max_iter=1000)
    )
])

# Train model
prediction_model.fit(X_train, y_train)


# Prediction form
st.write("### Enter Student Details")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox(
        "Gender",
        sorted(df["gender"].dropna().unique())
    )

    ssc_p = st.number_input(
        "SSC Percentage",
        min_value=0.0,
        max_value=100.0,
        value=70.0
    )

    hsc_p = st.number_input(
        "HSC Percentage",
        min_value=0.0,
        max_value=100.0,
        value=70.0
    )

    degree_p = st.number_input(
        "Degree Percentage",
        min_value=0.0,
        max_value=100.0,
        value=70.0
    )

    etest_p = st.number_input(
        "Entrance Test Percentage",
        min_value=0.0,
        max_value=100.0,
        value=70.0
    )

    mba_p = st.number_input(
        "MBA Percentage",
        min_value=0.0,
        max_value=100.0,
        value=70.0
    )

with col2:
    ssc_b = st.selectbox(
        "SSC Board",
        sorted(df["ssc_b"].dropna().unique())
    )

    hsc_b = st.selectbox(
        "HSC Board",
        sorted(df["hsc_b"].dropna().unique())
    )

    hsc_s = st.selectbox(
        "HSC Specialization",
        sorted(df["hsc_s"].dropna().unique())
    )

    degree_t = st.selectbox(
        "Degree Type",
        sorted(df["degree_t"].dropna().unique())
    )

    workex = st.selectbox(
        "Work Experience",
        sorted(df["workex"].dropna().unique())
    )

    specialisation = st.selectbox(
        "MBA Specialization",
        sorted(df["specialisation"].dropna().unique())
    )


if st.button("Predict Placement Probability"):

    student_data = pd.DataFrame({
        "gender": [gender],
        "ssc_p": [ssc_p],
        "ssc_b": [ssc_b],
        "hsc_p": [hsc_p],
        "hsc_b": [hsc_b],
        "hsc_s": [hsc_s],
        "degree_p": [degree_p],
        "degree_t": [degree_t],
        "workex": [workex],
        "etest_p": [etest_p],
        "specialisation": [specialisation],
        "mba_p": [mba_p]
    })

    probability = prediction_model.predict_proba(
        student_data
    )[0][1]

    percentage = probability * 100

    st.success(
        f"Estimated Placement Probability: {percentage:.2f}%"
    )

    if probability >= 0.70:
        risk = "Lower Risk"
    elif probability >= 0.40:
        risk = "Medium Risk"
    else:
        risk = "Higher Risk"

    st.info(f"Project-defined Risk Category: {risk}")
# ------------------------------------------------------------
# SALARY ANALYSIS
# ------------------------------------------------------------

st.header("4. Salary Analysis")

st.subheader("Salary Distribution of Placed Students")

placed_df = df[df["status"] == "Placed"].copy()

st.bar_chart(
    placed_df["salary"].value_counts().sort_index()
)

st.subheader("Average Salary by MBA Specialization")

salary_by_specialisation = (
    placed_df
    .groupby("specialisation")["salary"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(salary_by_specialisation)

st.write(
    "Salary analysis is based only on students who were placed "
    "and have salary information available."
)    
# ------------------------------------------------------------
# KEY BUSINESS INSIGHTS
# ------------------------------------------------------------

st.header("5. Key Business Insights")

st.write("### Work Experience")

workex_rates = (
    df.groupby("workex")["status"]
    .apply(lambda x: (x == "Placed").mean() * 100)
)

for category, rate in workex_rates.items():
    st.write(
        f"- Students with **{category}** work experience "
        f"had a placement rate of **{rate:.2f}%** in this dataset."
    )

st.write("### MBA Specialization")

specialisation_rates = (
    df.groupby("specialisation")["status"]
    .apply(lambda x: (x == "Placed").mean() * 100)
)

for category, rate in specialisation_rates.items():
    st.write(
        f"- **{category}** specialization had a placement rate "
        f"of **{rate:.2f}%** in this dataset."
    )

st.write("### Academic Performance")

degree_rates = (
    df.groupby("degree_group", observed=True)["status"]
    .apply(lambda x: (x == "Placed").mean() * 100)
)

for category, rate in degree_rates.items():
    st.write(
        f"- The **{category}** degree-percentage group had a "
        f"placement rate of **{rate:.2f}%**."
    )

st.caption(
    "These findings describe associations observed in the dataset. "
    "They should not be interpreted as proof of causation."
)