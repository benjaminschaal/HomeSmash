"""
Module Display - Affichage des disponibilités dans le terminal
"""

from .api import get_disponibilites


def affiche_dispo(semaine_depart, nb_semaines=1):
    """
    Affiche les disponibilités dans le terminal avec un tableau récapitulatif.
    
    Args:
        semaine_depart: Numéro de la première semaine
        nb_semaines: Nombre de semaines à analyser
    """
    print(f"\n--- DÉBUT DE LA RECHERCHE ---")
    
    resultats = get_disponibilites(semaine_depart, nb_semaines)
    
    if not resultats:
        print("\n\n📊 Aucun terrain trouvé sur toute la période.")
        return resultats
    
    # Affichage détaillé par jour
    current_semaine = None
    current_date = None
    
    for r in resultats:
        if r['semaine'] != current_semaine:
            current_semaine = r['semaine']
            print(f"\n🚀 SEMAINE {current_semaine}")
            print("=" * 25)
        
        if r['date'] != current_date:
            current_date = r['date']
            print(f"📅 {r['jour']} {r['date']} :")
        
        print(f"    ✅ {r['heure']} - {', '.join(r['terrains'])}")
    
    # Tableau récapitulatif
    print("\n\n" + "📊 TABLEAU RÉCAPITULATIF DES DISPONIBILITÉS".center(75))
    hr = "+" + "-"*10 + "+" + "-"*12 + "+" + "-"*12 + "+" + "-"*10 + "+" + "-"*15 + "+"
    print(hr)
    print(f"| {'Semaine':^8} | {'Date':^10} | {'Jour':^10} | {'Heure':^8} | {'Nb Terrains':^13} |")
    print(hr)
    for r in resultats:
        print(f"| {r['semaine']:^8} | {r['date']:^10} | {r['jour']:^10} | {r['heure']:^8} | {r['nb_terrains']:^13} |")
    print(hr)
    
    return resultats


def affiche_resa(reservations, weeks_history=2):
    """
    Affiche les réservations dans le terminal.
    """
    if not reservations:
        print("\n📊 Aucune réservation trouvée.")
        return

    sections = [
        ('🏸 RÉSERVATIONS À VENIR', reservations.get('a_venir', [])),
        (f'⏳ RÉSERVATIONS PASSÉES ({weeks_history} dernières semaines)', reservations.get('passees', [])),
        ('❌ RÉSERVATIONS ANNULÉES', reservations.get('annulees', []))
    ]

    for title, items in sections:
        if not items:
            if weeks_history == 0 and ('PASSÉES' in title or 'ANNULÉES' in title):
                continue
            print(f"\n{title}")
            print("  Aucune")
            continue
            
        print(f"\n{title}")
            
        hr = "+" + "-"*12 + "+" + "-"*10 + "+" + "-"*15 + "+" + "-"*12 + "+"
        print(hr)
        print(f"| {'Date':^10} | {'Heure':^8} | {'Terrain':^13} | {'Statut':^10} |")
        print(hr)
        for r in items:
            print(f"| {r['date']:^10} | {r['heure']:^8} | {r['terrain']:^13} | {r['status']:^10} |")
        print(hr)
