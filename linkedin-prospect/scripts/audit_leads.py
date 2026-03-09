"""
Auditer les leads d'une campagne Lemlist : détecter ceux sans messages personnalisés.

Utilise l'endpoint d'export (seul à retourner les custom variables) puis filtre
les leads dont les variables requises sont vides.

Usage :
  uv run python3 scripts/audit_leads.py <campaign_id> <variables_requises> [--pause]

  variables_requises : liste séparée par des virgules (ex: m1_message,invitation_note)
  --pause : pauser automatiquement les leads incomplets dans Lemlist

Exemples :
  uv run python3 scripts/audit_leads.py cam_xxx m1_message
  uv run python3 scripts/audit_leads.py cam_xxx m1_message,invitation_note --pause
"""

import json
import os
import subprocess
import sys
import time
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
        print("Erreur : LEMLIST_API_KEY introuvable (.env ou variable d'environnement)", file=sys.stderr)
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


def export_leads(campaign_id: str, api_key: str) -> list[dict]:
    """Exporte tous les leads d'une campagne avec leurs custom variables."""
    data = api("GET", f"/campaigns/{campaign_id}/export/leads?state=all&format=json", api_key)
    if isinstance(data, dict) and "error" in data:
        print(f"Erreur export : {data}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, list):
        print(f"Erreur : réponse inattendue de l'export ({type(data).__name__})", file=sys.stderr)
        sys.exit(1)
    return data


def check_variables(leads: list[dict], required_vars: list[str]) -> tuple[list[dict], list[dict]]:
    """Sépare les leads complets des incomplets."""
    complete = []
    incomplete = []

    for lead in leads:
        missing = []
        for var in required_vars:
            value = lead.get(var, "")
            if not value or not str(value).strip():
                missing.append(var)

        entry = {
            "lead_id": lead.get("_id", ""),
            "name": f"{lead.get('firstName', '')} {lead.get('lastName', '')}".strip(),
            "email": lead.get("email", ""),
            "company": lead.get("companyName", ""),
        }

        if missing:
            entry["missing"] = missing
            incomplete.append(entry)
        else:
            complete.append(entry)

    return complete, incomplete


def pause_leads(leads: list[dict], campaign_id: str, api_key: str) -> int:
    """Pause les leads incomplets. Rate limit : 20 req / 2s."""
    paused = 0
    for i, lead in enumerate(leads):
        lead_id = lead["lead_id"]
        if not lead_id:
            continue
        api("POST", f"/leads/pause/{lead_id}?campaignId={campaign_id}", api_key)
        paused += 1
        # Respecter le rate limit
        if (i + 1) % 18 == 0:
            time.sleep(2)
    return paused


def main():
    if len(sys.argv) < 3:
        print("Usage : audit_leads.py <campaign_id> <variables_requises> [--pause]", file=sys.stderr)
        print("  variables_requises : m1_message,invitation_note", file=sys.stderr)
        sys.exit(1)

    campaign_id = sys.argv[1]
    required_vars = [v.strip() for v in sys.argv[2].split(",")]
    should_pause = "--pause" in sys.argv

    api_key = load_api_key()

    leads = export_leads(campaign_id, api_key)
    complete, incomplete = check_variables(leads, required_vars)

    paused_count = 0
    if should_pause and incomplete:
        paused_count = pause_leads(incomplete, campaign_id, api_key)

    print(json.dumps({
        "ok": True,
        "campaign_id": campaign_id,
        "required_variables": required_vars,
        "total_leads": len(leads),
        "complete": len(complete),
        "incomplete": len(incomplete),
        "paused": paused_count,
        "incomplete_leads": incomplete,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
