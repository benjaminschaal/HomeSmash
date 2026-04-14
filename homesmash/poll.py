"""
Module Poll - Création de sondages Google Chat via Webhook
"""

import requests
from .api import get_disponibilites
from .config import GOOGLE_CHAT_WEBHOOK


def _format_balance(balance):
    if balance is None:
        return "0"
    if isinstance(balance, float) and balance.is_integer():
        return str(int(balance))
    return str(balance)


def _construire_message_sondage(resultats, titre="🏸 Sondage Badminton - Disponibilités", credits_list=None):
    """
    Construit un message Card Google Chat avec les disponibilités comme options de sondage.
    
    Args:
        resultats: Liste des disponibilités
        titre: Titre du sondage
        credits_list: Liste optionnelle de crédits (affichés s'ils sont type Ticket CE ou solde > 0)
    
    Returns:
        dict: Payload JSON pour le webhook Google Chat
    """
    if not resultats:
        return {
            "text": "❌ Aucune disponibilité trouvée pour créer le sondage."
        }
    
    # Grouper les dispos par jour pour les options du sondage
    options_par_jour = {}
    for r in resultats:
        cle = f"{r['jour']} {r['date']}"
        if cle not in options_par_jour:
            options_par_jour[cle] = []
        options_par_jour[cle].append(f"{r['heure']} ({r['nb_terrains']} terrain(s))")
    
    # Construire les widgets pour la card
    widgets = []
    
    # En-tête
    widgets.append({
        "decoratedText": {
            "topLabel": "📅 Créneaux disponibles",
            "text": f"<b>{titre}</b>",
            "wrapText": True
        }
    })
    
    # Divider
    widgets.append({"divider": {}})
    
    # Instructions
    widgets.append({
        "decoratedText": {
            "text": "Réagissez avec un emoji pour voter !",
            "startIcon": {"knownIcon": "BOOKMARK"}
        }
    })
    
    # Liste des options numérotées (style sondage)
    emoji_numeros = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    option_num = 0
    
    for jour, heures in options_par_jour.items():
        for heure in heures:
            if option_num < len(emoji_numeros):
                emoji = emoji_numeros[option_num]
                widgets.append({
                    "decoratedText": {
                        "text": f"{emoji} <b>{jour}</b> - {heure}",
                        "wrapText": True
                    }
                })
                option_num += 1
    
    # Option "Pas dispo"
    widgets.append({"divider": {}})
    widgets.append({
        "decoratedText": {
            "text": "❌ Pas disponible",
            "wrapText": True
        }
    })
    
    # Ajout des crédits si fournis
    if credits_list:
        credits_lines = []
        for c in credits_list:
            name = c.get("name", "Pack")
            balance = c.get("balance", 0)
            if balance > 0 or "CE" in name:
                credits_lines.append(f"• {name} : {_format_balance(balance)}")
        credits_text = "\n".join(credits_lines)
        if credits_text:
            widgets.append({"divider": {}})
            widgets.append({
                "decoratedText": {
                    "topLabel": "🎟️ Mes crédits restants",
                    "text": credits_text,
                    "wrapText": True,
                    "startIcon": {"knownIcon": "TICKET"}
                }
            })
    
    # Construction de la card finale
    card = {
        "cardsV2": [{
            "cardId": "poll-badminton",
            "card": {
                "header": {
                    "title": "🏸 Sondage Badminton",
                    "subtitle": "Votez pour vos créneaux préférés",
                    "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/sports_tennis/default/48px.svg",
                    "imageType": "CIRCLE"
                },
                "sections": [{
                    "widgets": widgets
                }]
            }
        }]
    }
    
    return card


def publie_dispo(semaine_depart=None, nb_semaines=1, webhook_url=None, resultats=None, credits_list=None):
    """
    Crée et envoie un sondage sur Google Chat à partir des disponibilités.
    
    Args:
        semaine_depart: Numéro de la première semaine (ignoré si resultats est fourni)
        nb_semaines: Nombre de semaines à analyser (ignoré si resultats est fourni)
        webhook_url: URL du webhook (utilise la config par défaut si non spécifié)
        resultats: Liste pré-calculée des dispos (évite un appel API)
        credits_list: Liste de crédits à inclure en bas du sondage
    
    Returns:
        dict: Réponse de l'API Google Chat
    """
    webhook = webhook_url or GOOGLE_CHAT_WEBHOOK
    
    if resultats is None:
        print(f"\\n📋 Récupération des disponibilités...")
        resultats = get_disponibilites(semaine_depart, nb_semaines)
        
    if not resultats:
        print("❌ Aucune disponibilité trouvée.")
        return None
    
    print(f"✅ {len(resultats)} créneaux trouvés")
    
    # Construire le message
    payload = _construire_message_sondage(resultats, credits_list=credits_list)
    
    # Envoyer au webhook
    print(f"\n📤 Envoi du sondage sur Google Chat...")
    
    try:
        response = requests.post(
            webhook,
            json=payload,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )
        response.raise_for_status()
        
        print("✅ Sondage envoyé avec succès !")
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erreur lors de l'envoi : {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Détail : {e.response.text}")
        return None


def publie_resa(reservations, weeks_history=1, webhook_url=None, credits_list=None):
    """
    Publie les réservations actuelles sur Google Chat sous forme de Card.
    """
    webhook = webhook_url or GOOGLE_CHAT_WEBHOOK
    
    if not reservations:
        # Envoi d'un simple message texte lorsqu'aucune réservation n'est trouvée
        payload = {"text": "📋 Aucune réservation trouvée."}
        try:
            response = requests.post(
                webhook,
                json=payload,
                headers={"Content-Type": "application/json; charset=UTF-8"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erreur lors de l'envoi : {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"   Détail : {e.response.text}")
            return None
        except Exception as e:
            print(f"⚠️ Erreur lors de la publication : {e}")
            return None

    # Notification : n'afficher que les réservations à venir
    sections_data = [
        ("🏸 À VENIR", reservations.get('a_venir', []), "star"),
    ]
    
    widgets = []
    
    for title, items, icon in sections_data:
        if not items:
            if weeks_history == 0 and ('PASSÉES' in title or 'ANNULÉES' in title):
                continue
            widgets.append({
                "decoratedText": {
                    "topLabel": title,
                    "text": "<b>Liste des créneaux</b>",
                    "startIcon": {"knownIcon": icon.upper()}
                }
            })
            widgets.append({
                "decoratedText": {
                    "text": "<i>Aucune réservation</i>"
                }
            })
        else:
            widgets.append({
                "decoratedText": {
                    "topLabel": title,
                    "text": "<b>Liste des créneaux</b>",
                    "startIcon": {"knownIcon": icon.upper()}
                }
            })
            for r in items:
                status_emoji = "✅" if r['status'] == 'Confirmée' else "❌"
                widgets.append({
                    "decoratedText": {
                        "text": f"{status_emoji} <b>{r['date']}</b> à <b>{r['heure']}</b>",
                        "bottomLabel": f"Terrain: {r['terrain']} | {r['status']}",
                        "wrapText": True
                    }
                })
        
        widgets.append({"divider": {}})
    
    # Ajout des crédits si fournis
    if credits_list:
        credits_lines = []
        for c in credits_list:
            name = c.get("name", "Pack")
            balance = c.get("balance", 0)
            if balance > 0 or "CE" in name:
                credits_lines.append(f"• {name} : {_format_balance(balance)}")
        credits_text = "\n".join(credits_lines)
        if credits_text:
            widgets.append({
                "decoratedText": {
                    "topLabel": "🎟️ Mes crédits restants",
                    "text": credits_text,
                    "wrapText": True,
                    "startIcon": {"knownIcon": "TICKET"}
                }
            })
            widgets.append({"divider": {}})
            
    # Petit message texte au-dessus de la card
    nb_avenir = len(reservations.get("a_venir", []))
    summary_text = f"📅 Réservations à venir : {nb_avenir}."

    payload = {
        "text": summary_text,
        "cardsV2": [{
            "cardId": "reservations-list",
            "card": {
                "header": {
                    "title": "HomeSmash - Réservations",
                    "subtitle": "État de vos créneaux",
                    "imageUrl": "https://fonts.gstatic.com/s/i/short-term/release/materialsymbolsoutlined/calendar_month/default/48px.svg",
                    "imageType": "CIRCLE"
                },
                "sections": [{"widgets": widgets}]
            }
        }]
    }
    
    try:
        response = requests.post(
            webhook,
            json=payload,
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )
        response.raise_for_status()
        print("✅ Liste des réservations publiée sur Google Chat !")
        return response.json()
    except Exception as e:
        print(f"⚠️ Erreur lors de la publication des réservations : {e}")
        return None
