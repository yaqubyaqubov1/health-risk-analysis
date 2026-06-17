import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Page Configuration & UI Layout
# ---------------------------------------------------------
st.set_page_config(
    page_title="Fuzzy Health Risk Assessment",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Fuzzy Decision Support System (FDSS)")
st.subheader("Family Member Health Risk Assessment Dashboard")
st.markdown("""
This system uses **Fuzzy Logic principles** to evaluate health risk index on a normalized scale (0 to 1). 
By shifting away from strict binary limits, it maps human health uncertainty cleanly using a heuristic priority vector.
""")

st.divider()

# ---------------------------------------------------------
# 2. Sidebar Input Layer (User Parameters)
# ---------------------------------------------------------
st.sidebar.header("👤 Patient Demographics & Vitals")
member_name = st.sidebar.text_input("Family Member Name", value="John Doe")

# Quantifiable variables
age = st.sidebar.slider("Age (Years)", min_value=1, max_value=100, value=35)
bmi = st.sidebar.slider("Body Mass Index (BMI)", min_value=10.0, max_value=50.0, value=24.5, step=0.1)
systolic_bp = st.sidebar.slider("Systolic Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)

st.sidebar.header("🏃‍♂️ Lifestyle Context")
lifestyle_score = st.sidebar.selectbox(
    "Lifestyle Habits",
    options=["Excellent (Active, Balanced Diet)", "Moderate (Sedentary, Standard Diet)", "Poor (Smoking, High Stress)"],
    index=1
)

# NEW SECTION: Chronic Medical Diagnosis Sidebar Tracking
st.sidebar.header("📋 Clinical Health History")
health_status = st.sidebar.radio(
    "General Health Status",
    options=["Healthy / No Known Conditions", "Has Existing Diagnosis / Diagnoses"],
    index=0
)

# Render diagnoses choices dynamically if they aren't marked as completely healthy
selected_diagnoses = []
if health_status == "Has Existing Diagnosis / Diagnoses":
    selected_diagnoses = st.sidebar.multiselect(
        "Select Confirmed Diagnoses:",
        options=[
            "Hypertension (High Blood Pressure)",
            "Diabetes (Type 1 or Type 2)",
            "Hashimoto's Thyroiditis (Autoimmune)",
            "Hypercholesterolemia (High Cholesterol)",
            "Asthma / Chronic Respiratory",
            "Other Autoimmune / Chronic Diagnosis"
        ],
        help="You can select multiple conditions. This will mathematically adjust the systemic history risk value."
    )

# ---------------------------------------------------------
# 3. Fuzzy Inference Engine & Aggregation Logic
# ---------------------------------------------------------
def fuzzify_age(val):
    if val < 30: return 0.2
    if val < 55: return 0.6
    return 1.0

def fuzzify_bmi(val):
    if 18.5 <= val <= 24.9: return 0.1  
    if 25.0 <= val <= 29.9: return 0.5  
    return 1.0  

def fuzzify_bp(val):
    if val < 120: return 0.1
    if val < 140: return 0.5
    return 1.0

# Extract numerical scores for lifestyle
lifestyle_map = {"Excellent (Active, Balanced Diet)": 0.1, "Moderate (Sedentary, Standard Diet)": 0.5, "Poor (Smoking, High Stress)": 1.0}
mu_lifestyle = lifestyle_map[lifestyle_score]

# NEW Fuzzy Logic for Medical History / Diagnoses Score Calculation (mu_5)
if health_status == "Healthy / No Known Conditions" or not selected_diagnoses:
    mu_med = 0.1  # Baseline risk score for healthy profile
else:
    # Assign specific risk weights to different diseases
    disease_weights = {
        "Hypertension (High Blood Pressure)": 0.5,
        "Diabetes (Type 1 or Type 2)": 0.6,
        "Hashimoto's Thyroiditis (Autoimmune)": 0.4,
        "Hypercholesterolemia (High Cholesterol)": 0.4,
        "Asthma / Chronic Respiratory": 0.3,
        "Other Autoimmune / Chronic Diagnosis": 0.4
    }
    
    # Calculate risk using a fuzzy boundary accumulation (cap max risk at 1.0)
    total_disease_risk = sum(disease_weights[d] for d in selected_diagnoses)
    mu_med = min(1.0, 0.2 + total_disease_risk)

# Generate remaining crisp fuzzy values
mu_age = fuzzify_age(age)
mu_bmi = fuzzify_bmi(bmi)
mu_bp = fuzzify_bp(systolic_bp)

# Clinical priority vector aggregation layer
weights = np.array([0.25, 0.20, 0.20, 0.25, 0.10])  
fuzzy_values = np.array([mu_age, mu_bmi, mu_bp, mu_lifestyle, mu_med])

# Defuzzification / Weighted Synthesis Layer
overall_risk_index = np.dot(fuzzy_values, weights)

# Categorization logic
if overall_risk_index < 0.35:
    risk_category = "🟢 Low Risk"
    risk_color = "green"
elif overall_risk_index < 0.70:
    risk_category = "🟡 Moderate Risk"
    risk_color = "orange"
else:
    risk_category = "🔴 High Risk"
    risk_color = "red"

# ---------------------------------------------------------
# 4. Interactive UI Display Layout
# ---------------------------------------------------------
col1, col2 = st.columns()

with col1:
    st.subheader(f"Analysis Profile: {member_name}")
    
    st.metric(label="Overall Risk Index (μ)", value=f"{overall_risk_index:.2f}")
    st.markdown(f"Inferred Status Category: **:{risk_color}[{risk_category}]**")
    
    # Render selected diagnoses in the main view for clarity
    if selected_diagnoses:
        st.markdown("**Logged Diagnoses:** " + ", ".join([f"`{d.split(' (')[0]}`" for d in selected_diagnoses]))
    else:
        st.markdown("**Logged Diagnoses:** `None (Healthy Profile)`")
        
    st.markdown("### 📊 Factor Membership Risk Breakdown")
    breakdown_data = {
        "Fuzzy Metric Indicator": ["Age Risk (μ1)", "BMI Risk (μ2)", "BP Risk (μ3)", "Lifestyle Risk (μ4)", "Medical History Risk (μ5)"],
        "Assigned Priority Weight": weights,
        "Calculated Fuzzy Value": fuzzy_values
    }
    st.table(breakdown_data)

with col2:
    st.subheader("🕸️ Comparative Radar Profile")
    
    labels = ['Age', 'BMI', 'Blood Pressure', 'Lifestyle', 'Medical Hist.']
    num_vars = len(labels)
    
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    values = fuzzy_values.tolist()
    values += values[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='#ff4b4b', alpha=0.25)
    ax.plot(angles, values, color='#ff4b4b', linewidth=2)
    
    ax.set_yticklabels([])  
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_title(f"Health Vector Signature: {member_name}", size=12, y=1.1)
    
    st.pyplot(fig)
