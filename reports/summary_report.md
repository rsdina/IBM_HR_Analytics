# HR Analytics Project - Results Summary

## Overview
- **Analysis Date:** 2026-09-06 13:29:01
- **Dataset:** IBM HR Analytics Employee Attrition
- **Total Records:** 1470
- **Features:** 36

## Key Metrics
| Metric | Value |
|--------|-------|
| Total Employees | 1,470 |
| Attrition Rate | 16.12% |
| Attrition Count | 237 |
| Stayed Count | 1,233 |

## Compensation Analysis
| Group | Average Monthly Income |
|-------|----------------------|
| Employees Who Left | $4,787.09 |
| Employees Who Stayed | $6,832.74 |
| Income Gap | $2,045.65 |

## Department Attrition Rates
| Department | Attrition Rate |
|------------|---------------|
| Sales | 20.63% |
| Human Resources | 19.05% |
| Research & Development | 13.84% |

## Model Performance Summary
**Best Model:** Logistic Regression

| Metric | Score |
|--------|-------|
| Accuracy | 0.8741 |
| Precision | 0.6923 |
| Recall | 0.3830 |
| F1 Score | 0.4932 |
| AUC-ROC | 0.8057 |

## Top 10 Attrition Drivers
| Feature | Coefficient | Impact |
|---------|------------|--------|
| OverTime | 0.7820 | Positive |
| YearsSinceLastPromotion | 0.4812 | Positive |
| Department | 0.4713 | Positive |
| NumCompaniesWorked | 0.4492 | Positive |
| YearsWithCurrManager | -0.4400 | Negative |
| EnvironmentSatisfaction | -0.4360 | Negative |
| TotalWorkingYears | -0.4207 | Negative |
| Age | -0.4096 | Negative |
| JobSatisfaction | -0.3832 | Negative |
| YearsInCurrentRole | -0.3624 | Negative |

## Key Insights
1. **Overtime is the strongest predictor** - 30.53% of overtime employees leave
2. **Income disparity** - Leavers earn $2,046 less on average
3. **Sales department** has the highest attrition rate at 20.63%
4. **Job satisfaction** negatively correlates with attrition
5. **Single employees** show 25.53% attrition rate

## Recommendations
1.  Focus on improving job satisfaction, especially in departments with high attrition
2.  Review compensation packages, particularly for roles with high attrition rates
3.  Address work-life balance issues, especially for employees working overtime
4.  Implement career development programs to improve employee engagement
5.  Enhance employee well-being programs to reduce turnover
