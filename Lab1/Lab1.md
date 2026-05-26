# CST8921 Lab 1 - Report

## Section 1 – Cover Page

- Name: Bosi Chen
- Student ID: 041040774
- Course: CST8921 Cloud Industry Trends
- Lab: Lab 1
- Submission Date:

---

## Section 2 – Introduction

Azure Machine Learning (Azure ML) is a cloud-based platform provided by Microsoft for building, training, deploying, and managing machine learning models. It provides a set of tools and services to help users work with data, create machine learning workflows, and monitor model performance in cloud environment. 

The Azure Machine Learning Designer is a visual interface which allows the users to build a machine learning pipelines without writing code.

These tools are highly relevant to cloud professionals in 2025 because many organizations are integrating AI and machine learning into business operations. Cloud professionals also need to understand how to manage the ML infrastructure, automate workflows, and deploy scalable AI solutions using modern cloud platforms such as Azure.

## Section 3 – Lab Walkthrough with Screenshots

### A1 - Workspace deployment completion

![A1-1](/Lab1/screenshots/A1-1.png)
![A1-2](/Lab1/screenshots/A1-2.png)

These screenshots show the deployment settings and completion of deployment.

### A2 - AML workspace overview in Azure Portal

![A2](/Lab1/screenshots/A2.png)

This screenshot shows the AML workspace Overview page in the Azure Portal.

### B1 - AML Studio navigation pane (all three sections)

![B1](/Lab1/screenshots/B1.png)

This screenshot shows the AML Studio home page with the Authoring, Assets, and Manage sections in left pane.

### C1 - Compute instance in Running state

![C1](/Lab1/screenshots/C1-1.png)
![C1](/Lab1/screenshots/C1-2.png)

These screenshots shows the running compute instance `lab1-compute-cst8921` under `Standard_DS11_v2` VM size, created on 5/23/2026, 6:41:53 PM.

### D1 - Blank Designer canvas with renamed pipeline title

![D1](/Lab1/screenshots/D1-1.png)
![D1](/Lab1/screenshots/D1-2.png)

These screenshots shows the designer canvas with the pipeline title `Automobile price prediction`.

### E1 - Dataset component placed on canvas

![E1](/Lab1/screenshots/E1.png)

This screenshot shows the Automobile price data is placed on the designer canvas.

### E2 - Data preview window (dataset structure)

![E2](/Lab1/screenshots/E2-1.png)
![E2](/Lab1/screenshots/E2-2.png)

This screenshot is a preview of a few rows and columns from Automobile price data columns.

### F1 - Column selector showing Include All + Exclude normalized-losses

![F1](/Lab1/screenshots/F1.png)

This screenshot shows the column selector dialog from Select Columns, where the Include All columns rule AND the Exclude normalized-losses rule configured.

### F2 - Canvas with first three components connected

![F2](/Lab1/screenshots/F2.png)

This screenshot shows the designer canvas with the connected components: Automobile price data (Raw) → Select Columns in Dataset → Clean Missing Data.

### G1 - Canvas with Linear Regression, Split Data, Train Model connected

![G1](/Lab1/screenshots/G1.png)

This screenshot shows the Linear Regression, Split Data, and Train Model connections.

### H1 - Complete pipeline (all 7 components connected)

![H1](/Lab1/screenshots/H1.png)

This screenshot shows the final complete pipeline on the design canvas.

### I1 - Runtime settings tab with compute instance selected

![I1](/Lab1/screenshots/I1.png)

This screeshot shows the runtime settings of the pipeline job.

### J1 - Job detail page showing completed (green) components

![J1](/Lab1/screenshots/J1.png)

This screenshot shows the job detail page with the components showing green (completed) status, also the job status indicator at the top.

### J2 - Score Model output with Scored Labels visible

![J2](/Lab1/screenshots/J2.png)

This screenshot shows the Score Model preview output with the Scored Labels column and the original price column both visible.

### J3 - Evaluate Model metrics table

![J3](/Lab1/screenshots/J3.png)

The Evaluate model will give the following metrics: Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), 
Relative Absolute Error, Relative Squared Error, Coefficient of Determination (R²).

This screenshot shows the Evaluate Model preview output with all five metric values.

### K1 - Resource group deleted (no longer in list)

![K1](/Lab1/screenshots/K1.png)

This screenshot shows the Azure Resource Groups page, with the RG `aml-lab-rg` deleted.

### Section 4 – Analysis and Reflection

#### Step J.5 – Analysis Questions (Answer in Lab Report)

> Answer the following questions using the actual numbers from your pipeline run:

1. What **R² value** did your model achieve? Using the scale below, how would you classify your model's performance?
   - R² > 0.90 → Excellent fit
   - R² 0.75–0.90 → Good fit
   - R² 0.50–0.75 → Moderate fit
   - R² < 0.50 → Poor fit

The model achieved a R² value of 0.868204. Since the value falls between 0.75 and 0.9, it indicates a good fit.

---

2. What is your **MAE** value? In plain language, on average, how many dollars is your model's price prediction off from the actual car price?

The Mean Absolute Error (MAE) value was 1773.614473, which means the model’s price predictions were off from the actual prices by approximately $1773.6.

---

3. Find **one specific row** in the Score Model output. Record the actual `price` and the `Scored Label` (predicted price). Calculate the **percentage error** for that row:
   ```
   Percentage Error = |Actual Price – Predicted Price| / Actual Price × 100%
   ```

Take the first row from screenshot J2 where we have：
```
Actual price: 9639
Predicted price: 10909.222803
```

Percentage Error = |Actual Price – Predicted Price| / Actual Price × 100% = |9639-10909.222803| / 9639 × 100% ≈ 13.18%

The percentage error was approximately 13.18%, which means the prediction differed from the actual value by about 13%.

---

4. In the pipeline, you used a **70/30 train/test split**. Why is it essential to evaluate the model on data it was *not* trained on? What problem would arise if you evaluated on the same data used for training?

It is important because it can measure how well the model generalizes to new data. If the same data were used for both training and testing, the model may appear to be more accurate than it actually is.

---

5. The **Clean Missing Data** component was set to "Remove entire row." What is the trade-off of this approach compared to replacing missing values with the column mean? When might you prefer one approach over the other?

Removing entire rows with missing values improves data quality because the incomplete records are excluded, but this also reduces the amount of available training data. While replacing the missing values with the column mean preserves more data, it may reduce accuracy if the estimated values are not realistic. 

Thus, removing rows is often preferred when there are relatively few missing values.

---

6. The **Select Columns in Dataset** component excluded `normalized-losses`. What would likely happen to model performance if you had kept this column without handling its many missing values?

If the `normalized-losses` column had been kept without handling its missing values, model performance would likely decrease. The missing data could introduce errors, reduce training quality, or result in unreliable predictions.

---

7. Looking at the Automobile dataset columns, list **three features** you believe most strongly predict `price`, and explain briefly why each might be predictive.

Three features that likely predict automobile price strongly are:

1. engine-size — Cars with larger engines are more powerful and expensive, so engine size is likely strongly related to price.
2. horsepower — Cars with higher horsepower often provide better performance and are usually sold at higher prices.
3. curb-weight — Heavier cars are often larger, include more features, or use stronger materials, which can increase manufacturing cost and price.

## Section 5 – Conclusion

This lab provided a hands-on tutorial with Azure Machine Learning and Azure ML Designer, from which I learned how to create an AML workspace, configure compute resources, prepare datasets, and build a complete regression pipeline using visual components. I also learned the importance of preprocessing data, handling missing values, splitting datasets into training and testing sets, and evaluating model performance using metrics such as MAE and R².

One real-world application of this regression pipeline approach could be predicting housing prices in the real estate industry. Features such as location, house size, and number of rooms could be used to estimate property values and support business decision-making.
