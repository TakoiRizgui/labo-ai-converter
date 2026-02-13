"""
Unit tests for the converter module.
"""

import pytest
from src.converter import (
    convert_units,
    validate_units,
    get_conversion_formula
)


class TestConvertUnits:
    """Tests for the convert_units function."""
    
    def test_cholesterol_mg_dl_to_mmol_l(self):
        """Test conversion of cholesterol from mg/dL to mmol/L."""
        # Reference: 200 mg/dL = 5.17 mmol/L for cholesterol
        result = convert_units(200, "mg/dL", "mmol/L", 386.65)
        assert result is not None
        assert abs(result - 5.17) < 0.01
    
    def test_creatinine_umol_l_to_g_l(self):
        """Test conversion of creatinine from µmol/L to g/L."""
        # Reference: 19243 µmol/L = 2.1767 g/L for creatinine
        result = convert_units(19243, "µmol/L", "g/L", 113.12)
        assert result is not None
        assert abs(result - 2.1767) < 0.0001
    
    def test_glucose_mg_dl_to_mmol_l(self):
        """Test conversion of glucose from mg/dL to mmol/L."""
        # Reference: 90 mg/dL ≈ 5.0 mmol/L for glucose
        result = convert_units(90, "mg/dL", "mmol/L", 180.16)
        assert result is not None
        assert abs(result - 5.0) < 0.1
    
    def test_same_unit_conversion(self):
        """Test that converting to the same unit returns original value."""
        result = convert_units(100, "mmol/L", "mmol/L", 180.16)
        assert result is not None
        assert abs(result - 100) < 0.01
    
    def test_negative_value(self):
        """Test that negative values return None."""
        result = convert_units(-100, "mg/dL", "mmol/L", 386.65)
        assert result is None
    
    def test_zero_molar_mass(self):
        """Test that zero molar mass returns None."""
        result = convert_units(100, "mg/dL", "mmol/L", 0)
        assert result is None
    
    def test_invalid_from_unit(self):
        """Test that invalid source unit returns None."""
        result = convert_units(100, "invalid_unit", "mmol/L", 386.65)
        assert result is None
    
    def test_invalid_to_unit(self):
        """Test that invalid target unit returns None."""
        result = convert_units(100, "mg/dL", "invalid_unit", 386.65)
        assert result is None
    
    def test_reversibility(self):
        """Test that conversion is reversible."""
        # Convert 200 mg/dL to mmol/L
        result1 = convert_units(200, "mg/dL", "mmol/L", 386.65)
        assert result1 is not None
        
        # Convert back to mg/dL
        result2 = convert_units(result1, "mmol/L", "mg/dL", 386.65)
        assert result2 is not None
        assert abs(result2 - 200) < 0.01
    
    def test_umol_l_to_mmol_l(self):
        """Test conversion between µmol/L and mmol/L."""
        result = convert_units(1000, "µmol/L", "mmol/L", 113.12)
        assert result is not None
        assert abs(result - 1.0) < 0.0001
    
    def test_g_l_to_mg_dl(self):
        """Test conversion from g/L to mg/dL."""
        result = convert_units(2.0, "g/L", "mg/dL", 386.65)
        assert result is not None
        assert result > 0


class TestValidateUnits:
    """Tests for the validate_units function."""
    
    def test_valid_units(self):
        """Test that valid units return True."""
        valid = ["µmol/L", "mmol/L", "mg/dL", "g/L", "umol/L"]
        for unit in valid:
            assert validate_units(unit) is True
    
    def test_case_insensitive(self):
        """Test that validation is case-insensitive."""
        assert validate_units("MMOL/L") is True
        assert validate_units("Mmol/L") is True
    
    def test_spaces_ignored(self):
        """Test that spaces are ignored."""
        assert validate_units("mmol / L") is True
    
    def test_invalid_units(self):
        """Test that invalid units return False."""
        invalid = ["invalid", "mol/L", "kg/m3", ""]
        for unit in invalid:
            assert validate_units(unit) is False


class TestGetConversionFormula:
    """Tests for the get_conversion_formula function."""
    
    def test_formula_generation(self):
        """Test that formula is generated correctly."""
        formula = get_conversion_formula("mg/dL", "mmol/L")
        assert "mg/dL" in formula
        assert "mmol/L" in formula
        assert "mol/L" in formula
    
    def test_different_units(self):
        """Test formula with different unit combinations."""
        formulas = [
            get_conversion_formula("µmol/L", "g/L"),
            get_conversion_formula("mmol/L", "mg/dL"),
        ]
        for formula in formulas:
            assert isinstance(formula, str)
            assert len(formula) > 0


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_very_small_value(self):
        """Test conversion of very small values."""
        result = convert_units(0.001, "mmol/L", "µmol/L", 180.16)
        assert result is not None
        assert result > 0
    
    def test_very_large_value(self):
        """Test conversion of very large values."""
        result = convert_units(100000, "µmol/L", "mmol/L", 113.12)
        assert result is not None
        assert result > 0
    
    def test_precision(self):
        """Test that conversions maintain reasonable precision."""
        # Test that we get at least 4 significant figures
        result = convert_units(123.45, "mg/dL", "mmol/L", 386.65)
        assert result is not None
        # Result should be around 3.19, check we have precision
        assert abs(result - 3.19) < 0.01


# Medical reference tests (based on clinical standards)
class TestMedicalReferences:
    """Tests using known medical reference values."""
    
    def test_normal_glucose_fasting(self):
        """Test normal fasting glucose conversion."""
        # Normal fasting glucose: 70-100 mg/dL = 3.9-5.6 mmol/L
        result_low = convert_units(70, "mg/dL", "mmol/L", 180.16)
        result_high = convert_units(100, "mg/dL", "mmol/L", 180.16)
        
        assert result_low is not None
        assert result_high is not None
        assert 3.8 < result_low < 4.0
        assert 5.5 < result_high < 5.7
    
    def test_normal_cholesterol(self):
        """Test normal cholesterol conversion."""
        # Normal cholesterol: <200 mg/dL = <5.2 mmol/L
        result = convert_units(200, "mg/dL", "mmol/L", 386.65)
        assert result is not None
        assert 5.1 < result < 5.3
    
    def test_normal_creatinine(self):
        """Test normal creatinine conversion."""
        # Normal creatinine: ~80-100 µmol/L = ~0.9-1.1 mg/dL
        result = convert_units(90, "µmol/L", "mg/dL", 113.12)
        assert result is not None
        assert 0.9 < result < 1.1
