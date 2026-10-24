product = {"name":"laptop", "price": 50000, "in_stock":100 }

print("data pertama:",product)

product["category"] = "electronic"

print("data kedua:",product)

product["price"] = 10000000

print("data ketiga:",product)

print("discount:", product.get("discount",0))

# print(product["discount"])

if "discount" in product:
    print(product["discount"])
else :
    print("xixi")