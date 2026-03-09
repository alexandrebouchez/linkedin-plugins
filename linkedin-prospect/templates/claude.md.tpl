# Prospection — {Nom du produit}

Ce dossier contient la configuration de prospection LinkedIn pour {produit}.

## Fichiers

| Fichier | Contenu |
|---------|---------|
| `product.md` | Produit, core loop, différenciants, paysage concurrentiel |
| `icp.md` | Persona cible, segments, qualification, trigger events |
| `voice.md` | Ton de l'expéditeur, vocabulaire, anti-patterns |
| `arguments.md` | Angles de douleur, stats, objections |
| `examples.md` | Messages annotés par étape de séquence |
| `config.md` | Campaign ID Lemlist |

## Sources

{Section remplie par le setup — URLs, docs, résumés des sources collectées}

## Commandes

```
/prospect                → Diagnostic + prochaine étape
/prospect setup          → Onboarding complet
/prospect find-prospects → Trouver et enrichir des prospects
/prospect campaign       → Créer/configurer campagne Lemlist
/prospect status         → Stats campagne
```

## Règles

- Lire product.md + voice.md + arguments.md + examples.md avant chaque rédaction
- La séquence se lit depuis Lemlist (`get_campaign_sequences`), pas depuis un fichier local
- 1 stat max par message, intégrée naturellement
- Chaque message doit passer les 6 quality checks
- JAMAIS lancer la campagne sans approbation explicite
- JAMAIS ajouter des leads et lancer dans la même action
