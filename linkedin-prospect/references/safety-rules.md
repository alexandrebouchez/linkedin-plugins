# Safety Rules — Règles de sécurité Lemlist

## Non négociable

Ces règles ne peuvent pas être contournées, même si l'utilisateur le demande.

### 1. JAMAIS lancer automatiquement

```
❌ mcp__lemlist__review_and_launch_leads(...)
❌ mcp__lemlist__set_campaign_state({ action: "start" })
```

Ne jamais appeler ces outils sans approbation **explicite** et **spécifique** de l'utilisateur dans le message courant. "Lance la campagne" doit être dit clairement, pas déduit.

### 2. JAMAIS ajouter + lancer dans la même action

Si on ajoute des leads dans un batch, on n'active pas la campagne dans la même session. L'utilisateur doit vérifier dans le dashboard Lemlist avant de lancer.

### 3. Toujours review avant push

Le batch complet doit être affiché et validé par l'utilisateur **avant** d'appeler `add_lead_to_campaign`. Pas de push silencieux.

### 4. Pauser, pas supprimer (campagnes)

En cas de doute ou de problème :
```
✅ mcp__lemlist__set_campaign_state({ action: "pause" })
❌ Supprimer la campagne
```

Ne jamais supprimer une campagne entière. Pour retirer un lead individuel (client existant, doublon, erreur), utiliser `remove_lead.py`.

### 5. Pas d'update via MCP

Le MCP Lemlist n'a pas d'outil update lead. Utiliser le script `update_lead.py` pour les modifications de custom variables.

### 6. JAMAIS activer l'auto-launch

L'auto-launch doit rester **désactivé** sur toutes les campagnes. Avec l'auto-launch OFF, les leads ajoutés passent par un état "review" avant d'entrer dans la séquence. C'est le filet de sécurité contre les leads avec des variables manquantes (Lemlist envoie les messages avec des variables vides sans bloquer).

Pour lancer les leads en attente après vérification, utiliser `launch_leads.py`. Ne jamais activer l'auto-launch comme contournement.

### 7. TOUJOURS ajouter les leads avec leurs messages

Ne jamais ajouter un lead à Lemlist sans ses custom variables de messages (`m1_message`, `invitation_note`, etc.) déjà remplies. Utiliser le paramètre `customVariables` de `add_lead_to_campaign` pour pousser les messages en même temps que le lead.

## Bonnes pratiques

- Vérifier les stats de la campagne avant chaque batch (`get_campaign_stats`)
- Utiliser `deduplicate: true` pour chaque `add_lead_to_campaign`
- Ne pas dépasser 20 leads par batch (risque de ban LinkedIn)
- Vérifier que le campaign ID dans `config.md` est correct avant chaque opération
- Utiliser `audit_leads.py` comme vérification secondaire avant un lancement
