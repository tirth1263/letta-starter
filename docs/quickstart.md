# Quickstart

This starter follows the screenshot workflow: run the Letta server, install the client, configure environment variables, then start the CLI.

## 1. Run the Letta server

Using Docker Compose:

```bash
cp .env.example .env
# edit NEBIUS_API_KEY in .env
docker compose up -d
```

Using Docker directly:

```bash
docker run -d --name letta -p 8283:8283 \
  -e OPENAI_API_KEY=$NEBIUS_API_KEY \
  -e OPENAI_API_BASE=https://api.tokenfactory.nebius.com/v1 \
  letta/letta:latest
```

PowerShell equivalent:

```powershell
docker run -d --name letta -p 8283:8283 `
  -e OPENAI_API_KEY=$env:NEBIUS_API_KEY `
  -e OPENAI_API_BASE=https://api.tokenfactory.nebius.com/v1 `
  letta/letta:latest
```

## 2. Install the client

```bash
pip install -r requirements.txt
# or: uv sync
```

## 3. Configure env

```bash
cp .env.example .env
# edit NEBIUS_API_KEY and optionally LETTA_BASE_URL
```

If your Nebius dashboard still shows the older Studio endpoint from the reference screenshot, set:

```bash
NEBIUS_BASE_URL=https://api.studio.nebius.ai/v1
```

## 4. Use the agent

```bash
python main.py
```

Try this sequence, then restart the script:

1. `Hi, my name is Arindam and I love building AI apps.`
2. Restart.
3. `What's my name and what do I like to build?`

The agent should answer from its persistent `human` memory block.
