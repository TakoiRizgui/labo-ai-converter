"""
Unit tests for the data_loader module.
"""

import pytest
import pandas as pd
from pathlib import Path
from src.data_loader import ScientificDataLoader


class TestScientificDataLoader:
    """Tests for the ScientificDataLoader class."""
    
    def test_load_data_success(self):
        """Test successful loading of scientific data."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        data = loader.load_data()
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
    
    def test_load_data_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        loader = ScientificDataLoader("nonexistent_file.csv")
        
        with pytest.raises(FileNotFoundError):
            loader.load_data()
    
    def test_required_columns_present(self):
        """Test that all required columns are present."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        data = loader.load_data()
        
        required_columns = ["analyte", "molar_mass", "unit", "source", "common_units"]
        for col in required_columns:
            assert col in data.columns
    
    def test_get_all_analytes(self):
        """Test retrieving list of all analytes."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        analytes = loader.get_all_analytes()
        
        assert isinstance(analytes, list)
        assert len(analytes) > 0
        assert "creatinine" in analytes
    
    def test_get_analyte_info_existing(self):
        """Test getting info for an existing analyte."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        info = loader.get_analyte_info("creatinine")
        
        assert info is not None
        assert "molar_mass" in info
        assert "source" in info
        assert "common_units" in info
        assert info["analyte"] == "creatinine"
        assert info["molar_mass"] == 113.12
    
    def test_get_analyte_info_nonexistent(self):
        """Test getting info for a non-existent analyte."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        info = loader.get_analyte_info("nonexistent_analyte")
        
        assert info is None
    
    def test_get_analyte_info_case_insensitive(self):
        """Test that analyte lookup is case-insensitive."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        
        info1 = loader.get_analyte_info("creatinine")
        info2 = loader.get_analyte_info("CREATININE")
        info3 = loader.get_analyte_info("Creatinine")
        
        assert info1 is not None
        assert info2 is not None
        assert info3 is not None
        assert info1["molar_mass"] == info2["molar_mass"] == info3["molar_mass"]
    
    def test_get_molar_mass(self):
        """Test retrieving molar mass for an analyte."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        
        mm_creatinine = loader.get_molar_mass("creatinine")
        assert mm_creatinine == 113.12
        
        mm_glucose = loader.get_molar_mass("glucose")
        assert mm_glucose == 180.16
    
    def test_get_molar_mass_nonexistent(self):
        """Test that None is returned for non-existent analyte."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        mm = loader.get_molar_mass("nonexistent")
        
        assert mm is None
    
    def test_get_common_units(self):
        """Test retrieving common units for an analyte."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        units = loader.get_common_units("creatinine")
        
        assert units is not None
        assert isinstance(units, list)
        assert len(units) > 0
        assert "µmol/L" in units or "mg/dL" in units
    
    def test_get_common_units_nonexistent(self):
        """Test that None is returned for non-existent analyte."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        units = loader.get_common_units("nonexistent")
        
        assert units is None
    
    def test_data_property(self):
        """Test the data property accessor."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        data = loader.data
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
    
    def test_lazy_loading(self):
        """Test that data is only loaded when accessed."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        
        # Data should not be loaded yet
        assert loader._data is None
        
        # Access data property triggers loading
        _ = loader.data
        assert loader._data is not None
    
    def test_multiple_analytes(self):
        """Test that multiple analytes are loaded correctly."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        
        expected_analytes = [
            "creatinine",
            "uree",
            "glucose",
            "cholesterol"
        ]
        
        for analyte in expected_analytes:
            info = loader.get_analyte_info(analyte)
            assert info is not None, f"Analyte {analyte} not found"
            assert info["molar_mass"] > 0
    
    def test_source_attribution(self):
        """Test that source is properly attributed."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        info = loader.get_analyte_info("creatinine")
        
        assert info is not None
        assert "source" in info
        assert "PubChem" in info["source"] or "NIH" in info["source"]
    
    def test_common_units_format(self):
        """Test that common_units are properly formatted."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        units = loader.get_common_units("glucose")
        
        assert units is not None
        assert isinstance(units, list)
        # Should have multiple units
        assert len(units) >= 2
        # Each unit should be a non-empty string
        for unit in units:
            assert isinstance(unit, str)
            assert len(unit) > 0


class TestDataValidation:
    """Tests for data validation functionality."""
    
    def test_molar_mass_positive(self):
        """Test that all molar masses are positive."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        data = loader.load_data()
        
        assert (data["molar_mass"] > 0).all()
    
    def test_no_missing_values(self):
        """Test that there are no missing values in critical columns."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        data = loader.load_data()
        
        critical_columns = ["analyte", "molar_mass", "source"]
        for col in critical_columns:
            assert not data[col].isna().any(), f"Missing values in {col}"
    
    def test_unique_analytes(self):
        """Test that analyte names are unique."""
        loader = ScientificDataLoader("data/scientific_data.csv")
        data = loader.load_data()
        
        assert len(data["analyte"].unique()) == len(data)
