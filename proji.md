1. Project Overview: What is FamAi?
Diseases and illness in the human body are often vague and subjective. Doctors' diagnoses are based on specific symptoms and test results based on medical theories. However, the symptoms of a person's illness may not be expressed in specific numbers, such as "mild", "moderate", or "severe". Therefore, doctors can make an approximate diagnosis. In cases of such vague symptoms, Fuzzy logic plays the role of a practical and effective and quick support system. FamAi -proposes a Fuzzy Decision Support System (FDSS) to assess the health risk levels of family members by integrating multiple heterogeneous parameters. The proposed approach focuses on the development of a fuzzy decision support method by combining physiological measurements, lifestyle indicators, and family medical history. Unlike classical binary logic, the fuzzy logic-based approach utilizes membership functions to provide a more realistic, granular evaluation of health status.

The "Intelligence" Behind FamAi
The system uses Fuzzy Logic, a branch of AI that mimics human reasoning.

The Problem: Traditional decision-making methods sometimes have difficulty interpreting such complex and uncertain data accurately

The FamAi Solution: Fuzzy logic, introduced by Lutfi A. Zadeh, offers a powerful solution to solve many problems by referring to more than one category. Unlike classical binary logic, fuzzy logic allows for a more realistic assessment of health conditions by including logical variables such as "low", "medium" or "high". The proposed theoretical framework is particularly effective for medical applications where data often lacks rigid numerical boundaries.

Why FamAi Matters
Personalized Monitoring: It doesn't treat everyone the same; it adapts to the individual's specific background.
Early Detection: By catching "Moderate" risks (like the father's 0.68), the family can act before a medical emergency occurs.
Smarter Decisions: It provides medical personnel with a "nuanced alternative" to traditional diagnosis.
How the System Works (The Workflow)
The project follows a structured AI pipeline:

Data Collection (Inputs): The proposed fuzzy decision support system evaluates the health risk of individuals based on multiple input parameters given in below:
Age
Body weight / BMI
Lifestyle (sleep pattern, physical activity, stress)
Blood pressure
Dietary habits
Smoking and alcohol consumption
Medical history and family disease history
Fuzzification: Based on the general form of the membership function, the raw numbers are converted into fuzzy values between 0 and 1 is defined as:
𝜇(𝑥) ∈ [0,1]

Where x- represents the input parameter and μ(x)denotes the corresponding degree of membership.

Inference Engine (The "Brain"): The AI applies to "If-Then" rules. For example: If Age is High AND Blood Pressure is High, then Health Risk is High.
Weighted Aggregation: Everyone is represented by a fuzzy vector:
μ = [𝜇age, 𝜇lifestyle, 𝜇BP, 𝜇medical, 𝜇habits]

The overall health risk is calculated using a weighted aggregation method:

where:

𝑖=1

𝑤𝑖is the weight of parameter 𝑖
∑𝑤𝑖 = 1
𝜇overall = ∑𝑛

𝑤𝑖 ⋅ 𝜇𝑖

Defuzzification: This value represents the final health risk score and is mapped into linguistic categories:
Low, 𝜇overall < 0.4

Risk Category = {Moderate, 0.4 ≤ 𝜇overall < 0.7

High, 𝜇overall ≥ 0.7

AI-based Implementation
The fuzzy aggregation and weighting process was implemented using a Python-based computational model. This enables automatic risk evaluation, reproducibility, and scalability of the proposed system.

import matplotlib.pyplot as plt

# Fuzzy membership values (0-1)

# Parameters: Age, Weight, Lifestyle, Blood Pressure, Medical History

data = {

"Father": [0.4, 0.7, 0.6, 0.2, 0.1],

"Mother": [0.4, 0.5, 0.3, 0.6, 0.3],

"Grandmother": [0.9, 0.6, 0.8, 0.9, 0.8],

"Grandfather": [1.0, 0.7, 0.4, 0.9, 0.9],

"Aunt": [0.4, 0.7, 0.2, 0.1, 0.1]

}

# Weights of parameters

# Age, Weight, Lifestyle, Blood Pressure, Medical History

weights = [0.25, 0.20, 0.15, 0.25, 0.15]

risk_scores = {}

# Risk calculation using weighted fuzzy model for person, values in data.items():

risk = sum(v * w for v, w in zip(values, weights)) risk_scores[person] = round(risk, 2)

# Print results

print("Health Risk Assessment Results") print(" ")

for person, score in risk_scores.items(): print(person, ":", score)

# Visualization

names = list(risk_scores.keys()) scores = list(risk_scores.values())

plt.bar(names, scores)

plt.title("Health Risk Comparison") plt.xlabel("Family Members") plt.ylabel("Risk Score")

plt.show()

Results and Analysis
The results of the health assessment are presented in Table 1. These variables were evaluated together to determine the overall health risk level of everyone using a fuzzy logic-based perspective.

Table 1. Health Parameters of the members of family

Parameter	Father	Mother	Grandmother	Grandfather	Aunt
Age (years)	40	40	65	70	40
Weight (kg)	100	60	100	85	90
Parameter	Father	Mother	Grandmother	Grandfather	Aunt
Lifestyle (To assess lifestyle, the therapist conducted a questionnaire and evaluated it as active or passive.)	Passive	Active	Passive	Passive	Passive
Blood pressure (mmHg)	80-140	70-120	85-140	70-120	70-110
Diet	High intake of meat and fatty food	Balanced diet	Balanced diet	Night-time eating	Night- time eating
Health history	Healthy	Hashimoto's thyroiditis	Hypertension	Diabetes	Healthy
Smoking	Yes	No	No	No	No
Alcohol	Yes	No	No	No	No
Medication/Treatment	No	No	No	No	No
A numerical description of the fuzzy logic inputs and outputs used in a data-driven Fuzzy Decision Support System (FDSS) for health risk assessment is given in Table 2

Table 2. Fuzzy Membership Values for Health Risk

Individual	Age μ	Lifestyle μ	BP μ	Medical History μ	Habits μ	Overall Risk μ
Father	0.4	0.7	0.6	0.2	0.9	0.68
Mother	0.4	0.5	0.3	0.6	0.1	0.46
Grandmother	0.9	0.6	0.8	0.9	0.1	0.82
Grandfather	1.0	0.7	0.4	0.9	0.2	0.76
Aunt	0.4	0.7	0.2	0.1	0.2	0.38
The fuzzy decision support system evaluates the overall health risk for everyone by aggregating multiple risk factors. The overall risk is computed as a weighted sum of the membership values, resulting in a single scalar fuzzy output that represents the individual's health risk.

The selected weight vector is defined as:

𝐰 = [0.25, 0.20, 0.20, 0.25, 0.10]

Where the w = weights correspond respectively to age, lifestyle, blood pressure, medical history, and habits. The sum of all weights equals one, ensuring normalization and consistency within the fuzzy aggregation process.

Overall Analysis
Based on the FamAi pilot study, here is how the AI ranks different profiles:

Family Member	Risk Score (μ)	AI Classification	Primary Concern
Grandmother	0.82	High Risk	Hypertension + Age + Weight
Grandfather	0.76	High Risk	Diabetes + Advanced Age
Father	0.68	Moderate-High	Smoking + Diet + Lifestyle
Mother	0.46	Moderate	Medical History (Hashimoto's)
Aunt	0.38	Low-Moderate	Passive Lifestyle + Weight
The fuzzy membership results indicate that the grandmother has the highest health risk (μ = 0.82), mainly due to advanced age, hypertension, and body weight. The grandfather also exhibits a high-risk level (μ = 0.76), primarily influenced by diabetes and age-related factors. The father shows a moderate-to-high risk level (μ = 0.68), associated with lifestyle habits such as smoking, alcohol consumption, and dietary patterns.

The mother falls into a moderate risk category (μ = 0.46), where medical history plays a significant role despite otherwise healthy habits. The aunt presents the lowest risk level (μ = 0.38), although irregular sleep patterns and body weight contribute to a slight increase in risk.

Overall, the results confirm that fuzzy logic is a powerful decision-support tool for healthcare assessment. By capturing uncertainty and gradual transitions between health states, fuzzy systems can support medical staff in early risk detection and contribute to improved healthcare quality and preventive strategies.
