from strands import Agent, tool
from strands.models.ollama import OllamaModel

PRODUCTS = {
    "laptop lenovo" : {"stock":5, "price":10000000},
    "laptop asus" : {"stock":0, "price":9000000},
    "hp samsung" : {"stock":5, "price":20000000}
}

@tool
def checkStock(product:str)->str:
    """"Cek jumlah produk tersedia berdasarkan nama
    Bisa juga untuk melihat harga dari produk"""
    data = PRODUCTS.get(product)
    if data is None:
        return f"produk {product} tidak ditemukan"
    return f"produk {product} ditemukan dengan data {data}"

@tool
def orderProduct(product:str, quantity:int)-> str:
    """Panggil tool ini jika ada yang mau beli produk.
    Buat pesanan dari produk yang tersedia dan update data stock setelah dipesan."""
    data = PRODUCTS.get(product)
    if data is None:
        return f"produk tidak di temukan"
    if data["stock"] < quantity:
        return f"persediaan tidak cukup untuk product {product}"
    data["stock"] -= quantity
    return f"Pesanan produk {product} berhasil dipesan sebanyak {quantity}"

_model = OllamaModel(host="http://localhost:11434", model_id="llama3.1")

_agent = Agent(
    model=_model,
    tools= [checkStock,orderProduct],
    system_prompt="Kamu asisten toko. jawab dalam bahasa indonesia dengan bahasa yang jelas dan ringkas"
)

# _agent("Apakah ada laptop lenovo, kalau ada berapa harganya? saya mau beli 1")
print("Asisten toko siap. Ketik 'exit' untuk keluar.")
while True:
    pesan = input("\nKamu: ")
    if pesan.lower() in ("exit", "keluar"):
        break
    _agent(pesan)

print("check isi", _agent.messages)