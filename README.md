# 🧪 Labo AI Converter Pro

**Professional Biochemical Unit Conversion Application with AI Integration**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Scientific Foundation](#scientific-foundation)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Future Developments](#future-developments)
- [Author](#author)

---

## 🎯 Overview

**Labo AI Converter Pro** is a local AI-powered application designed for clinical biochemistry laboratories to automate and standardize unit conversions between different measurement systems.

This project addresses a critical need in medical laboratories: **reducing human error in biochemical unit conversions** while maintaining full compliance with ISO 15189 quality standards.

### 🏥 Context

In clinical laboratories, biochemical results are reported in various units (µmol/L, mmol/L, mg/dL, g/L) depending on regional standards and laboratory equipment. Manual conversions are time-consuming and error-prone. This application provides:

- ✅ **Automated multi-unit conversions** based on validated molar masses
- ✅ **Traceability** through calculation history and CSV export
- ✅ **Offline operation** for data security compliance
- ✅ **Quality assurance** aligned with ISO 15189 principles

---

## ✨ Key Features

### 🔬 Multi-Analyte Support
- Creatinine
- Urea
- Glucose
- Cholesterol
- Triglycerides
- Bilirubin
- Uric Acid

### 🔄 Intelligent Unit Conversion
Supports conversion between:
- **µmol/L** (micromoles per liter)
- **mmol/L** (millimoles per liter)
- **mg/dL** (milligrams per deciliter)
- **g/L** (grams per liter)

Conversion algorithm uses **mol/L as intermediate unit** for maximum accuracy.

### 📊 Calculation History
- Automatic timestamp recording
- Session-based storage (last 50 conversions)
- CSV export for quality control documentation

### 🛡️ Quality & Compliance
- Source attribution (PubChem - NIH)
- Molar mass validation
- Non-decisional tool disclaimer (ISO 15189)
- Calculation transparency

---

## 🔬 Scientific Foundation

All molar mass values are sourced from **PubChem** (National Institutes of Health):

| Analyte | Molar Mass (g/mol) | Source |
|---------|-------------------|--------|
| Creatinine | 113.12 | [PubChem CID 588](https://pubchem.ncbi.nlm.nih.gov/compound/588) |
| Urea | 60.06 | [PubChem CID 1176](https://pubchem.ncbi.nlm.nih.gov/compound/1176) |
| Glucose | 180.16 | [PubChem CID 5793](https://pubchem.ncbi.nlm.nih.gov/compound/5793) |
| Cholesterol | 386.65 | [PubChem CID 5997](https://pubchem.ncbi.nlm.nih.gov/compound/5997) |
| Triglycerides | 885.43 | Average molecular weight |
| Bilirubin | 584.66 | [PubChem CID 5280352](https://pubchem.ncbi.nlm.nih.gov/compound/5280352) |
| Uric Acid | 168.11 | [PubChem CID 1175](https://pubchem.ncbi.nlm.nih.gov/compound/1175) |

### Conversion Formula

```
mol/L = (value × unit_factor) / molar_mass
result = mol/L × target_unit_factor × molar_mass
```

**Example: Cholesterol 200 mg/dL → mmol/L**
1. Convert to g/L: 200 mg/dL = 2.0 g/L
2. Convert to mol/L: 2.0 / 386.65 = 0.00517 mol/L
3. Convert to mmol/L: 0.00517 × 1000 = 5.17 mmol/L ✅

---

## 🛠️ Technology Stack

- **Python 3.11+** - Core programming language
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and CSV handling
- **Regex** - Text parsing (planned AI integration)

### Why These Technologies?

- **Streamlit**: Rapid development, professional UI, easy deployment
- **Local-first**: No external API dependencies, data remains secure
- **Pandas**: Industry standard for data processing in scientific computing

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/labo-ai-converter.git
cd labo-ai-converter
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`

---

## 🚀 Usage

### Basic Workflow

1. **Select analyte** from dropdown menu
2. **Enter measured value**
3. **Choose origin unit**
4. **Choose target unit**
5. **Click "Convert"** to see results

### Example Conversions

**Example 1: Creatinine**
- Input: 19243 µmol/L
- Output: 2.1767 g/L

**Example 2: Cholesterol**
- Input: 200 mg/dL
- Output: 5.1726 mmol/L

**Example 3: Glucose**
- Input: 90 mg/dL
- Output: 4.9956 mmol/L

### Exporting History

Click the **"📥 Export"** button to download calculation history as CSV for quality control documentation.

---

## 📁 Project Structure

```
Labo_AI_App/
├── app.py                    # Main application
├── scientific_data.csv       # Molar mass database
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── TECHNICAL_DOC.md         # Technical documentation
└── venv/                    # Virtual environment (not committed)
```

---

## 🔮 Future Developments

### Phase 1: AI Integration (In Progress)
- **Ollama** local LLM integration
- Natural language input: *"Convert 200 cholesterol to mmol"*
- Intelligent analyte recognition
- Contextual help and explanations

### Phase 2: Enhanced Features
- Additional analytes (electrolytes, enzymes)
- Batch conversion mode
- PDF report generation
- Multi-language support (French, English, Arabic)

### Phase 3: Deployment
- Docker containerization
- Internal lab network deployment
- User authentication for audit trails
- Database integration for persistent history

---

## 🎓 Academic Context

This project was developed as part of a professional reconversion from clinical biology to data science and artificial intelligence. It demonstrates:

- **Domain expertise**: Deep understanding of clinical laboratory requirements
- **Technical skills**: Python, data processing, web development
- **Quality mindset**: ISO 15189 compliance awareness
- **AI/ML readiness**: Foundation for local LLM integration

### Skills Demonstrated

- ✅ Scientific data validation
- ✅ User interface design
- ✅ Software architecture
- ✅ Quality assurance principles
- ✅ Technical documentation

---

## 👩‍🔬 Author

Takoi RIZGUI
- 🔬 Background: Medical Laboratory Technician
- 🤖 Transition: Data Science & Artificial Intelligence
- 🎯 Goal: Master's program in AI/Data Science (Europe)
- 📧 Contact: [takoirizgui@gmail.com]
- 💼 LinkedIn: [www.linkedin.com/in/takoi-rizgui-094b1a95]
- 🐙 GitHub: [https://github.com/TakoiRizgui]

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**This application is a non-decisional support tool.**

It is designed to assist laboratory professionals in performing unit conversions but does not replace professional judgment or validated laboratory information systems. All results should be verified according to your laboratory's quality management system and ISO 15189 requirements.

---

## 🙏 Acknowledgments

- **PubChem (NIH)** for scientific data
- **Streamlit** community for excellent documentation
- Clinical laboratory colleagues for requirements validation

---

## 📞 Support

For questions, suggestions, or collaboration inquiries:
- Open an issue on GitHub
- Contact via email: [takoirizgui@gmail.com]

---

**Built with ❤️ for the clinical laboratory community**
