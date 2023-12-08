import math

h_down_10symbols=2.50951431750726
h_up_10symbols=3.13151077748777

h_down_20symbols=1.60620306386131 
h_up_20symbols=2.23552442325821

h_down_30symbols=1.30319886813902 
h_up_30symbols=1.95418595763795

r_down_for_10symbols = 1 - (h_down_10symbols/math.log2(34))
r_up_for_10symbols = 1 - (h_up_10symbols/math.log2(34))

r_down_for_20symbols = 1 - (h_down_20symbols/math.log2(34))
r_up_for_20symbols = 1 - (h_up_20symbols/math.log2(34))

r_down_for_30symbols = 1 - (h_down_30symbols/math.log2(34))
r_up_for_30symbols= 1 - (h_up_30symbols/math.log2(34))

print(r_down_for_10symbols, "< R for 10 symbols <", r_up_for_10symbols)
print(r_down_for_20symbols,"< R for 20 symbols <", r_up_for_20symbols)
print(r_down_for_30symbols,"< R for 30 symbols <", r_up_for_30symbols)
