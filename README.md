# Protocole Flipper

Par Timothé ALBOUY & Youssef EL HOR

Le protocole Flipper (FLPR) est un protocole permettant à plusieurs ordinateurs d'un même réseau informatique de jouer à une simulation d'envoi de balles, un message symbolisant un envoi de balle entre deux machines. Une fois interceptée par un joueur, une balle doit être renvoyée à un autre joueur et ce jusqu'à ce que la balle n'ait plus de rebonds restants. FLPR fonctionne totalement en pair à pair, sans passer par un serveur central qui servirait d'arbitre.

- [Spécification non-sécurisée][specs-unsafe]
- [Spécification sécurisée][specs-safe]

FLPR version non-sécurisée possède une implémentation de référence en Python réalisée avec la librairie Scapy se trouvant dans le paquetage `impl`.

## Utilisation

D'abord, installez les dépendances :

    pip install -r requirements.txt

Pour lancer la phase d'écoute de messages FLPR, exécutez `listen.py`. Pour lancer une nouvelle balle, exécutez `start_ball.py`.


[specs-unsafe]: /TimotheAlbouy/flipper-protocol/blob/master/specs-unsafe.md
[specs-safe]: /TimotheAlbouy/flipper-protocol/blob/master/specs-safe.md