# Spécification protocole Flipper : Version non-sécurisée

Par Timothé Albouy
Ecole Nationale d'Ingénieurs de Bretagne Sud (ENSIBS)

## 1. Sommaire

- [1. Sommaire][1]
- [2. Pré-requis][2]
- [3. Structure d'un message FLPR][3]
- [4. Etapes du jeu][4]
  - [4.1. Ecoute de messages FLPR][4.1]
  - [4.2. Lancement d'une nouvelle balle][4.2]
  - [4.3. Renvoi d'une balle][4.3]
  - [4.4. Communication des scores][4.4]
  - [4.5. Election du gagnant][4.5]
- [5. Améliorations possibles][5]

### 2. Pré-requis

FLPR est un protocole de couche applicative basé sur l'architecture TCP/IP (pour ne pas avoir à se soucier des paquets perdus), c'est-à-dire que chaque message FLPR sera encapsulé dans un segment TCP, lui-même encapsulé dans un packet IPv4.

Par convention, le port TCP utilisé par FLPR est **16 180** (le début du nombre d'or).

Chaque joueur doit stocker en local la liste des adresses IP de tous les participants au jeu.

Sont laissées libres par le développeur chargé de l'implémentation :
- la méthode de stockage des adresses IP,
- la méthode de distribution des adresses IP.

## 3. Structure d'un message FLPR

Un message FLPR doit posséder les en-têtes suivants :
- `Ball ID` (16 bits), l'identifiant de la balle généré aléatoirement ;
- `Counter` (8 bits), un entier non signé donnant le nombre de rebonds effectués par la balle ;
- `Bounce Limit` (8 bits), un entier non signé donnant la limite (inatteignable) du nombre de rebonds de balle ;
- `Bounce History` (taille variable), qui contient l'historique de tous les rebonds qu'a faits la balle, c'est-à-dire pour chacun d'entre-eux une ligne contenant l'adresse IP du récepteur.

Voici le schéma des en-têtes de message FLPR :

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |            Ball ID            |    Counter    |  Bounce Limit |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    ~                Bounce History (taille variable)               ~
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
                  Format d'Entêtes d'un Message FLPR

Sachant que la charge utile d'un paquet TCP est de de à peu près 1400 octets soit 11 200 bits, on peut donc y stocker au maximum 350 adresses IPv4 de 32 bits. La puissance de 2 la plus proche est 256, soit 2^8, donc on peut stocker le nombre de rebonds sur 8 bits, d'où les en-têtes `Counter` et `Bounce Limit` codés sur 1 octet. Cela signifie aussi que le nombre maximum d'adresses IPv4 dans `Bounce History` est de 254 : la balle ne peut faire que 254 rebonds maximum. Deux valeurs du compteur sont réservées : 0 (il n'y a aucune IP dans l'historique) et 255 (la 255ème valeur de l'historique ne peut jamais être une IP donnant un rebond). L'avantage de cette version naïve du protocole est donc qu'un message est contenu dans un seul segment TCP, pas besoin de faire du réassemblage de paquets.

### 4. Etapes du jeu

#### 4.1. Ecoute de messages FLPR

Cette étape est le point d'entrée du protocole et l'état initial de chaque joueur. Le joueur doit être constamment en position d'écoute de messages, et afin de ne pas interrompre cette écoute, toutes les sous-étapes qu'il lancera d'ici doivent être exécutées en parallèle.

**Spécification :**
- reçevoir un message FLPR
- si `Bounce Limit` = 0 : ne rien faire
- sinon si `Counter` = `Bounce Limit` : passer à [Election du gagnant][4.5]
- sinon si `Counter` = `Bounce Limit` - 1 : passer à [Communication des scores][4.4]
- sinon si `Counter` < `Bounce Limit` - 1 : passer à [Renvoi d'une balle][4.3]
- sinon : ne rien faire

#### 4.2. Lancement d'une nouvelle balle

Chaque joueur peut lancer cette étape quand il le souhaite, ce qui signifie qu'il peut y avoir plusieurs balles qui circulent en même temps parmi les joueurs.

**Spécification :**
- créer un message FLPR :
  - `Ball ID` = nombre aléatoire
  - `Counter` = 1
  - `Bounce Limit` = nombre aléatoire différent de 0
  - `Bounce History` = une autre adresse IP aléatoire de la liste
- envoyer le message FLPR à l'adresse IP choisie précédemment

#### 4.3. Renvoi d'une balle

**Spécification :**
- créer un message FLPR :
  - `Ball ID` = `Ball ID` reçu
  - `Counter` = `Counter` reçu + 1
  - `Bounce Limit` = `Bounce Limit` reçu
  - `Bounce History` = `Bounce History` recu . une autre adresse IP aléatoire de la liste
- envoyer le message FLPR à l'adresse IP choisie précédemment

L'opérateur . est la concaténation.

#### 4.4. Communication des scores

**Spécification :**
- créer un message FLPR :
  - `Ball ID` = `Ball ID` reçu
  - `Counter` = `Bounce Limit` reçu
  - `Bounce Limit` = `Bounce Limit` reçu
  - `Bounce History` = `Bounce History` recu . "0.0.0.0"
- envoyer le message FLPR à toutes les autres adresses IP de la liste
- élire comme gagnant de l'échange de balles le(s) joueur(s) dont l'adresse IP apparaît le plus souvent dans `Bounce History`

L'opérateur . est la concaténation.

L'IP 0.0.0.0 à la fin de `History` et le fait que les valeurs de `Counter` et `Bounce Limit` soient les mêmes assurera les récepteurs de ce message qu'il s'agit d'une communication des scores.

#### 4.5. Election du gagnant

**Spécification :**
- élire comme gagnant de l'échange de balles le(s) joueur(s) dont l'adresse IP apparaît le plus souvent dans `Bounce History`

## 5. Améliorations possibles

La version naïve du protocole FLPR laisse place à une faille assez importante, qui est qu'un joueur peut mentir sur l'historique des rebonds de la balle lorsqu'il la renvoie à un autre joueur. En effet, il peut la changer pour faire apparaître son adresse IP plus souvent afin de faire gonfler son propre score.

Ce problème peut être réglé en ajoutant au protocole FLPR un système de traçabilité des balles grâce à des signatures électroniques. Ces signatures permettent la non-répudiation des messages, au cas où leurs émetteurs venaient à nier le fait qu'il les aient envoyés, mais cela empêche aussi qu'un joueur mal intentionné altère l'historique des rebonds de la balle.


[1]: #1-sommaire
[2]: #2-pré-requis
[3]: #3-structure-dun-message-flpr
[4]: #4-etapes-du-jeu
[4.1]: #41-ecoute-de-messages-flpr
[4.2]: #42-lancement-dune-nouvelle-balle
[4.3]: #43-renvoi-dune-balle
[4.4]: #44-communication-des-scores
[4.5]: #45-election-du-gagnant
[5]: #5-améliorations-possibles