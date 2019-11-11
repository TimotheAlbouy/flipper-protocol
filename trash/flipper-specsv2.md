# Spécification Protocole Flipper

Haitam Sbaity & Timothé Albouy & Benjamin Rozenfeld
Ecole Nationale d'Ingénieurs de Bretagne Sud (ENSIBS)

## 1. Sommaire

- [1. Sommaire][1]
- [2. Introduction][2]
- [3. Version naïve][3]
  - [3.1. Pré-requis][3.1]
  - [3.2. Structure d'un message FLPR][3.2]
  - [3.3. Etapes du jeu][]
    - [3.3.1. Ecoute de messages FLPR][]
    - [3.3.2. Lancement d'une nouvelle balle][]
    - [3.3.3. Vérification du message FLPR reçu][]
    - [3.3.4. Renvoi de la balle][]
    - [3.3.5. Lancement du décompte des points][]
    - [3.3.6. Communication du score][]
    - [3.3.7. Ajout d'un score][]
    - [3.3.8. Election du gagnant][]
- [4. Version sécurisée][4]
  - [4.1. Pré-requis][4.1]
  - [4.2. Structure d'un message FLPR][4.2]
  - [4.3. Etapes du jeu][]
    - [4.3. Lancement d'une balle][4.3]
    - [4.4. Echange de balle][4.4]
    - [4.4.1. Vérification du message reçu][4.4.1]
    - [4.4.2. Création et envoi d'un nouveau message FLPR][4.4.2]
  - [4.5. Décompte des points][4.5]

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
- [Ajout d'un score][] si et seulement si la phase de jeu est **décompte des points**,
- [Communication du score][] si et seulement si la valeur de l'en-tête `Bounce Number` est 0,
- [Vérification du message FLPR reçu][] sinon.

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
  - [Lancement du décompte des points][] si et seulement si la valeur contenue dans `Bounce Number` est 1,
  - [Renvoi de la balle][] sinon.

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
- changer la phase stockée en local et associée au `Ball ID` du message reçu en **décompte de points**,
- créer un message FLPR avec comme en-têtes :
  - la même valeur que celle qui était dans le message reçu dans `Ball ID`,
  - son score stocké en local pour la valeur de `Ball ID` donnée dans `Bounce Number`.
- envoyer le message FLPR en broadcast à toutes les autres adresses IP de la liste d'adresses des joueurs.

#### 3.3.7. Ajout d'un score

Le joueur doit :
- changer le score associé au `Ball ID` du message reçu et au `Source Address` du packet IP enveloppant en la valeur de `Bounce Number` donné,
- passer à l'étape [Election du gagnant][] si et seulement si les scores de tous les joueurs pour l'identifiant `Ball ID` donné ont été enregistrés en local.

#### 3.3.8. Election du gagnant

Le joueur doit :
- trouver le score le plus haut qui a été enregistré en local pour pouvoir déduire l'adresse IP du gagnant de l'échange de balles associé au `Ball ID` correspondant,
- supprimer du stockage local l'enregistrement ayant pour clé le `Ball ID` correspondant.

## 4. Version sécurisée

La version naïve du protocole FLPR laisse place à un certain nombre de failles :
1) un joueur peut mentir sur son score lors de la phase de décompte,
2) un joueur peut ne pas décrémenter le nombre de rebonds restants quand il reçoit une balle,
3) l'ordre causal des messages n'est pas garanti : par exemple, lors du décompte des points, un joueur pourrait recevoir un message de communication de score avant le message de lancement du décompte, ce qui signifierait qu'il interpréterait incorrectement le premier comme un message d'envoi de balle,
4) un joueur peut envoyer une même balle valide à plusieurs joueurs en même temps,
5) deux joueurs peuvent génèrer deux balles avec le même identifiant,
6) un joueur ne renvoie simplement pas la balle après l'avoir interceptée alors q

Les 2 premier problèmes peuvent être réglés en ajoutant au protocole FLPR un système de traçabilité des balles grâce à des signatures électroniques. C'est ce que nous allons faire dans la nouvelle version du protocole FLPR donnée dans cette partie.

Le troisième problème, typique des réseaux distribués, pourrait être réglé avec un système de messages idempotents. Par exemple, tant que nous n'avons pas reçu la confirmation qu'un joueur a bien reçu et interprété le message qu'on lui a envoyé, nous continuons de lui en envoyer. En revanche, si le récepteur a bien reçu et interprété le message une fois, lui renvoyer des messages ne servira à rien. Cependant, nous n'allons pas régler ce problème dans la nouvelle version.

Les deux dernier problèmes pourraient altérer le score final pour un `Ball ID` donné si le décompte des points des deux balles se fait en même temps. Néanmoins, nous considérerons que le dédoublement d'une balle est accepté comme une règle valable durant le jeu.

### 4.1. Pré-requis

Chaque joueur souhaitant participer doit stocker en local :
- la liste des adresses IP et des clés publiques des joueurs participants,
- la liste, vide au départ, associant les identifiants de balle connus du joueur à la liste des messages FLPR envoyés durant l'échange de balle correspondant,
- leur propre clé privée.

Sont laissées libres par le développeur chargé de l'implémentation :
- la logique de stockage des adresses IP et des clés publiques sur les clients FLPR,
- la logique de stockage des identifiants de balle et des messages associés sur les clients FLPR,
- la logique de stockage de la clé privée sur les clients FLPR,
- le cryptosystème (RSA, ECC, ...) utilisé pour réaliser les signature électroniques,
- la fonction de hachage (SHA-2, SHA-3, ...) utilisée pour réaliser les signature électroniques,
- la méthode de distribution des adresses IP,
- la méthode de distribution des clés publiques.

La taille des clés publiques et des signatures dans les messages du protocole FLPR dépendra des mesures de sécurité et des paramètres choisis par le développeur.

### 4.2. Structure d'un message FLPR

Un message FLPR doit posséder les en-têtes suivants :
- `Ball ID` (16 bits), l'identifiant de la balle généré aléatoirement,
- `Bounce Number` (16 bits), un entier non signé donnant le nombre de rebonds restants de la balle, 
- `Source Public Key` (taille variable), la clé publique de l'envoyeur du message qui sert à vérifier la signature du message actuel,
- `Destination Public Key` (taille variable), la clé publique de celui qui reçoit le message,
- `Previous Signature` (taille variable), qui est la signature électronique du message reçu,
- `Current Signature` (taille variable), qui est le résultat du hachage de la concaténation des en-têtes précédents,
- `C` (1 bit) pour `Counting`, égal à :
  - 0 si le message est envoyé pendant la phase **échange de balles**,
  - 1 si le message est envoyé pendant la phase **décompte des points**.

Voici le nouveau schéma des en-têtes de message FLPR :

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |            Ball ID            |         Bounce Number         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~              Source Public Key (taille variable)              ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~            Destination Public Key (taille variable)           ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~              Previous Signature (taille variable)             ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~              Current Signature (taille variable)            +-+
    |                                                             |C|
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

                  Format d'Entêtes d'un Message FLPR

### 4.3. Etapes du jeu

#### 4.3.1. Ecoute de messages FLPR

Cette étape est le point d'entrée du protocole et l'état initial de chaque joueur. Le joueur doit être constamment en position d'écoute de messages, et afin de ne pas interrompre cette écoute, toutes les sous-étapes qu'il lancera d'ici doivent être exécutées en asynchrone (dans un nouveau thread par exemple).

Si le joueur reçoit un message FLPR, il doit passer à l'étape :
- [Vérification du message FLPR de décompte des points][] si et seulement si la valeur de l'en-tête `C` est 1,
- [Vérification du message FLPR de renvoi de balle][] sinon.

#### 4.3.2. Lancement d'une nouvelle balle

Chaque joueur peut lancer cette étape quand il le souhaite, ce qui signifie qu'il peut y avoir plusieurs balles qui circulent en parallèle parmi les joueurs.

Le joueur doit :
- créer un nouveau message FLPR avec comme en-têtes :
  - un identifiant de balle généré aléatoirement dans `Ball ID`,
  - un nombre de rebonds initial positif ou nul dans `Bounce Number`.
  - sa propre clé publique dans `Source Public Key`,
  - une clé publique choisie aléatoirement dans la liste des joueurs participants dans `Destination Public Key`,
  - que des 0 dans `Previous Signature` (car il n'y a pas de message précédent),
  - le hash de tous les en-têtes précédents, le tout encrypté avec la clé privée du joueur dans `Current Signature`,
  - 0 dans `C`,
- envoyer le message FLPR au joueur choisi précédemment.

##### 4.3.3. Vérification du message FLPR de renvoi de balle

Le joueur doit :
- créer un nouvel enregistrement, si et seulement si le `Ball ID` n'est pas connu dans le stockage local, contenant :
  - en clé : `Ball ID` comme identifiant de balle,
  - en valeur : une liste vide comme liste des messages FLPR envoyés durant l'échange de balle correspondant,
- ignorer le message reçu (et donc arrêter l'exécution de cette étape) si :
  - la clé publique de l'envoyeur est incorrecte : la valeur contenue dans `Source Public Key` n'est pas égale à la clé publique stockée en local qui correspond au `Source address` du packet IP enveloppant,
  - la clé publique du receveur est incorrecte : la valeur contenue dans `Destination Public Key` n'est pas égale à la clé publique du joueur qui fait la vérification,
  - la signature du message actuel n'est pas valide : la valeur contenue dans `Current Signature`, une fois décryptée avec `Source Public Key`, n'est pas égale au hash des 5 premiers en-têtes.
- stocker le message entier en local dans la liste des des messages associée au `Ball ID` donné pour s'en resservir lors de la phase de décompte des points,
- passer à l'étape [Lancement du décompte des points][] si et seulement si la valeur contenue dans `Bounce Number` est 0,
- sinon, passer à l'étape [Renvoi d'une balle][].

*Note : Lorsque les informations du messages se révèlent incorrectes, la meilleure option pour le récepteur du message est de ne rien faire. Il ne peut pas prévenir les autres joueurs de la tentative de triche en leur envoyant le message, car il ne peut pas prouver qu'il n'accuse pas injustement l'envoyeur :*
- *en créant un message de toute pièce si la signature est invalide, ou*
- *en interceptant un message qu'il n'est pas censé recevoir (Man in the Middle) si les clés publiques sont incorrectes.*

#### 4.3.4. Renvoi d'une balle

Le joueur doit :
- créer un nouveau message FLPR avec comme en-têtes :
  - la même valeur que celle qui était dans le message reçu dans `Ball ID`,
  - la même valeur que celle qui était dans le message reçu dans `Bounce Number` mais décrémentée de 1,
  - sa propre clé publique dans `Source Public Key`,
  - une clé publique choisie aléatoirement dans la liste de joueurs dans `Destination Public Key`,
  - la valeur qui était dans le message reçu à l'en-tête `Current Signature` dans `Previous Signature`,
  - le hash de tous les en-têtes précédents, le tout encrypté avec la clé privée du joueur dans `Current Signature`,
  - 0 dans `C`,
- envoyer le message FLPR au joueur choisi précédemment.

#### 4.3.5. Lancement du décompte des points

Le joueur doit :
- créer un message FLPR semblable au dernier qu'il a reçu, à l'exception que la valeur de `C` est 1,
- envoyer le message FLPR en broadcast à toutes les adresses IP de la liste d'adresses des joueurs (y compris lui-même).

*Note : Sachant que la valeur de `C` est 1, les autres joueurs comprendront que le jeu entre en phase de **décompte des points**.*

#### 4.3.6. Vérification du message FLPR de décompte des points

Le joueur doit :
- ignorer le message reçu (et donc arrêter l'exécution de cette étape) si :
  - la clé publique de l'envoyeur est inconnue : la valeur contenue dans `Source Public Key` n'est pas dans la liste stockée en local des clés publiques des joueurs,
  - la clé publique du receveur est inconnue : la valeur contenue dans `Destination Public Key` n'est pas dans la liste stockée en local des clés publiques des joueurs,
  - la signature du message actuel n'est pas valide : la valeur contenue dans `Current Signature`, une fois décryptée avec `Source Public Key`, n'est pas égale au hash des 5 premiers en-têtes.
- stocker le message entier en local dans la liste des des messages associée au `Ball ID` donné,
- passer à l'étape [Election du gagnant][] si et seulement si la valeur contenue dans `Previous Signature` n'est constituée que de 0,
- passer à l'étape [Envoi d'un message FLPR de décompte des points][] si et seulement si la valeur contenue dans `Previous Signature` correspond à une `Current Signature` stockée en local dans la liste des message associée au `Ball ID`.

#### 4.3.7. Envoi d'un message FLPR de décompte des points

Le joueur doit :
- retrouver le message incrémenter de 1 son propre score stocké en local et associé à l'identifiant contenu dans `Ball ID`,
- créer un message FLPR semblable au dernier qu'il a reçu, à l'exception que la valeur de `C` est 1,
- envoyer le message FLPR en broadcast à toutes les adresses IP de la liste d'adresses des joueurs (y compris lui-même).

// A FAIRE

// TODO

// /!\

Le joueur doit :
- créer un message FLPR avec comme en-têtes :
  - la même valeur que celle qui était dans le message reçu dans `Ball ID`,
  - son score stocké en local pour la valeur de `Ball ID` donnée dans `Bounce Number`.
- envoyer le message FLPR en broadcast à toutes les autres adresses IP de la liste d'adresses des joueurs.

#### 3.3.7. Ajout d'un score

Le joueur doit :
- changer le score associé au `Ball ID` du message reçu et au `Source Address` du packet IP enveloppant en la valeur de `Bounce Number` donné,
- passer à l'étape [Election du gagnant][] si et seulement si les scores de tous les joueurs pour l'identifiant `Ball ID` donné ont été enregistrés en local.

#### 3.3.8. Election du gagnant

Cette étape ne consiste pas à envoyer de message, mais juste à trouver le score le plus haut qui a été enregistré en local pour pouvoir déduire l'adresse IP du joueur qui a gagné l'échange de balles.













La structure de données formée par les messages rappelle une liste chaînée de Merkle ou une chaîne de blocs, où chaque item contient le hash de son prédécesseur. La spécificité supplémentaire est que ce hash est signé cryptographiquement, permettant ainsi la non-répudiation du message, au cas où l'émetteur venait à nier le fait qu'il l'ait envoyé.


Lorsqu'un joueur atteint le nombre de rebonds restants 0, il envoie le message qu'il a reçu en broadcast à tous les autres joueurs pour lancer prouver qu'i




Ce genre de triche n'est pas puni par le protocole, mais il revient plutôt aux joueurs de boycotter un participant dans les parties suivantes, voire de se mettre d'accord pour le bannir de l'éventail d'adresses, si celui-ci tente de frauder.

On considère qu'un joueur a objectivement gagné lorsque plus de la moitié des joueurs s'accordent à dire que c'est le cas.


Si un joueur reçoit un message qui n'a pas été signé par une clé appartenant au , il ne doit pas renvoyer la balle. On considère qu'il y a triche 
ne respecte pas ces conditions


Cependant, la méthode préconisée 

[1]: #1-sommaire
[2]: #2-introduction
[3]: #3-version-naïve
[3.1]: #31-pré-requis
[3.2]: #32-structure-dun-message-flpr
[3.3]: #33-lancement-dune-balle
[3.4]: #34-echange-de-la-balle
[3.4.1]: #341-vérification-du-message-reçu
[3.4.2]: #342-création-et-envoi-dun-nouveau-message-flpr
[3.5]: #35-décompte-des-points
[3.5.1]: #351-lancement-du-décompte
[3.5.2]: #352-communication-des-scores
[4]: #4-version-sécurisée
[4.1]: #41-pré-requis
[4.2]: #42-structure-dun-message-flpr
[4.3]: #43-lancement-dune-balle
[4.4]: #44-echange-de-balle
[4.4.1]: #441-vérification-du-message-reçu
[4.4.2]: #442-création-et-envoi-dun-nouveau-message-flpr
[4.5]: #45-décompte-des-points

Si l'une d'entre elle n'a pas encore communiqué son score au joueur, c'est probablement dû au fait que l'autre joueur n'a pas encore reçu le message FLPR de lancement du décompte et donc qu'il interprète les messages de communication du score comme des messages d'envoi de balle. Dans ce cas-là, le premier joueur doit continuer à envoyer le message FLPR à l'adresse IP qui n'a pas encore donné son score.




    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |          Source Port          |       Destination Port        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Acknowledgment Number                      |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Data |           |U|A|P|R|S|F|                               |
   | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
   |       |           |G|K|H|T|N|N|                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Checksum            |         Urgent Pointer        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                             data                              |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

                            TCP Header Format