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
    - [3.3.4. Renvoi de la balle][3.3.4]
    - [3.3.5. Lancement du décompte des points][3.3.5]
    - [3.3.6. Communication du score][3.3.6]
    - [3.3.7. Ajout d'un score][3.3.7]
    - [3.3.8. Election du gagnant][3.3.8]
  - [3.4. Améliorations possibles][3.4]
- [4. Version sécurisée][4]
  - [4.1. Pré-requis][4.1]
  - [4.2. Structure d'un message FLPR][4.2]
  - [4.3. Etapes du jeu][4.3]
    - [4.3.1. Ecoute de messages FLPR][4.3.1]
    - [4.3.2. Lancement d'une nouvelle balle][4.3.2]
    - [4.3.3. Vérification d'un message FLPR reçu][4.3.3]
    - [4.3.4. Renvoi d'une balle][4.3.4]
    - [4.3.5. Election du gagnant][4.3.5]
  - [4.4. Améliorations possibles][4.4]

## 2. Introduction

Le protocole Flipper (FLPR) est un protocole de couche applicative basé sur l'architecture TCP/IP (pour ne pas avoir à se soucier des paquets perdus), c'est-à-dire que chaque message FLPR sera encapsulé dans un segment TCP, lui-même encapsulé dans un packet IPv4. FLPR permet à plusieurs ordinateurs d'un même réseau informatique de jouer à une simulation d'envoi de balles, un message symbolisant un envoi de balle entre deux machines. Une fois interceptée par un joueur, une balle doit être renvoyée à un autre joueur et ce jusqu'à ce que le nombre de rebonds restants de la balle s'annule. FLPR fonctionne totalement en pair à pair, sans passer par un serveur central qui servirait d'arbitre.

## 3. Version naïve

### 3.1. Pré-requis

Chaque joueur souhaitant participer doit stocker en local :
- la liste des adresses IP des joueurs participants,
- la liste, vide au départ, associant les identifiants de balle connus du joueur au score de chacun des joueurs et à la phase de jeu courante (**échange de balle** ou **décompte des points**).

Sont laissées libres par le développeur chargé de l'implémentation :
- la logique de stockage des adresses IP sur les clients FLPR,
- la logique de stockage des identifiants de balle et des scores et phases associés sur les clients FLPR,
- la méthode de distribution des adresses IP.

## 3.2. Structure d'un message FLPR

Un message FLPR doit posséder les en-têtes suivants :
- `Ball ID` (16 bits), l'identifiant de la balle généré aléatoirement,
- `Bounce Number` (16 bits), un entier non signé donnant :
  - le nombre de rebonds restants de la balle si le message est envoyé pendant la phase **échange de balle**, 
  - le score d'un joueur si le message est envoyé pendant la phase **décompte des points**.

Voici le schéma des en-têtes de message FLPR :

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |            Ball ID            |         Bounce Number         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
                  Format d'Entêtes d'un Message FLPR

### 3.3. Etapes du jeu

#### 3.3.1. Ecoute de messages FLPR

Cette étape est le point d'entrée du protocole et l'état initial de chaque joueur. Le joueur doit être constamment en position d'écoute de messages, et afin de ne pas interrompre cette écoute, toutes les sous-étapes qu'il lancera d'ici doivent être exécutées en asynchrone (dans un nouveau thread par exemple).

Si le joueur reçoit un message FLPR, il doit passer à l'étape :
- [Ajout d'un score][3.3.7] si et seulement si la phase de jeu est **décompte des points**,
- [Communication du score][3.3.6] si et seulement si la valeur de l'en-tête `Bounce Number` est 0,
- [Vérification du message FLPR reçu][3.3.3] sinon.

#### 3.3.2. Lancement d'une nouvelle balle

Chaque joueur peut lancer cette étape quand il le souhaite, ce qui signifie qu'il peut y avoir plusieurs balles qui circulent en parallèle parmi les joueurs.

Le joueur doit :
- créer un message FLPR avec comme en-têtes :
  - un identifiant de balle généré aléatoirement dans `Ball ID`,
  - un nombre de rebonds initial positif ou nul dans `Bounce Number`.
- envoyer le message FLPR à une adresse IP qui n'est pas la sienne choisie aléatoirement dans la liste d'adresses des joueurs.

#### 3.3.3. Vérification du message FLPR reçu

Le joueur doit :
- créer un nouvel enregistrement, si et seulement si le `Ball ID` n'est pas connu dans le stockage local, contenant :
  - en clé : `Ball ID` comme identifiant de balle,
  - en valeur :
    - une liste vide comme liste des scores de chacun des joueurs de la liste d'adresses IP,
    - **échange de balle** comme phase de jeu,
- incrémenter de 1 son propre score stocké en local et associé à l'identifiant contenu dans `Ball ID`,
- passer à l'étape :
  - [Lancement du décompte des points][3.3.5] si et seulement si la valeur contenue dans `Bounce Number` est 1,
  - [Renvoi de la balle][3.3.4] sinon.

#### 3.3.4. Renvoi de la balle

Le joueur doit :
- créer un nouveau message FLPR avec comme en-têtes :
  - la même valeur que celle qui était dans le message reçu dans `Ball ID`,
  - la même valeur que celle qui était dans le message reçu dans `Bounce Number` mais décrémentée de 1,
- envoyer le message FLPR à une adresse IP qui n'est pas la sienne choisie aléatoirement dans la liste d'adresses des joueurs.

#### 3.3.5 Lancement du décompte des points

Le joueur doit :
- créer un message FLPR avec comme en-têtes :
  - la même valeur que celle qui était dans le dernier message dans `Ball ID`,
  - 0 dans `Bounce Number`.
- envoyer le message FLPR en broadcast à toutes les adresses IP de la liste d'adresses des joueurs (y compris lui-même).

*Note : Sachant que la valeur de `Bounce Number` est 0, les autres joueurs comprendront que le jeu entre en phase de **décompte des points**.*

#### 3.3.6. Communication du score

Le joueur doit :
- changer la phase stockée en local et associée au `Ball ID` du message reçu en **décompte des points**,
- créer un message FLPR avec comme en-têtes :
  - la même valeur que celle qui était dans le message reçu dans `Ball ID`,
  - son score stocké en local pour la valeur de `Ball ID` donnée dans `Bounce Number`.
- envoyer le message FLPR en broadcast à toutes les autres adresses IP de la liste d'adresses des joueurs.

#### 3.3.7. Ajout d'un score

Le joueur doit :
- changer le score associé au `Ball ID` du message reçu et au `Source Address` du packet IP enveloppant en la valeur de `Bounce Number` donné,
- passer à l'étape [Election du gagnant][3.3.8] si et seulement si les scores de tous les joueurs pour l'identifiant `Ball ID` donné ont été enregistrés en local.

#### 3.3.8. Election du gagnant

L'/Les adresse(s) IP associée(s) au score le plus haut qui a été enregistré en local pour le `Ball ID` donné est/sont celle(s) du/des gagnant(s) de l'échange de balle.

Ensuite, le joueur doit supprimer du stockage local l'enregistrement ayant pour clé le `Ball ID` correspondant.

## 3.4. Améliorations possibles

La version naïve du protocole FLPR laisse place à un certain nombre de failles :
1) un joueur peut mentir sur son score lors de la phase de décompte,
2) un joueur peut ne pas décrémenter le nombre de rebonds restants quand il reçoit une balle,
3) lors du décompte des points, un joueur pourrait recevoir un message de communication de score avant le message de lancement du décompte, ce qui signifierait qu'il interpréterait incorrectement le premier comme un message d'envoi de balle (pas de garantie de l'ordre causal).

Les problèmes 1) et 2) peuvent être réglés en ajoutant au protocole FLPR un système de traçabilité des balles grâce à des signatures électroniques. Ces signatures permettent la non-répudiation des messages, au cas où leurs émetteurs venaient à nier le fait qu'il les aient envoyés.

Le problème 3) peut être réglé en donnant une indication explicite (qui ne dépende pas du moment de réception du message) que l'on passe en phase de **décompte des points**, par exemple en ajoutant un en-tête d'un seul bit disant si c'est un message de lancement de décompte des points ou non.

## 4. Version sécurisée

### 4.1. Pré-requis

Chaque joueur souhaitant participer doit stocker en local :
- la liste des adresses IP et des clés publiques des joueurs participants,
- leur propre clé privée.

Sont laissées libres par le développeur chargé de l'implémentation :
- la logique de stockage des adresses IP et des clés publiques sur les clients FLPR,
- la logique de stockage de la clé privée sur les clients FLPR,
- le cryptosystème (RSA, ECC, ...) utilisé pour réaliser les signature électroniques,
- la fonction de hachage (SHA-2, SHA-3, ...) utilisée pour réaliser les signature électroniques,
- la méthode de distribution des adresses IP,
- la méthode de distribution des clés publiques.

La taille des clés publiques et des signatures dans les messages du protocole FLPR dépendra des mesures de sécurité et des paramètres choisis par le développeur.

### 4.2. Structure d'un message FLPR

Un message FLPR doit posséder les en-têtes suivants :
- `Ball ID` (16 bits), l'identifiant de la balle généré aléatoirement,
- `Bounces Number` (16 bits), un entier non signé donnant le nombre de rebonds initial de la balle, 
- `Creator Public Key` (taille variable), la clé publique du créateur de la balle qui sert à vérifier la première signature électronique,
- `Bounces History` (taille variable), qui contient l'historique de tous les rebonds qu'a fait la balle, c'est-à-dire pour chacun d'entre-eux une ligne contenant la clé publique du récepteur et la signature électronique de toutes les informations précédentes du message FLPR (y compris les clé publiques et signatures précédentes).

Voici le schéma des en-têtes de message FLPR :

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |            Ball ID            |         Bounces Number        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~              Creator Public Key (taille variable)             ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~               Bounces History (taille variable)               ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

                  Format d'Entêtes d'un Message FLPR

### 4.3. Etapes du jeu

#### 4.3.1. Ecoute de messages FLPR

Cette étape est le point d'entrée du protocole et l'état initial de chaque joueur. Le joueur doit être constamment en position d'écoute de messages, et afin de ne pas interrompre cette écoute, toutes les sous-étapes qu'il lancera d'ici doivent être exécutées en asynchrone (dans un nouveau thread par exemple).

Si le joueur reçoit un message FLPR, il doit passer à l'étape :
- [Vérification du message FLPR de communication des scores][] si et seulement si le nombre de lignes de `Bounces History` est égal à la valeur de `Bounces Number` plus 1,
- [Vérification du message FLPR de renvoi de balle][] sinon.

#### 4.3.2. Lancement d'une nouvelle balle

Chaque joueur peut lancer cette étape quand il le souhaite, ce qui signifie qu'il peut y avoir plusieurs balles qui circulent en parallèle parmi les joueurs.

Le joueur doit :
- créer un nouveau message FLPR avec comme en-têtes :
  - un identifiant de balle généré aléatoirement dans `Ball ID`,
  - un nombre de rebonds initial positif ou nul dans `Bounces Number`.
  - sa propre clé publique dans `Creator Public Key`,
  - une ligne dans `Bounces History` contenant :
    - une clé publique choisie aléatoirement dans la liste des joueurs participants,
    - le hash de tous les bits précédents dans le message FLPR, le tout encrypté avec la clé privée du joueur,
- envoyer le message FLPR au joueur choisi précédemment.

#### 4.3.3. Vérification du message FLPR reçu

Le joueur doit :
- ignorer le message reçu (et donc arrêter l'exécution de cette étape) si :
  - la clé publique du receveur est incorrecte : la valeur contenue dans `Destination Public Key` n'est pas égale à la clé publique du joueur qui fait la vérification,
  - la vérification des signatures échoue : la signature de chaque ligne de `Bounces History`, une fois décryptée avec la clé publique de l'envoyeur (i.e. `Creator Public Key` s'il s'agit de la première ligne, ou la clé publique de la ligne précédente sinon), doit être égale au hash de tous les bits la précédant dans le message FLPR,
  - la balle a surpassé la limite de rebonds : le nombre de lignes de `Bounces History` est supérieur à la valeur de `Bounces Number` plus 1,
- passer à l'étape [Communication des scores][] si et seulement si le nombre de lignes de `Bounces History` est égal à la valeur contenue dans `Bounces Number` plus 1,
- sinon, passer à l'étape [Renvoi d'une balle][].

*Note : Lorsque les informations du messages se révèlent incorrectes, la meilleure option pour le récepteur du message est de ne rien faire. Il ne peut pas prévenir les autres joueurs de la tentative de triche en leur envoyant le message, car il ne peut pas prouver qu'il n'accuse pas injustement l'envoyeur :*
- *en créant un message de toute pièce si une des signatures est invalide, ou*
- *en interceptant un message qu'il n'est pas censé recevoir (Man in the Middle) si une des clés publiques est incorrecte.*

#### 4.3.4. Renvoi d'une balle

Le joueur doit :
- créer un nouveau message FLPR avec comme en-têtes :
  - la même valeur que celle qui était dans le message reçu dans `Ball ID`,
  - la même valeur que celle qui était dans le message reçu dans `Bounces Number`,
  - le même contenu que précédemment dans `Bounces History` mais avec une nouvelle ligne contenant :
    - une clé publique choisie aléatoirement dans la liste des joueurs participants,
    - le hash de tous les bits précédents dans le message FLPR, le tout encrypté avec la clé privée du joueur,
- envoyer le message FLPR au joueur choisi précédemment.

#### 4.3.5. Communication des scores

Le joueur doit envoyer exactement le même message FLPR qu'il a reçu en broadcast à toutes les adresses IP de la liste d'adresses des joueurs (y compris lui-même).

*Note : Sachant que le nombre de lignes de `Bounces History` est égal à la valeur de `Bounces Number` plus 1, les autres joueurs comprendront que le jeu entre en phase de **décompte des points**.*

#### 4.3.6. Election du gagnant

Le joueur doit ignorer le message reçu (et donc arrêter l'exécution de cette étape) si et seulement si la vérification des signatures échoue : la signature de chaque ligne de `Bounces History`, une fois décryptée avec la clé publique de l'envoyeur (i.e. `Creator Public Key` s'il s'agit de la première ligne, ou la clé publique de la ligne précédente sinon), doit être égale au hash de tous les bits la précédant dans le message FLPR.

La/les clé(s) publique(s) apparaissant le plus souvent dans `Bounces History` est/sont celle(s) du/des joueur(s) qui a/ont gagné l'échange de balles.

## 4.4. Améliorations possibles

La version sécurisée du protocole FLPR possède toujours certains problèmes :
1) un joueur peut envoyer une même balle valide à plusieurs joueurs en même temps,
2) deux joueurs peuvent génèrer deux balles avec le même identifiant,
3) un joueur peut ne pas respecter le protocole (envoyer des messages invalides ou ne pas en envoyer du tout alors que la spécification le demande),
4) certains joueurs complices peuvent se renvoyer la balle qu'entre eux une fois qu'ils l'ont réceptionnée pour augmenter que leurs scores et pas ceux des autres.

Les problèmes 1) et 2) pourraient altérer le score final pour un `Ball ID` donné si le décompte des points des deux balles se fait en même temps. Néanmoins, ce problème n'est pas résoluble trivialement, donc nous considérerons que le dédoublement d'une balle est accepté comme une règle valable du jeu.

Le problème 3) est inhérent aux réseaux suivant le zero-trust et ce genre de triche n'est pas puni par le protocole, cependant il revient plutôt aux joueurs de boycotter (voire bannir de la liste d'adresses) un participant s'ils détectent que celui-ci tente de frauder. Un joueur peut arrêter d'envoyer la balle à un autre joueur s'il constate que celui-ci lui a envoyé des messages incorrects par exemple. Les implémentations du protocole peuvent définir une surcouche à celui qui consisterait à envoyer des messages aux autres joueurs pour dénoncer un participant particulier qui ne suivrait pas le protocole. 

Le problème 4) pourrait être mitigé si les cycles de la balle de moins de n/2 de longueur (avec n le nombre total de joueurs) sont interdits par le protocole. Cela signifie que si une balle qu'un joueur a envoyée lui revient après seulement 4 rebonds (s'il y a 10 joueurs) alors on ne doit pas effectuer de décompte des points sur celle-ci. Tricher nécessiterait théoriquement aux attaquants de corrompre plus de la moitié des joueurs.

[1]: #1-sommaire
[2]: #2-introduction
[3]: #3-version-naïve
[3.1]: #31-pré-requis
[3.2]: #32-structure-dun-message-flpr
[3.3]: #33-etapes-du-jeu
[3.3.1]: #331-ecoute-de-messages-flpr
[3.3.2]: #332-lancement-dune-nouvelle-balle
[3.3.3]: #333-vérification-du-message-flpr-reçu
[3.3.4]: #334-renvoi-de-la-balle
[3.3.5]: #335-lancement-du-décompte-des-points
[3.3.6]: #336-communication-du-score
[3.3.7]: #337-ajout-dun-score
[3.3.8]: #338-election-du-gagnant
[3.4]: #34-améliorations-possibles
[4]: #4-version-sécurisée
[4.1]: #41-pré-requis
[4.2]: #42-structure-dun-message-flpr
[4.3]: #43-etapes-du-jeu
[4.3.1]: #431-ecoute-de-messages-flpr
[4.3.2]: #432-lancement-dune-nouvelle-balle
[4.3.3]: #433-vérification-du-message-flpr-reçu
[4.3.4]: #434-renvoi-dune-balle
[4.3.5]: #435-election-du-gagnant
[4.4]: #44-améliorations-possibles