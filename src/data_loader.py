"""
Scientific Data Loader Module

This module handles loading and validation of scientific data from CSV files.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict


class ScientificDataLoader:
    """Loads and manages biochemical analyte data."""
    
    def __init__(self, data_path: str = "data/scientific_data.csv"):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the CSV file containing scientific data
        """
        self.data_path = Path(data_path)
        self._data: Optional[pd.DataFrame] = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load scientific data from CSV file.
        
        Returns:
            DataFrame containing analyte data
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV format is invalid
        """
        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Scientific data file not found: {self.data_path}"
            )
        
        try:
            self._data = pd.read_csv(self.data_path)
            self._validate_data()
            return self._data
        except Exception as e:
            raise ValueError(f"Error loading scientific data: {str(e)}")
    
    def _validate_data(self) -> None:
        """
        Validate that loaded data has required columns.
        
        Raises:
            ValueError: If required columns are missing
        """
        required_columns = ["analyte", "molar_mass", "unit", "source", "common_units"]
        
        if self._data is None:
            raise ValueError("No data loaded")
        
        missing_columns = set(required_columns) - set(self._data.columns)
        if missing_columns:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_columns)}"
            )
    
    def get_analyte_info(self, analyte: str) -> Optional[Dict]:
        """
        Get information about a specific analyte.
        
        Args:
            analyte: Name of the analyte (e.g., "creatinine")
            
        Returns:
            Dictionary with analyte information, or None if not found
        """
        if self._data is None:
            self.load_data()
        
        result = self._data[self._data["analyte"] == analyte.lower()]
        
        if result.empty:
            return None
        
        row = result.iloc[0]
        return {
            "analyte": row["analyte"],
            "molar_mass": float(row["molar_mass"]),
            "source": row["source"],
            "common_units": row["common_units"].split(";")
        }
    
    def get_all_analytes(self) -> List[str]:
        """
        Get list of all available analytes.
        
        Returns:
            List of analyte names
        """
        if self._data is None:
            self.load_data()
        
        return self._data["analyte"].tolist()
    
    def get_molar_mass(self, analyte: str) -> Optional[float]:
        """
        Get molar mass for a specific analyte.
        
        Args:
            analyte: Name of the analyte
            
        Returns:
            Molar mass in g/mol, or None if analyte not found
        """
        info = self.get_analyte_info(analyte)
        return info["molar_mass"] if info else None
    
    def get_common_units(self, analyte: str) -> Optional[List[str]]:
        """
        Get common units for a specific analyte.
        
        Args:
            analyte: Name of the analyte
            
        Returns:
            List of common units, or None if analyte not found
        """
        info = self.get_analyte_info(analyte)
        return info["common_units"] if info else None
    
    @property
    def data(self) -> pd.DataFrame:
        """
        Get the loaded data.
        
        Returns:
            DataFrame with scientific data
        """
        if self._data is None:
            self.load_data()
        return self._data
