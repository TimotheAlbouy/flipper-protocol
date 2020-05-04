# Protocole Flipper

Par Timothé ALBOUY & Youssef EL HOR

Le protocole Flipper (FLPR) est un protocole permettant à plusieurs ordinateurs d'un même réseau informatique de jouer à une simulation d'envoi de balles, un message symbolisant un envoi de balle entre deux machines. Une fois interceptée par un joueur, une balle doit être renvoyée à un autre joueur et ce jusqu'à ce que la balle n'ait plus de rebonds restants. FLPR fonctionne totalement en pair à pair, sans passer par un serveur central qui servirait d'arbitre.

- [Spécification non-sécurisée][spec-unsafe]
- [Spécification sécurisée][spec-safe]

FLPR version non-sécurisée possède une implémentation de référence en Python réalisée avec la librairie Scapy se trouvant dans le paquetage `impl`.

## Utilisation

D'abord, installez Python ainsi que les dépendances du projet :

    apt update
    apt install python3.6
    pip install -r requirements.txt

Ensuite, modifiez la liste des IP des participants dans `pool.py`, par exemple :

    pool = [
        "192.168.1.15",
        "192.168.1.20"
    ]

Pour lancer la phase d'écoute de messages FLPR :

    python listen.py

Pour lancer une nouvelle balle :

    python start_ball.py

Pour lancer sur la machine attaquante l'attaque 1 :

    python atk_flpr_1.py

Pour lancer sur l'IPS le code prémunissant contre l'attaque 1 :

    python ips_flpr_1.py

Pour lancer sur la machine attaquante l'attaque 2 :

    python atk_flpr_2.py

Pour lancer sur l'IPS le code prémunissant contre l'attaque 2 :

    python ips_flpr_2.py




[spec-unsafe]: /spec-unsafe.md
[spec-safe]: /spec-safe.md
