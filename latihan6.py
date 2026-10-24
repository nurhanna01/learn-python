prices = [15000, 200000, 50000, 1200000, 75000]

cheap = [n for n in prices if n < 100000]

print("cheap=>",cheap)

with_tax = [round(n+(0.1*n)) for n in prices]

print("with_tax",with_tax)

# ==================

print(int(0.29 * 100))
print(round(0.29 * 100))