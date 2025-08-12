# ITcredibl Enterprise Demo Suite (Python)

One SDK. Many models. **Smart routing** for cost, latency, reliability, and compliance.

### What’s included
- Chat + **true streaming** (SSE)
- **Policy‑based smart routing** (allow/deny, health score, residency hint)
- **Automatic fallbacks** to meet SLAs
- **Tool/function calling**
- **Embeddings** + **Moderation**
- **Usage/FinOps analytics**
- Batch/parallel + stress tests
- Cost caps & residency flags (demo)
- Extensible **metrics hook** for Datadog/Splunk

### Quickstart (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# set your key
[Environment]::SetEnvironmentVariable('ITCREDIBL_API_KEY','your_key','Process')
# run a quick demo
python demos\01_basic_chat.py


# create venv and install
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .

# env
Copy-Item .env.example .env
$env:ITCREDIBL_API_KEY="your_key_here"
$env:ITCREDIBL_API_URL="https://api.itcredibl.com/functions/v1/itcredibl-api"

# run a few demos
python demos\01_basic_chat.py
python demos\02_streaming.py
python demos\04_fallbacks.py
python demos\11_policy_enforcement.py


# run via CLI wrapper
python -m itcredibl_enterprise_cli basic
python -m itcredibl_enterprise_cli streaming
python -m itcredibl_enterprise_cli routing
python -m itcredibl_enterprise_cli fallbacks
python -m itcredibl_enterprise_cli tools
python -m itcredibl_enterprise_cli embeddings
python -m itcredibl_enterprise_cli moderation
python -m itcredibl_enterprise_cli usage
python -m itcredibl_enterprise_cli batch
python -m itcredibl_enterprise_cli stress
python -m itcredibl_enterprise_cli policy
python -m itcredibl_enterprise_cli residency