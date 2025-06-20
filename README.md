# MadaVoyage

**MadaVoyage** est un chatbot de voyage interactif pour Madagascar, offrant une expérience multilingue (français et malgache) pour aider les voyageurs à planifier leurs séjours. Développé avec Django, ce projet propose des fonctionnalités pratiques et une interface conviviale.

## Fonctionnalités principales

- **FAQ dynamique** : Répond aux questions fréquentes (ex. visa, souvenirs, sécurité) via une base de 50 FAQs (25 en français, 25 en malgache).
- **Réservation de voyage** : Processus guidé pour réserver une destination, avec génération d’un devis PDF et confirmation par email.
- **Guide des destinations** : Informations sur Nosy Be, Allée des Baobabs, et Parc de l’Isalo, incluant descriptions et activités.
- **Calculateur de budget** : Estime les coûts selon la destination, la durée, le nombre de personnes, et le type d’hébergement (économique, standard, luxe), avec option d’envoi par email.
- **Support multilingue** : Interface et réponses en français et malgache, sélectionnables par l’utilisateur.

## Technologies utilisées

- **Backend** : Django (Python)
- **Frontend** : HTML, Tailwind CSS, JavaScript
- **Base de données** : SQLite (développement)
- **PDF** : ReportLab
- **Email** : Django Email
- **Sessions** : Django Sessions pour gérer les interactions


## Prérequis

- Python 3.9+
- Git
- Compte email pour envoyer des confirmations (ex. Gmail avec mot de passe d’application)

## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/Tsong030205/MadaVoyage.git
2. Creer un environnement virtuel
    python -m venv venv
    # Linux/MacOS : source venv/bin/activate
    # Windows : venv\Scripts\activate
3. Installer les dependances necessaires
    pip install -r requirements.txt

4. Configurer les variables d'environnement 
    -Creer un fichier .env a la racine :
        SECRET_KEY=your-secret-key
        DEBUG=True
        EMAIL_HOST_USER=your-email@gmail.com
        EMAIL_HOST_PASSWORD=your-app-password
    -Remplacer par vos propres valeurs

5. Appliquer les migrations
    python manage.py migrate

# Comment utiliser
# Chatbot
Choisir la langue (français ou malgache) dans le menu.
Poser des questions (ex. "Quels souvenirs ramener ?") pour des réponses FAQ.
Utiliser les commandes :
réserver / mampandray : Lancer une réservation.
guide / toerana : Explorer les destinations.
budget / teti-bola : Calculer un budget.
annuler / fanafoana : Réinitialiser.
Les réservations génèrent un PDF et un email ; les budgets peuvent être envoyés par email.
# Admin
Gérer les FAQs, réservations, destinations, et estimations à /admin/.
Ajouter des données via l’interface ou des scripts.
Données initiales
FAQs : 50 questions/réponses (25 par langue) sur les voyages à Madagascar.
Destinations : Nosy Be, Allée des Baobabs, Parc de l’Isalo.
Ajouter des données via l’admin si nécessaire.
# Dépendances clés
Django
reportlab
python-decouple (Voir requirements.txt pour la liste complète)