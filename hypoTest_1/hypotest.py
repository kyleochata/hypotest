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
print(1-binom.cdf(57, 100, 0.6)) 

