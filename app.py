import streamlit as st
import pandas as pd
import re
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Labo AI Converter Pro", 
    page_icon="🧪",
    layout="wide"
)

# Charger la base scientifique
@st.cache_data
def load_scientific_data():
    return pd.read_csv("scientific_data.csv")

# Initialiser l'historique dans la session
if 'history' not in st.session_state:
    st.session_state.history = []

# Fonction de conversion entre unités
def convert_units(value, from_unit, to_unit, molar_mass):
    """
    Convertit une valeur entre différentes unités biochimiques
    Passage par mol/L comme unité intermédiaire
    """
    
    # Étape 1 : Convertir vers mol/L (unité de base)
    if from_unit in ["µmol/L", "umol/L"]:
        mol_per_L = value * 1e-6
    elif from_unit == "mmol/L":
        mol_per_L = value * 1e-3
    elif from_unit == "g/L":
        mol_per_L = value / molar_mass
    elif from_unit == "mg/dL":
        # mg/dL → g/L → mol/L
        g_per_L = value / 100
        mol_per_L = g_per_L / molar_mass
    else:
        return None
    
    # Étape 2 : Convertir de mol/L vers l'unité cible
    if to_unit in ["µmol/L", "umol/L"]:
        return mol_per_L * 1e6
    elif to_unit == "mmol/L":
        return mol_per_L * 1e3
    elif to_unit == "g/L":
        return mol_per_L * molar_mass
    elif to_unit == "mg/dL":
        # mol/L → g/L → mg/dL
        g_per_L = mol_per_L * molar_mass
        return g_per_L * 100
    else:
        return None

# Interface principale
st.title("🧪 Labo AI Converter Pro")
st.markdown("**Application d'aide à la conversion biochimique** | ⚠️ Outil non décisionnel")
st.markdown("---")

# Créer deux colonnes principales
col_main, col_history = st.columns([2, 1])

# COLONNE PRINCIPALE - Conversion
with col_main:
    st.subheader("📊 Nouvelle conversion")
    
    try:
        # Charger les données
        data = load_scientific_data()
        
        # Sélection de l'analyte
        analyte = st.selectbox(
            "🔬 Sélectionnez l'analyte",
            options=data["analyte"].tolist(),
            format_func=lambda x: x.replace("_", " ").capitalize()
        )
        
        # Récupérer les informations de l'analyte sélectionné
        analyte_info = data[data["analyte"] == analyte].iloc[0]
        molar_mass = float(analyte_info["molar_mass"])
        source = analyte_info["source"]
        available_units = analyte_info["common_units"].split(";")
        
        # Afficher la masse molaire
        st.info(f"📐 **Masse molaire : {molar_mass} g/mol** (Source : {source})")
        
        # Inputs de conversion
        col_input1, col_input2 = st.columns(2)
        
        with col_input1:
            st.markdown("**Valeur d'entrée**")
            value_input = st.number_input(
                "Valeur mesurée",
                min_value=0.0,
                value=100.0,
                step=0.01,
                format="%.4f",
                label_visibility="collapsed"
            )
            from_unit = st.selectbox("Unité d'origine", available_units, key="from")
        
        with col_input2:
            st.markdown("**Conversion vers**")
            st.write("")  # Espacement
            st.write("")  # Espacement
            to_unit = st.selectbox("Unité cible", available_units, key="to")
        
        # Bouton de calcul
        if st.button("🔄 Convertir", type="primary", use_container_width=True):
            if from_unit == to_unit:
                st.warning("⚠️ Les unités d'origine et cible sont identiques")
            else:
                result = convert_units(value_input, from_unit, to_unit, molar_mass)
                
                if result is not None:
                    # Affichage du résultat
                    st.success(f"✅ **Résultat : {result:.4f} {to_unit}**")
                    
                    # Détails du calcul dans un expander
                    with st.expander("📐 Voir les détails du calcul"):
                        st.markdown(f"""
                        **Analyte :** {analyte.replace("_", " ").capitalize()}  
                        **Masse molaire :** {molar_mass} g/mol  
                        **Conversion :** {value_input} {from_unit} → {result:.4f} {to_unit}  
                        **Source :** {source}  
                        **Date :** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
                        
                        **Méthode :** Conversion via mol/L comme unité intermédiaire
                        """)
                    
                    # Ajouter à l'historique
                    st.session_state.history.insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "analyte": analyte.replace("_", " ").capitalize(),
                        "value_input": value_input,
                        "unit_from": from_unit,
                        "value_output": round(result, 4),
                        "unit_to": to_unit,
                        "molar_mass": molar_mass,
                        "source": source
                    })
                    
                    # Limiter l'historique à 50 entrées
                    if len(st.session_state.history) > 50:
                        st.session_state.history = st.session_state.history[:50]
                    
                    st.rerun()
                else:
                    st.error("❌ Erreur de conversion")
    
    except FileNotFoundError:
        st.error("❌ **Erreur** : Le fichier `scientific_data.csv` est introuvable.")
        st.info("Vérifiez qu'il est bien dans le même dossier que app.py")
    except Exception as e:
        st.error(f"❌ **Erreur** : {str(e)}")

# COLONNE HISTORIQUE
with col_history:
    st.subheader("📜 Historique")
    
    if len(st.session_state.history) > 0:
        # Boutons d'action
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🗑️ Effacer", use_container_width=True):
                st.session_state.history = []
                st.rerun()
        
        with col_btn2:
            # Export CSV
            df_history = pd.DataFrame(st.session_state.history)
            csv = df_history.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Export",
                data=csv,
                file_name=f"historique_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Afficher les 10 dernières conversions
        for idx, entry in enumerate(st.session_state.history[:10]):
            with st.container():
                st.markdown(f"""
                **{entry['analyte']}**  
                `{entry['value_input']} {entry['unit_from']}` → **`{entry['value_output']} {entry['unit_to']}`**  
                🕐 {entry['timestamp'].split()[1]}
                """)
                if idx < min(9, len(st.session_state.history) - 1):
                    st.markdown("---")
        
        if len(st.session_state.history) > 10:
            st.info(f"📊 +{len(st.session_state.history) - 10} conversion(s)")
    else:
        st.info("Aucune conversion effectuée")
        st.markdown("Les conversions apparaîtront ici automatiquement")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.85em;'>
⚠️ <b>Disclaimer</b> : Outil d'aide interne non décisionnel<br>
Respecte les principes ISO 15189 pour usage en laboratoire médical<br>
Développé pour améliorer la qualité des conversions biochimiques
</div>
""", unsafe_allow_html=True)
