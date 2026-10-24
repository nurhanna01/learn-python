tasks = ["login", "register", "logout"]

for i, task in enumerate(tasks):
    print(i+1,task)

for i, task in enumerate(tasks,start=1):
    print(f"[{i}]. {task}")

product = {"name": "laptop", "price": 10000000}


for key,value in product.items():
    print(key," : ",value)