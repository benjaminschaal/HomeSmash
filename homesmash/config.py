"""
Configuration du module HomeSmash (accès Doinsport + webhooks Google Chat).
"""

import streamlit as st

# --- CONFIGURATION DOINSPORT ---

# Identifiants de connexion
LOGIN = st.secrets["doinsport"]["login"]
PASSWORD = st.secrets["doinsport"]["password"]

# Identifiants du club (Badsclub)
CLUB_ID = st.secrets["doinsport"]["club_id"]
ACTIVITY_ID = st.secrets["doinsport"]["activity_id"]  # Badminton
CATEGORY_ID = st.secrets["doinsport"]["category_id"]

# Liste des créneaux horaires ciblés
HEURES_CIBLES = ["12:00", "12:15", "12:30", "12:45", "13:00", "13:15"]

# En-têtes HTTP standards
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Origin": "https://badsclub.doinsport.club",
    "Referer": "https://badsclub.doinsport.club/",
    "Accept": "application/json, text/plain, */*",
    "X-Locale": "fr",
    "Content-Language": "fr",
}

# --- CONFIGURATION GOOGLE CHAT ---

# SALON PROD
GOOGLE_CHAT_WEBHOOK = st.secrets["google_chat"]["webhook_prod"]

# SALON DEV / TEST
GOOGLE_CHAT_WEBHOOK_TEST = st.secrets["google_chat"]["webhook_test"]
