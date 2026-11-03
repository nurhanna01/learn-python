from strands import Agent, tool
from strands.models.ollama import OllamaModel

@tool
def letter_counter(word: str, letter: str) -> int:
    """Hitung berapa kali sebuah huruf muncul dalam sebuah kata."""
    return word.lower().count(letter.lower())
@tool
def kuadrat(number: float) -> float:
    "Hitung hasil kuadrat dari number"
    return number * number

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
)

agent = Agent(model=model, tools=[letter_counter, kuadrat])
agent('Ada berapa huruf "e" dalam kata development? Lalu kuadratkan hasilnya')