# 🏸 HomeSmash

Application pour visualiser et gérer les disponibilités et les réservations du Badsclub (API Doinsport).
HomeSmash propose une interface graphique interactive via **Streamlit** ainsi qu'un outil en **ligne de commande (CLI)**.

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
   - `APP_PASSWORD` : Le mot de passe global protégeant l'accès à l'application.
   - Les identifiants de Doinsport.
   - Les URLs Google Chat Webhooks.

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

---

## 💻 Utilisation en Ligne de Commande (CLI)

Si vous préférez le terminal sans interface graphique, l'application est exécutable directement. Assurez-vous d'avoir activé votre `.venv` et configuré vos secrets au préalable :

```bash
# Afficher les disponibilités des 2 prochaines semaines
python -m homesmash affiche_dispo

# Afficher les réservations (anciennes et futures)
python -m homesmash affiche_resa
```

*Utilisez `python -m homesmash -h` pour voir toutes les options disponibles.*

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
