import matplotlib.pyplot as plt
import numpy as np
# import scipy as stats
from scipy.stats import binom, norm
import math
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import utils

# cdf(correctTrials, total_Trials, prob_of_success_perTrial)
prob = 1 - binom.cdf(56, 100, 0.5)
# extract scalar value from the nompy array before rounding
print(f"{round(float(prob)*100)} %") # 10%

# Determine the number of flips needed to determine confidence of 95% to reject the null (the success rate wasn't due to chance)
calls = binom.ppf(0.95, 100, 0.5)+1
print(calls) # 59 calls needed to have 95% confidence for the predictive power

# Compare 2 competing hypothesis: A = no predictive power; B = 60% predictive power. Center one at 50% and other at 60%
def compare_hypos(mu: int, variance: int) -> None:
    sigma = math.sqrt(variance)
    x = np.linspace(1, 100, 200)
    plt.plot(x, norm.pdf(x, mu, sigma))

compare_hypos(50, 10)
compare_hypos(60, 10)
plt.xlim(30, 80)
plt.title("Comparison of Hypothesis: 50% vs 60% Predictive Power", pad=20)
plt.xlabel("Number of successes in 100 trials")
plt.ylabel('Probability Density')
plt.tight_layout()
utils.new_dir("plots")
path = 'plots/competing_hypos.png'

if not utils.check_asset_exists(path):
    utils.savePlot(path)

# 57 correct calls lie within 95% confidence of both curves
# p-val for H0
print(1-binom.cdf(57, 100, 0.5)) # 6.6% chance of getting > 57 success out of 100 if true rate was 50%
print(binom.cdf(57, 100, 0.6)) # 30% chance of <= 57 success if the true rate is 60%
# Power of H1. "If H1 is true, then 69% chance correctly rejecting the null"
# Power >= 80%. Increase sample size to increase power
print(1-binom.cdf(57, 100, 0.6)) 

# Decrease Confidence 
# Claim at 50 & 60. If we can predict over 55, then predictive power leading to a decreased confidence level
print(1-binom.cdf(55, 100, 0.5))
print(binom.cdf(54, 100, 0.6))

print('bias')
x = binom.ppf(0.95, 100, 0.5) # inverse of cdf
print(1-binom.cdf(x, 100, 0.5)) # 5% chance that someone has no power but we say they do (Type I)
print(binom.cdf(x, 100, 0.6)) # 38% chance someone has predictive power and we say no (Type II)

n_small = 100   # Original sample size
n_large = 1000  # Increased sample size
p_null = 0.5    # Null hypothesis (random guessing)
p_alt = 0.6     # Alternative hypothesis (predictive power)

# Helper function to compute normal approximation
def plot_normal(n, p, label, color):
    mu = n * p
    variance = n * p * (1 - p)
    sigma = math.sqrt(variance)
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
    plt.plot(x, norm.pdf(x, mu, sigma), label=label, color=color)

# # Plot for n=100
# plot_normal(n_small, p_null, "H₀ (n=100)", "red")
# plot_normal(n_small, p_alt, "H₁ (n=100)", "blue")

# Plot for n=1000
plot_normal(n_large, p_null, "H₀ (n=1000)", "green")
plot_normal(n_large, p_alt, "H₁ (n=1000)", "purple")

plt.xlabel("Number of Correct Predictions")
plt.ylabel("Probability Density")
plt.legend()
plt.xlim(300, 1000)  # Adjust based on n_large

path = "plots/largerSamples_compare_hypos.png"

if not utils.check_asset_exists(path):
    utils.savePlot(path)
print("Larger Samples")
print(binom.ppf(0.95, 1000, 0.5)) # 95% of the time you will see 526 or fewer success
print(binom.ppf(0.95, 1000, 0.6)) # 95% of the time will see 621 or fewer success
print (1-binom.cdf(550, 1000, 0.5)) # 0.06% for seeing at least 550 success. Reject null
print (binom.cdf(550, 1000, 0.6)) #0.07% chance for seeing 550 or fewer success if rate is 60%. Type II error rate of 0.7%

'''
Binomal Distribution

    binom.pmf(k, n, p): Exact chance for a specific score
        - What's the probability you get exactly k number in n trials
        - % chance of exactly k success when the probability is p
    binom.cdf(k, n, p): Running total from 0 to k
        - What's the probability you get k or fewer successes in n trials?
        - % of the time you'll see k or fewer success in n trials
    binom.sf(k, n, p): Survival function: Opposite tail
        - Probability you get more than k successes in n trials
        - % chance of > k successes
    binom.ppf(q, n, p): Reverse lookup
        - Give the smallest number of k success so that the cumulative probability is still at least q
        - q% of the time you'll see k successes or fewer
'''