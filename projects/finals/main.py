import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score, confusion_matrix, classification_report

# ── CONNECTION ──────────────────────────────────────────────
engine = create_engine(
    "mysql+mysqlconnector://root:2006Ferdinand?@localhost/student_performance_system")

query = """
SELECT 
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
print("Data loaded successfully!")
print(df.head())

# ── FEATURE ENGINEERING ─────────────────────────────────────
# Create Pass/Fail column (pass = final score 50 and above)
df['pass_fail'] = (df['final_score'] >= 50).astype(int)

# Features we use for prediction
features = ['attendance_percentage', 'assignment_score', 'midterm_score']

X = df[features]

# ── MODEL 1: PREDICT FINAL SCORE (Regression) ───────────────
y_score = df['final_score']

X_train, X_test, y_train, y_test = train_test_split(
    X, y_score, test_size=0.2, random_state=42)

reg_model = LinearRegression()
reg_model.fit(X_train, y_train)
y_pred_score = reg_model.predict(X_test)
print("\n== REGRESSION RESULTS (Predicting Final Score) ==")
print(f"MAE  : {mean_absolute_error(y_test, y_pred_score):.2f}")
print(f"R²   : {r2_score(y_test, y_pred_score):.2f}")

# ── MODEL 2: PREDICT PASS/FAIL (Classification) ─────────────
y_pass = df['pass_fail']

X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X, y_pass, test_size=0.2, random_state=42)

clf_model = LogisticRegression()
clf_model.fit(X_train2, y_train2)
y_pred_pass = clf_model.predict(X_test2)

print("\n== CLASSIFICATION RESULTS (Predicting Pass/Fail) ==")
print(f"Accuracy : {accuracy_score(y_test2, y_pred_pass):.2f}")
print(classification_report(y_test2, y_pred_pass, zero_division=0))

# ── VISUALIZATIONS ───────────────────────────────────────────
# Chart 1: Attendance vs Final Score
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='attendance_percentage', y='final_score',
                hue='pass_fail', palette={0: 'red', 1: 'green'})
plt.title('Attendance vs Final Score (Green=Pass, Red=Fail)')
plt.xlabel('Attendance %')
plt.ylabel('Final Score')
plt.tight_layout()
plt.savefig('attendance_vs_score.png')
plt.show()

# Chart 2: Average Score by Department
plt.figure(figsize=(8, 5))
df.groupby('department')['final_score'].mean().plot(
    kind='bar', color='steelblue')
plt.title('Average Final Score by Department')
plt.xlabel('Department')
plt.ylabel('Average Score')
plt.tight_layout()
plt.savefig('avg_score_by_department.png')
plt.show()

# Chart 3: Feature Importance (Regression Coefficients)
plt.figure(figsize=(8, 5))
importance = pd.Series(reg_model.coef_, index=features)
importance.plot(kind='bar', color='orange')
plt.title('Feature Importance (Impact on Final Score)')
plt.ylabel('Coefficient Value')
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.show()

# Chart 4: Confusion Matrix
plt.figure(figsize=(6, 4))
cm = confusion_matrix(y_test2, y_pred_pass)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Fail', 'Pass'],
            yticklabels=['Fail', 'Pass'])
plt.title('Confusion Matrix (Pass/Fail Prediction)')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig('confusion_matrix.png')
plt.show()

print("\nAll charts saved successfully!")
