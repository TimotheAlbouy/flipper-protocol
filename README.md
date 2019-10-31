# Spécification Protocole Flipper

Haitam Sbaity & Timothé Albouy & Benjamin Rozenfeld
Ecole Nationale d'Ingénieurs de Bretagne Sud (ENSIBS)

## 1. Sommaire

- [1. Sommaire][1]
- [2. Introduction][2]
- [3. Version naïve][3]
  - [3.1. Pré-requis][3.1]
  - [3.2. Structure d'un message FLPR][3.2]
  - [3.3. Lancement d'une balle][3.3]
  - [3.4. Echange de la balle][3.4]
    - [3.4.1. Vérification de la balle][3.4.1]
    - [3.4.2. Création et envoi d'un nouveau message FLPR][3.4.2]
  - [3.5. Décompte des points][3.5]
    - [3.5.1. Lancement du décompte][3.5.1]
    - [3.5.2. Communication des scores][3.5.2]
- [4. Version sécurisée][4]
  - [4.1. Pré-requis][4.1]
  - [4.2. Structure d'un message FLPR][4.2]
  - [4.3. Lancement d'une balle][4.3]
  - [4.4. Echange de balle][4.4]
    - [4.4.1. Vérification de la balle][4.4.1]
    - [4.4.2. Création du nouveau message FLPR][4.4.2]
  - [4.5. Décompte des points][4.5]

## 2. Introduction

Le protocole Flipper (FLPR) est un protocole de couche applicative basé sur l'architecture TCP/IP (pour ne pas avoir à se soucier des paquets perdus), c'est-à-dire que chaque message FLPR sera encapsulé dans un segment TCP, lui-même encapsulé dans un packet IPv4. FLPR permet à plusieurs ordinateurs d'un même réseau informatique de jouer à une simulation d'envoi de balles, un message symbolisant un envoi de balle entre deux machines. FLPR fonctionne totalement en pair à pair, sans passer par un serveur central qui servirait d'arbitre.

## 3. Version naïve

### 3.1. Pré-requis

Les joueurs souhaitant participer doivent stocker en local :
- l'éventail des adresses IP des joueurs participants,
- leur propre score qui est initialisé à 0.

Sont laissées libres par le développeur chargé de l'implémentation :
- la logique de stockage des adresses IP sur les clients FLPR,
- la logique de stockage des scores sur les clients FLPR,
- la méthode de distribution des adresses IP.

L'état initial du jeu est l'étape [3.3. Lancement d'une balle][3.3].

## 3.2. Structure d'un message FLPR

Un message FLPR doit posséder les en-têtes suivants :
- `Ball ID` (16 bits), l'identifiant de la balle généré lors de l'étape [3.3. Lancement d'une balle][3.3],
- `Bounce Number` (16 bits), un entier non signé donnant :
  - le nombre de rebonds restants de la balle lors des étapes [3.3. Lancement d'une balle][3.3] et [3.4. Echange de la balle][3.4], 
  - le score d'un joueur lors de l'étape [3.5. Décompte des points][3.5].

Voici nouveau schéma des en-têtes de message FLPR :

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |            Ball ID            |         Bounce Number         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
                  Format d'Entêtes d'un Message FLPR

### 3.3. Lancement d'une balle

Tous les joueurs participants commencent en position d'écoute de messages.

N'importe quel joueur peut envoyer un message de lancement de balle totalement spontanément, il doit alors créer un message FLPR avec comme en-têtes :
- un identifiant de balle généré aléatoirement dans `Ball ID`,
- un nombre de rebonds initial positif ou nul dans `Bounce Number`.

Ensuite, les actions qui doivent se réaliser sont :
- le joueur envoie le message FLPR à une adresse IP qui n'est pas la sienne choisie aléatoirement dans l'éventail d'adresses,
- le jeu passe à l'étape [3.4. Echange de la balle][3.4].

### 3.4. Echange de la balle

Dès qu'un joueur réceptionne un message FLPR d'envoi de balle (`Bounce Number` supérieur ou égal à 1), il doit passer à l'étape de [3.4.1. Vérification de la balle][3.4.1].

#### 3.4.1. Vérification de la balle

Les actions qui doivent se réaliser sont :
- le joueur incrémente son propre score stocké en local de 1,
- le jeu passe à l'étape [3.5. Décompte des points][3.5] si la valeur contenue dans `Nombre de rebonds` est 1,
- sinon, le joueur passe à l'étape [3.4.2. Création d'un nouveau message][3.4.2].

#### 3.4.2. Création et envoi d'un nouveau message FLPR

Le joueur doit créer un nouveau message FLPR avec comme en-têtes :
- la même valeur que celle qui était dans le message précédent dans `Ball ID`,
- la valeur qui était dans le message précédent décrémentée de 1 dans `Bounce Number`.

Ensuite, le joueur doit :
- envoyer le message FLPR à une adresse IP qui n'est pas la sienne choisie aléatoirement dans l'éventail d'adresses,
- revenir en position d'écoute.

### 3.5. Décompte des points

Le joueur qui a reçu le dernier message d'envoi (`Bounce Number` à 1) pour un `Ball ID` donné doit passer à l'étape [3.5.1. Lancement du décompte][3.5.1].

Dès qu'un joueur réceptionne un message FLPR de lancement de décompte (`Bounce Number` à 0), il doit passer à l'étape de [3.5.2. Communication des scores][3.5.2].

#### 3.5.1. Lancement du décompte

Le joueur doit créer un message FLPR avec comme en-têtes :
- la même valeur que celle qui était dans le dernier message dans `Ball ID`,
- 0 dans `Bounce Number`.

Ensuite, le joueur doit envoyer le message FLPR en broadcast à toutes les adresses IP de l'éventail. Sachant que la valeur de `Bounce Number` est 0, les autres joueurs comprendront que le jeu entre en phase de décompte des points.

#### 3.5.2. Communication des scores

Le joueur doit créer un message FLPR avec comme en-têtes :
- la même valeur que celle qui était dans le message reçu dans `Ball ID`,
- son score stocké en local pour la valeur de `Ball ID` donnée dans `Bounce Number`.

Enfin, le joueur doit envoyer le message FLPR en broadcast à toutes les autres adresses IP de l'éventail.

En parallèle, le joueur reçoit les message FLPR de communication du score des autres adresses IP de l'éventail. Si l'une d'entre elle n'a pas encore communiqué son score au joueur, c'est probablement dû au fait que l'autre joueur n'a pas encore reçu le message FLPR de lancement du décompte et donc qu'il interprète les messages de communication du score comme des messages d'envoi de balle. Dans ce cas-là, le premier joueur doit continuer à envoyer le message FLPR à l'adresse IP qui n'a pas encore donné son score.

Une fois que tous les participants connaissent tous les scores, le (ou les) joueur(s) qui possède(nt) le plus haut score sont considérés comme vainqueurs pour le `Ball ID` donné.

## 4. Version sécurisée

La version naïve du protocole FLPR laisse place à un certain nombre de failles :
- un joueur peut mentir sur son score lors de la phase de décompte,
- un joueur peut ne pas décrémenter le nombre de rebonds restants quand il reçoit une balle,
- un joueur peut envoyer une même balle valide à plusieurs joueurs en même temps.

Pour résoudre une partie de ces problèmes, on ajoute au protocole un système de traçabilité de la balle grâce à des signatures électroniques. La nouvelle version du protocole FLPR est donnée dans cette partie.

### 4.1. Pré-requis

Les joueurs souhaitant participer doivent stocker en local :
- l'éventail des adresses IP des joueurs participants,
- la clé publique associée à chaque adresse IP de l'éventail d'adresses,
- leur propre clé privée.

Sont laissés libres au développeur chargé de l'implémentation :
- la logique de stockage des adresses IP sur les clients FLPR,
- la logique de stockage des clés publiques sur les clients FLPR,
- la logique de stockage de la clé privée sur les clients FLPR,
- le cryptosystème (RSA, ECC, ...) utilisé pour réaliser les signature électroniques,
- la fonction de hachage (SHA-2, SHA-3, ...) utilisée pour réaliser les signature électroniques,
- la méthode de distribution des adresses IP,
- la méthode de distribution des clés publiques.

La taille des clés publiques et des signatures dans les messages du protocole FLPR dépendra des mesures de sécurité et des paramètres choisis par le développeur.

### 4.2. Structure d'un message FLPR

Un message FLPR doit posséder les en-têtes suivants :
- `Ball ID` (16 bits), l'identifiant de la balle généré lors de l'étape [4.3. Lancement d'une balle][4.3],
- `Bounce Number` (16 bits), un entier non signé donnant le nombre de rebonds restants de la balle, 
- `Source Public Key` (taille variable), la clé publique de l'envoyeur du message qui sert à vérifier la signature du message actuel.
- `Destination Public Key` (taille variable), la clé publique de celui qui reçoit le message.
- `Previous Signature` (taille variable), qui est la signature électronique du message reçu.
- `Current Signature` (taille variable), qui est le résultat du hachage de la concaténation des en-têtes précédents,
- `C` (1 bit) pour 'Counting', si cet en-tête est égal à 0, alors le message est envoyé durant la phase d'échange de balles, sinon il est envoyé durant la phase de décompte des balles.

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

### 4.3. Lancement d'une balle

Tout joueur peut générer une balle avec un identifiant et un nombre de rebonds initial, il peut donc y avoir plusieurs balles qui circulent en parallèle parmi les joueurs. Deux personnes qui génèreraient deux balles avec le même identifiant ne créera pas d'erreur, puisque les joueurs renverront la balle et décompteront les points peu importe l'identifiant. Les fraudes possibles n'impliquent pas l'identifiant de balle.

Le joueur qui lance la balle au départ doit créer un message FP avec comme en-têtes :
- un identifiant de balle généré aléatoirement dans `Ball ID`,
- un nombre de rebonds initial positif ou nul dans `Bounce Number`.
- sa propre clé publique dans `Clé publique de l'envoyeur`,
- la clé publique d'un joueur choisi aléatoirement dans l'éventail d'adresses dans `Clé publique du receveur`,
- que des 0 dans `Signature du message précédent` (car il n'y a pas de message précédent),
- la signature avec sa clé privée de toutes les informations qui ont été entrées jusque-là dans `Signature du message actuel`,
- 0 dans `C`.

Enfin, il envoie le message rassemblant toutes ces informations au joueur choisi précédemment. Le jeu passe à l'étape `3.3. Echange de la balle`.

### 4.4. Echange de balle

Dès qu'un joueur réceptionne une balle (un message FLPR), il doit passer à l'étape de '3.3.1. Vérification de la balle'.

#### 4.4.1. Vérification de la balle

Lors de la réception d'un message FLPR, un joueur doit d'abord vérifier la validité de celui ci. Le message doit être ignoré si :
- la clé publique de l'envoyeur est incorrecte : la valeur contenue dans `Source Public Key` n'est pas égale à la clé publique stockée en local qui correspond à l'adresse IP `Source address` du packet IP enveloppant,
- la clé publique du receveur est incorrecte : la valeur contenue dans `Destination Public Key` n'est pas égale à la clé publique du joueur qui fait la vérification,
- la signature du message actuel n'est pas valide : la valeur contenue dans `Current Signature`, une fois décryptée avec `Source Public Key`, n'est pas égale au hash des 5 premiers en-têtes.

Le joueur qui fait la vérification ne peut pas prévenir les autres joueurs des éventuelles tentatives de triche, car il ne peut pas prouver qu'il n'a pas créé le message de toute pièce si la signature est invalide, ou qu'il n'a fait une attaque de l'homme du milieu pour intercepter un message qu'il n'est pas censé recevoir si les clés publiques sont incorrectes, tout ça afin d'accuser l'envoyeur du message. La meilleure option est donc de ne rien faire.

Si et seulement si toutes les informations vérifiées sont correctes, le joueur doit :
- stocker le message en local pour s'en resservir lors de la phase de décompte des points,
- passer à l'étape '3.3. Décompte des points' si la valeur contenue dans `Nombre de rebonds` est 0,
- sinon, passer à l'étape '3.3.2. Création d'un nouveau message'.

#### 4.4.2. Création du nouveau message

Lorsque la vérification de la balle s'est terminée avec succès, le joueur doit créer un nouveau message FLPR avec comme en-têtes :
- la même valeur que celle qui était dans le message précédent dans `Ball ID`,
- la valeur qui était dans le message précédent décrémentée de 1 dans `Bounce Number`,
- sa propre clé publique dans `Source Public Key`,
- la clé publique d'un joueur choisi aléatoirement dans l'éventail d'adresses dans `Destination Public Key`,
- la valeur qui était dans le message précédant à l'en-tête `Current Signature` dans `Previous Signature`,
- le hash de tous les en-têtes précédents, le tout encrypté avec la clé privée du joueur dans `Current Signature`,
- 0 dans `C`.

Enfin, il envoie le message rassemblant toutes ces informations au joueur choisi précédemment.

### 4.5. Décompte des points

Il n'est plus nécessaire pour les joueurs de stocker leur propre score en local, car le décompte des points se passe d'une manière différente. Lorsqu'un joueur atteint le nombre de rebonds restants 0, il envoie le message qu'il a reçu en broadcast à tous les autres joueurs pour lancer prouver qu'i

Les signatures électroniques servent à s'assurer de la non-répudiation des messages, au cas où un envoyeur venait à nier le fait qu'il ait envoyé un message.



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
[3.4.1]: #341-vérification-de-la-balle
[3.4.2]: #342-création-et-envoi-dun-nouveau-message-flpr
[3.5]: #35-décompte-des-points
[3.5.1]: #351-lancement-du-décompte
[3.5.2]: #352-communication-des-scores
[4]: #4-version-sécurisée
[4.1]: #41-pré-requis
[4.2]: #42-structure-dun-message-flpr
[4.3]: #43-lancement-dune-balle
[4.4]: #44-echange-de-balle
[4.4.1]: #441-vérification-de-la-balle
[4.4.2]: #442-création-du-nouveau-message
[4.5]: #45-décompte-des-points


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