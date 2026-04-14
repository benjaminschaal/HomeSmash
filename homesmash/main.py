#!/usr/bin/env python3
"""
Point d'entrée principal du module HomeSmash (interface CLI).

Usage: python -m homesmash [commande] [options]

Commandes:
    affiche_dispo    Affiche les disponibilités dans le terminal (défaut)
    publie_dispo     Envoie un sondage sur Google Chat
    affiche_resa     Affiche vos réservations (passées, à venir, annulées)
    publie_resa      Publie la liste des réservations sur Chat

Options:
    --semaine N     Semaine de départ (défaut: courant)
    --nb-semaines N Nombre de semaines (défaut: 2)
    --historique N  Nombre de semaines d'historique pour les réservations (défaut: 0)
"""

import argparse
import sys
from .display import affiche_dispo, affiche_resa
from .poll import publie_dispo, publie_resa
from .api import get_reservations


def main():
    parser = argparse.ArgumentParser(
        description="Gestion des disponibilités Badsclub et sondages Google Chat (HomeSmash)"
    )
    
    parser.add_argument(
        'commande',
        nargs='?',
        default='affiche_dispo',
        choices=['affiche_dispo', 'publie_dispo', 'affiche_resa', 'publie_resa'],
        help="Commande à exécuter (défaut: affiche_dispo)"
    )
    
    import datetime
    current_week = datetime.date.today().isocalendar()[1]
    
    parser.add_argument(
        '--semaine', '-s',
        type=int,
        default=current_week,
        help=f"Semaine de départ (défaut: {current_week} - semaine actuelle)"
    )
    
    parser.add_argument(
        '--nb-semaines', '-n',
        type=int,
        default=2,
        help="Nombre de semaines à analyser (défaut: 2)"
    )
    
    parser.add_argument(
        '--historique', '-H',
        type=int,
        default=0,
        help="Nombre de semaines d'historique pour les réservations (défaut: 0)"
    )
    
    args = parser.parse_args()
    
    if args.commande == 'affiche_dispo':
        affiche_dispo(args.semaine, args.nb_semaines)
    elif args.commande == 'publie_dispo':
        publie_dispo(args.semaine, args.nb_semaines)
    elif args.commande == 'affiche_resa':
        res = get_reservations(weeks_history=args.historique)
        affiche_resa(res, weeks_history=args.historique)
    elif args.commande == 'publie_resa':
        res = get_reservations(weeks_history=args.historique)
        publie_resa(res, weeks_history=args.historique)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
