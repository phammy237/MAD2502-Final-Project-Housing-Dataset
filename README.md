# MAD2502 Capstone Project — Ames Housing Price Regression

**Course:** MAD2502 — Introduction to Computational Mathematics  
**Author:** My Pham (UFID: 12494292)

Predicts residential sale prices in Ames, Iowa using linear regression derived from first principles (the Normal Equation) and compared against several scikit-learn models.

---

## Dataset

**Ames Housing Dataset** — 2,930 observations, 82 features covering physical characteristics, location, and sale conditions of homes sold in Ames, IA between 2006 and 2010.

Source file: `MAD Final Project Housing Dataset/data/AmesHousing.csv`

---

## Project Structure

```
MAD Final Project Housing Dataset/
├── code/
│   └── Ames_Regression_Project.ipynb   # Main notebook
└── data/
    ├── AmesHousing.csv                 # Raw dataset
    ├── AmesHousing_cleaned.csv         # After cleaning (output)
    ├── AmesHousing_model.csv           # 3-feature modeling subset (output)
    ├── AmesHousing_predictions.csv     # 3-feature predictions (output)
    ├── AmesHousing_predictions_extended.csv  # 5-feature predictions (output)
    └── model_comparison_results.csv    # Train/test metrics for all models (output)
```

---

## Notebook Walkthrough

### 1. Data Loading
Searches common paths for `AmesHousing.csv` and loads it into a DataFrame.

### 2. Data Cleaning
- Drops duplicate rows
- Drops columns with >50% missing values (`Alley`, `Pool QC`, `Fence`, etc.)
- Fills numeric NaNs with column median; categorical NaNs with column mode
- Converts low-cardinality string columns to `category` dtype

Final shape after cleaning: **(2930, 77)**

### 3. Feature Selection
Two modeling datasets are built:

| Model | Features |
|-------|----------|
| 3-feature | `Gr Liv Area`, `Overall Qual`, `Year Built` |
| 5-feature | above + `Bedroom AbvGr`, `Full Bath` |

**Target:** `SalePrice`

### 4. Mathematical Work

#### Correlation Analysis
Pearson correlations with `SalePrice`:
- Overall Qual: **0.80**
- Gr Liv Area: **0.71**
- Year Built: **0.56**

#### Least-Squares Regression (Normal Equation)

The model minimizes the sum of squared residuals:

$$S(\beta) = (y - X\beta)^T(y - X\beta)$$

Setting the gradient to zero yields the **Normal Equation**:

$$\beta = (X^TX)^{-1}X^Ty$$

Solved numerically via `np.linalg.pinv` for stability.

#### Extended 5-Feature Model
Adding bedrooms and bathrooms reveals multicollinearity: their coefficients become slightly negative when square footage and quality are held constant, because adding rooms without increasing total area implies smaller individual rooms. R² improves marginally (~0.76).

#### Train-Test Split and Model Comparison (80/20)
Six models trained and evaluated:

| Model | Test R² | Test RMSE |
|-------|---------|-----------|
| Normal Equation | ~0.76 | ~$38k |
| Linear Regression (sklearn) | ~0.76 | ~$38k |
| Ridge (α=100) | ~0.76 | ~$38k |
| Lasso (α=100) | ~0.76 | ~$38k |
| Random Forest | best | lowest |
| Gradient Boosting | high | low |

Random Forest and Gradient Boosting achieve the best test R² by capturing non-linear relationships that the linear models miss.

### 5–6. Interpretation
- **Overall Qual** is the strongest driver (~$26k per quality point)
- **Gr Liv Area** adds ~$63 per square foot
- **Year Built** adds ~$495 per year
- RMSE of ~$38–40k is reasonable for a 3-feature linear model; error is proportionally larger for high-value homes

---

## Requirements

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

Run the notebook top-to-bottom from `MAD Final Project Housing Dataset/code/`.
