"""
Soil Health Monitoring Module
Tracks and analyzes soil conditions to maintain long-term agricultural productivity
while protecting environmental quality.
"""

from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class SoilTestType(Enum):
    """Types of soil tests available."""
    PHYSICAL = "physical"
    CHEMICAL = "chemical"
    BIOLOGICAL = "biological"
    COMPREHENSIVE = "comprehensive"


@dataclass
class SoilTest:
    """Represents a soil test result."""
    test_id: str
    test_date: datetime
    test_type: SoilTestType
    field_id: str
    
    # Physical properties
    texture_sand_percent: Optional[float] = None
    texture_silt_percent: Optional[float] = None
    texture_clay_percent: Optional[float] = None
    bulk_density: Optional[float] = None  # g/cm³
    water_holding_capacity: Optional[float] = None  # %
    
    # Chemical properties
    ph: Optional[float] = None
    organic_carbon: Optional[float] = None  # %
    total_nitrogen: Optional[float] = None  # %
    available_phosphorus: Optional[float] = None  # mg/kg
    available_potassium: Optional[float] = None  # mg/kg
    electrical_conductivity: Optional[float] = None  # dS/m
    
    # Biological properties
    microbial_biomass_carbon: Optional[float] = None  # μg/g
    enzymatic_activity: Optional[float] = None  # score
    earthworm_count: Optional[int] = None  # per m²
    
    def is_valid(self) -> bool:
        """Check if test results are valid."""
        return self.test_date is not None


class SoilHealthMonitor:
    """Monitors and tracks soil health over time."""
    
    def __init__(self, field_id: str):
        self.field_id = field_id
        self.test_history: List[SoilTest] = []
        self.ideal_values = {
            'ph': 6.5,
            'organic_carbon': 3.5,
            'total_nitrogen': 0.3,
            'available_phosphorus': 20.0,
            'available_potassium': 150.0,
            'microbial_biomass_carbon': 500.0,
            'bulk_density': 1.3
        }
    
    def add_test(self, test: SoilTest) -> bool:
        """Add a soil test result to history."""
        if not test.is_valid():
            return False
        
        self.test_history.append(test)
        return True
    
    def get_latest_test(self) -> Optional[SoilTest]:
        """Get the most recent soil test."""
        if not self.test_history:
            return None
        
        return sorted(self.test_history, key=lambda t: t.test_date)[-1]
    
    def calculate_soil_health_score(self, test: SoilTest) -> float:
        """
        Calculate overall soil health score (0-100).
        Based on physical, chemical, and biological properties.
        """
        scores = []
        weights = []
        
        # Physical health (25% weight)
        if test.bulk_density is not None:
            bd_score = self._score_parameter(
                test.bulk_density, 
                ideal=self.ideal_values['bulk_density'], 
                range_val=0.3
            )
            scores.append(bd_score)
            weights.append(0.25)
        
        # Chemical health (50% weight)
        chemical_scores = []
        chemical_params = [
            ('ph', test.ph, 0.5),
            ('organic_carbon', test.organic_carbon, 1.0),
            ('total_nitrogen', test.total_nitrogen, 0.1),
            ('available_phosphorus', test.available_phosphorus, 5.0),
            ('available_potassium', test.available_potassium, 30.0),
        ]
        
        for param_name, param_value, range_val in chemical_params:
            if param_value is not None:
                score = self._score_parameter(
                    param_value, 
                    ideal=self.ideal_values[param_name], 
                    range_val=range_val
                )
                chemical_scores.append(score)
        
        if chemical_scores:
            scores.append(sum(chemical_scores) / len(chemical_scores))
            weights.append(0.50)
        
        # Biological health (25% weight)
        if test.microbial_biomass_carbon is not None:
            bio_score = self._score_parameter(
                test.microbial_biomass_carbon, 
                ideal=self.ideal_values['microbial_biomass_carbon'], 
                range_val=100.0
            )
            scores.append(bio_score)
            weights.append(0.25)
        
        if not scores:
            return 0.0
        
        # Weighted average
        total_weight = sum(weights)
        weighted_score = sum(s * w for s, w in zip(scores, weights)) / total_weight
        
        return min(100, max(0, weighted_score))
    
    def _score_parameter(self, value: float, ideal: float, 
                        range_val: float) -> float:
        """
        Score a parameter using Gaussian-like function.
        Returns 0-100, where ideal value = 100.
        """
        deviation = abs(value - ideal)
        score = 100 * (1 - (deviation / range_val) ** 2)
        
        return min(100, max(0, score))
    
    def get_soil_recommendations(self) -> List[str]:
        """Get recommendations to improve soil health."""
        latest_test = self.get_latest_test()
        if not latest_test:
            return ["Conduct initial soil test to establish baseline"]
        
        recommendations = []
        
        # pH recommendations
        if latest_test.ph is not None:
            if latest_test.ph < 6.0:
                recommendations.append("Add lime to raise soil pH")
            elif latest_test.ph > 8.0:
                recommendations.append("Add sulfur to lower soil pH")
        
        # Organic matter recommendations
        if latest_test.organic_carbon is not None and latest_test.organic_carbon < 2.5:
            recommendations.append("Increase organic matter: use compost, manure, or crop residues")
        
        # Nitrogen recommendations
        if latest_test.total_nitrogen is not None and latest_test.total_nitrogen < 0.2:
            recommendations.append("Consider planting nitrogen-fixing cover crops")
        
        # Phosphorus recommendations
        if latest_test.available_phosphorus is not None and latest_test.available_phosphorus < 15:
            recommendations.append("Apply phosphate fertilizer or rock phosphate")
        
        # Microbial activity
        if latest_test.microbial_biomass_carbon is not None and latest_test.microbial_biomass_carbon < 300:
            recommendations.append("Improve microbial activity: reduce tillage and add organic matter")
        
        # Biological recommendations
        if latest_test.earthworm_count is not None and latest_test.earthworm_count < 5:
            recommendations.append("Reduce pesticide use and maintain surface residue to support earthworm populations")
        
        if not recommendations:
            recommendations.append("Soil conditions are excellent. Maintain current practices.")
        
        return recommendations


class SoilCarbonTracker:
    """Tracks soil carbon sequestration for climate impact assessment."""
    
    def __init__(self):
        self.carbon_measurements: Dict[str, List[float]] = {}
    
    def add_measurement(self, field_id: str, organic_carbon_percent: float):
        """Add a soil carbon measurement."""
        if field_id not in self.carbon_measurements:
            self.carbon_measurements[field_id] = []
        
        self.carbon_measurements[field_id].append(organic_carbon_percent)
    
    def calculate_carbon_sequestration_rate(self, field_id: str) -> float:
        """
        Calculate annual carbon sequestration rate in tons CO2/hectare/year.
        Conversion: 1% organic carbon = ~20 tons CO2/hectare in top 30cm
        """
        if field_id not in self.carbon_measurements or len(self.carbon_measurements[field_id]) < 2:
            return 0.0
        
        measurements = self.carbon_measurements[field_id]
        carbon_change = measurements[-1] - measurements[0]
        
        # Approximate annual sequestration (assumes measurements are annual)
        annual_sequestration = carbon_change * 20
        
        return max(0, annual_sequestration)
    
    def estimate_climate_benefit(self, annual_sequestration: float, 
                                hectares: float) -> Dict[str, float]:
        """Estimate climate benefits of soil carbon sequestration."""
        return {
            'co2_removed_annual_tons': annual_sequestration * hectares,
            'equivalent_cars_offset': (annual_sequestration * hectares) / 4.6,
            'climate_impact_score': min((annual_sequestration * hectares) / 100 * 10, 10)
        }


@dataclass
class SoilProfile:
    """Represents a soil profile with multiple layers."""
    profile_id: str
    depth_cm: int
    soil_color: str
    soil_texture: str
    compaction_resistance: Optional[float] = None
    
    def is_suitable_for_roots(self) -> bool:
        """Check if soil layer is suitable for root penetration."""
        return self.compaction_resistance is None or self.compaction_resistance < 3.0