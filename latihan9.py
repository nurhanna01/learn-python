def safe_int(text, default=0):
    try:
        return int(text)
    except:
        return default
    finally:
        print("selesai")

print(safe_int("hell"))
