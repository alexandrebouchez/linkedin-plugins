# Find Prospects

> **Rappel communication** : ce fichier est une référence technique pour l'agent. Ne jamais exposer les termes techniques (custom variables, m1_message, enrichment_notes, sequenceId, tension niveau X, etc.) à l'utilisateur. Table de communication : voir `commands/prospect.md`.

## Objectif

Trouver des prospects qui matchent l'ICP, les enrichir, rédiger leurs messages personnalisés, et les ajouter complets à la campagne Lemlist. Un lead ne touche Lemlist que quand il est complet.

## Prérequis

Vérifier avant de commencer :
- `icp.md` doit exister (critères de ciblage)
- `arguments.md` doit exister (angles pour orienter l'enrichissement)
- `config.md` doit exister avec un campaign ID valide — le vérifier en appelant `mcp__lemlist__get_campaign_stats`. Si absent ou invalide → proposer de créer la campagne d'abord.

## Workflow

### 1. Comprendre le besoin

Demander à l'utilisateur :
- Combien de prospects il veut trouver (cadrer à 20 max par lot pour la sécurité du compte LinkedIn — si l'utilisateur en demande plus, proposer de faire plusieurs lots)
- Des critères spécifiques pour ce batch (segment particulier, secteur, géographie, ou "selon l'ICP")
- Des noms/entreprises déjà identifiés à enrichir (optionnel)

### 2. Sourcing

Deux cas :

**A. L'utilisateur fournit des noms/entreprises/URLs**
→ Passer directement à l'enrichissement (étape 3)

**B. Recherche ouverte**
Chercher des prospects via WebSearch en croisant les critères de `icp.md` :
- `WebSearch "{poste cible} {secteur} {géographie}"` — trouver des profils
- `WebSearch "{type d'entreprise} {critère ICP}"` — trouver des entreprises puis leurs décideurs
- Croiser avec les trigger events de `icp.md` : `WebSearch "{secteur} levée de fonds 2025"`, `WebSearch "{secteur} recrutement {poste}"`

Collecter : nom, entreprise, poste, URL LinkedIn si trouvée.

Filtrer silencieusement les prospects qui correspondent aux exclusions de `icp.md` — ce sont des décisions déjà prises, ne pas les présenter.

**Vérifier la contactabilité** : si un prospect n'a ni email ni URL LinkedIn trouvée, le signaler à l'utilisateur maintenant (avant l'enrichissement). Pas la peine d'enrichir quelqu'un qu'on ne peut pas contacter.

### 3. Enrichissement

Pour chaque prospect trouvé, spawner un agent scout en background avec en input :
- Nom, entreprise, poste, URL LinkedIn
- Chemin du dossier de prospection (pour lire `icp.md` et `arguments.md`)
- Chemin racine du plugin (pour lire `references/enrichment.md`)
- Notes existantes si disponibles

Les scouts tournent en parallèle. Afficher un feedback progressif au fil de l'eau :
```
✓ {Nom} — recherche d'infos terminée
⏳ {Nom} — en cours...
```

Ne pas attendre que tous soient finis pour commencer à afficher les résultats.

### 4. Dédup

Avant de continuer, vérifier que chaque prospect n'est pas déjà dans la campagne :
```
mcp__lemlist__search_campaign_leads({ campaignId, email/nom })
```
Retirer les doublons silencieusement.

### 5. Rédaction des messages

Les messages sont rédigés AVANT l'ajout à Lemlist.

1. Lire la séquence depuis Lemlist (`mcp__lemlist__get_campaign_sequences`) et identifier les étapes personnalisées (custom variables) vs templates fixes
2. Pour chaque prospect enrichi, spawner un agent writer avec en input :
   - L'enrichissement du prospect (output du scout)
   - Le chemin du dossier de prospection
   - Chemin racine du plugin (pour lire `references/messaging.md`)
   - La séquence avec les étapes personnalisées identifiées
3. Les writers tournent en parallèle. Même feedback progressif :
```
✓ {Nom} — messages rédigés
⏳ {Nom} — rédaction en cours...
```

### 6. Review du batch complet

Afficher chaque prospect avec ses messages pour une seule review complète :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BATCH — {date}
{N} prospects prêts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

① {Nom} — {Entreprise} ({segment})
   Raison de le contacter : {résumé court}
   Message 1 : {preview m1_message}
   Invitation : {preview invitation_note}

② ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

L'utilisateur valide, ajuste ou rejette par prospect. Le prospect ET ses messages sont validés ensemble, en une seule passe.

### 7. Ajout à Lemlist (avec messages)

Après validation explicite, ajouter chaque prospect à la campagne **avec ses messages déjà remplis** :
```
mcp__lemlist__add_lead_to_campaign({
  campaignId,
  email (si disponible),
  firstName, lastName, companyName,
  linkedinUrl,
  customVariables: {
    enrichment_notes: "...",
    m1_message: "...",
    invitation_note: "..."
  },
  deduplicate: true
})
```

Les leads arrivent en état "review" dans Lemlist (auto-launch est OFF). Ils ne sont pas envoyés tant qu'ils ne sont pas lancés via `review_and_launch_leads`.

Afficher le résumé :
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Batch terminé — {date}
Ajoutés : {N} (en attente de lancement)
Total prospects dans la campagne : {total}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Pour modifier un message après l'ajout, utiliser `update_lead.py` (voir `references/campaign.md`).

### 8. Proposer la suite

- Si `examples.md` n'existe pas et que c'est le premier batch → proposer : "On a maintenant de vrais messages qui marchent. Tu veux qu'on les garde comme référence pour que les prochains soient encore meilleurs ?"
- Si la campagne n'est pas encore lancée → rappeler : "Quand tu es prêt à lancer, `/prospect review-and-start`."
- Si la campagne tourne déjà → "Les prospects sont ajoutés. `/prospect status` pour suivre."

## Safety

Voir `references/safety-rules.md` pour les règles complètes. En résumé : review avant ajout, jamais lancer après ajout, max 20 leads par batch.
