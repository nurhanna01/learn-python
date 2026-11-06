# Strands Code Review Agents

A learning project that builds a **multi-agent code review API** using the [Strands Agents SDK](https://strandsagents.com) (Python) and FastAPI.

Several agents with different roles (security, developer, tech lead) review a **merge request (MR)**, and the result is returned through an HTTP API in a structured format.

## Tech Stack

- Python 3.14
- [Strands Agents SDK](https://strandsagents.com)
- FastAPI
- Pydantic
- [uv](https://docs.astral.sh/uv/) as the package manager
- Model: Mercury (Inception Labs) through an OpenAI-compatible interface.

## Installation

```bash
git clone https://github.com/nurhanna01/strands-code-review-api.git
cd strands-code-review-api
uv sync
```

## Configuration

Create a `.env` file in the project root and fill it with the API key from your model provider:

```dotenv
INCEPTION_API_KEY=your-key-here
```

## Running

```bash
uv run fastapi dev api.py
```

Once it is running:

- API: http://127.0.0.1:8000
- Interactive documentation (Swagger): http://127.0.0.1:8000/docs

## API Usage

### `POST /mr-review`

Reviews a single merge request by its ID.

Request:

```json
{
  "mr_id": "1"
}
```

## References

- [Strands Agents Documentation](https://strandsagents.com)
- [FastAPI](https://fastapi.tiangolo.com)
- [Pydantic](https://docs.pydantic.dev)