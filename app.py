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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS - DESIGN PROFESSIONNEL
# ============================================================================

st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
    }
    
    /* Header Gradient */
    .header-container {
        background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%);
        padding: 2rem 2rem 2.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.2);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .header-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        backdrop-filter: blur(10px);
    }
    
    /* Card Styles */
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0, 102, 204, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.15);
    }
    
    .card-header {
        color: #0066CC;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 1rem 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #0066CC;
        margin: 1rem 0;
    }
    
    .info-box-text {
        color: #1565C0;
        font-size: 0.95rem;
        margin: 0;
        font-weight: 500;
    }
    
    /* Success Box */
    .success-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #00AA66;
        margin: 1.5rem 0;
    }
    
    .success-title {
        color: #00AA66;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .success-result {
        color: #2E7D32;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    /* History Item */
    .history-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
        border-left: 3px solid #0066CC;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .history-analyte {
        color: #0066CC;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .history-conversion {
        color: #2C3E50;
        font-size: 0.95rem;
        margin: 0.3rem 0;
    }
    
    .history-time {
        color: #7F8C8D;
        font-size: 0.85rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3);
        background: linear-gradient(135deg, #0052A3 0%, #003D7A 100%);
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #00AA66 0%, #008850 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 170, 102, 0.3);
    }
    
    /* Input Fields */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #E0E7EF;
        transition: border-color 0.3s;
    }
    
    .stSelectbox > div > div:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #0066CC;
        box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
    }
    
    /* Radio Buttons */
    .stRadio > label {
        background: white;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        border: 2px solid #E0E7EF;
        margin-right: 1rem;
        transition: all 0.3s;
    }
    
    .stRadio > label:hover {
        border-color: #0066CC;
        background: #F0F7FF;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #F8FAFB;
        border-radius: 8px;
        border: 1px solid #E0E7EF;
        font-weight: 600;
        color: #2C3E50;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Mode Badge */
    .mode-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .mode-standard {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        color: #0066CC;
    }
    
    .mode-ai {
        background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
        color: #7B1FA2;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="header-container">
    <h1 class="header-title">🧪 Labo AI Converter Pro</h1>
    <p class="header-subtitle">Application professionnelle de conversion d'unités biochimiques</p>
    <span class="header-badge">✅ 42 tests | ISO 15189 | 100% Offline</span>
</div>
""", unsafe_allow_html=True)

# Charger la base scientifique
@st.cache_data
def load_scientific_data():
    return pd.read_csv("data/scientific_data.csv")

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

Si l'information n'est pas claire ou manquante, mets null pour ce champ."""
    
    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        content = response['message']['content'].strip()
        content = content.replace('```json', '').replace('```', '').strip()
        result = json.loads(content)
        
        return result
        
    except Exception as e:
        st.error(f"Erreur IA : {str(e)}")
        return None

# Sélecteur de mode
if OLLAMA_AVAILABLE:
    mode = st.radio(
        "",
        ["🔢 Mode Standard", "🤖 Mode IA (langage naturel)"],
        horizontal=True
    )
else:
    mode = "🔢 Mode Standard"
    st.info("💡 **Installez Ollama** pour activer le mode IA avec compréhension du langage naturel")

# ============================================================================
# MAIN LAYOUT
# ============================================================================

# Créer deux colonnes principales
col_main, col_history = st.columns([2, 1])

# COLONNE PRINCIPALE - Conversion
with col_main:
    
    try:
        # Charger les données
        data = load_scientific_data()
        
        # MODE IA
        if mode == "🤖 Mode IA (langage naturel)" and OLLAMA_AVAILABLE:
            
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">🤖 Conversion avec Intelligence Artificielle</div>', unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
                <p class="info-box-text">
                    💡 <strong>Exemples de phrases :</strong><br>
                    • "Convertis 200 de cholestérol en mmol"<br>
                    • "Creatinine 19243 µmol/L vers g/L"<br>
                    • "Quelle est la masse molaire de l'urée ?"
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            ai_input = st.text_area(
                "💬 Posez votre question en langage naturel :",
                height=100,
                placeholder="Ex: Convertis 200 de cholestérol de mg/dL vers mmol/L"
            )
            
            if st.button("🤖 Analyser avec l'IA", type="primary", use_container_width=True):
                if ai_input:
                    with st.spinner("🧠 L'IA analyse votre demande..."):
                        extracted = extract_with_ai(ai_input, data)
                        
                        if extracted:
                            # Vérifier si c'est une question sur la masse molaire
                            if extracted.get('value') is None:
                                analyte = extracted.get('analyte')
                                if analyte and analyte in data['analyte'].values:
                                    analyte_info = data[data['analyte'] == analyte].iloc[0]
                                    st.markdown(f"""
                                    <div class="info-box">
                                        <p class="info-box-text">
                                            <strong>{analyte.replace('_', ' ').capitalize()}</strong><br>
                                            📐 Masse molaire : <strong>{analyte_info['molar_mass']} g/mol</strong><br>
                                            📚 Source : {analyte_info['source']}
                                        </p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            # Faire la conversion
                            elif extracted.get('analyte') and extracted.get('value') and extracted.get('unit_from'):
                                analyte = extracted['analyte']
                                value = extracted['value']
                                from_unit = extracted['unit_from']
                                to_unit = extracted.get('unit_to')
                                
                                if analyte in data['analyte'].values:
                                    analyte_info = data[data['analyte'] == analyte].iloc[0]
                                    molar_mass = float(analyte_info['molar_mass'])
                                    source = analyte_info['source']
                                    
                                    if to_unit:
                                        result = convert_units(value, from_unit, to_unit, molar_mass)
                                        
                                        if result is not None:
                                            st.markdown(f"""
                                            <div class="success-box">
                                                <div class="success-title">✅ Résultat de la conversion</div>
                                                <div class="success-result">{result:.4f} {to_unit}</div>
                                                <p style="color: #2E7D32; margin-top: 0.5rem;">
                                                    {analyte.replace("_", " ").capitalize()} : {value} {from_unit} → {result:.4f} {to_unit}
                                                </p>
                                            </div>
                                            """, unsafe_allow_html=True)
                                            
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
                    st.warning("⚠️ Veuillez entrer une question")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # MODE STANDARD
        else:
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-header">📊 Nouvelle conversion</div>', unsafe_allow_html=True)
            
            # Sélection de l'analyte
            analyte = st.selectbox(
                "🔬 Sélectionnez l'analyte",
                options=data["analyte"].tolist(),
                format_func=lambda x: x.replace("_", " ").capitalize()
            )
            
            # Récupérer les informations
            analyte_info = data[data["analyte"] == analyte].iloc[0]
            molar_mass = float(analyte_info["molar_mass"])
            source = analyte_info["source"]
            available_units = analyte_info["common_units"].split(";")
            
            # Afficher la masse molaire
            st.markdown(f"""
            <div class="info-box">
                <p class="info-box-text">
                    📐 <strong>Masse molaire : {molar_mass} g/mol</strong> | 📚 Source : {source}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Inputs de conversion
            col_input1, col_input2 = st.columns(2)
            
            with col_input1:
                st.markdown("**💉 Valeur d'entrée**")
                value_input = st.number_input(
                    "Valeur mesurée",
                    min_value=0.0,
                    value=100.0,
                    step=0.01,
                    format="%.4f",
                    label_visibility="collapsed"
                )
                from_unit = st.selectbox("🔄 Unité d'origine", available_units, key="from")
            
            with col_input2:
                st.markdown("**🎯 Conversion vers**")
                st.write("")
                st.write("")
                to_unit = st.selectbox("🎯 Unité cible", available_units, key="to")
            
            # Bouton de calcul
            if st.button("🔄 Convertir", type="primary", use_container_width=True):
                if from_unit == to_unit:
                    st.warning("⚠️ Les unités d'origine et cible sont identiques")
                else:
                    result = convert_units(value_input, from_unit, to_unit, molar_mass)
                    
                    if result is not None:
                        st.markdown(f"""
                        <div class="success-box">
                            <div class="success-title">✅ Résultat de la conversion</div>
                            <div class="success-result">{result:.4f} {to_unit}</div>
                            <p style="color: #2E7D32; margin-top: 0.5rem;">
                                {analyte.replace("_", " ").capitalize()} : {value_input} {from_unit} → {result:.4f} {to_unit}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
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
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    except FileNotFoundError:
        st.error("❌ **Erreur** : Le fichier `data/scientific_data.csv` est introuvable.")
    except Exception as e:
        st.error(f"❌ **Erreur** : {str(e)}")

# COLONNE HISTORIQUE
with col_history:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">📜 Historique des conversions</div>', unsafe_allow_html=True)
    
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
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Afficher les 10 dernières conversions
        for idx, entry in enumerate(st.session_state.history[:10]):
            st.markdown(f"""
            <div class="history-item">
                <div class="history-analyte">{entry['analyte']}</div>
                <div class="history-conversion">
                    {entry['value_input']} {entry['unit_from']} → <strong>{entry['value_output']} {entry['unit_to']}</strong>
                </div>
                <div class="history-time">🕐 {entry['timestamp'].split()[1]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        if len(st.session_state.history) > 10:
            st.info(f"📊 +{len(st.session_state.history) - 10} conversion(s)")
    else:
        st.info("Aucune conversion effectuée pour le moment")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 2rem; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);'>
    <p style='color: #7F8C8D; font-size: 0.9rem; margin: 0;'>
        ⚠️ <b>Disclaimer</b> : Outil d'aide interne non décisionnel<br>
        Respecte les principes ISO 15189 pour usage en laboratoire médical<br>
        🧪 Développé avec ❤️ pour la communauté des laboratoires cliniques
    </p>
</div>
""", unsafe_allow_html=True)
