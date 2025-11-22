#!/usr/bin/env python3
"""Simple script to reproduce the curl POST to Perplexity's chat/completions endpoint.

Features:
- Builds the JSON payload used in the curl command
- Prints the prepared request (headers + body) by default (dry-run)
- Use --send to actually POST the request (requires API key via env or --api-key)

Usage examples:
  # dry-run (no network call)
  python perplexity_request.py

  # actually send using PERPLEXITY_API_KEY environment variable
  PERPLEXITY_API_KEY=sk_xxx python perplexity_request.py --send

  # or pass key on command line (less secure)
  python perplexity_request.py --send --api-key sk_xxx

"""
import os
import sys
import json
import argparse

try:
    import requests
except Exception:
    requests = None

API_URL = "https://api.perplexity.ai/chat/completions"

DEFAULT_PAYLOAD = {
    "model": "sonar",
    "stream": False,
    "max_tokens": 1024,
    "frequency_penalty": 1,
    "temperature": 0.0,
    "messages": [
        {"role": "system", "content": "Be precise and concise in your responses."},
        {"role": "user", "content": "How many stars are there in our galaxy?"}
    ]
}


def build_headers(api_key: str):
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }


def print_prepared_request(url: str, headers: dict, payload: dict):
    print("Prepared POST request:")
    print(f"URL: {url}")
    print("Headers:")
    for k, v in headers.items():
        if k.lower() == "authorization":
            print(f"  {k}: Bearer <REDACTED>")
        else:
            print(f"  {k}: {v}")
    print("\nJSON payload:")
    print(json.dumps(payload, indent=2))


def send_request(url: str, headers: dict, payload: dict, timeout: int = 30):
    if requests is None:
        raise RuntimeError("The 'requests' library is required to send HTTP requests. Install it in your venv: pip install requests")
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    return resp


def main(argv):
    parser = argparse.ArgumentParser(description="Perplexity API chat/completions example")
    parser.add_argument("--api-key", help="Perplexity API key (optional; falls back to PERPLEXITY_API_KEY env var)")
    parser.add_argument("--send", action="store_true", help="Actually send the request instead of dry-run")
    parser.add_argument("--payload-file", help="Optional JSON file to use as payload instead of the default")
    args = parser.parse_args(argv)

    api_key = args.api_key or os.environ.get("PERPLEXITY_API_KEY")

    payload = DEFAULT_PAYLOAD
    if args.payload_file:
        with open(args.payload_file, "r", encoding="utf-8") as f:
            payload = json.load(f)

    if args.send and not api_key:
        print("Error: --send requested but no API key found. Provide PERPLEXITY_API_KEY env var or --api-key.", file=sys.stderr)
        sys.exit(2)

    headers = build_headers(api_key if api_key else "<no-key>")

    # Dry-run: print the prepared request
    print_prepared_request(API_URL, headers, payload)

    if args.send:
        print("\nSending request...\n")
        try:
            resp = send_request(API_URL, headers, payload)
            print(f"HTTP {resp.status_code}")
            try:
                print(json.dumps(resp.json(), indent=2))
            except Exception:
                print(resp.text)
        except Exception as e:
            print("Request failed:", e, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
