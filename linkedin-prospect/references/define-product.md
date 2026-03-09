# Define Product

## Objectif

Créer ou mettre à jour `product.md` dans le dossier de prospection. Ce fichier est la base de tout : sans produit bien défini, pas de message pertinent.

## Template cible

Voir `templates/product.md.tpl` pour la structure de référence.

## Workflow

### Si des sources existent (pré-scan du setup)

Lire le `CLAUDE.md` du dossier. Si une section `## Sources` existe, explorer ces sources pour tout ce qui concerne le produit. Pré-remplir un brouillon du template. Présenter à l'utilisateur pour correction/complétion, puis passer à la review.

### Si le fichier existe déjà

Lire `product.md`, analyser proactivement les faiblesses (sections vagues, chiffres manquants, différenciants génériques) et proposer des améliorations concrètes.

### Si on part de zéro

1. Demander à l'utilisateur de décrire son produit librement
2. Analyser la description contre le template cible, identifier les lacunes
3. Combler les lacunes par des questions ciblées — l'objectif est d'obtenir pour chaque section du template des faits concrets, pas du marketing. Si la description initiale couvre un point, ne pas re-questionner.
4. Générer le fichier structuré

### Review

Valider les choix structurants avec l'utilisateur : le problème résolu, les différenciants, le paysage concurrentiel. Soumettre en priorité ce qui a été déduit ou extrapolé (pas ce qui vient directement des sources).

Ne pas terminer sans validation explicite.

## Output

Écrire `product.md` dans le dossier de prospection.
