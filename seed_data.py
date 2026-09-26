import sqlite3
import random
from datetime import datetime, timedelta

def seed_database():
    conn = sqlite3.connect('hospital_it.db')
    cursor = conn.cursor()

    # Charger le schéma SQL
    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())

    # Réinitialiser la table
    cursor.execute("DELETE FROM tickets")

    # Services de l'Institut de Neurologie Mongi Ben Hmida
    DEPARTMENTS = [
        'Neuroradiologie (IRM/Scanner)',
        'EFSN (EEG/EMG)',
        'Neurochirurgie',
        'Unité Neuro-Vasculaire (UNV)',
        'Réanimation Neurochirurgicale',
        'Consultation Externe Neurologie',
        'Urgences Neurologiques',
        'Administration & Bureau d\'Ordre'
    ]
    
    # ÉQUIPEMENTS STRICTEMENT INFORMATIQUES & RÉSEAU
    EQUIPMENT = [
        'Station Workstation PACS Neuroradio',
        'PC de Bureau / DMI',
        'Imprimante Thermique Étiquettes/Bracelets',
        'Lecteur Code-Barres / Douchette',
        'Switch Réseau / Prise RJ45',
        'Écran / Moniteur Diagnostic',
        'Onduleur (UPS) Informatique'
    ]
    
    PRIORITIES = ['Faible', 'Moyenne', 'Élevée', 'Critique']
    STATUSES = ['Nouveau', 'En cours', 'Résolu']

    # PANNES STRICTEMENT INFORMATIQUES (Hors biomédical)
    COMMON_ISSUES = [
        ("Déconnexion Station PACS", "L'écran Workstation PACS n'accède plus au serveur d'images de l'IRM", "Réseau", "Port du switch réseau désactivé sur la baie", "Reconfiguration du port switch Vlan Santé"),
        ("Blocage Session DMI", "Impossible d'accéder aux fiches de prise en charge AVC sur le PC médical", "Système / Logiciel", "Session Windows/RDP orpheline sur le serveur", "Réinitialisation du compte sur l'Active Directory"),
        ("Bourrage Imprimante ÉTIQ", "L'imprimante à étiquettes thermiques ne sort plus les formulaires de garde", "Matériel Informatique", "Spouleur d'impression bloqué et rouleau encrassé", "Nettoyage de la tête thermique et relance du service d'impression"),
        ("Lecteur Code-Barres Inactif", "La douchette USB ne lit plus les codes-barres des dossiers patients", "Périphérique", "Port USB défectueux sur la station", "Changement de port USB et réinitialisation du pilote"),
        ("Écran Noir Moniteur PACS", "Affichage clignotant lors de la consultation des coupes scannographiques", "Affichage / Connectique", "Câble DisplayPort/HDMI endommagé", "Remplacement du câble vidéo de la station")
    ]

    # Génération de 60 incidents informatiques
    for i in range(60):
        issue = random.choice(COMMON_ISSUES)
        dept = random.choice(DEPARTMENTS)
        eq = random.choice(EQUIPMENT)
        asset_tag = f"INN-IT-{eq[:3].upper()}-{random.randint(1000, 9999)}"
        created_at = (datetime.now() - timedelta(days=random.randint(0, 45), hours=random.randint(0, 23))).strftime("%Y-%m-%d %H:%M:%S")
        status = random.choice(STATUSES)
        
        cause = issue[3] if status == 'Résolu' else None
        sol = issue[4] if status == 'Résolu' else None

        cursor.execute('''
            INSERT INTO tickets (title, description, category, department, equipment_type, asset_tag, priority, status, root_cause, solution, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            issue[0],
            f"{issue[1]} - Bureau/Salle {random.randint(101, 305)}",
            issue[2],
            dept,
            eq,
            asset_tag,
            random.choice(PRIORITIES),
            status,
            cause,
            sol,
            created_at
        ))

    conn.commit()
    conn.close()
    print("Base de données mise à jour : 100% Incidents Matériel & Réseau Informatique !")

if __name__ == '__main__':
    seed_database()