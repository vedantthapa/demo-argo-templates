from pathlib import Path

# argo service account
NAME = "argo-server"

# argo namespace
NAMESPACE = "argo"

# token path
TOKEN = Path("argo_token").read_text()
