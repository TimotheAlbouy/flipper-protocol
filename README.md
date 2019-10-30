# Spécification Flipper Protocol

Haitam Sbaity & Timothé Albouy & Benjamin Rozenfeld
Ecole Nationale d'Ingénieurs de Bretagne Sud (ENSIBS)

## 1. Introduction

Le Flipper Protocol (FP) est un protocole de couche applicative basé sur l'architecture TCP/IP, et permettant à plusieurs ordinateurs d'un même réseau informatique de jouer à une simulation d'envoi de balles.

Le protocole Flipper fonctionne totalement en pair à pair, sans passer par un serveur central qui servirait d'arbitre.

## 2. Fonctionnement

### 2.1. Pré-requis

On suppose au préalable que les machines souhaitant participer ont connaissance de l'éventail des adresses IP des joueurs. La méthode de distribution de ces adresses est laissé libre par le développeur chargé de l'implémentation.

### 2.2. Lancement d'une balle

Tout joueur peut générer une balle avec un identifiant et un nombre de rebonds initial, il peut donc y avoir plusieurs balles qui circulent en parallèle parmi les joueurs. Deux personnes qui génèreraient deux balles avec le même identifiant ne créera pas d'erreur, puisque les joueurs renverront la balle et décompteront les points peu importe l'identifiant. Les fraudes possibles n'impliquent pas l'identifiant de balle.

Le joueur générant la balle doit donc générer le premier message d'envoi de balle qui doit contenir les en-têtes suivants :

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |         ID de balle           |       Nombre de rebonds       |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
                    Format d'Entêtes Envoi Flipper

Il place dans l'en-tête `ID de balle` un identifiant de 16 bits qu'il a généré aléatoirement, et dans l'en-tête `Nombre de rebonds` un entier positif (codé sur 16 bits) qu'il choisit et qui est le nombre total de rebonds que la balle fera entre les joueurs. Le joueur générant la balle va ensuite envoyer ce message à un autre joueur de l'éventail d'adresses.

### 2.3. Echange de la balle

Lorsqu'un joueur reçoit un message d'envoi de balle suivant le schéma ci-dessus, il commence par décrémenter le nombre de rebonds dans l'entête correspondante, puis il incrémente en local (et pas sur le message) son score de 1. Si le nombre de rebonds est arrivé à 0, le jeu passe en phase de décompte des points. Sinon, le joueur doit renvoyer le message avec le nombre de rebonds décrémenté à un joueur de l'éventail d'adresses autre que lui-même.

### 2.4. Décompte des points

Lorsque le nombre de rebonds est arrivé à 0, le dernier récepteur de la balle envoie le message en broadcast à l'éventail d'adresses. Les joueurs sauront qu'il s'agit d'un message pour lancer le décompte car l'entête du nombre de rebonds sera égal à 0. A partir de là, tous les joueurs de l'éventail d'adresse doivent envoyer en broadcast leur scores respectifs. Le (ou les) joueur(s) qui possède(nt) le plus haut score sont considérés comme vainqueurs.

## 3. Modifications pour la version sécurisée

La version naïve du protocole Flipper laisse place à beaucoup de failles. Par exemple, rien n'empêche un attaquant de mentir sur son score lors de la phase de décompte. La version sécurisée du protocole utilise donc un système de signatures électroniques pour pallier une partie de ces problèmes. Les changements qui ont été effectués dans chaque phase sont donnés dans cette partie.

### 3.1. Pré-requis

Pour que les joueurs puissent signer leurs messages, il faut qu'ils possèdent un couple clé-privée/clé-publique. Chaque joueur devra donc stocker la clé publique associée à chaque adresse IP de l'éventail. Le cryptosystème (RSA, ECC, ...) et la fonction de hachage (SHA-2, SHA-3, ...) utilisés pour réaliser les signature électroniques, ainsi que la méthode de distribution des clés publiques, sont laissés libres au développeur chargé de l'implémentation. La taille des clés publiques et des signatures dans les messages du protocole Flipper dépendra des mesures de sécurité et des paramètres choisis précédement.

### 3.2. Lancement d'une balle

Le message d'envoi d'une balle doit s'enrichir de plusieurs en-têtes:

- `Clé publique de l'envoyeur`, la clé publique de l'envoyeur du message et qui sert à vérifier la signature du message actuel.
- `Clé publique du receveur`, la clé publique de celui qui reçoit le message.
- `Signature du message précédent` qui est la signature électronique du message reçu.
- `Signature du message actuel` qui est le résultat du hachage de la concaténation des en-têtes précédents (`ID de balle`, `Nombre de rebonds`, `Clé publique de l'envoyeur`, `Clé publique du receveur` et `Signature du message précédent`).
- `C` pour "Comptage", si cet en-tête codé sur 1 seul bit est égal à 0, alors le message est envoyé durant la phase d'échange de balles, sinon il est envoyé durant la phase de décompte des balles.

Voici le nouveau schéma des en-têtes de message du protocole Flipper :

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |         ID de balle           |       Nombre de rebonds       |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~         Clé publique de l'envoyeur (taille variable)          ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~          Clé publique du receveur (taille variable)           ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~       Signature du message précédent (taille variable)        ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~        Signature du message actuel (taille variable)        +-+
    |                                                             |C|
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

                    Format d'Entêtes Envoi Flipper

Le joueur qui lance la balle au départ doit mettre dans les en-têtes du message initial les informations suivantes :
- un identifiant de balle généré aléatoirement dans `ID de balle`,
- un nombre de rebonds initial dans `Nombre de rebonds`,
- sa propre clé publique dans `Clé publique de l'envoyeur`,
- la clé publique d'un joueur choisi aléatoirement dans l'éventail d'adresses dans `Clé publique du receveur`,
- que des 0 dans `Signature du message précédent` (car il n'y a pas de message précédent),
- la signature avec sa clé privée de toutes les informations qui ont été entrées jusque-là dans `Signature du message actuel`,
- 0 dans `C`.

Enfin, il envoie le message rassemblant toutes ces informations au joueur choisi précédemment.

### 3.3. Echange de balle

Lors de la réception d'un message, un joueur doit d'abord vérifier la validité de celui ci. Le message doit être ignoré si :
- la clé publique de l'envoyeur est incorrecte (elle n'est pas égale à celle qui a été stockée en local et qui correspond à l'adresse IP et qui a effectué l'envoi),
- la clé publique du receveur est incorrecte (elle n'est pas égale à celle du joueur qui fait la vérification),
- la signature du message actuel n'est pas valide (décryptée avec la clé publique de l'envoyeur, elle n'est pas égale au hash des autres en-têtes),

Le joueur qui a fait la vérification ne peut pas prévenir les autres joueurs de cette tentative de triche, car il ne peut pas prouver qu'il n'a pas créé le message de toute pièce si la signature est invalide, ou qu'il n'a fait une attaque de l'homme du milieu pour intercepter un message qu'il n'est pas censé recevoir si les clés publiques sont incorrectes, tout ça afin d'accuser l'envoyeur du message.

Si le message a passé la vérification, alors le joueur le stocke en local pour s'en resservir lors de la phase de décompte des points. Comme précédemment, le joueur vérifie si le nombre de rebonds restants est égal à 0, auquel cas on passe en phase de décompte des points. Sinon, le jeu continue et le joueur doit mettre dans les en-têtes du nouveau message les informations suivantes :
- le même identifiant de balle dans `ID de balle`,
- le même nombre de rebonds décrémenté de 1 dans `Nombre de rebonds`,
- sa clé publique dans `Clé publique de l'envoyeur`,
- la clé publique d'un joueur choisi aléatoirement dans l'éventail d'adresses dans `Clé publique du receveur`,
- le contenu de l'en-tête `Signature du message actuel` dans `Signature du message précédent`,
- la signature avec sa clé privée de toutes les informations qui ont été entrées jusque-là dans `Signature du message actuel`,
- 0 dans `C`.

Enfin, il envoie le message rassemblant toutes ces informations au joueur choisi précédemment.

### 3.3. Décompte des points

Il n'est plus nécessaire pour les joueurs de stocker leur propre score en local, car le décompte des points se passe d'une manière différente. Lorsqu'un joueur atteint le nombre de rebonds restants 0, il envoie le message qu'il a reçu en broadcast à tous les autres joueurs pour lancer prouver qu'i

Les signatures électroniques servent à s'assurer de la non-répudiation des messages, au cas où un envoyeur venait à nier le fait qu'il ait envoyé un message.



Ce genre de triche n'est pas puni par le protocole, mais il revient plutôt aux joueurs de boycotter un participant dans les parties suivantes, voire de se mettre d'accord pour le bannir de l'éventail d'adresses, si celui-ci tente de frauder.

On considère qu'un joueur a objectivement gagné lorsque plus de la moitié des joueurs s'accordent à dire que c'est le cas.


Si un joueur reçoit un message qui n'a pas été signé par une clé appartenant au , il ne doit pas renvoyer la balle. On considère qu'il y a triche 
ne respecte pas ces conditions


Cependant, la méthode préconisée 



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