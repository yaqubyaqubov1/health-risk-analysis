import matplotlib.pyplot as plt

def get_fuzzy_value(value, param_type, person_name=None):
    if param_type  == "age":
        if value >= 70: return 1.0
        if value >= 65: return 0.9
        if value <= 40: return 0.4
        return round((value / 70), 1)

    elif param_type  == "lifestyle":
        return 0.7 if value.lower()  == "passive" else 0.5

    elif param_type  == "blood_pressure":
        if "-" in value:
            systolic = int(value.split("-")[1])
            if systolic >= 140: return 0.8
            if systolic <= 110: return 0.2
            if systolic <= 120:
                return 0.4 if person_name  == "Grandfather" else 0.3
        return 0.5

    return 0.1

family_data = {
    "Father":      {"age": 40, "lifestyle": "Passive", "bp": "80-140", "habits": 0.9, "medical": 0.2},
    "Mother":      {"age": 40, "lifestyle": "Active",  "bp": "70-120", "habits": 0.1, "medical": 0.6},
    "Grandmother": {"age": 65, "lifestyle": "Passive", "bp": "85-140", "habits": 0.1, "medical": 0.9},
    "Grandfather": {"age": 70, "lifestyle": "Passive", "bp": "70-120", "habits": 0.2, "medical": 0.9},
    "Aunt":        {"age": 40, "lifestyle": "Passive", "bp": "70-110", "habits": 0.2, "medical": 0.1}
}

weights = [0.25, 0.20, 0.20, 0.25, 0.10]

print(f"{'Member':<12} | {'Fuzzy Values (μ)':<35} | {'Final Risk Score'}")
print("-" * 75)

names = []
final_scores = []

for person, info in family_data.items():
    f_age = get_fuzzy_value(info["age"], "age")
    f_life = get_fuzzy_value(info["lifestyle"], "lifestyle")
    f_bp = get_fuzzy_value(info["bp"], "blood_pressure", person)
    f_med = info["medical"]
    f_habits = info["habits"]

    fuzzy_set = [f_age, f_life, f_bp, f_med, f_habits]
    risk_score = round(sum(parameter * w for parameter, w in zip(fuzzy_set, weights)), 2)

    print(f"{person:<12} | {str(fuzzy_set):<35} | {risk_score}")

    names.append(person)
    final_scores.append(risk_score)

plt.figure(figsize=(9, 5))
plt.bar(names, final_scores, color='cadetblue')
plt.title("FamAi Health Risk Assessment")
plt.ylabel("Risk Score (μ)")
plt.ylim(0, 1.0)
plt.show()