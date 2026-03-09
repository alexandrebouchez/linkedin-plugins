# Enrichment — Recherche prospect

## Glossaire

- **Tension** : tout signal exploitable pour personnaliser un message (catégorie générale, classée par niveaux 1-6)
- **Trigger event** : tension de niveau 3 spécifiquement — un événement daté (levée de fonds, nouveau poste, pivot...)
- **Accroche / Hook** : la phrase d'entrée du message, construite à partir de la meilleure tension trouvée

## Objectif

Trouver des **tensions activables** sur un prospect pour personnaliser les messages de la séquence. Pas un rapport factuel — une matière qui crée de l'accroche. L'enrichissement doit fournir assez de tension pour que chaque message soit impossible à ignorer pour CE prospect.

## Pré-requis

Avant d'enrichir, lire :
- `icp.md` — les trigger events définis (où les détecter, quel angle ils activent)
- `arguments.md` — les angles disponibles (pour orienter la recherche vers ce qui est utile)

## Hiérarchie des tensions (du plus au moins puissant)

| Niveau | Type | Exemple | Valeur pour le message |
|--------|------|---------|----------------------|
| **1** | **Signal de douleur exprimé** | Post LinkedIn, interview, commentaire où le prospect verbalise une frustration | Ses propres mots = accroche parfaite |
| **2** | **Contradiction visible** | Recrute massivement mais pas de process structuré, site cassé mais ambitions de croissance | Montre qu'on voit un problème non adressé |
| **3** | **Trigger event** | Levée de fonds, nouveau poste, pivot produit, réorg, expansion géo | Fenêtre où les décisions se prennent |
| **4** | **Gap concurrentiel** | Un concurrent du prospect utilise un outil similaire au nôtre | Pression compétitive = urgence |
| **5** | **Scaling signal** | Croissance rapide, recrutements en série, ouverture de bureaux | Processus actuels ne tiendront pas |
| **6** | **Fait contextuel** | Secteur d'activité, taille, positionnement | Utile en fallback, mais ne crée pas de tension seul |

**Règle** : un signal de niveau 1-2 vaut 10 faits de niveau 6. Si on trouve un niveau 1 ou 2, c'est ça qui drive le message. Ne pas noyer la pépite dans du descriptif.

### Ce qu'on ignore

- Vie personnelle, hobbies (sauf si directement lié au business)
- Awards, certifications (décoratif, pas utile pour le message)
- Historique complet de carrière (on se concentre sur le poste actuel)
- Avis/reviews (bruit)

## Méthodologie

### 2-3 recherches web ciblées

Les recherches sont orientées par la hiérarchie ci-dessus. On cherche des tensions, pas une fiche Wikipedia.

1. `WebSearch "{nom} {entreprise}"` — interviews, posts, prises de parole (signal de douleur ?)
2. `WebSearch "{entreprise} {secteur}"` ou `WebSearch "site:{domaine}"` — activités récentes, recrutements, actualités (trigger event ? scaling signal ?)
3. Si pertinent : profil public LinkedIn, page entreprise, Crunchbase (levée ? gap concurrentiel ?)

### Orienter par les triggers

Consulter les trigger events de `icp.md`. Pour chaque trigger défini, vérifier s'il est détectable pour ce prospect via les sources indiquées. Un trigger détecté = accroche à fort timing.

### Orienter par les angles

Consulter `arguments.md`. Savoir quels angles on veut jouer aide à chercher les bonnes infos. Si un angle est "scale impossible", chercher des signaux de croissance. Si un angle est "temps mal investi", chercher des indices de process manuels.

## Format de sortie

L'enrichissement produit un champ `enrichment_notes` structuré :

```
Entreprise : {ce que fait l'entreprise, en 1 phrase}
Prospect : {rôle, responsabilités}

Meilleure tension trouvée (niveau {1-6}) :
{La tension la plus forte, formulée en 1-2 phrases. Si c'est un signal de douleur exprimé, citer les mots du prospect.}

Trigger event : {oui/non — si oui, lequel et source}

Angle suggéré : {quel angle de arguments.md, et pourquoi il colle à ce prospect}

Faits complémentaires :
- {fait utile pour le message}
- {fait utile pour le message}
```

## Fallback

Si rien de fort trouvé en web search :
- Utiliser les notes existantes (du JSONL ou du fichier prospect)
- Observer le poste et l'entreprise pour déduire les enjeux
- Rester factuel : mieux vaut un angle segment-level qu'une personnalisation inventée
- **Indiquer clairement** que l'enrichissement est de niveau 6 (fait contextuel uniquement) — le writer adaptera ses attentes

## Parallélisation

L'enrichissement est parallélisable : un agent scout par prospect, en background. Le batch n'attend pas que tous les enrichissements soient finis pour commencer la rédaction. Dès qu'un prospect est enrichi, la rédaction peut commencer.
