# Lemlist — Intégration campagne

> **Rappel communication** : ce fichier est une référence technique pour l'agent. Ne jamais exposer les termes techniques (custom variables, sequenceId, campaignId, m1_message, etc.) à l'utilisateur. Table de communication : voir `commands/prospect.md`.

## Objectif

Créer et configurer une campagne Lemlist pour la prospection LinkedIn. L'utilisateur choisit ou personnalise sa séquence, valide les messages de chaque étape, et la campagne est créée en pause.

Génère `config.md` dans le dossier de prospection (campaign ID uniquement). La séquence et les templates vivent dans Lemlist (source de vérité).

## Prérequis

- `product.md`, `icp.md`, `voice.md`, `arguments.md` doivent exister
- `examples.md` est un bonus (créé après le premier batch)
- Le MCP Lemlist doit être connecté

## Références

Lire avant toute action :
- `references/sequence-patterns.md` — architectures de séquences proposées
- `references/safety-rules.md` — règles de sécurité non négociables

## Workflow : création de campagne

### 1. Collecte d'informations

Demander à l'utilisateur :
- **Nom de la campagne**
- **Timezone** (défaut : Europe/Paris)

### 2. Choix de la séquence

Proposer les patterns disponibles via AskUserQuestion (voir `references/sequence-patterns.md`). L'utilisateur peut :
- Choisir un pattern tel quel
- Mixer des éléments de plusieurs patterns
- Décrire une séquence custom

Afficher la séquence choisie sous forme de diagramme pour validation.

### 3. Messages personnalisés par prospect (custom variables)

Définir les custom variables selon la séquence choisie. Les variables standards correspondent aux étapes personnalisées (ex: `m1_message` pour le premier message, `invitation_note` si l'invitation est personnalisée). Les templates fixes ne nécessitent pas de variables. Ajouter `enrichment_notes` pour stocker l'enrichissement.

L'utilisateur peut ajouter des variables supplémentaires.

### 4. Rédaction des templates fixes

Pour chaque étape fixe (pas de personnalisation par prospect) : lire `references/messaging.md` et `voice.md`, rédiger le template, valider avec l'utilisateur. Les templates fixes sont intégrés directement dans les steps Lemlist.

### 5. Création via MCP

1. Créer la campagne :
```
mcp__lemlist__create_campaign_with_sequence({
  name: "{nom}",
  timezone: "{tz}"
})
```
Réponse : contient le `campaignId` et le `sequenceId` principal.

2. Ajouter les steps dans l'ordre avec `add_sequence_step`. Chaque step nécessite `sequenceId`, `type` (`linkedinSend`, `linkedinInvite`, `linkedinNetworkCheck`, `condition`) et `delay` en jours.

Pour les `linkedinSend` : custom variable (ex: `{{m1_message}}`) si personnalisé, contenu fixe sinon.

3. Vérifier avec `get_campaign_sequences` que la séquence est correcte.

### 6. Sauvegarde

Générer `config.md` dans le dossier de prospection :
```
# Configuration Campagne

## Lemlist

- Campaign ID : {id}
- Nom : {nom}
- Timezone : {tz}

La séquence, les steps et les templates fixes vivent dans Lemlist (source de vérité).
```

### 7. NE PAS lancer

Afficher : "Campagne créée et en pause. Vérifie dans le dashboard Lemlist, puis lance quand tu es prêt." Voir `references/safety-rules.md`.

## Lire la séquence en cours

```
mcp__lemlist__get_campaign_sequences({ campaignId })
```
Source de vérité. Ne jamais se fier à un fichier local pour la structure de la séquence.

## Outils MCP disponibles

| Outil | Usage |
|-------|-------|
| `create_campaign_with_sequence` | Créer une campagne |
| `add_sequence_step` | Ajouter un step à une séquence |
| `get_campaign_stats` | Stats de la campagne |
| `get_campaign_sequences` | Lire la séquence (source de vérité) |
| `add_lead_to_campaign` | Ajouter un lead avec custom variables |
| `search_campaign_leads` | Chercher un lead existant |
| `set_campaign_state` | Pauser/démarrer (voir safety-rules.md) |
| `review_and_launch_leads` | Lancer les leads en attente de review |

## Mise à jour de leads

Le MCP Lemlist n'a pas d'outil update lead. Utiliser le script :

```bash
uv run python3 "${CLAUDE_PLUGIN_ROOT}/scripts/update_lead.py" <campaign_id> "Prénom Nom" '{"m1_message": "..."}'
uv run python3 "${CLAUDE_PLUGIN_ROOT}/scripts/update_lead.py" <campaign_id> lea_xxx '{"m1_message": "..."}'
```

## Audit des messages personnalisés

Détecter les leads dont les messages personnalisés ne sont pas remplis, et les mettre en pause pour éviter des envois avec des variables vides :

```bash
# Auditer seulement (rapport)
uv run python3 "${CLAUDE_PLUGIN_ROOT}/scripts/audit_leads.py" <campaign_id> "m1_message,invitation_note"

# Auditer + pauser les leads incomplets
uv run python3 "${CLAUDE_PLUGIN_ROOT}/scripts/audit_leads.py" <campaign_id> "m1_message,invitation_note" --pause
```

Les leads pausés ne recevront aucun message. Une fois leurs variables remplies (via `update_lead.py`), les reprendre via l'API : `POST /leads/start/{leadId}?campaignId=xxx`.
