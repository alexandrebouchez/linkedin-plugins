# Design : Protection des leads incomplets

Date : 2026-03-08

## Problème

Lemlist n'empêche pas l'envoi de messages avec des custom variables vides. Une variable non remplie (`{{m1_message}}`) est remplacée par une chaîne vide, produisant un message cassé envoyé au prospect. Aucun mécanisme natif de skip ou de blocage n'existe pour les variables de contenu.

## Décision

### Principe : "Complete before Lemlist"

Un lead ne touche Lemlist que quand il est complet (enrichissement + messages personnalisés remplis).

### Workflow restructuré

```
Source → Enrich → Write messages → Review batch complet → Add à Lemlist avec customVariables
```

Les messages sont rédigés AVANT l'ajout à Lemlist. L'ajout utilise le paramètre `customVariables` de `add_lead_to_campaign` pour pousser les messages en même temps que le lead.

### Filets de sécurité

1. **Auto-launch OFF** (défaut Lemlist, vérifié au setup) : les leads ajoutés arrivent en état "review", pas dans la séquence active.
2. **`review_and_launch_leads`** : lance uniquement les leads complets après vérification.
3. **`audit_leads.py`** : script de diagnostic secondaire qui peut détecter et pauser les leads incomplets.

### Safety rules ajoutées

- Ne jamais activer l'auto-launch
- Toujours ajouter les leads avec leurs messages via `customVariables`

## Fichiers modifiés

- `references/find-prospects.md` : étapes 6-7-8 restructurées (messages avant ajout)
- `references/lemlist-setup.md` : check auto-launch OFF
- `references/safety-rules.md` : règles 6 et 7 ajoutées
- `commands/prospect.md` : review-and-start utilise `review_and_launch_leads`
- `scripts/audit_leads.py` : créé (audit + pause optionnelle)

## Risques couverts

| Risque | Protection |
|---|---|
| Lead ajouté sans messages | Messages écrits AVANT l'ajout via customVariables |
| Ajout à campagne en cours | Lead arrive en "review" (auto-launch OFF) |
| Variable vide envoyée | review_and_launch_leads vérifie avant lancement |
| Leads incomplets oubliés | audit_leads.py en filet de sécurité |
