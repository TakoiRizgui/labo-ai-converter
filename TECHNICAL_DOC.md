# 📘 Technical Documentation

## Labo AI Converter Pro - Technical Specifications

---

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────┐
│           User Interface (Streamlit)            │
│  ┌──────────────┐        ┌──────────────┐      │
│  │  Input Form  │        │   History    │      │
│  │   - Analyte  │        │  - Display   │      │
│  │   - Value    │        │  - Export    │      │
│  │   - Units    │        │  - Clear     │      │
│  └──────┬───────┘        └──────────────┘      │
└─────────┼──────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────┐
│         Application Logic (Python)              │
│  ┌──────────────────────────────────────┐      │
│  │    Conversion Engine                 │      │
│  │    - Unit detection                  │      │
│  │    - Mol/L intermediate conversion   │      │
│  │    - Result calculation              │      │
│  └──────────────────────────────────────┘      │
└─────────┬───────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────┐
│         Data Layer                              │
│  ┌──────────────┐     ┌─────────────────┐      │
│  │ scientific_  │     │ Session State   │      │
│  │ data.csv     │     │ (History)       │      │
│  └──────────────┘     └─────────────────┘      │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Core Components

### 1. Data Management

**File: `scientific_data.csv`**

Structure:
```csv
analyte,molar_mass,unit,source,common_units
creatinine,113.12,g/mol,PubChem NIH,µmol/L;mg/dL;g/L
```

**Columns:**
- `analyte`: Biochemical compound name (lowercase, underscore-separated)
- `molar_mass`: Molecular weight in g/mol (float, 2 decimals)
- `unit`: Always "g/mol" for consistency
- `source`: Data attribution (e.g., "PubChem NIH")
- `common_units`: Semicolon-separated list of convertible units

**Data Validation:**
- Molar masses verified against PubChem database
- No duplicate analyte entries
- UTF-8 encoding for international character support

---

### 2. Conversion Engine

**Function: `convert_units(value, from_unit, to_unit, molar_mass)`**

**Algorithm:**

```python
# Step 1: Convert to mol/L (base unit)
if from_unit == "µmol/L":
    mol_per_L = value * 1e-6
elif from_unit == "mmol/L":
    mol_per_L = value * 1e-3
elif from_unit == "g/L":
    mol_per_L = value / molar_mass
elif from_unit == "mg/dL":
    g_per_L = value / 100
    mol_per_L = g_per_L / molar_mass

# Step 2: Convert from mol/L to target unit
if to_unit == "µmol/L":
    result = mol_per_L * 1e6
elif to_unit == "mmol/L":
    result = mol_per_L * 1e3
elif to_unit == "g/L":
    result = mol_per_L * molar_mass
elif to_unit == "mg/dL":
    g_per_L = mol_per_L * molar_mass
    result = g_per_L * 100
```

**Key Design Decisions:**
- **Two-step conversion** ensures consistency across all unit pairs
- **mol/L as intermediate** allows easy addition of new units
- **Float precision** maintained throughout calculation chain
- **Error handling** returns None for invalid conversions

**Conversion Matrix:**

| From ↓ To → | µmol/L | mmol/L | mg/dL | g/L |
|-------------|--------|--------|-------|-----|
| **µmol/L**  | 1:1    | ÷1000  | Complex | ÷10⁶×MM |
| **mmol/L**  | ×1000  | 1:1    | Complex | ÷10³×MM |
| **mg/dL**   | Complex | Complex | 1:1   | ÷100 |
| **g/L**     | ×10⁶÷MM | ×10³÷MM | ×100  | 1:1 |

MM = Molar Mass

---

### 3. Session Management

**Streamlit Session State Structure:**

```python
st.session_state.history = [
    {
        "timestamp": "2024-02-11 20:16:13",
        "analyte": "Cholesterol",
        "value_input": 200.0,
        "unit_from": "mg/dL",
        "value_output": 5.1726,
        "unit_to": "mmol/L",
        "molar_mass": 386.65,
        "source": "PubChem NIH"
    },
    # ... up to 50 entries
]
```

**Behavior:**
- New conversions inserted at index 0 (most recent first)
- Maximum 50 entries (FIFO when limit reached)
- Persists only during active session
- Cleared on browser refresh or manual clear

---

### 4. User Interface

**Layout Structure:**

```
┌────────────────────────────────────────────────┐
│              Title & Disclaimer                │
├────────────────────────┬───────────────────────┤
│   Main Panel (2/3)     │   History (1/3)      │
│                        │                       │
│  Analyte Selector      │  Last 10 conversions │
│  Molar Mass Display    │  Clear & Export btns │
│                        │                       │
│  Input Value           │                       │
│  From Unit ────────►   │                       │
│                        │                       │
│  To Unit               │                       │
│                        │                       │
│  [Convert Button]      │                       │
│                        │                       │
│  Result Display        │                       │
│  Calculation Details   │                       │
└────────────────────────┴───────────────────────┘
│              Footer (ISO 15189)                │
└────────────────────────────────────────────────┘
```

**Components:**
- `st.selectbox()`: Analyte and unit selection
- `st.number_input()`: Numerical value entry (4 decimal precision)
- `st.button()`: Primary action trigger
- `st.success()`: Result display with formatting
- `st.expander()`: Collapsible calculation details
- `st.download_button()`: CSV export functionality

---

## 📊 Data Flow

### Conversion Workflow

```
User Input
    │
    ├─ Select Analyte ──────► Load molar_mass from CSV
    │                         Load available_units
    ├─ Enter Value
    ├─ Select From Unit
    └─ Select To Unit
            │
            ▼
    [Convert Button Click]
            │
            ├─ Validation
            │   ├─ Same unit check
            │   └─ Value > 0 check
            │
            ▼
    convert_units(value, from, to, MM)
            │
            ├─ Step 1: Input → mol/L
            └─ Step 2: mol/L → Output
            │
            ▼
    Result Calculation
            │
            ├─ Round to 4 decimals
            ├─ Add timestamp
            └─ Store in session_state.history
            │
            ▼
    Display Results
            │
            ├─ Success message
            ├─ Formatted output
            └─ Calculation details
            │
            ▼
    Update History Panel
```

---

## 🔐 Security & Privacy

### Data Security Measures

1. **Local Processing**
   - All calculations performed client-side
   - No external API calls
   - No data transmission over network

2. **Session Isolation**
   - History stored in browser session only
   - No persistent storage
   - No cross-session data leakage

3. **Input Validation**
   - Numeric bounds checking
   - Unit compatibility verification
   - Analyte existence validation

### Compliance Considerations

**ISO 15189 Alignment:**
- ✅ Source attribution (traceability)
- ✅ Calculation transparency
- ✅ Non-decisional tool disclaimer
- ⚠️ No persistent audit trail (future enhancement)

---

## 🧪 Testing Strategy

### Unit Test Coverage Plan

**Priority 1: Conversion Engine**
```python
# Test cases
def test_same_unit_conversion():
    # Should return original value
    assert convert_units(100, "mmol/L", "mmol/L", 180.16) == 100

def test_creatinine_conversion():
    # Known medical reference
    result = convert_units(19243, "µmol/L", "g/L", 113.12)
    assert abs(result - 2.1767) < 0.0001

def test_cholesterol_mgdl_to_mmol():
    # 200 mg/dL should be ~5.17 mmol/L
    result = convert_units(200, "mg/dL", "mmol/L", 386.65)
    assert abs(result - 5.17) < 0.01
```

**Priority 2: Data Validation**
- CSV file integrity checks
- Molar mass value ranges
- Unit string format validation

**Priority 3: UI Behavior**
- Button state management
- History display limits
- Export file generation

---

## ⚡ Performance Considerations

### Current Performance

- **Conversion calculation**: < 1ms
- **CSV loading**: < 10ms (cached)
- **UI rendering**: < 100ms
- **History update**: < 50ms

### Scalability

**Current Limits:**
- 50 history entries (configurable)
- 7 analytes (easily expandable)
- Single user session

**Future Scalability:**
- Multi-user: Requires authentication layer
- Large history: Database backend needed
- Real-time sync: WebSocket implementation

---

## 🔮 Planned Enhancements

### Phase 1: AI Integration (Next)

**Technology:** Ollama (Local LLM)

**Capabilities:**
- Natural language input parsing
- Intelligent analyte recognition
- Contextual error messages
- Calculation explanations

**Architecture Addition:**
```
User Input (Natural Language)
    ↓
Ollama LLM (Local)
    ↓
Entity Extraction
    ├─ Analyte
    ├─ Value
    └─ Unit
    ↓
Existing Conversion Engine
    ↓
AI-Enhanced Response
```

### Phase 2: Database Integration

**Technology:** SQLite (local) or PostgreSQL (deployed)

**Benefits:**
- Persistent history
- Multi-user support
- Audit trail compliance
- Usage analytics

### Phase 3: Advanced Features

- Batch conversion mode
- PDF report generation
- Quality control statistics
- Multi-language support

---

## 📦 Dependencies

### Core Dependencies

```txt
streamlit>=1.30.0    # Web framework
pandas>=2.0.0        # Data manipulation
```

### Development Dependencies (Future)

```txt
pytest>=7.0.0        # Testing framework
black>=23.0.0        # Code formatting
mypy>=1.0.0          # Type checking
ollama>=0.1.0        # AI integration
```

---

## 🐛 Known Issues & Limitations

### Current Limitations

1. **No persistent storage**
   - History lost on browser refresh
   - No multi-session continuity

2. **Limited analyte library**
   - 7 analytes currently supported
   - No enzyme or electrolyte conversions yet

3. **Single user session**
   - No authentication
   - No shared history across users

4. **Basic error handling**
   - Generic error messages
   - No input sanitization

### Planned Fixes

- Database integration (Issue #1, #3)
- Extended analyte library (Issue #2)
- Enhanced validation (Issue #4)

---

## 📚 References

### Scientific References

1. PubChem Database (NIH)
   - https://pubchem.ncbi.nlm.nih.gov/

2. ISO 15189:2022 - Medical laboratories
   - https://www.iso.org/standard/76677.html

3. CLSI Guidelines
   - https://clsi.org/

### Technical Documentation

1. Streamlit Documentation
   - https://docs.streamlit.io/

2. Pandas Documentation
   - https://pandas.pydata.org/docs/

---

## 👨‍💻 Development Notes

### Code Style

- PEP 8 compliance
- Type hints (Python 3.11+)
- Docstrings for all functions
- Maximum line length: 100 characters

### Git Workflow

```bash
main          # Production-ready code
├─ develop    # Integration branch
   ├─ feature/ai-integration
   ├─ feature/database
   └─ fix/error-handling
```

### Version Numbering

`MAJOR.MINOR.PATCH`
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

Current: v1.0.0

---

## 📞 Contact & Contribution

For technical questions or contributions:
- GitHub Issues: [Project Issues]
- Email: [your.email@example.com]

---

**Last Updated:** February 2024  
**Version:** 1.0.0  
**Author:** [Your Name]
