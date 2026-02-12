import streamlit as st
import pandas as pd
import re
from datetime import datetime
import json

# Importer Ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

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
    """Convertit une valeur entre différentes unités biochimiques"""
    
    # Étape 1 : Convertir vers mol/L (unité de base)
    if from_unit in ["µmol/L", "umol/L"]:
        mol_per_L = value * 1e-6
    elif from_unit == "mmol/L":
        mol_per_L = value * 1e-3
    elif from_unit == "g/L":
        mol_per_L = value / molar_mass
    elif from_unit == "mg/dL":
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
        g_per_L = mol_per_L * molar_mass
        return g_per_L * 100
    else:
        return None

# Fonction pour extraire les infos avec l'IA
def extract_with_ai(user_input, data):
    """Utilise Ollama pour extraire analyte, valeur et unités depuis texte naturel"""
    
    # Créer le contexte avec les analytes disponibles
    analytes_list = ", ".join(data["analyte"].tolist())
    units_list = "µmol/L, mmol/L, mg/dL, g/L"
    
    prompt = f"""Tu es un assistant de laboratoire médical. Analyse cette phrase et extrais les informations suivantes.

Phrase de l'utilisateur : "{user_input}"

Analytes disponibles : {analytes_list}
Unités disponibles : {units_list}

Réponds UNIQUEMENT avec un JSON valide (sans markdown, sans backticks, sans texte supplémentaire) au format :
{{
  "analyte": "nom de l'analyte détecté (en minuscules, avec underscore si besoin)",
  "value": nombre (float),
  "unit_from": "unité d'origine",
  "unit_to": "unité cible si mentionnée, sinon null"
}}

Si l'information n'est pas claire ou manquante, mets null pour ce champ.
Exemples :
- "Convertis 200 de cholestérol en mmol" → {{"analyte": "cholesterol", "value": 200, "unit_from": "mg/dL", "unit_to": "mmol/L"}}
- "Creatinine 19243 µmol/L" → {{"analyte": "creatinine", "value": 19243, "unit_from": "µmol/L", "unit_to": null}}
- "Quelle est la masse molaire de glucose" → {{"analyte": "glucose", "value": null, "unit_from": null, "unit_to": null}}
"""
    
    try:
        # Appeler Ollama
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        # Extraire le contenu
        content = response['message']['content'].strip()
        
        # Nettoyer le contenu (enlever markdown si présent)
        content = content.replace('```json', '').replace('```', '').strip()
        
        # Parser le JSON
        result = json.loads(content)
        
        return result
        
    except Exception as e:
        st.error(f"Erreur IA : {str(e)}")
        return None

# Interface principale
st.title("🧪 Labo AI Converter Pro")
st.markdown("**Application d'aide à la conversion biochimique avec IA** | ⚠️ Outil non décisionnel")

# Sélecteur de mode
if OLLAMA_AVAILABLE:
    mode = st.radio(
        "Mode de fonctionnement",
        ["🔢 Mode Standard", "🤖 Mode IA (langage naturel)"],
        horizontal=True
    )
else:
    mode = "🔢 Mode Standard"
    st.info("💡 Installez Ollama pour activer le mode IA")

st.markdown("---")

# Créer deux colonnes principales
col_main, col_history = st.columns([2, 1])

# COLONNE PRINCIPALE - Conversion
with col_main:
    
    try:
        # Charger les données
        data = load_scientific_data()
        
        # MODE IA
        if mode == "🤖 Mode IA (langage naturel)" and OLLAMA_AVAILABLE:
            st.subheader("🤖 Conversion avec IA")
            
            st.markdown("""
            **Exemples de phrases :**
            - "Convertis 200 de cholestérol en mmol"
            - "Creatinine 19243 µmol/L vers g/L"
            - "Je veux convertir 90 mg/dL de glucose en mmol/L"
            - "Quelle est la masse molaire de l'urée ?"
            """)
            
            ai_input = st.text_area(
                "Posez votre question en langage naturel :",
                height=100,
                placeholder="Ex: Convertis 200 de cholestérol de mg/dL vers mmol/L"
            )
            
            if st.button("🤖 Analyser avec l'IA", type="primary", use_container_width=True):
                if ai_input:
                    with st.spinner("🧠 L'IA analyse votre demande..."):
                        extracted = extract_with_ai(ai_input, data)
                        
                        if extracted:
                            st.success("✅ Demande comprise par l'IA")
                            
                            # Afficher ce qui a été détecté
                            with st.expander("🔍 Détection IA"):
                                st.json(extracted)
                            
                            # Vérifier si c'est une question sur la masse molaire
                            if extracted.get('value') is None:
                                analyte = extracted.get('analyte')
                                if analyte and analyte in data['analyte'].values:
                                    analyte_info = data[data['analyte'] == analyte].iloc[0]
                                    st.info(f"""
                                    **{analyte.replace('_', ' ').capitalize()}**
                                    - Masse molaire : **{analyte_info['molar_mass']} g/mol**
                                    - Source : {analyte_info['source']}
                                    """)
                                else:
                                    st.warning("Analyte non reconnu")
                            
                            # Sinon faire la conversion
                            elif extracted.get('analyte') and extracted.get('value') and extracted.get('unit_from'):
                                analyte = extracted['analyte']
                                value = extracted['value']
                                from_unit = extracted['unit_from']
                                to_unit = extracted.get('unit_to')
                                
                                # Vérifier que l'analyte existe
                                if analyte in data['analyte'].values:
                                    analyte_info = data[data['analyte'] == analyte].iloc[0]
                                    molar_mass = float(analyte_info['molar_mass'])
                                    source = analyte_info['source']
                                    available_units = analyte_info['common_units'].split(';')
                                    
                                    # Si pas d'unité cible, proposer
                                    if not to_unit:
                                        st.warning("⚠️ Unité cible non spécifiée")
                                        to_unit = st.selectbox("Choisissez l'unité cible :", available_units)
                                        
                                        if st.button("Convertir"):
                                            result = convert_units(value, from_unit, to_unit, molar_mass)
                                            if result:
                                                st.success(f"✅ **Résultat : {result:.4f} {to_unit}**")
                                    else:
                                        # Conversion directe
                                        result = convert_units(value, from_unit, to_unit, molar_mass)
                                        
                                        if result is not None:
                                            st.success(f"✅ **Résultat : {result:.4f} {to_unit}**")
                                            
                                            # Ajouter à l'historique
                                            st.session_state.history.insert(0, {
                                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                "analyte": analyte.replace("_", " ").capitalize(),
                                                "value_input": value,
                                                "unit_from": from_unit,
                                                "value_output": round(result, 4),
                                                "unit_to": to_unit,
                                                "molar_mass": molar_mass,
                                                "source": source
                                            })
                                            
                                            if len(st.session_state.history) > 50:
                                                st.session_state.history = st.session_state.history[:50]
                                            
                                            st.rerun()
                                        else:
                                            st.error("❌ Conversion impossible")
                                else:
                                    st.error(f"❌ Analyte '{analyte}' non trouvé dans la base")
                            else:
                                st.warning("⚠️ Informations incomplètes détectées")
                        else:
                            st.error("❌ Impossible d'analyser la demande")
                else:
                    st.warning("⚠️ Veuillez entrer une question")
        
        # MODE STANDARD
        else:
            st.subheader("📊 Nouvelle conversion")
            
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
                st.write("")
                st.write("")
                to_unit = st.selectbox("Unité cible", available_units, key="to")
            
            # Bouton de calcul
            if st.button("🔄 Convertir", type="primary", use_container_width=True):
                if from_unit == to_unit:
                    st.warning("⚠️ Les unités d'origine et cible sont identiques")
                else:
                    result = convert_units(value_input, from_unit, to_unit, molar_mass)
                    
                    if result is not None:
                        st.success(f"✅ **Résultat : {result:.4f} {to_unit}**")
                        
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
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🗑️ Effacer", use_container_width=True):
                st.session_state.history = []
                st.rerun()
        
        with col_btn2:
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
if OLLAMA_AVAILABLE:
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.85em;'>
    ⚠️ <b>Disclaimer</b> : Outil d'aide interne non décisionnel<br>
    🤖 IA locale activée (Ollama + Llama 3.2) - Aucune donnée envoyée en ligne<br>
    Respecte les principes ISO 15189 pour usage en laboratoire médical
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.85em;'>
    ⚠️ <b>Disclaimer</b> : Outil d'aide interne non décisionnel<br>
    Respecte les principes ISO 15189 pour usage en laboratoire médical
    </div>
    """, unsafe_allow_html=True)
