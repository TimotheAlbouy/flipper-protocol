# Spécification Protocole Flipper

Haitam Sbaity & Timothé Albouy & Benjamin Rozenfeld
Ecole Nationale d'Ingénieurs de Bretagne Sud (ENSIBS)

## 1. Sommaire

- [1. Sommaire][1]
- [2. Introduction][2]
- [3. Version naïve][3]
  - [3.1. Pré-requis][3.1]
  - [3.2. Structure de messages FLPR][3.2]
  - [3.3. Etapes du jeu][3.3]
    - [3.3.1. Ecoute de messages FLPR][3.3.1]
    - [3.3.2. Lancement d'une nouvelle balle][3.3.2]
    - [3.3.3. Vérification du message FLPR reçu][3.3.3]
    - [3.3.4. Renvoi d'une balle][3.3.4]
    - [3.3.5. Communication du score][3.3.5]
    - [3.3.6. Election du gagnant][3.3.6]
  - [3.4. Améliorations possibles][3.4]
- [4. Version sécurisée][4]
  - [4.1. Pré-requis][4.1]
  - [4.2. Structure d'un message FLPR][4.2]
  - [4.3. Etapes du jeu][4.3]
    - [4.3.1. Ecoute de messages FLPR][4.3.1]
    - [4.3.2. Lancement d'une nouvelle balle][4.3.2]
    - [4.3.3. Vérification d'un message FLPR reçu][4.3.3]
    - [4.3.4. Renvoi d'une balle][4.3.4]
    - [4.3.5. Communication des scores][4.3.5]
    - [4.3.6. Election du gagnant][4.3.6]
  - [4.4. Améliorations possibles][4.4]

## 2. Introduction

Le protocole Flipper (FLPR) est un protocole de couche applicative basé sur l'architecture TCP/IP (pour ne pas avoir à se soucier des paquets perdus), c'est-à-dire que chaque message FLPR sera encapsulé dans un segment TCP, lui-même encapsulé dans un packet IPv4. FLPR permet à plusieurs ordinateurs d'un même réseau informatique de jouer à une simulation d'envoi de balles, un message symbolisant un envoi de balle entre deux machines. Une fois interceptée par un joueur, une balle doit être renvoyée à un autre joueur et ce jusqu'à ce que le nombre de rebonds restants de la balle s'annule. FLPR fonctionne totalement en pair à pair, sans passer par un serveur central qui servirait d'arbitre.

## 3. Version naïve

### 3.1. Pré-requis

Chaque joueur souhaitant participer doit stocker en local la liste des adresses IP des joueurs participants.

Sont laissées libres par le développeur chargé de l'implémentation :
- la logique de stockage des adresses IP sur les clients FLPR,
- la méthode de distribution des adresses IP.

## 3.2. Structure d'un message FLPR

Un message FLPR doit posséder les en-têtes suivants :
- `Ball ID` (16 bits), l'identifiant de la balle généré aléatoirement,
- `Bounces Number` (16 bits), un entier non signé donnant le nombre de rebonds initial de la balle, 
- `Bounces History` (taille variable), qui contient l'historique de tous les rebonds qu'a fait la balle, c'est-à-dire pour chacun d'entre-eux une ligne contenant l'adresse IP du récepteur.

Voici le schéma des en-têtes de message FLPR :

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |            Ball ID            |         Bounces Number        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~               Bounces History (taille variable)               ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
                  Format d'Entêtes d'un Message FLPR

### 3.3. Etapes du jeu

#### 3.3.1. Ecoute de messages FLPR

Cette étape est le point d'entrée du protocole et l'état initial de chaque joueur. Le joueur doit être constamment en position d'écoute de messages, et afin de ne pas interrompre cette écoute, toutes les sous-étapes qu'il lancera d'ici doivent être exécutées en asynchrone (dans un nouveau thread par exemple).

Si le joueur reçoit un message FLPR, il doit passer à l'étape :
- [Election du gagnant][3.3.6] si et seulement si le nombre de lignes de `Bounces History` est égal à la valeur de `Bounces Number` plus 2,
- [Vérification du message FLPR reçu][3.3.3] sinon,

#### 3.3.2. Lancement d'une nouvelle balle

Chaque joueur peut lancer cette étape quand il le souhaite, ce qui signifie qu'il peut y avoir plusieurs balles qui circulent en parallèle parmi les joueurs.

Le joueur doit :
- créer un message FLPR avec comme en-têtes :
  - un identifiant de balle généré aléatoirement dans `Ball ID`,
  - un nombre de rebonds initial positif ou nul dans `Bounces Number`.
  - une ligne dans `Bounces History` contenant une adresse IP qui n'est pas la sienne choisie aléatoirement dans la liste des joueurs participants,
- envoyer le message FLPR au joueur choisi précédemment.

#### 3.3.3. Vérification du message FLPR reçu

Le joueur doit passer à l'étape :
  - [Communication des scores][3.3.5] si et seulement si le nombre de lignes de `Bounces History` est égal à la valeur de `Bounces Number` plus 1,
  - [Renvoi d'une balle][3.3.4] sinon.

#### 3.3.4. Renvoi d'une balle

Le joueur doit :
- créer un nouveau message FLPR avec comme en-têtes :
  - la même valeur que celle qui était dans le message reçu dans `Ball ID`,
  - la même valeur que celle qui était dans le message reçu dans `Bounces Number`,
  - le même contenu que précédemment dans `Bounces History` mais avec une nouvelle ligne contenant une adresse IP qui n'est pas la sienne choisie aléatoirement dans la liste des joueurs participants,
- envoyer le message FLPR au joueur choisi précédemment.

#### 3.3.5. Communication du score

Le joueur doit :
- créer un nouveau message FLPR avec comme en-têtes :
  - la même valeur que celle qui était dans le message reçu dans `Ball ID`,
  - la même valeur que celle qui était dans le message reçu dans `Bounces Number`,
  - le même contenu que précédemment dans `Bounces History` mais avec une nouvelle ligne contenant la chaîne de caractères "STOP",
- envoyer le message FLPR en broadcast à toutes les adresses IP de la liste d'adresses des joueurs (y compris lui-même).

*Note : Sachant que le nombre de lignes de `Bounces History` est égal à la valeur de `Bounces Number` plus 2, les autres joueurs comprendront que le jeu entre en phase de décompte des points.*

#### 3.3.6. Election du gagnant

La/les adresse(s) IP apparaissant le plus souvent dans `Bounces History` est/sont celle(s) du/des joueur(s) qui a/ont gagné l'échange de balles.

## 3.4. Améliorations possibles

La version naïve du protocole FLPR laisse place à une faille assez importante, qui est qu'un joueur peut mentir sur l'historique des rebonds de la balle lorsqu'il la renvoie à un autre joueur. En effet, il peut la changer pour faire apparaître son adresse IP plus souvent afin de faire gonfler son propre score.

Ce problème peut être réglé en ajoutant au protocole FLPR un système de traçabilité des balles grâce à des signatures électroniques. Ces signatures permettent la non-répudiation des messages, au cas où leurs émetteurs venaient à nier le fait qu'il les aient envoyés, mais cela empêche aussi qu'un joueur mal intentionné altère l'historique des rebonds de la balle.