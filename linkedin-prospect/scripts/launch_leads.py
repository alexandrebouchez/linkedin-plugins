"""
Lancer les leads en attente de review (scanned → running) dans une campagne Lemlist.

Le MCP Lemlist n'expose pas d'outil pour lancer les leads en état "scanned".
Ce script utilise l'API REST : POST /leads/start/{leadId}?campaignId={campaignId}

Usage :
  uv run python3 scripts/launch_leads.py <campaign_id>
  uv run python3 scripts/launch_leads.py <campaign_id> --dry-run
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
        return {"error": result.stdout[:200]}


def export_leads(campaign_id: str, api_key: str) -> list[dict]:
    """Exporte tous les leads d'une campagne."""
    data = api("GET", f"/campaigns/{campaign_id}/export/leads?state=all&format=json", api_key)
    if isinstance(data, dict) and "error" in data:
        print(f"Erreur export : {data}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, list):
        print(f"Erreur : réponse inattendue de l'export ({type(data).__name__})", file=sys.stderr)
        sys.exit(1)
    return data


def main():
    if len(sys.argv) < 2:
        print("Usage : launch_leads.py <campaign_id> [--dry-run]", file=sys.stderr)
        sys.exit(1)

    campaign_id = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    api_key = load_api_key()

    leads = export_leads(campaign_id, api_key)

    # Filtrer les leads en état "scanned" (= review, en attente de lancement)
    scanned = [l for l in leads if l.get("leadStatus") == "scanned"]
    already_running = [l for l in leads if l.get("leadStatus") not in ("scanned", "paused")]

    if not scanned:
        print(json.dumps({
            "ok": True,
            "campaign_id": campaign_id,
            "dry_run": dry_run,
            "launched_count": 0,
            "already_running": len(already_running),
            "message": "Aucun lead en attente de lancement",
        }, ensure_ascii=False, indent=2))
        return

    if dry_run:
        print(json.dumps({
            "ok": True,
            "campaign_id": campaign_id,
            "dry_run": True,
            "would_launch": len(scanned),
            "already_running": len(already_running),
            "leads": [
                {
                    "lead_id": l.get("_id", ""),
                    "name": f"{l.get('firstName', '')} {l.get('lastName', '')}".strip(),
                    "company": l.get("companyName", ""),
                }
                for l in scanned
            ],
        }, ensure_ascii=False, indent=2))
        return

    # Lancer les leads
    launched = 0
    errors = []

    for i, lead in enumerate(scanned):
        lead_id = lead.get("_id", "")
        name = f"{lead.get('firstName', '')} {lead.get('lastName', '')}".strip()
        if not lead_id:
            errors.append({"name": name, "error": "no lead_id"})
            continue

        result = api("POST", f"/leads/start/{lead_id}?campaignId={campaign_id}", api_key)

        if isinstance(result, dict) and "error" in result:
            errors.append({"lead_id": lead_id, "name": name, "error": result["error"]})
        else:
            launched += 1

        # Rate limit : 18 req / 2s
        if (i + 1) % 18 == 0:
            time.sleep(2)

    print(json.dumps({
        "ok": len(errors) == 0,
        "campaign_id": campaign_id,
        "dry_run": False,
        "launched_count": launched,
        "already_running": len(already_running),
        "errors": errors if errors else [],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
