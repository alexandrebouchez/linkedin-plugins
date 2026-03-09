# Define Examples

## Objectif

Créer ou mettre à jour `examples.md` dans le dossier de prospection. Messages annotés par étape de séquence — la référence concrète que l'agent writer utilise.

## Quand utiliser ce guide

Pas dans le setup initial. Les exemples théoriques ont peu de valeur. Ce workflow prend son sens :
- Après le premier batch de messages (vrais messages à annoter)
- Quand l'utilisateur a des messages existants
- Quand des résultats arrivent (message qui a converti = gold standard)

## Prérequis

`product.md`, `icp.md`, `voice.md`, `arguments.md` doivent exister.

## Template cible

Voir `templates/examples.md.tpl` pour la structure de référence.

## Adaptation à la séquence

Les exemples doivent couvrir chaque étape de la séquence active. Si une campagne Lemlist existe, lire la séquence via `get_campaign_sequences` avant de générer. Si aucune séquence n'est définie, couvrir les étapes standard (invitation, premier message, 1-2 follow-ups) et ajuster après configuration.

## Workflow

### Si le fichier existe déjà

Vérifier la couverture : chaque étape a ses exemples ? Chaque angle est illustré ? Identifier les écarts avec la séquence actuelle et proposer des ajouts.

### Si on part de zéro

**Avec des messages existants** : annoter chaque message (étape, angle, ce qui marche, anti-patterns), classer par étape, identifier les étapes manquantes.

**Sans messages existants** : lire les fichiers de référence (`references/messaging.md`, `voice.md`, `arguments.md`) et générer des exemples couvrant les angles disponibles et les segments définis. Le nombre de variantes découle du contenu (un exemple par angle, par segment significativement différent), pas d'un quota fixe.

Annoter chaque message : pourquoi ça marche, quel angle, quel segment.

### Review

Valider l'authenticité ("L'expéditeur enverrait ça tel quel ?") et la couverture (étapes x angles).

Ne pas terminer sans validation explicite.

## Sync avec la campagne

Ce workflow peut être relancé quand la séquence change : nouvelle étape → nouveaux exemples, étape supprimée → archiver, cadence modifiée → vérifier le ton des follow-ups.

## Output

Écrire `examples.md` dans le dossier de prospection.
