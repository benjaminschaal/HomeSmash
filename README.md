# 🏸 HomeSmash

Application pour visualiser et gérer les disponibilités et les réservations du Badsclub (API Doinsport).
HomeSmash propose une interface graphique interactive via **Streamlit** ainsi qu'un outil en **ligne de commande (CLI)**.

## 🚀 Démarrer l'application (Interface Graphique)

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

### 2. Lancer Streamlit

Une fois l'environnement activé et les dépendances installées, lancez l'application :

```bash
streamlit run homesmash/app.py
```

L'application s'ouvrira automatiquement dans votre navigateur (par défaut sur [http://localhost:8501](http://localhost:8501)).

Sur la page d’accueil :
- utilisez les **boutons d’action** (“Voir les Disponibilités”, “Mes Réservations”, “Statistiques”, “Documentation”) pour accéder directement aux pages correspondantes ;
- activez le **Mode Test (Salon privé)** depuis la **barre latérale** uniquement si vous souhaitez envoyer les messages sur le salon Google Chat de test.
- le bandeau “🎟️ **Mes crédits restants**” affiche les crédits récupérés depuis Doinsport (ex: Ticket CE).

---

## 💻 Utilisation en Ligne de Commande (CLI)

Si vous préférez le terminal sans interface graphique, l'application est exécutable directement. Assurez-vous d'avoir activé votre `.venv` au préalable :

```bash
# Afficher les disponibilités des 2 prochaines semaines
python -m homesmash affiche_dispo

# Afficher les réservations (anciennes et futures)
python -m homesmash affiche_resa
```

*Utilisez `python -m homesmash -h` pour voir toutes les options disponibles.*

---

## 🛠️ Dépannage (Troubleshooting)

### Erreur "No such file or directory" au lancement de Streamlit ou Python
Si vous avez **déplacé ou renommé** le dossier du projet `HomeSmash` de votre ordinateur, l'environnement virtuel (`.venv`) va se casser car il contient des chemins absolus liés à son emplacement de création initial.

**Solution : Recréer l'environnement virtuel.**
Exécutez les commandes suivantes dans votre terminal depuis le dossier `HomeSmash` :

```bash
# 1. Supprimer l'ancien environnement cassé
rm -rf .venv

# 2. Recréer un environnement tout neuf
python3 -m venv .venv

# 3. L'activer
source .venv/bin/activate

# 4. Réinstaller les dépendances
pip install -r requirements.txt
```
Vous pourrez ensuite relancer Streamlit normalement.
