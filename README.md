# Letta Starter

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Letta](https://img.shields.io/badge/Letta-stateful_agents-0EAD9F)
![Nebius](https://img.shields.io/badge/Nebius-Token_Factory-F0A33A)
![License](https://img.shields.io/badge/license-MIT-white)

A minimal starter for [Letta](https://docs.letta.com/) (formerly MemGPT), built for developers who want to create stateful agents that keep useful memory across sessions. Instead of sending every prompt to a stateless chat endpoint, this project runs a Letta agent with persistent `human` and `persona` memory blocks. The agent can update those blocks as it learns about the user, then remember them when the CLI restarts.

The default inference path is Nebius Token Factory through an OpenAI-compatible endpoint, using `Qwen/Qwen3-30B-A3B`.

## Why this project is useful

Most starter agents feel impressive until you restart them. Letta Starter is designed to show the missing piece: durable agent memory. You can tell the agent your name, preferences, goals, or favorite project style, close the CLI, run it again, and ask what it remembers.

This makes it a clean foundation for:

- personal assistants that remember user preferences
- prototype support agents with long-lived context
- memory-first demos for AI agent portfolios
- experiments with Letta, MemGPT-style memory, and OpenAI-compatible model providers

## Features

- Stateful Letta agent with persistent core memory
- Two editable memory blocks: `human` and `persona`
- Automatic memory management through Letta memory tools
- Nebius Token Factory inference via OpenAI-compatible configuration
- Interactive Python CLI with readable output
- Docker Compose setup for the Letta server
- Static project website ready for deployment

## Architecture

```text
User terminal
  |
  v
Python CLI (main.py)
  |
  v
Letta client SDK
  |
  v
Local Letta server on Docker
  |
  v
Nebius Token Factory model endpoint
```

Letta stores the agent state, message history, and memory blocks on the server side. The CLI only loads or creates the agent, sends user messages, and displays the current memory after each turn.

## Prerequisites

- Python 3.10+
- Docker
- Nebius API key from [Nebius Token Factory](https://dub.sh/nebius)

## Setup

### 1. Run the Letta server

Copy the environment template:

```bash
cp .env.example .env
```

Add your Nebius key to `.env`:

```bash
NEBIUS_API_KEY=your_nebius_token_factory_api_key
```

Start Letta:

```bash
docker compose up -d
```

Or run Docker directly:

```bash
docker run -d --name letta -p 8283:8283 \
  -e OPENAI_API_KEY=$NEBIUS_API_KEY \
  -e OPENAI_API_BASE=https://api.tokenfactory.nebius.com/v1 \
  letta/letta:latest
```

PowerShell:

```powershell
docker run -d --name letta -p 8283:8283 `
  -e OPENAI_API_KEY=$env:NEBIUS_API_KEY `
  -e OPENAI_API_BASE=https://api.tokenfactory.nebius.com/v1 `
  letta/letta:latest
```

The original reference screenshot used `https://api.studio.nebius.ai/v1`. Nebius Token Factory currently documents `https://api.tokenfactory.nebius.com/v1`, so this starter uses the current endpoint by default. You can set `NEBIUS_BASE_URL` in `.env` if your account uses a different endpoint.

### 2. Install the client

```bash
pip install -r requirements.txt
# or: uv sync
```

### 3. Configure the agent

The defaults in `.env.example` are ready for the local Docker server:

```bash
LETTA_BASE_URL=http://localhost:8283
LETTA_AGENT_NAME=letta-starter-agent
LETTA_MODEL=openai/Qwen/Qwen3-30B-A3B
LETTA_EMBEDDING=openai/Qwen/Qwen3-Embedding-8B
```

Leave `LETTA_API_KEY` blank when using the local Docker server. Set it only if you adapt the starter for Letta Cloud.

## Usage

```bash
python main.py
```

Try this sequence:

1. Say: `Hi, my name is Arindam and I love building AI apps.`
2. Exit the CLI.
3. Start it again with `python main.py`.
4. Ask: `What's my name and what do I like to build?`

The agent should answer from its persisted `human` memory block.

## Project structure

```text
.
|-- main.py              # Interactive Letta CLI
|-- requirements.txt     # pip dependencies
|-- pyproject.toml       # uv-compatible project metadata
|-- docker-compose.yml   # Letta server container
|-- .env.example         # Safe environment template
|-- docs/quickstart.md   # Screenshot-style setup walkthrough
|-- site/                # Deployment-ready static website
`-- LICENSE
```

## Troubleshooting

If the CLI cannot connect, make sure the Letta container is running:

```bash
docker ps
docker logs letta
```

If the model call fails, check:

- `NEBIUS_API_KEY` is set and valid
- `NEBIUS_BASE_URL` matches the endpoint shown in your Nebius dashboard
- `LETTA_MODEL` matches an available Nebius model name
- `LETTA_EMBEDDING` matches an available embedding model

If Docker says the container name already exists:

```bash
docker rm -f letta
docker compose up -d
```

## Official references

- [Letta Python SDK](https://docs.letta.com/api/python/)
- [Letta memory blocks](https://docs.letta.com/guides/agents/memory-blocks)
- [Letta Docker guide](https://docs.letta.com/guides/docker/)
- [Nebius Token Factory API introduction](https://docs.studio.nebius.com/api-reference/introduction)

## License

MIT
