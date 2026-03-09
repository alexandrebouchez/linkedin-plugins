# Lemlist Setup

> **Rappel communication** : ce fichier est une référence technique pour l'agent. Guider l'utilisateur en langage clair. Table de communication : voir `commands/prospect.md`.

## Workflow

### 1. Diagnostic

Tenter d'appeler `mcp__lemlist__get_campaigns`. Deux issues :

- **Ça marche** → Lemlist est déjà connecté. Afficher le nombre de campagnes trouvées et passer directement à l'étape suivante du workflow (`/prospect campaign`).
- **Ça échoue** → Guider l'installation ci-dessous.

### 2. Installation (OAuth)

Guider l'utilisateur en langage clair :

"Pour connecter Lemlist, il faut ajouter la connexion dans Claude Code. Je vais te guider étape par étape."

Instructions à donner :
1. "Va dans les paramètres de Claude Code (Settings)"
2. "Cherche la section 'Tools & MCP'"
3. "Clique sur 'Add MCP Server'"
4. "Choisis le type HTTP et colle cette adresse : `https://mcp.lemlist.com/mcp`"
5. "Quand ton navigateur s'ouvre, autorise l'accès à ton compte Lemlist"
6. "C'est fait !"

Documentation officielle : https://www.lemlist.com/integrations/mcp

### 3. Vérification

Appeler `mcp__lemlist__get_campaigns` pour confirmer que la connexion fonctionne. Si ça échoue :

- "Tool not found" → "La connexion Lemlist n'est pas active. Ferme Claude Code complètement et réouvre-le."
- "Unauthorized" → "L'autorisation a expiré. Je vais relancer la connexion, ton navigateur va s'ouvrir pour te reconnecter."
- "Connection refused" → "Impossible de joindre Lemlist. Vérifie ta connexion internet."

### 4. Vérifier que l'auto-launch est désactivé

L'auto-launch doit être **OFF** sur toutes les campagnes. C'est le défaut Lemlist, mais c'est critique : si activé, les leads ajoutés démarrent la séquence immédiatement sans passer par la review. Avec l'auto-launch OFF, chaque lead passe par une étape de vérification avant d'être lancé.

Si l'utilisateur ne sait pas où vérifier : Settings de la campagne > Launch > Auto-launch doit être désactivé.

### 5. Suite

Connexion confirmée → proposer la prochaine étape logique.
