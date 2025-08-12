# ITcredibl Enterprise SDK and Demo

This repo contains:
- python_sdk to exercise streaming, retries, and parallel load
- ts_sdk enterprise TypeScript SDK ready for publishing and local testing

## Prerequisites
- Set ITCREDIBL_API_KEY in your shell
- Optional ITCREDIBL_API_URL

## Python quick start
```bash
cd python_sdk
python -m venv .venv && . .venv/Scripts/activate
pip install -r requirements.txt
setx ITCREDIBL_API_KEY "your_key"
python -m examples.cli_demo
python -m examples.stream_demo
ITCREDIBL_STRESS_N=100 python -m examples.stress_test
```

## TypeScript quick start
```bash

cd ts_sdk
# $env:Path="C:\Program Files\nodejs;$env:Path"
npm install
npm run example
```

## CI and automation
- Makefile for setup, build, test, demo
- GitHub Actions for both SDKs


