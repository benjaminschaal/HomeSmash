# 🏸 HomeSmash

Application pour visualiser et gérer les disponibilités et les réservations du Badsclub (API Doinsport).
HomeSmash propose une interface graphique interactive via **Streamlit** ainsi qu'un outil en **ligne de commande (CLI)**.

## 📸 Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 🔍 **Disponibilités** | Rechercher les créneaux libres sur plusieurs semaines (Lun→Jeu, 12h–13h15) |
| 📅 **Réservations** | Consulter vos réservations à venir, passées et annulées |
| 🎟️ **Crédits** | Voir le solde de vos packs et tickets CE |
| 📣 **Sondage Google Chat** | Publier un sondage interactif dans un salon Google Chat |
| 📊 **Statistiques** | Accéder à l'historique des participations (Google Sheets) |

## 📁 Structure du projet

```
HomeSmash/
├── .streamlit/
│   ├── secrets.example.toml   # Modèle de configuration (sans secrets)
│   └── secrets.toml           # Vos secrets (ignoré par Git)
├── homesmash/
│   ├── __init__.py            # Exports du module
│   ├── __main__.py            # Point d'entrée python -m homesmash
│   ├── api.py                 # Appels à l'API Doinsport
│   ├── app.py                 # Interface Streamlit
│   ├── config.py              # Configuration centralisée
│   ├── display.py             # Affichage console (CLI)
│   ├── main.py                # Point d'entrée CLI (argparse)
│   └── poll.py                # Sondages & messages Google Chat
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🚀 Démarrer l'application en Local (Interface Graphique)

Voici les étapes pour lancer l'interface web locale sur votre machine.

### 1. Prérequis environnement

Assurez-vous d'utiliser un environnement virtuel Python pour isoler les dépendances. Dans le terminal, depuis le dossier `HomeSmash` :

```bash
# Créer l'environnement virtuel (à faire une seule fois)
python3 -m venv .venv

# Activer l'environnement virtuel (à faire à chaque nouveau terminal)
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration Sécurisée (Secrets)

L'application protège vos mots de passe via le mécanisme natif **Streamlit Secrets**.

1. Créez un fichier `.streamlit/secrets.toml` à la racine de ce dossier (il est masqué et ignoré par Git pour des raisons de sécurité).
2. Un fichier modèle `.streamlit/secrets.example.toml` est disponible. Vous pouvez le copier :

```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```

3. **Ouvrez `.streamlit/secrets.toml`** et complétez les valeurs :

| Clé | Description |
|---|---|
| `APP_PASSWORD` | Mot de passe global protégeant l'accès à l'application |
| `[doinsport].login` | Email ou numéro de téléphone du compte Doinsport |
| `[doinsport].password` | Mot de passe Doinsport |
| `[doinsport].club_id` | UUID du club sur Doinsport |
| `[doinsport].activity_id` | UUID de l'activité (Badminton) |
| `[doinsport].category_id` | UUID de la catégorie |
| `[google_chat].webhook_prod` | URL Webhook du salon Google Chat de production |
| `[google_chat].webhook_test` | URL Webhook du salon Google Chat de test |

> ⚠️ **Ne jamais commiter le fichier `secrets.toml`** – il contient vos identifiants réels.

### 3. Lancer Streamlit

Une fois les secrets configurés, lancez l'application :

```bash
streamlit run homesmash/app.py
```

L'application s'ouvrira automatiquement dans le navigateur (par défaut [http://localhost:8501](http://localhost:8501)) et vous demandera le mot de passe (`APP_PASSWORD`).

---

## ☁️ Déploiement sur Streamlit Community Cloud

L'application est prête à être déployée gratuitement sur Streamlit Cloud !

1. Poussez votre code sur GitHub (ex: `https://github.com/votre_pseudo/HomeSmash`).
2. Allez sur [share.streamlit.io](https://share.streamlit.io/) et cliquez sur **New app**.
3. Appliquez la configuration suivante :
   - **Repository** : `votre_pseudo/HomeSmash`
   - **Branch** : `main`
   - **Main file path** : `homesmash/app.py`
4. ⚠️ **Sécurité** : Avant de cliquer sur "Deploy", cliquez sur **Advanced settings**. 
5. Dans l'encart texte "Secrets", **copiez-collez l'intégralité du contenu de votre fichier local `.streamlit/secrets.toml`**.
6. Enregistrez et cliquez sur **Deploy !**

> 💡 Les secrets saisis dans Streamlit Cloud ne sont jamais visibles dans le code source ni dans l'interface publique.

---

## 💻 Utilisation en Ligne de Commande (CLI)

Si vous préférez le terminal sans interface graphique, l'application est exécutable directement. Assurez-vous d'avoir activé votre `.venv` et configuré vos secrets au préalable :

```bash
# Afficher les disponibilités des 2 prochaines semaines
python -m homesmash affiche_dispo

# Afficher les disponibilités à partir de la semaine 20, sur 4 semaines
python -m homesmash affiche_dispo --semaine 20 --nb-semaines 4

# Publier un sondage sur Google Chat
python -m homesmash publie_dispo

# Afficher les réservations (futures uniquement par défaut)
python -m homesmash affiche_resa

# Afficher les réservations avec 4 semaines d'historique
python -m homesmash affiche_resa --historique 4

# Publier les réservations sur Google Chat
python -m homesmash publie_resa
```

*Utilisez `python -m homesmash -h` pour voir toutes les options disponibles.*

---

## 🔐 Sécurité

L'application applique plusieurs niveaux de protection :

- ✅ **Secrets externalisés** : aucun mot de passe ou clé API dans le code source.
- ✅ **`.gitignore`** : le fichier `secrets.toml` n'est jamais versionné.
- ✅ **Authentification** : un mot de passe est requis pour accéder à l'interface Streamlit.
- ✅ **Mode Test** : un toggle permet de basculer entre le salon Google Chat de production et celui de test.

---

## 🛠️ Dépannage (Troubleshooting)

### Erreur "No such file or directory" au lancement de Streamlit
Si vous avez **déplacé ou renommé** le dossier du projet `HomeSmash` de votre ordinateur, l'environnement virtuel (`.venv`) va se casser.

**Solution : Recréer l'environnement virtuel.**
Exécutez dans votre terminal depuis le dossier `HomeSmash` :

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Erreur d'authentification Doinsport
Vérifiez que les identifiants dans `.streamlit/secrets.toml` sont corrects. Le login est votre numéro de téléphone (format `0612345678`) ou email.

### Le sondage Google Chat ne s'envoie pas
Vérifiez que l'URL du webhook dans `secrets.toml` est valide et que l'espace Google Chat est toujours actif.
