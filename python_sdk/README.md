# ITcredibl Enterprise Python SDK Demo

## Quick start
```bash
python -m venv .venv && . .venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
setx ITCREDIBL_API_KEY "your_key"
python -m examples.cli_demo
python -m examples.stream_demo
ITCREDIBL_STRESS_N=100 python -m examples.stress_test
```