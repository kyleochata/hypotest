import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats import chi2_contingency
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
import utils


URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-ML0232EN-SkillsNetwork/asset/insurance.csv'
utils.new_dir("data")
utils.download(URL, "data/insurance.csv")

data = pd.read_csv('data/insurance.csv')
print(data.head())

d_info = data.info()
print(d_info)
print(f"describe raw data\n {data.describe()}")
columns = data.columns.to_list()
print(f"cols: {columns}")

# Charges will be the response variable 
# age, sex, bmi, children, smoker, region = predictor variables.
# Examine how predictors influence charges
# 1: Choose sample statistic
# Prove (or disprove) that bmi of females is different from males
# Check pop mean for BMI of male to pop mean for BMI for female

#2: Define hypothesis
# Null = BMI of male and BMI of female have no diff
# H1 = difference between BMI's of genders

#3: Set Decision Criteria
# two-tailed test at 5% significance level: 0.025 for each tail. If p-val is less than alpha (0.025) reject the null
# t-test: test the mean of one pop against standard or comparing the means of 2 pops if std dev is not known / limited sample size (n < 30).
    # if std dev is known use z-test rather than t-test
# z-test: test the mean of apop vs a standard or compare the means of 2 pops with large samples regardless of if std dev is known.
    # Able to test portion of some characteristic vs a standard population or comparing the proportions of 2 pops
# f-test: compare variance b/w 2 pops. Samples of any size. ANOVA
# chi-squared test: determine wheter there's a statistically significant diff b/w the expected and observed frequrencies in categories of a contingency table
    #Contingency table - tabular representation of categorical data. Frequency distribution of the variables

#4: Evaluate and interpret results

female = data.loc[data["sex"] == "female"]
male = data.loc[data["sex"] == "male"]
# single column selection in a DataFrame returns a Series
f_bmi = female["bmi"]
m_bmi = male["bmi"]
#plot distribution of 'bmi' values b/w male and female. Expects a DataFrame 
sns.displot(
    data=data,
    x='bmi',
    hue='sex',
    kind='kde',
    palette={'female': 'green', 'male': 'blue'}
)
utils.new_dir("plots")
path = "plots/gender_bmi.png"
if not utils.check_asset_exists(path):
    utils.savePlot(path)

f_mean_bmi = f_bmi.mean()
m_mean_bmi = male.bmi.mean()
print(f"f_m_bmi: {f_mean_bmi}\tm_m_bmi: {m_mean_bmi}")

# Calculate t-value & p-value
a = 0.05
t_val1, p_val1 = stats.ttest_ind(m_bmi, f_bmi)
print(f"t1: {t_val1}\tp1: {p_val1}")
print("P-Value Evaluation")
if p_val1 < a: # type: ignore
    print(f"Conclusion: p_val is {p_val1:.2f} is less than alpha {a}\n Reject the null. There is a difference in BMI for gender")
else:
    print(f"Conclusion: p-val: {p_val1:.2f} is greater than alpha: {a}\n Accept the null that there's no difference of BMI between genders.")
print("T-Test Evaluation")
if t_val1 > 0: # type: ignore
    print(f"The male mean bmi of {m_mean_bmi:.2f} is about {t_val1:.2f} standard errors GREATER than the female mean BMI of {f_mean_bmi:.2f}")
else:
    print(f"The male mean bmi of {m_mean_bmi:.2f} is about {t_val1:.2f} standard errors SMALLER than the female mean BMI of {f_mean_bmi:.2f}")

# Prove that medical claims made by people who smoke are greater than those who don't
smoker = data.loc[data["smoker"]=='yes']
smoker_charges = smoker["charges"]
non_smoker = data.loc[data["smoker"]=='no']
non_charges = non_smoker["charges"]

# Null: average charges of smokers <= non_smokers
#H1: average charges of smokers > non_smokers
# t-test to compare means of smokeing and non_smoking
sch_mean = smoker_charges.mean()
print(f"sch_mean: ${sch_mean:.2f}")
nch_mean = non_charges.mean()
print(f"nch_mean: ${nch_mean:.2f}")

sns.boxplot(x=data.charges, y=data.smoker, data=data).set(title="Fig: Smoker vs Charges")
plt.xlabel("charges")
plt.ylabel("Smoker")
path = "plots/smoker_v_non_charges.png"
if not utils.check_asset_exists(path):
    utils.savePlot(path)

result = stats.ttest_ind(smoker_charges, non_charges)
print(result)
# Extract ttest value
t_val2 = result.statistic # type: ignore
# Extract pValue 
p_val2 = result.pvalue # type: ignore
# Remember that we are asking if smokers pay more. So we are looking in the rightward distribution
# Compared to bmi where we just cared if there is a difference. Here we want to know if group A (smokers) pay s more than group B
"""
    Two-tailed: “Is there any difference?” → we split the 5 % risk into two 2.5 % tails so we can catch the difference whichever direction it goes.
    One-tailed: “I already assume group A is bigger (or smaller).” → we put the whole 5 % risk in one tail; if we land in that single 5 % slice, we say “yes, the difference is significant in the direction I predicted.” 
"""
p_val2_oneTail = p_val2 / 2

if p_val2_oneTail < a:
    print(f"Conclusion: pvalue of {p_val2_oneTail:.2f} < alpha for singleTail {a:.2f}")
    print(f"Reject the null. There is a stat significant difference that smokers are charged more")
else: 
    print(f"Conclusion: pvalue of {p_val2_oneTail:.2f} > alpha for singleTail {a:.2f}")
    print(f"Accept the null, reject alt. There is no difference in charges between smokers and non-smokers")

# Compare BMI of women with no children, one child, two children
f_children = female.loc[female['children'] <= 2]
print(f"f_child\n{f_children.head()}")
print(f"counts\n{f_children['children'].value_counts().sort_index()}")
grouped_f_children = f_children.groupby('children')['bmi'].mean()
print(grouped_f_children)
plt.close('all')
sns.boxplot(x="children", y="bmi", data=f_children).set(title="Female BMI vs Number of Children (<= 2)")
path = "plots/fBMI_v_numChildren.png"
if not utils.check_asset_exists(path):
    utils.savePlot(path)

# Construct ANOVA table to check each groups count (0-2 children) against BMI values. 
# ANOVA answers: Does average BMI look different for women with differring num of children
# Ordinary Least Squares (ols) for estimation of unknown parameters
formula = 'bmi ~ C(children)' # bmi is what is being explained. C(children): treats number of kids a different groups
model = ols(formula, f_children).fit()
aov_table = anova_lm(model)
print(f"ANOVA Table\n{aov_table}") # PR(>F) == p-value > 0.05

# Determine if portion of smokers is significantly different across regions
'''
    Null: Smokers proportions not different 
    H1: Smokers proportions are different
    Comparing 2 categorical groups --> Chi-square test
'''

contingency = pd.crosstab(data.region, data.smoker)
print(contingency)

# Plot distribution of non-smokers/smokers across 4 different regions
contingency.plot(kind="bar", ylabel="Number of people")
path = "plots/smokers_per_region.png"
if not utils.check_asset_exists(path):
    utils.savePlot(path)

# perform chi-square, p-val,degrees of freedom, expected frequencies through chi2_contingency()
chi_res = chi2_contingency(contingency, correction=False)
print(f"chi test res\n {chi_res}")

if chi_res.pvalue < a: # type: ignore
    print(f"Reject the null. p-val: {chi_res.pvalue:.2f} is  < 0.05. \n There's a significant difference in smoker proportions across the various regions")# type: ignore
else:
    print(f"Accept the null. p-val: {chi_res.pvalue:.2f} is > 0.05. \nThere's no difference in smoker proportion across the regions")# type: ignore