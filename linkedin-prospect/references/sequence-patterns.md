# Sequence Patterns — Architectures de séquences Lemlist

## Pattern 1 : networkCheck → invite si nécessaire → messages (recommandé)

Le pattern le plus complet. Gère automatiquement les cas connecté/non connecté.

```
Main
└─ CONDITIONAL linkedinNetworkCheck
   │
   ├─ YES (connecté)
   │   ├─ linkedinSend {{m1_message}} J+0
   │   ├─ linkedinSend [follow-up 1 template] J+4
   │   └─ linkedinSend [follow-up 2 template] J+10
   │
   └─ NO (pas connecté)
       ├─ linkedinInvite (vide) J+0
       └─ CONDITIONAL inviteAccepted within 7j
           │
           ├─ YES
           │   ├─ linkedinSend {{m1_message}} J+1
           │   ├─ linkedinSend [follow-up 1 template] J+5
           │   └─ linkedinSend [follow-up 2 template] J+11
           │
           └─ NO
               ├─ linkedinInvite avec note J+1
               └─ CONDITIONAL inviteAccepted within 14j
                   │
                   ├─ YES
                   │   ├─ linkedinSend {{m1_message}} J+1
                   │   ├─ linkedinSend [follow-up 1 template] J+5
                   │   └─ linkedinSend [follow-up 2 template] J+11
                   │
                   └─ NO → Fin définitive
```

## Pattern 2 : direct message (déjà connecté)

Pour cibler des contacts déjà dans le réseau. Plus simple, pas d'invite.

```
Main
├─ linkedinSend {{m1_message}} J+0
├─ linkedinSend [follow-up 1 template] J+4
└─ linkedinSend [follow-up 2 template] J+10
```

## Pattern 3 : invite + message unique

Minimaliste. Une invite puis un seul message si accepté. Adapté aux approches très ciblées (petit volume, haute personnalisation).

```
Main
├─ linkedinInvite avec note J+0
└─ CONDITIONAL inviteAccepted within 14j
    │
    ├─ YES
    │   └─ linkedinSend {{m1_message}} J+1
    │
    └─ NO → Fin définitive
```

## Personnalisation

Ces patterns sont des points de départ. L'utilisateur peut :
- Ajouter ou retirer des étapes de follow-up
- Modifier les délais entre les étapes
- Ajouter des étapes InMail, email, ou autre canal supporté par Lemlist
- Changer les conditions (timeout d'invitation, etc.)

Pour la cadence recommandée entre les messages, voir `references/messaging.md`.

## Arrêt automatique

Lemlist stoppe automatiquement la séquence quand un prospect répond sur LinkedIn. Pas besoin de condition "replied" entre les messages.

## Notes d'invitation

La note d'invitation doit être courte et personnalisée :
- Pas de pitch produit
- Mentionner un intérêt professionnel
- Max 300 caractères (limite LinkedIn)
- Générée à partir de `voice.md` et des exemples d'invitation dans `examples.md`
