# EC Test/Sécurité 2026

Robin Penea v1.0.0

## Format

L'objectif de cette épreuve est d'évaluer vos capacités de dev, algorithmie et sécurité au niveau B3 de la Coding Factory. L'épreuve s'étale sur 3 jours, du 10/06/2026 au 12/06/2026 :

- **Jour 1 (10/06)**  Journée de développement en distanciel, en autonomie complète, pour tous les étudiants. Je serai disponible toute la journée pour vous aider sur la partie setup de l'environnement et répondre à vos questions.
- **Jours 2 et 3 (11/06 et 12/06)** Passage individuel à l'oral de 15 minutes en présentiel sur le site de Cergy. Chaque étudiant passe sur un seul des deux jours. L'ordre de passage vous sera communiqué rapidement.

Le lancement du projet se fera en distanciel sur le Discord de la Coding à 09h00 le 10/06, dans un channel accessible à tous. **Merci de vérifier que vous avez accès à ce serveur Discord avec les bons droits.**

## Projet de développement

Le premier jour de l'épreuve, un sujet ainsi qu'un lien GitHub Classroom vous seront partagés sur Discord afin de réaliser le développement. Dans ce projet, vous allez devoir développer des fonctionnalités, corriger des bugs et améliorer la sécurité. La stack technique choisie est :

- Langage Python >= 3.12 avec virtualenv et pip
- Framework FastAPI
- Base de données SQLite + ORM SQLModel
- pytest + httpx TestClient

Une UI basique est fournie et n'est pas à modifier. Votre travail porte sur la logique des endpoints, les tests, et les failles de sécurité à colmater.

La notation côté code s'appuiera principalement sur la CI fournie, branchée automatiquement sur le repo GitHub Classroom. Elle exécute à chaque commit une suite de tests qui couvre bugs, failles de sécurité et fonctionnalités attendues : les corriger fait passer les tests. Vous suivez ainsi votre progression commit après commit.

Le projet est réalisé en distanciel sur vos ordinateurs individuels. Le rendu évalué est le **dernier commit poussé sur la branche `main`** avant 23h59 le 10/06. Aucun rendu par mail ou archive ZIP ne sera accepté.

## Prérequis techniques

Avant l’épreuve, assurez-vous d’avoir :
- Python >= 3.12 installé
- git installé et configuré
- un compte GitHub fonctionnel
- accès à GitHub Classroom
- accès au Discord de la Coding Factory
- la capacité à créer un virtualenv et installer des dépendances avec pip
- un éditeur de code prêt à l’emploi

## Passage à l'oral

Chaque étudiant passe environ 15 minutes en présentiel sur le site de Cergy avec son ordinateur portable, sur l'un des deux jours suivant la journée de projet. La discussion se fait directement à partir de votre projet, code sous les yeux. Les sujets abordés seront les suivants :

- Fonctionnalités réalisées
- Explication des algorithmes
- Explication des failles de sécurité corrigées

## Utilisation de l'IA

L'objectif de cette épreuve est de vérifier vos capacités de développement et votre niveau technique, pas vos skills de prompt engineering. Règles d'utilisation :

- Vous pouvez utiliser les IA. Le repo du projet contiendra des instructions (AGENTS.md) orientant l'utilisation des IA pour vous accompagner au lieu de réfléchir à votre place.
- **La discussion de l'oral aura un coefficient plus fort que le dev (environ 60/40)**. C'est le seul moyen effectif de vérifier votre vraie compréhension de ce qui a été fait. Néanmoins, un oral brillant ne peut pas compenser un projet non rendu. Les deux parties sont nécessaires.
- Pendant l'oral, vous devez pouvoir expliquer **n'importe quelle ligne** de votre code. Si vous ne comprenez pas ce que vous rendez, l'IA ne vous a pas aidé, elle vous a desservi.

