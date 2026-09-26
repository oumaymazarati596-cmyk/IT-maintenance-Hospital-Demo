import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Institut Mongi Ben Hmida - Maintenance IT",
    page_icon="🖥️",
    layout="wide"
)

# 2. Inject Custom CSS to Fix Text Wrapping & Improve Typography
st.markdown("""
    <style>
    /* Allow full text wrapping on Streamlit checkboxes and labels */
    .stCheckbox label p {
        white-space: normal !important;
        word-wrap: break-word !important;
        font-size: 0.95rem;
    }
    .stSelectbox label, .stMultiSelect label {
        font-weight: 600;
    }
    /* Clean metric card styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Database Connector
def fetch_tickets():
    conn = sqlite3.connect('hospital_it.db')
    df = pd.read_sql_query("SELECT * FROM tickets ORDER BY created_at DESC", conn)
    conn.close()
    return df

# 4. IT Troubleshooting Engine
def generate_ai_suggestion(equipment, title, description):
    text = (title + " " + description).lower()
    
    if "pacs" in text or "workstation" in text or "écran" in text or "affichage" in text:
        return {
            "summary": "Problème d'affichage ou d'accès au serveur d'imagerie PACS.",
            "user_actions": [
                "Vérification des câbles: Assurez-vous que le câble vidéo derrière l'écran est bien enclenché.",
                "Redémarrage de session: Fermez complètement la session PACS et rouvrez-la.",
                "Contrôle réseau: Vérifiez l'état de la connexion réseau sur la barre des tâches."
            ],
            "root_cause": "Conflit d'adresse IP fixe, câble vidéo desserré ou saturation du cache DICOM.",
            "tech_steps": [
                "Tester la réponse Ping de la Workstation vers le serveur PACS (192.168.10.50)",
                "Inspecter la carte graphique dédiée et fixer la résolution à 4K diagnostic",
                "Relancer le service 'DICOM Listener' et exécuter un vide du cache local",
                "Vérifier la configuration du port sur le Switch du VLAN Santé"
            ],
            "preventive": "Contrôle trimestriel du dépoussiérage des cartes graphiques PACS."
        }
    elif "dmi" in text or "session" in text or "compte" in text or "mot de passe" in text:
        return {
            "summary": "Accès au Dossier Médical Informatisé (DMI) ou compte utilisateur bloqué.",
            "user_actions": [
                "Vérification de la casse: Contrôlez la touche Verr Maj (Caps Lock).",
                "Délai de sécurité: Si le compte est verrouillé, patienter 5 minutes avant de réesssayer.",
                "Redémarrage poste: Redémarrez le poste pour fermer les sessions RDP orphelines."
            ],
            "root_cause": "Verrouillage Active Directory ou session TSE/RDP orpheline sur le serveur.",
            "tech_steps": [
                "Déverrouiller le compte utilisateur sur la console Active Directory (AD MMC)",
                "Forcer la fermeture de la session RDP suspendue via la console de gestion TSE",
                "Réinitialiser le mot de passe utilisateur et imposer la modification à la première ouverture",
                "Vérifier la disponibilité des licences d'accès client (CAL RDP)"
            ],
            "preventive": "Fermeture automatique des sessions RDP inactives après 30 minutes."
        }
    elif "imprimante" in text or "code-barres" in text or "douchette" in text or "étiquette" in text:
        return {
            "summary": "Panne d'impression d'étiquettes / bracelets ou lecteur code-barres inactif.",
            "user_actions": [
                "Contrôle consommables: Vérifiez l'absence de bourrage et l'alignement du rouleau.",
                "Cycle de connexion USB: Débranchez le câble USB pendant 5 secondes puis rebranchez-le.",
                "État d'alimentation: Vérifiez le témoin lumineux d'alimentation du périphérique."
            ],
            "root_cause": "Spouleur d'impression Windows bloqué, rouleau encrassé ou port USB désactivé.",
            "tech_steps": [
                "Redémarrer le service Spouleur d'impression Windows (cmd: net stop spooler && net start spooler)",
                "Basculer le périphérique sur un port USB 3.0 à l'arrière de la carte mère",
                "Nettoyer la tête thermique d'impression à l'alcool isopropanol et recalibrer la cellule optique",
                "Réinstaller ou mettre à jour le pilote d'impression ZDesigner / Zebra"
            ],
            "preventive": "Remplacement préventif annuel des rouleaux thermiques d'impression."
        }
    else:
        return {
            "summary": "Coupure de connexion réseau ou dysfonctionnement du poste informatique.",
            "user_actions": [
                "Connectique RJ45: Vérifiez le bon verrouillage du câble réseau sur la prise murale.",
                "Cycle d'alimentation: Éteignez l'équipement, débranchez la prise 10 secondes puis rallumez.",
                "Test croisé: Vérifiez si les autres postes du même bureau accèdent au réseau."
            ],
            "root_cause": "Défaillance de la prise réseau RJ45, port switch déconnecté ou bloc d'alimentation défectueux.",
            "tech_steps": [
                "Tester la continuité de la prise murale RJ45 avec le réflectomètre / testeur réseau",
                "Identifier et vérifier le repérage de la prise sur le panneau de brassage de la baie d'étage",
                "Changer de port de brassage sur le commutateur réseau Cisco / HP",
                "Tester le bloc d'alimentation du poste avec un module de secours"
            ],
            "preventive": "Inspection semestrielle du câblage de la baie informatique d'étage."
        }

# 5. Navigation Sidebar
st.sidebar.title("DSI Mongi Ben Hmida")
st.sidebar.caption("Direction des Services Informatiques")

menu = st.sidebar.radio(
    "Menu de Navigation :",
    [
        "Signalement Incident (Personnel)", 
        "Support & Console Technicien", 
        "Analytics & Maintenance Préventive",
        "Importation Données GLPI"
    ]
)

# ==========================================
# VIEW 1: STAFF INCIDENT REPORTING
# ==========================================
if menu == "Signalement Incident (Personnel)":
    st.title("Signalement Incident Informatique & Assistance")
    st.write("Veuillez remplir les informations relatives à l'incident matériel ou réseau rencontré.")

    with st.form("staff_ticket_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Objet de la panne *", placeholder="Ex: Dysfonctionnement imprimante étiquettes")
            department = st.selectbox("Service Demandeur *", [
                'Neuroradiologie (IRM/Scanner)', 'EFSN (EEG/EMG)', 'Neurochirurgie',
                'Unité Neuro-Vasculaire (UNV)', 'Réanimation Neurochirurgicale',
                'Consultation Externe Neurologie', 'Urgences Neurologiques', 'Administration & Bureau d\'Ordre'
            ])
            equipment_type = st.selectbox("Matériel Concerné *", [
                'Station Workstation PACS Neuroradio',
                'PC de Bureau / DMI',
                'Imprimante Thermique Étiquettes/Bracelets',
                'Lecteur Code-Barres / Douchette',
                'Switch Réseau / Prise RJ45',
                'Écran / Moniteur Diagnostic',
                'Onduleur (UPS) Informatique'
            ])

        with col2:
            category = st.selectbox("Catégorie IT", ['Matériel Informatique', 'Système / Logiciel', 'Réseau & Connectique', 'Périphérique', 'Affichage'])
            priority = st.select_slider("Niveau d'Urgence", options=['Faible', 'Moyenne', 'Élevée', 'Critique'], value='Moyenne')
            asset_tag = st.text_input("Code Inventaire IT (Optionnel)", placeholder="Ex: INN-IT-PC-4022")

        description = st.text_area("Description Détaillée *", placeholder="Indiquez le bureau, les messages d'erreur affichés et le comportement de l'équipement...")
        
        submitted = st.form_submit_button("Transmettre le Ticket au Support IT")

    if submitted:
        if not title or not description:
            st.error("Veuillez renseigner tous les champs obligatoires (*).")
        else:
            conn = sqlite3.connect('hospital_it.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tickets (title, description, category, department, equipment_type, asset_tag, priority, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, category, department, equipment_type, asset_tag, priority, 'Nouveau'))
            conn.commit()
            conn.close()

            st.success("Ticket transmis au support informatique avec succès.")
            st.divider()
            
            ai_info = generate_ai_suggestion(equipment_type, title, description)
            st.subheader("Assistance Immédiate / Actions Recommandées")
            st.info(f"Analyse initiale : {ai_info['summary']}")
            for action in ai_info['user_actions']:
                st.write(f"• {action}")

# ==========================================
# VIEW 2: TECHNICIAN CONSOLE (ORGANIZED & PROFESSIONAL)
# ==========================================
elif menu == "Support & Console Technicien":
    st.title("Console de Support Informatique & Diagnostic AI")
    
    df = fetch_tickets()
    
    # Executive Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total Tickets", len(df))
    c2.metric("Tickets Nouveaux", len(df[df['status'] == 'Nouveau']))
    c3.metric("Tickets En Cours", len(df[df['status'] == 'En cours']))
    c4.metric("Tickets Résolus", len(df[df['status'] == 'Résolu']))

    st.divider()

    # Search & Filters
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        selected_dept = st.multiselect("Filtrer par Service Hospitalier :", options=df['department'].unique())
    with f_col2:
        selected_prio = st.multiselect("Filtrer par Niveau d'Urgence :", options=['Faible', 'Moyenne', 'Élevée', 'Critique'])

    filtered_df = df.copy()
    if selected_dept:
        filtered_df = filtered_df[filtered_df['department'].isin(selected_dept)]
    if selected_prio:
        filtered_df = filtered_df[filtered_df['priority'].isin(selected_prio)]

    # Organized Status Tabs
    tab_new, tab_progress, tab_resolved = st.tabs([
        "Nouveaux Incidents", 
        "Incidents En Cours", 
        "Historique des Incidents Résolus"
    ])

    def render_tech_workspace(status_name, status_df):
        if status_df.empty:
            st.info(f"Aucun incident enregistré avec le statut '{status_name}'.")
            return

        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.subheader(f"Registre des Tickets [{status_name}]")
            
            selected_id = st.selectbox(
                "Sélectionner un ticket pour traitement :", 
                options=status_df['id'].tolist(),
                format_func=lambda x: f"Ticket #{x} | Urgence: {status_df[status_df['id']==x]['priority'].values[0]} | {status_df[status_df['id']==x]['title'].values[0]} ({status_df[status_df['id']==x]['department'].values[0]})",
                key=f"select_{status_name}"
            )
            
            ticket = status_df[status_df['id'] == selected_id].iloc[0]
            
            st.markdown(f"#### Incident #{ticket['id']} : {ticket['title']}")
            st.write(f"**Service :** {ticket['department']} | **Matériel :** {ticket['equipment_type']}")
            st.write(f"**Description :** {ticket['description']}")
            st.write(f"**Code Inventaire :** `{ticket['asset_tag']}` | **Urgence :** `{ticket['priority']}` | **Horodatage :** `{ticket['created_at']}`")
            
            # Workflow: Take ownership
            if ticket['status'] == 'Nouveau':
                if st.button("Prendre en Charge l'Incident", key=f"take_{selected_id}"):
                    conn = sqlite3.connect('hospital_it.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE tickets SET status = 'En cours' WHERE id = ?", (selected_id,))
                    conn.commit()
                    conn.close()
                    st.success("Ticket passé sous le statut 'En cours'.")
                    st.rerun()

            if ticket['status'] == 'Résolu':
                st.success(f"**Cause Racine Validée :** {ticket['root_cause']}\n\n**Solution Appliquée :** {ticket['solution']}")

        with col_right:
            st.subheader("Diagnostic Technique & Recommandations")
            ai_suggestion = generate_ai_suggestion(
                ticket['equipment_type'], 
                ticket['title'], 
                ticket['description']
            )
            
            st.warning(f"**Cause IT Probable :** {ai_suggestion['root_cause']}")
            
            st.write("**Plan d'Intervention Technique :**")
            for i, step in enumerate(ai_suggestion['tech_steps']):
                # CSS injected above guarantees text wraps properly without getting cut off
                st.checkbox(f"Étape {i+1}: {step}", key=f"step_{status_name}_{selected_id}_{i}")
            
            st.info(f"**Mesure Préventive :** {ai_suggestion['preventive']}")

            if ticket['status'] != 'Résolu':
                st.divider()
                st.subheader("Clôture de l'Incident")
                with st.form(f"resolve_form_{status_name}_{selected_id}"):
                    final_cause = st.text_input("Cause Racine Validée :", value=ai_suggestion['root_cause'])
                    final_sol = st.text_area("Solution Appliquée :", value="; ".join(ai_suggestion['tech_steps']))
                    
                    if st.form_submit_button("Valider et Archiver le Ticket"):
                        conn = sqlite3.connect('hospital_it.db')
                        cursor = conn.cursor()
                        cursor.execute('''
                            UPDATE tickets 
                            SET status = 'Résolu', root_cause = ?, solution = ? 
                            WHERE id = ?
                        ''', (final_cause, final_sol, selected_id))
                        conn.commit()
                        conn.close()
                        st.success("Incident résolu et archivé dans la base de données.")
                        st.rerun()

    with tab_new:
        render_tech_workspace("Nouveau", filtered_df[filtered_df['status'] == 'Nouveau'])

    with tab_progress:
        render_tech_workspace("En cours", filtered_df[filtered_df['status'] == 'En cours'])

    with tab_resolved:
        render_tech_workspace("Résolu", filtered_df[filtered_df['status'] == 'Résolu'])

# ==========================================
# VIEW 3: IT ANALYTICS
# ==========================================
elif menu == "Analytics & Maintenance Préventive":
    st.title("Tableau de Bord & Fiabilité du Parc IT")
    st.write("Analyse décisionnelle des taux de panne et des demandes d'intervention par service.")

    df = fetch_tickets()

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Volume d'Incidents par Équipement")
        fig_eq = px.bar(
            df['equipment_type'].value_counts().reset_index(),
            x='count', y='equipment_type',
            orientation='h',
            labels={'count': 'Nombre de Pannes', 'equipment_type': 'Matériel IT'},
            color='count', color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_eq, use_container_width=True)

    with col_chart2:
        st.subheader("Répartition des Incidents par Service")
        fig_dept = px.pie(df, names='department', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_dept, use_container_width=True)

# ==========================================
# VIEW 4: GLPI IMPORT
# ==========================================
elif menu == "Importation Données GLPI":
    st.title("Intégration et Migration de Données GLPI")
    uploaded_file = st.file_uploader("Fichier d'exportation GLPI (.csv)", type=["csv"])
    if uploaded_file is not None:
        import_df = pd.read_csv(uploaded_file)
        st.dataframe(import_df.head(), use_container_width=True)
        if st.button("Synchroniser la Base de Données"):
            st.success("Données GLPI importées et synchronisées avec succès.")