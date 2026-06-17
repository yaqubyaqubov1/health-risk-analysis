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

# 2. Sidebar Input Layer (User Parameters)

st.sidebar.header("👤 Patient Demographics & Vitals")
member_name = st.sidebar.text_input("Family Member Name", value="John Doe")


# Quantifiable variables
age = st.sidebar.number_input(
    "Age (Years)", 
    min_value=1, 
    max_value=100, 
    value=35, 
    step=1
)

if "bmi_value" not in st.session_state:
    st.session_state.bmi_value = 24.5

# Define a clean callback function to force state updates immediately on click
def apply_calculated_bmi(val):
    st.session_state.bmi_value = val
    st.session_state.bmi_input = val  # Updates the number field value instantly

# 2. Main BMI Input Field (bound directly to 'bmi_input' state key)
bmi = st.sidebar.number_input(
    "Body Mass Index (BMI)", 
    min_value=10.0, 
    max_value=50.0, 
    value=st.session_state.bmi_value, 
    step=0.1, 
    format="%.1f",
    key="bmi_input"
)

# 3. Calculator Tool expander placed directly underneath
with st.sidebar.expander("📐 Don't know your BMI? Calculate it here"):
    st.markdown(f"**Context Age fetched:** `{age}` years old")
    gender = st.selectbox("Biological Gender", ["Male", "Female", "Other"])
    
    # Calculation inputs
    height_cm = st.number_input("Height (in cm)", min_value=100.0, max_value=250.0, value=175.0, step=0.5)
    weight_kg = st.number_input("Weight (in kg)", min_value=30.0, max_value=250.0, value=75.0, step=0.5)
    
    # Standard BMI Algorithm (kg / m^2)
    calculated_bmi_val = weight_kg / ((height_cm / 100) ** 2)
    calculated_bmi_val = float(round(calculated_bmi_val, 1))
    
    st.info(f"Calculated BMI Result: **{calculated_bmi_val}**")
    
    # 4. Action button running our direct callback update function
    st.button(
        "Apply Result to BMI Field", 
        use_container_width=True,
        on_click=apply_calculated_bmi,
        args=(calculated_bmi_val,)
    )

# Sync our final math variable with whatever is inside the active typing field
bmi = st.session_state.bmi_input

systolic_bp = st.sidebar.number_input(
    "Systolic Blood Pressure (mmHg)", 
    min_value=40, 
    max_value=220, 
    value=120, 
    step=1
)


# Categorical variables mapped to categorical membership values
st.sidebar.header("🏃‍♂️ Lifestyle & Medical Context")
lifestyle_score = st.sidebar.selectbox(
    "Lifestyle Habits",
    options=["Excellent (Active, Balanced Diet)", "Moderate (Sedentary, Standard Diet)", "Poor (Smoking, High Stress)"],
    index=1
)

med_history_score = st.sidebar.selectbox(
    "Family Medical History Risk",
    options=["No Genetic Risk Factors", "Minor Conditions (e.g., Mild Allergies)", "Major Conditions (e.g., Cardiovascular / Diabetes)"],
    index=0
)

st.sidebar.header("📋 Clinical Health History")
health_status = st.sidebar.radio(
    "Current Health Status",
    options=["Healthy", "Has Existing Diagnosis / Diagnoses"],
    index=0
)

selected_diagnoses = []
if health_status == "Has Existing Diagnosis / Diagnoses":
    selected_diagnoses = st.sidebar.multiselect(
        "Select Confirmed Diagnoses:",
        options=[
            "Diabetes", 
            "Hypertension", 
            "Hashimoto's", 
            "Other Chronic Conditions"
        ],
        default=[]
    )


# 3. Fuzzy Inference Engine & Aggregation Logic

# Helper functions for Fuzzification (Mapping parameters cleanly to 0.0 - 1.0 risk weight)
def fuzzify_age(val):
    if val < 30: return 0.2
    if val < 55: return 0.6
    return 1.0

def fuzzify_bmi(val):
    if 18.5 <= val <= 24.9: return 0.1  # Normal
    if 25.0 <= val <= 29.9: return 0.5  # Overweight
    return 1.0  # Obese / Underweight risk

def fuzzify_bp(val):
    if val < 120: return 0.1
    if val < 140: return 0.5
    return 1.0

# Extract numerical scores for categorical variables
lifestyle_map = {"Excellent (Active, Balanced Diet)": 0.1, "Moderate (Sedentary, Standard Diet)": 0.5, "Poor (Smoking, High Stress)": 1.0}
med_map = {"No Genetic Risk Factors": 0.1, "Minor Conditions (e.g., Mild Allergies)": 0.4, "Major Conditions (e.g., Cardiovascular / Diabetes)": 1.0}

# Generate crisp fuzzy values
mu_age = fuzzify_age(age)
mu_bmi = fuzzify_bmi(bmi)
mu_bp = fuzzify_bp(systolic_bp)
mu_lifestyle = lifestyle_map[lifestyle_score]
mu_med = med_map[med_history_score]

# Clinical priority vector aggregation layer
weights = np.array([0.25, 0.20, 0.20, 0.25, 0.10])  # Explicit clinical weightings
fuzzy_values = np.array([mu_age, mu_bmi, mu_bp, mu_lifestyle, mu_med])

# Defuzzification / Weighted Synthesis Layer
overall_risk_index = np.dot(fuzzy_values, weights)

# 1. Base Defuzzification Calculation
overall_risk_index = np.dot(fuzzy_values, weights)

# 2. Categorization Logic with Clinical Emergency Override Rules
if systolic_bp <= 40 or systolic_bp >= 220:
    # Critical vital override: force maximum emergency bounds
    risk_category = "🔴 High Risk (CRITICAL OVERRIDE)"
    risk_color = "red"
    overall_risk_index = 1.00  # Force index to max to reflect emergency state
elif overall_risk_index < 0.35:
    risk_category = "🟢 Low Risk"
    risk_color = "green"
elif overall_risk_index < 0.70:
    risk_category = "🟡 Moderate Risk"
    risk_color = "orange"
else:
    risk_category = "🔴 High Risk"
    risk_color = "red"

# 4. Interactive UI Display Layout
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"Analysis Profile: {member_name}")
    
    # --- Critical Vitals Warning Checks ---
    if systolic_bp <= 40:
        st.error("🚨 **CRITICAL MEDICAL EMERGENCY**: Systolic Blood Pressure of 40 mmHg or below indicates extreme, life-threatening hypotension (shock). This state is incompatible with sustained cellular life without immediate resuscitation.")
    elif systolic_bp >= 220:
        st.error("🚨 **CRITICAL MEDICAL EMERGENCY**: Systolic Blood Pressure has reached or exceeded 220 mmHg. This represents an extreme hypertensive crisis with a catastrophic risk of immediate organ failure, stroke, or fatal cardiovascular rupture.")
    
    # Showcase primary system metrics clearly
    st.metric(label="Overall Risk Index (μ)", value=f"{overall_risk_index:.2f}")
    st.markdown(f"Inferred Status Category: **:{risk_color}[{risk_category}]**")
    
    # Display precise breakdown tables
    st.markdown("### 📊 Factor Membership Risk Breakdown")
    breakdown_data = {
        "Fuzzy Metric Indicator": ["Age Risk (μ1)", "BMI Risk (μ2)", "BP Risk (μ3)", "Lifestyle Risk (μ4)", "Medical History Risk (μ5)"],
        "Assigned Priority Weight": weights,
        "Calculated Fuzzy Value": fuzzy_values
    }
    st.table(breakdown_data)

with col2:
    st.subheader("🕸️ Comparative Radar Profile")
    
    # Dynamic Radar Chart Generation Loop using Matplotlib
    labels = ['Age', 'BMI', 'Blood Pressure', 'Lifestyle', 'Medical Hist.']
    num_vars = len(labels)
    
    # Split the circle into even arcs
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # Connect the circular radar layout cleanly loop back
    values = fuzzy_values.tolist()
    values += values[:1]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='#ff4b4b', alpha=0.25)
    ax.plot(angles, values, color='#ff4b4b', linewidth=2)
    
    ax.set_yticklabels([])  # Hide traditional grid axis text for modern layout
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_title(f"Health Vector Signature: {member_name}", size=12, y=1.1)
    
    st.pyplot(fig)  # Direct native layout embedding
