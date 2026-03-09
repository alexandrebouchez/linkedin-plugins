"""
Retirer un lead d'une campagne Lemlist.

Le MCP Lemlist n'expose pas de remove lead. Ce script utilise l'API REST directement.
L'action "remove" retire le lead de la campagne sans l'unsubscribe globalement.

Usage :
  uv run python3 scripts/remove_lead.py <campaign_id> "Prénom Nom"
  uv run python3 scripts/remove_lead.py <campaign_id> lea_xxx
"""

import json
import os
import subprocess
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = PLUGIN_DIR / ".env"


def load_api_key() -> str:
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            if line.startswith("LEMLIST_API_KEY="):
                return line.split("=", 1)[1].strip()
    key = os.environ.get("LEMLIST_API_KEY", "")
    if not key:
        print("Erreur : LEMLIST_API_KEY introuvable (.env ou variable d'environnement)",
file=sys.stderr)
        sys.exit(1)
    return key


def api(method: str, path: str, api_key: str, data: dict | None = None) -> dict | list:
    url = f"https://api.lemlist.com/api{path}"
    cmd = ["curl", "-s", "-X", method, "--user", f":{api_key}"]
    if data is not None:
        cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(data, ensure_ascii=False)]
    cmd.append(url)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if not result.stdout.strip():
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Erreur API ({method} {path}): {result.stdout[:200]}", file=sys.stderr)
        sys.exit(1)


def find_lead_id_by_name(name: str, campaign_id: str, api_key: str) -> str:
    leads = api("GET", f"/campaigns/{campaign_id}/leads?limit=200", api_key)
    if not isinstance(leads, list):
        print("Erreur : réponse inattendue de l'API leads", file=sys.stderr)
        sys.exit(1)

    for lead in leads:
        contact_id = lead.get("contactId", "")
        lead_id = lead.get("_id", "")
        contact = api("GET", f"/contacts/{contact_id}", api_key)
        full_name = contact.get("fullName", "")
        if full_name == name:
            return lead_id

    print(f"Erreur : lead '{name}' introuvable dans la campagne {campaign_id}", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage : remove_lead.py <campaign_id> <nom_ou_lead_id>", file=sys.stderr)
        sys.exit(1)

    campaign_id = sys.argv[1]
    identifier = sys.argv[2]
    api_key = load_api_key()

    if identifier.startswith("lea_"):
        lead_id = identifier
    else:
        lead_id = find_lead_id_by_name(identifier, campaign_id, api_key)

    result = api("DELETE", f"/campaigns/{campaign_id}/leads/{lead_id}?action=remove", api_key)

    name = f"{result.get('firstName', '')} {result.get('lastName', '')}".strip()

    print(json.dumps({
        "ok": True,
        "action": "removed",
        "lead_id": lead_id,
        "campaign_id": campaign_id,
        "name": name or identifier,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
