# Health Risk Assessment of Family Members Using a Fuzzy Decision Support System (FDSS)

![Python Version](https://img.shields.io)
![License](https://img.shields.io)
![Field](https://img.shields.io)

## 📌 Project Overview
Traditional medical decision-making often struggles with the inherent uncertainty and complexity of physiological and lifestyle data. This project implements a **Fuzzy Decision Support System (FDSS)** to assess health risk levels by integrating multiple heterogeneous parameters, including age, BMI, blood pressure, lifestyle habits, and medical history.

Unlike classical binary logic, this fuzzy logic-based approach utilizes **membership functions** to provide a more realistic, granular evaluation of health status on a normalized scale (0–1).

## 🚀 Key Features
- **Multi-dimensional Inputs:** Evaluates 5+ critical health determinants simultaneously.
- **Fuzzy Inference Engine:** Uses heuristic rule-based logic to handle clinical uncertainty.
- **Weighted Aggregation:** Implements a clinical priority vector: `w = [0.25, 0.20, 0.20, 0.25, 0.10]`.
- **Visualization:** Generates Comparative Radar Charts to profile individual risk factors.

## 📊 System Architecture
The system follows a modular **Input-Process-Output (IPO)** workflow:

```mermaid
graph TD
    subgraph Inputs [1. Input Layer]
    A[Age, BMI, BP]
    B[Lifestyle, Med. History]
    end

    subgraph Process [2. Fuzzy Engine]
    C[Fuzzification: Mapping to μ]
    D[Inference: Rule-Base Logic]
    E[Weighted Aggregation: Σ w_i * μ_i]
    end

    subgraph Output [3. Output Synthesis]
    F[Overall Risk Index μ_overall]
    G[Category: Low/Moderate/High]
    end

    Inputs --> C
    C --> D
    D --> E
    E --> F
    F --> G