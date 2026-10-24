product_name = "laptop"
price = 15500000
discount = 0.15

print(f"{product_name} | Rp {price:,} | diskon {discount:.0%}")

final_price = round(price - (price*discount))
print(f"Harga akhir: Rp {final_price:,}")