import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score

# ── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance System",
    page_icon="🎓",
    layout="wide"
)

# ── CONNECTION ───────────────────────────────────────────────


@st.cache_data
def load_data():
    engine = create_engine(
        "mysql+mysqlconnector://root:2006Ferdinand?@localhost/student_performance_system")
    query = """
    SELECT 
        s.first_name,
        s.last_name,
        s.gender,
        s.department,
        c.course_name,
        p.attendance_percentage,
        p.assignment_score,
        p.midterm_score,
        p.final_score
    FROM students s
    JOIN enrollments e ON s.student_id = e.student_id
    JOIN courses c ON e.course_id = c.course_id
    JOIN performance p ON e.enrollment_id = p.enrollment_id
    """
    df = pd.read_sql(query, engine)
    df['pass_fail'] = (df['final_score'] >= 50).astype(int)
    return df


df = load_data()

# ── HEADER ───────────────────────────────────────────────────
st.title("🎓 Student Performance Prediction & Analytics System")
st.markdown("Final Year Project — Data Science & Database Analytics")
st.divider()

# ── SECTION 1: RAW DATA ──────────────────────────────────────
st.subheader("📋 Student Dataset")
st.dataframe(df, use_container_width=True)
st.divider()

# ── SECTION 2: KEY METRICS ───────────────────────────────────
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", len(df['first_name'].unique()))
col2.metric("Average Final Score", f"{df['final_score'].mean():.1f}")
col3.metric("Pass Rate", f"{(df['pass_fail'].mean()*100):.1f}%")
col4.metric("Avg Attendance", f"{df['attendance_percentage'].mean():.1f}%")
st.divider()

# ── SECTION 3: CHARTS ────────────────────────────────────────
st.subheader("📈 Analytics Charts")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Attendance vs Final Score**")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=df, x='attendance_percentage', y='final_score',
                    hue='pass_fail', palette={0: 'red', 1: 'green'}, ax=ax1)
    ax1.set_xlabel("Attendance %")
    ax1.set_ylabel("Final Score")
    st.pyplot(fig1)

with col2:
    st.markdown("**Average Score by Department**")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    df.groupby('department')['final_score'].mean().plot(
        kind='bar', color='steelblue', ax=ax2)
    ax2.set_xlabel("Department")
    ax2.set_ylabel("Average Score")
    plt.xticks(rotation=15)
    st.pyplot(fig2)

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Score Distribution**")
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.histplot(df['final_score'], bins=8, kde=True, color='green', ax=ax3)
    ax3.set_xlabel("Final Score")
    st.pyplot(fig3)

with col4:
    st.markdown("**Pass vs Fail Count**")
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    df['pass_fail'].value_counts().rename({0: 'Fail', 1: 'Pass'}).plot(
        kind='bar', color=['red', 'green'], ax=ax4)
    ax4.set_xlabel("Result")
    ax4.set_ylabel("Count")
    plt.xticks(rotation=0)
    st.pyplot(fig4)

st.divider()

# ── SECTION 4: ML MODELS ─────────────────────────────────────
st.subheader("🤖 Machine Learning Results")

features = ['attendance_percentage', 'assignment_score', 'midterm_score']
X = df[features]

# Regression
y_score = df['final_score']
X_train, X_test, y_train, y_test = train_test_split(
    X, y_score, test_size=0.2, random_state=42)
reg_model = LinearRegression()
reg_model.fit(X_train, y_train)
y_pred = reg_model.predict(X_test)

# Classification
y_pass = df['pass_fail']
X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X, y_pass, test_size=0.2, random_state=42)
clf_model = LogisticRegression()
clf_model.fit(X_train2, y_train2)
y_pred2 = clf_model.predict(X_test2)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Regression Model (Predicting Final Score)**")
    st.metric("MAE", f"{mean_absolute_error(y_test, y_pred):.2f}")
    st.metric("R² Score", f"{r2_score(y_test, y_pred):.2f}")

with col2:
    st.markdown("**Classification Model (Predicting Pass/Fail)**")
    st.metric("Accuracy", f"{accuracy_score(y_test2, y_pred2):.2f}")

st.divider()

# ── SECTION 5: PREDICTION TOOL ───────────────────────────────
st.subheader("🔮 Predict Student Performance")
st.markdown(
    "Enter student details below to predict their final score and pass/fail result")

col1, col2, col3 = st.columns(3)
with col1:
    attendance = st.slider("Attendance %", 0, 100, 75)
with col2:
    assignment = st.slider("Assignment Score", 0, 100, 70)
with col3:
    midterm = st.slider("Midterm Score", 0, 100, 65)

if st.button("Predict Now"):
    input_data = pd.DataFrame(
        [[attendance, assignment, midterm]], columns=features)
    predicted_score = reg_model.predict(input_data)[0]
    predicted_pass = clf_model.predict(input_data)[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predicted Final Score", f"{predicted_score:.1f}")
    with col2:
        if predicted_pass == 1:
            st.success("Result: PASS ✅")
        else:
            st.error("Result: FAIL ❌")
