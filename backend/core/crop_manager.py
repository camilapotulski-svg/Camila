"""
Crop Management Module
Handles crop planning, rotation strategies, and production optimization
for sustainable agriculture practices.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class CropType(Enum):
    """Enumeration of crop types for rotation planning."""
    LEGUME = "legume"
    GRAIN = "grain"
    ROOT = "root"
    BRASSICA = "brassica"
    SOLANACEAE = "solanaceae"


@dataclass
class Crop:
    """Represents a crop with its characteristics."""
    name: str
    crop_type: CropType
    growing_season_days: int
    nitrogen_requirement: float  # kg/hectare
    water_requirement: float     # mm/season
    pesticide_sensitivity: float # 0-1 scale
    environmental_impact: float  # 0-1 scale (lower is better)
    yield_potential: float       # tons/hectare
    
    def sustainability_score(self) -> float:
        """Calculate sustainability score for the crop."""
        return (1 - self.environmental_impact) * 0.6 + \
               (1 - self.pesticide_sensitivity) * 0.4


@dataclass
class Field:
    """Represents a physical field with its properties."""
    field_id: str
    area_hectares: float
    soil_ph: float
    soil_nitrogen: float      # kg/hectare
    soil_organic_matter: float # percentage
    water_availability: float  # mm/season
    
    def get_soil_health_score(self) -> float:
        """Calculate soil health score."""
        # Ideal pH: 6.5-7.5, OM: 3-5%, N: 50-100 kg/ha
        ph_score = 1 - abs(self.soil_ph - 7.0) / 3.0
        om_score = min(self.soil_organic_matter / 4.0, 1.0)
        n_score = min(self.soil_nitrogen / 100.0, 1.0)
        
        return (ph_score + om_score + n_score) / 3.0


class CropRotationPlanner:
    """Plans optimal crop rotations for soil health and sustainability."""
    
    def __init__(self, field: Field):
        self.field = field
        self.rotation_history: List[Crop] = []
        
    def calculate_crop_compatibility(self, crop: Crop) -> float:
        """
        Calculate how compatible a crop is with the current field state.
        Returns a score from 0-1 (higher is better).
        """
        # Check nitrogen requirements vs. availability
        nitrogen_score = 1 - abs(crop.nitrogen_requirement - self.field.soil_nitrogen) / 150.0
        nitrogen_score = max(0, min(nitrogen_score, 1))
        
        # Check water requirements vs. availability
        water_score = 1 - abs(crop.water_requirement - self.field.water_availability) / 500.0
        water_score = max(0, min(water_score, 1))
        
        # Soil health compatibility
        soil_score = self.field.get_soil_health_score()
        
        return (nitrogen_score + water_score + soil_score) / 3.0
    
    def get_crop_rotation_recommendation(self, available_crops: List[Crop]) -> Crop:
        """
        Recommend the best crop to plant next based on field conditions
        and crop rotation principles.
        """
        if not available_crops:
            raise ValueError("No crops available for rotation")
        
        # Avoid planting the same crop family consecutively
        if self.rotation_history:
            last_crop = self.rotation_history[-1]
            compatible_crops = [c for c in available_crops 
                              if c.crop_type != last_crop.crop_type]
            if not compatible_crops:
                compatible_crops = available_crops
        else:
            compatible_crops = available_crops
        
        # Score each compatible crop
        scored_crops = [
            (crop, self.calculate_crop_compatibility(crop)) 
            for crop in compatible_crops
        ]
        
        # Return the best option
        return max(scored_crops, key=lambda x: x[1])[0]
    
    def plan_rotation_sequence(self, available_crops: List[Crop], 
                              years: int = 4) -> List[List[Crop]]:
        """Plan a multi-year crop rotation strategy."""
        rotation_plan = []
        
        for year in range(years):
            recommended = self.get_crop_rotation_recommendation(available_crops)
            rotation_plan.append([recommended])
            self.rotation_history.append(recommended)
            
            # Simulate field changes after crop planting
            self._simulate_crop_impact(recommended)
        
        return rotation_plan
    
    def _simulate_crop_impact(self, crop: Crop):
        """Simulate the impact of planting a crop on field conditions."""
        if crop.crop_type == CropType.LEGUME:
            # Legumes fix nitrogen
            self.field.soil_nitrogen = min(
                self.field.soil_nitrogen + 50,
                150
            )
        
        # Crops improve soil organic matter
        self.field.soil_organic_matter = min(
            self.field.soil_organic_matter + 0.2,
            5.0
        )


class YieldPredictor:
    """Predicts crop yield based on field conditions and management practices."""
    
    @staticmethod
    def predict_yield(crop: Crop, field: Field, 
                     water_management_efficiency: float = 0.85,
                     pest_control_effectiveness: float = 0.9) -> float:
        """
        Predict crop yield in tons/hectare.
        
        Args:
            crop: The crop to predict yield for
            field: The field conditions
            water_management_efficiency: 0-1 scale
            pest_control_effectiveness: 0-1 scale
        
        Returns:
            Predicted yield in tons/hectare
        """
        # Base yield potential
        base_yield = crop.yield_potential
        
        # Water availability factor
        water_factor = min(field.water_availability / crop.water_requirement, 1.0)
        water_factor = water_factor * 0.5 + 0.5  # Scale to 0.5-1.0
        
        # Nitrogen availability factor
        nitrogen_available = field.soil_nitrogen / crop.nitrogen_requirement
        nitrogen_factor = 1.0 / (1.0 + (2.71828 ** (-3 * (nitrogen_available - 0.5))))
        
        # Soil health factor
        soil_factor = field.get_soil_health_score()
        
        # Management factors
        water_mgmt_factor = 0.7 + (water_management_efficiency * 0.3)
        pest_control_factor = 0.7 + (pest_control_effectiveness * 0.3)
        
        predicted_yield = base_yield * water_factor * nitrogen_factor * soil_factor * \
                         water_mgmt_factor * pest_control_factor
        
        return max(0, predicted_yield)


class SustainabilityAnalyzer:
    """Analyzes sustainability metrics for farming practices."""
    
    @staticmethod
    def calculate_carbon_footprint(crop: Crop, yield_tons: float,
                                  nitrogen_applied: float,
                                  water_pumped: float) -> float:
        """
        Calculate carbon footprint in kg CO2 per ton of product.
        
        Sources of emissions:
        - Nitrogen fertilizer: ~10 kg CO2/kg N
        - Water pumping: ~0.5 kg CO2/1000L
        - Diesel machinery: ~2.7 kg CO2/L
        """
        if yield_tons == 0:
            return 0
        
        nitrogen_emissions = nitrogen_applied * 10 / yield_tons
        water_emissions = (water_pumped / 1000) * 0.5 / yield_tons
        
        total_emissions = nitrogen_emissions + water_emissions
        
        return total_emissions
    
    @staticmethod
    def calculate_environmental_impact_score(crop: Crop, 
                                            yield_tons: float,
                                            carbon_kg_co2: float) -> float:
        """
        Calculate comprehensive environmental impact score.
        0-100 scale, higher is better (more sustainable).
        """
        # Yield efficiency (more yield with less input = better)
        yield_score = min((yield_tons / crop.yield_potential) * 50, 50)
        
        # Carbon efficiency (lower carbon = better)
        carbon_limit = 5.0  # kg CO2/ton
        carbon_score = (1 - min(carbon_kg_co2 / carbon_limit, 1.0)) * 30
        
        # Crop sustainability (inherent properties)
        crop_score = crop.sustainability_score() * 20
        
        return yield_score + carbon_score + crop_score