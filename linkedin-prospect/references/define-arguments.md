# Define Arguments

## Objectif

Créer ou mettre à jour `arguments.md` dans le dossier de prospection. Ce fichier définit **pourquoi** le prospect devrait s'intéresser : les angles de douleur, les stats, et les objections connues.

## Prérequis

`product.md` et `icp.md` doivent exister.

## Template cible

Voir `templates/arguments.md.tpl` pour la structure de référence.

## Workflow

### Si des sources existent

Lire le `CLAUDE.md` du dossier, `product.md` et `icp.md`. Le croisement produit x cible génère les angles naturellement. Pré-remplir un brouillon. Présenter à l'utilisateur.

### Si le fichier existe déjà

Lire `arguments.md`, `product.md` et `icp.md`. Analyser proactivement : angles trop vagues, stats manquantes ou périmées, segments non couverts, objections incomplètes.

### Si on part de zéro

1. Lire `product.md` et `icp.md`
2. Analyser le croisement produit x cible pour proposer 3+ angles. Pour chaque angle : la douleur dans les mots du prospect, comment le produit résout concrètement, une stat avec son niveau de fiabilité (confirmée, estimée, à valider), les segments qui résonnent
3. Valider avec l'utilisateur, puis compléter avec les objections fréquentes et les stats disponibles
4. Générer le fichier complet

### Aide-mémoire : types de douleur

| Type | Question à se poser |
|------|---------------------|
| Manque à gagner | Le prospect rate des revenus ? |
| Temps mal investi | Tâches automatisables ? |
| Crédibilité | Risque de paraître incompétent ? |
| Scale impossible | Goulot qui bloque la croissance ? |
| Compétition | Les concurrents ont un avantage ? |

### Review

Valider les angles et leur spécificité. Challenger les stats (confirmée ou inventée ?) et la pertinence par segment.

Ne pas terminer sans validation explicite.

## Output

Écrire `arguments.md` dans le dossier de prospection.
