# Protocole Flipper (FLPR)

Par Timothé ALBOUY

Le protocole Flipper (FLPR) est un protocole permettant à plusieurs ordinateurs d'un même réseau informatique de jouer à une simulation d'envoi de balles, un message symbolisant un envoi de balle entre deux machines. Une fois interceptée par un joueur, une balle doit être renvoyée à un autre joueur et ce jusqu'à ce que la balle n'ait plus de rebonds restants. FLPR fonctionne totalement en pair à pair, sans passer par un serveur central qui servirait d'arbitre.

- [Spécification non-sécurisée](spec-unsafe.md)
- [Spécification sécurisée](spec-safe.md)

La version **non-sécurisée** du protocole FLPR possède une implémentation de référence en Python réalisée avec la librairie Scapy, que vous pouvez trouver dans le paquetage `impl`.

## Pré-requis

D'abord, installez Python ainsi que les dépendances du projet :

    apt update
    apt install python3 pip3
    pip3 install -r requirements.txt

Ensuite, chaque participant doit avoir la même liste d'IP des participants dans `pool.py`. Par exemple :

    pool = [
        "192.168.1.15",
        "192.168.1.17",
        "192.168.1.20",
        "192.168.1.22",
        "192.168.1.25",
    ]

## Utilisation de l'implémentation

Chaque participant doit ensuite être en position d'écoute de messages FLPR. Pour cela, lancez :

    python3 listen.py

Enfin, un des participant peut lancer une nouvelle balle :

    python3 start_ball.py

## Attaques sur le protocole FLPR

Les attaques 

### Attaque 1

Pour lancer sur la machine attaquante l'attaque 1 :

    python3 atk_flpr_1.py

Pour lancer sur l'IPS le code prémunissant contre l'attaque 1 :

    python3 ips_flpr_1.py

### Attaque 2

Pour lancer sur la machine attaquante l'attaque 2 :

    python3 atk_flpr_2.py

Pour lancer sur l'IPS le code prémunissant contre l'attaque 2 :

    python3 ips_flpr_2.py

