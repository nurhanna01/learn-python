def format_tasks(tasks):
    result = []
    for i, task in enumerate(tasks,start=1):
        result.append(f"[{i}] {task}")
    return result

print(format_tasks(["login", "register", "logout"]))