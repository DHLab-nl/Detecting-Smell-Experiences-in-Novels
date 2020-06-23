"""quick script to perform a sign test between ...
   are the true positive outcomes 'significantly' different?

    i.e. pvalue is probability of observing a result (i.e., relative TP aounts) as least as significant, in the context of the assumption that both approaches are equally likely to yield TP.
"""
import json
from decimal import Decimal, ROUND_CEILING
from scipy.special import comb

with open("group_results_implimentation1+implementation2.json", "r") as f:
    set1 = json.load(f)
    # {"0":"TP", ...}

with open("group_results__aroma_NOUN+ADJ.json", "r") as f:
    set2 = json.load(f)

ties, plus, minus = 0, 0, 0
for r1, r2 in zip(set1.items(), set2.items()):
    # r1 ("0", "TP")

    result1, result2 = r1[1], r2[1]

    if result1 == "TP" and result2 == "TP":
        ties += 1
    elif result1 == "TP":
        plus += 1
    elif result2 == "TP":
        minus += 1

print ("ties:", str(ties))
print ("plus:", str(plus))
print ("minus:", str(minus))

n = 2 * Decimal(ties/2).to_integral_exact(rounding=ROUND_CEILING) + plus + minus
print ("n:", str(n))
k = Decimal(ties/2).to_integral_exact(rounding=ROUND_CEILING) + min(plus, minus)
print ("k:", str(k))

summation = Decimal(0.0)
for i in range(0,int(k)+1):
    q = Decimal(0.5)
    di = Decimal(i)
    
    c = Decimal(comb(int(n),int(i), exact = True))
    a = (q**di)
    b = (q**(n-di))
    summation += (c * a * b)

# use two-tailed version of test
summation *= 2
#     summation *= (Decimal(0.5)**Decimal(n)) # we think this line is not necessary

print("the difference is", 
    "not significant" if summation >= 0.05 else "significant")

print("p_value =", summation)

