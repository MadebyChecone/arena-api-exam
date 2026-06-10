# EC Test/Sécurité 2026 - Sujet

```Robin Penea v1.0.0```

## Contexte
ArenaAPI est une API de gestion de tournois (Échecs, Go, Tennis, Esport, etc). Son objectif est d'en faciliter la gestion :
- Gérer les phases du tournoi (inscription ouverte, tournoi en cours, tournoi terminé, etc)
- Générer les brackets pour les différentes manches
- Mettre à jour automatiquement le [score ELO](https://fr.wikipedia.org/wiki/Classement_Elo) de chaque joueur à l'issue d'un match

Un tournoi à élimination directe ressemble à ceci :

```
  Manche 1        Demi-finales      Finale

  Alice ─┐
         ├─ Alice ─┐
  Bob   ─┘         │
                   ├─ Alice ─┐
  Carol ─┐         │         │
         ├─ Dan ──┘          │
  Dan   ─┘                   ├─ 🏆 Alice
                             │
  Eve   ─┐                   │
         ├─ Eve ───┐         │
  Frank ─┘         │         │
                   ├─ Grace ─┘
  Grace ─┐         │
         ├─ Grace ─┘
  Heidi ─┘
```

Le projet est partiellement terminé et contient des bugs ainsi que des failles de sécurité volontaires. Votre objectif est de le compléter, corriger les bugs et colmater les failles, en vous appuyant sur les tests unitaires pour vérifier le bon fonctionnement. Une partie de la note porte spécifiquement sur la sécurité (hachage des mots de passe, contrôle d'accès, fuite de données, etc).

## Notation

Votre note se base entièrement sur les critères vérifiés automatiquement. Il y a 26 critères répartis sur 100 points (chaque critère a un poids différent). La liste détaillée est disponible avec la commande :
```bash
make criteria
```

La liste complète est disponible dans `grader/criteria/*.py`, avec un fichier pour chaque grande fonctionnalité.

2 types de tests :
- **Behavior**: le test est implémenté `grader/tests/`. Vous devez écrire le code qui fait passer le test. Allez lire le test pour comprendre le comportement attendu.
- **Student test**: vous devez implémenter le test et la fonctionnalité associée. `make criteria` décrit le nom du test attendu ainsi que les `assert` qui doivent être présents.

À chaque push, la pipeline exécute automatiquement les tests et votre note sera visible dans l'onglet **Actions**. Vous pouvez également voir en local avec la commande :
```bash
make grade
```

## Rendu

Le rendu est attendu le **10/06/2026 à 23h59**. Seule la branche `main` est évaluée (le dernier commit poussé avant l'échéance). Pas besoin de m'envoyer vos repos : j'ai automatiquement accès à tout.

## Démarrage

Suivez le guide du [README.md](../README.md) pour démarrer le projet. 

N'oubliez pas que les routes suivantes sont disponibles :
- [http://localhost:8000/](http://localhost:8000/) : UI Web de debug
- [http://localhost:8000/docs](http://localhost:8000/docs) : API Swagger

## UI Web

L'UI Web est accessible à l'adresse [http://localhost:8000/](http://localhost:8000/). Elle est volontairement minimaliste pour éviter de multiplier les outils (npm, CORS, autres dépendances, etc). Son objectif est de vous fournir une UI de debug en supplément des tests.

📣 Vous pouvez modifier `app/web` comme vous le souhaitez. 

## Critères de disqualification

Une disqualification à l'épreuve de dev entraîne un 0/20 et un échec automatique à l'oral (il n'y aura pas de passage à l'oral). Les critères de disqualifications sont :
- Modification d'un fichier protégé du projet (liste ci-dessous)
- Commit > 1000 lignes de diff (ajout + suppression)

### Fichiers protégés

La liste technique est dans `grader/engine/reviewed_files.py`. À retenir :
- `.github/`
- `AGENTS.md`
- `CLAUDE.md`
- `conftest.py`
- `grader/`

**Seul `app/` est modifiable. Le contenu et l'historique Git des fichiers protégés seront vérifiés.**

📣 Vous pouvez modifier [app/seed.py](/app/seed.py) librement pour modifier les données de départ du projet.

