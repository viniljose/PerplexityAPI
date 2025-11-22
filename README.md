# PerplexityAPI Example

This small repo contains a script to reproduce the curl POST to Perplexity's
`/chat/completions` endpoint.

Files added:

- `perplexity_request.py` — A script that builds the JSON payload, prints the
  prepared request by default (dry-run), and optionally sends the request when
  `--send` is passed and an API key is available.
- `requirements.txt` — Lists runtime dependencies (requests).

Quick start (macOS, zsh):

1. Activate the venv created earlier:

```bash
cd /Users/viniljose/VJ/work/git/PerplexityAPI
source .venv/bin/activate
```

2. Upgrade pip and install requirements:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Dry-run (prints prepared request, no network call):

```bash
python perplexity_request.py
```

4. To actually send the request, provide your API key and pass `--send`:

```bash
export PERPLEXITY_API_KEY="sk_..."
python perplexity_request.py --send
```

Or pass key on command-line (less secure):

```bash
python perplexity_request.py --send --api-key sk_...
```

Notes:
- The script supports `--payload-file` to load a custom JSON payload.
- By default the script does a dry-run so you can inspect the payload and
  headers before sending.
# PerplexityAPI