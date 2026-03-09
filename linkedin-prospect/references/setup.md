# Setup

> **Rappel communication** : ce fichier est une référence technique pour l'agent. Ne jamais exposer les termes techniques à l'utilisateur. Table de communication : voir `commands/prospect.md`.

## Objectif

Créer un dossier de prospection fonctionnel. L'utilisateur fournit ses sources, l'IA comprend et génère, l'utilisateur valide par sélection.

## Dossier de travail

Créer le dossier automatiquement dans un emplacement par défaut (ex: `~/Code/prospection/{nom-produit}/`). Ne pas demander un chemin technique — juste informer l'utilisateur : "Je crée un espace de travail pour cette campagne." Ne demander un emplacement spécifique que si l'utilisateur le souhaite.

## Phase 1 : Collecter

Demander à l'utilisateur tout ce qui peut aider : URL du site, pitch deck, messages existants, profils LinkedIn, exemples de clients. Rien n'est obligatoire, tout est utile.

Explorer chaque source fournie. Faire une recherche web rapide pour situer le produit dans son marché. Persister les sources dans le `CLAUDE.md` du dossier (section `## Sources`).

Plus l'utilisateur donne de matière, moins il y a de questions après.

## Phase 2 : Générer

À partir des sources, générer les 4 fichiers d'un coup :

- `product.md` — le produit, son problème, ses différenciants
- `icp.md` — la cible, les segments, les triggers
- `voice.md` — le ton de l'expéditeur
- `arguments.md` — les angles de douleur, stats, objections

Les templates (`templates/*.md.tpl`) donnent la structure cible. L'intelligence fait le reste : croiser les sources, déduire ce qui n'est pas dit explicitement, combler les lacunes avec du bon sens.

Ne pas générer `examples.md` à ce stade. Les exemples se construisent à partir de vrais messages, pas de théorie. Ils viendront après le premier batch.

## Phase 3 : Valider

Présenter les 4 fichiers à l'utilisateur et valider les décisions clés via AskUserQuestion. L'objectif n'est pas de tout reviewer ligne par ligne, mais de s'assurer que les choix structurants sont justes :

- **Le problème principal** : c'est bien ça que le produit résout ?
- **La cible prioritaire** : c'est bien ce segment qu'on attaque en premier ?
- **Le ton** : ça ressemble à comment l'expéditeur parle ?
- **L'angle principal** : cette douleur résonne vraiment chez les prospects ?

Les sections extraites directement des sources sont bonnes sauf correction. Soumettre en détail ce qui a été déduit ou extrapolé.

Si l'utilisateur veut creuser un fichier en particulier, il peut toujours lancer le define-* correspondant.

## Phase 4 : Finalisation

Mettre à jour le `CLAUDE.md` du dossier (depuis `claude.md.tpl`).

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Setup terminé — {produit}

Fichiers créés :
  ✓ product.md
  ✓ icp.md
  ✓ voice.md
  ✓ arguments.md

Prochaine étape : connecter Lemlist pour automatiser les envois.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Reprise

Si des fichiers existent déjà : lister ce qui existe, proposer de revoir ou de sauter aux manquants.
