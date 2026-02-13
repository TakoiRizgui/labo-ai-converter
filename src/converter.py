"""
Biochemical Unit Converter Module

This module provides functions for converting between different biochemical units.
All conversions use mol/L as an intermediate unit for maximum accuracy.
"""

from typing import Optional


def convert_units(
    value: float,
    from_unit: str,
    to_unit: str,
    molar_mass: float
) -> Optional[float]:
    """
    Convert a biochemical value between different units.
    
    Args:
        value: The numerical value to convert
        from_unit: Source unit (µmol/L, mmol/L, mg/dL, g/L)
        to_unit: Target unit (µmol/L, mmol/L, mg/dL, g/L)
        molar_mass: Molar mass of the analyte in g/mol
        
    Returns:
        Converted value, or None if conversion is not possible
        
    Examples:
        >>> convert_units(200, "mg/dL", "mmol/L", 386.65)
        5.1726
        
        >>> convert_units(19243, "µmol/L", "g/L", 113.12)
        2.1767
    """
    if value < 0 or molar_mass <= 0:
        return None
    
    # Step 1: Convert to mol/L (base unit)
    mol_per_L = _to_mol_per_liter(value, from_unit, molar_mass)
    
    if mol_per_L is None:
        return None
    
    # Step 2: Convert from mol/L to target unit
    result = _from_mol_per_liter(mol_per_L, to_unit, molar_mass)
    
    return result


def _to_mol_per_liter(
    value: float,
    unit: str,
    molar_mass: float
) -> Optional[float]:
    """
    Convert a value to mol/L.
    
    Args:
        value: Numerical value
        unit: Source unit
        molar_mass: Molar mass in g/mol
        
    Returns:
        Value in mol/L, or None if unit is invalid
    """
    unit_lower = unit.lower().replace(" ", "")
    
    if unit_lower in ["µmol/l", "umol/l"]:
        return value * 1e-6
    elif unit_lower == "mmol/l":
        return value * 1e-3
    elif unit_lower == "g/l":
        return value / molar_mass
    elif unit_lower == "mg/dl":
        # mg/dL → g/L → mol/L
        g_per_L = value / 100
        return g_per_L / molar_mass
    else:
        return None


def _from_mol_per_liter(
    mol_per_L: float,
    unit: str,
    molar_mass: float
) -> Optional[float]:
    """
    Convert from mol/L to target unit.
    
    Args:
        mol_per_L: Value in mol/L
        unit: Target unit
        molar_mass: Molar mass in g/mol
        
    Returns:
        Converted value, or None if unit is invalid
    """
    unit_lower = unit.lower().replace(" ", "")
    
    if unit_lower in ["µmol/l", "umol/l"]:
        return mol_per_L * 1e6
    elif unit_lower == "mmol/l":
        return mol_per_L * 1e3
    elif unit_lower == "g/l":
        return mol_per_L * molar_mass
    elif unit_lower == "mg/dl":
        # mol/L → g/L → mg/dL
        g_per_L = mol_per_L * molar_mass
        return g_per_L * 100
    else:
        return None


def get_conversion_formula(from_unit: str, to_unit: str) -> str:
    """
    Get a human-readable description of the conversion formula.
    
    Args:
        from_unit: Source unit
        to_unit: Target unit
        
    Returns:
        Formula description as string
    """
    return f"{from_unit} → mol/L → {to_unit}"


def validate_units(unit: str) -> bool:
    """
    Check if a unit is valid.
    
    Args:
        unit: Unit string to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_units = ["µmol/l", "umol/l", "mmol/l", "mg/dl", "g/l"]
    return unit.lower().replace(" ", "") in valid_units
