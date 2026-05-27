"""
Water Management Module
Optimizes water use for agriculture while ensuring sustainable water resource management
and environmental protection.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class WaterSource:
    """Represents a water source for irrigation."""
    source_id: str
    source_type: str  # e.g., "well", "surface_water", "rainwater"
    total_capacity_mm: float  # depth in mm for field area
    quality_rating: float  # 0-1 scale (1 = best)
    sustainability_score: float  # 0-1 scale
    cost_per_mm: float  # currency units per mm


@dataclass
class IrrigationEvent:
    """Records an irrigation event."""
    event_id: str
    date: datetime
    water_applied_mm: float
    water_source: str
    crop_stage: str
    soil_moisture_before: Optional[float] = None
    soil_moisture_after: Optional[float] = None


class WaterRequirementCalculator:
    """Calculates water requirements for crops based on conditions."""
    
    # Reference crop evapotranspiration values (mm/day)
    ET0_REFERENCE = {
        'low': 3.0,
        'moderate': 5.0,
        'high': 7.0
    }
    
    # Crop coefficients for different growth stages
    CROP_COEFFICIENTS = {
        'rice': {'initial': 0.3, 'development': 0.8, 'mid': 1.15, 'late': 0.7},
        'wheat': {'initial': 0.3, 'development': 0.7, 'mid': 1.15, 'late': 0.4},
        'maize': {'initial': 0.3, 'development': 0.8, 'mid': 1.15, 'late': 0.6},
        'cotton': {'initial': 0.4, 'development': 0.7, 'mid': 1.1, 'late': 0.8},
    }
    
    @staticmethod
    def calculate_et0(temperature_c: float, humidity_percent: float, 
                     wind_speed_ms: float, sunshine_hours: float) -> float:
        """
        Calculate reference evapotranspiration (ET0) using Hargreaves equation.
        Returns ET0 in mm/day.
        """
        # Simplified Hargreaves formula
        ra = 15.0  # Extraterrestrial radiation (simplified)
        et0 = 0.0023 * ra * (temperature_c + 17.8) * (humidity_percent - 35) ** 0.5
        
        return max(0, et0)
    
    @staticmethod
    def calculate_crop_water_requirement(crop_name: str, et0: float, 
                                        growing_days: int, 
                                        growth_stage: str = 'mid') -> float:
        """
        Calculate total crop water requirement in mm.
        
        Args:
            crop_name: Name of the crop
            et0: Reference evapotranspiration (mm/day)
            growing_days: Number of growing days
            growth_stage: Current growth stage
        
        Returns:
            Water requirement in mm
        """
        if crop_name not in WaterRequirementCalculator.CROP_COEFFICIENTS:
            # Default coefficient if crop not found
            kc = 1.0
        else:
            kc = WaterRequirementCalculator.CROP_COEFFICIENTS[crop_name].get(
                growth_stage, 1.0
            )
        
        etc = kc * et0  # Crop evapotranspiration
        total_requirement = etc * growing_days
        
        return total_requirement


class IrrigationOptimizer:
    """Optimizes irrigation scheduling for water conservation."""
    
    def __init__(self, field_area_hectares: float, 
                 field_capacity_mm: float, 
                 wilting_point_mm: float):
        """
        Initialize irrigation optimizer.
        
        Args:
            field_area_hectares: Area of the field
            field_capacity_mm: Maximum water holding capacity
            wilting_point_mm: Minimum water needed for plant survival
        """
        self.field_area_hectares = field_area_hectares
        self.field_capacity_mm = field_capacity_mm
        self.wilting_point_mm = wilting_point_mm
        self.current_soil_moisture_mm = field_capacity_mm
        self.irrigation_history: List[IrrigationEvent] = []
    
    def calculate_irrigation_requirement(self, crop_water_need: float,
                                        current_moisture: Optional[float] = None) -> float:
        """
        Calculate irrigation requirement in mm.
        
        Uses Available Water Depletion (AWD) strategy.
        """
        if current_moisture is None:
            current_moisture = self.current_soil_moisture_mm
        
        # Available water = Field Capacity - Wilting Point
        available_water = self.field_capacity_mm - self.wilting_point_mm
        
        # Allowable depletion (typically 50% for most crops)
        allowable_depletion = available_water * 0.5
        
        # Depletion level
        current_depletion = self.field_capacity_mm - current_moisture
        
        # Calculate irrigation need
        if current_depletion > allowable_depletion:
            irrigation_needed = current_moisture - self.wilting_point_mm
        else:
            irrigation_needed = max(0, crop_water_need - (self.field_capacity_mm - current_moisture))
        
        return irrigation_needed
    
    def schedule_irrigation(self, crop_name: str, planting_date: datetime,
                           et0: float, rainfall_forecast: Dict[str, float]) -> List[Dict]:
        """
        Schedule irrigation events for optimal water management.
        
        Returns a schedule of irrigation events with dates and amounts.
        """
        schedule = []
        crop_coeff = WaterRequirementCalculator.CROP_COEFFICIENTS.get(
            crop_name, {'initial': 0.3, 'development': 0.7, 'mid': 1.0, 'late': 0.5}
        )
        
        growth_stages = ['initial', 'development', 'mid', 'late']
        stage_duration = 25  # days per stage (simplified)
        
        current_moisture = self.field_capacity_mm
        current_date = planting_date
        
        for stage in growth_stages:
            kc = crop_coeff.get(stage, 1.0)
            etc = kc * et0
            
            for day in range(stage_duration):
                current_date_str = (current_date + timedelta(days=day)).strftime('%Y-%m-%d')
                rainfall = rainfall_forecast.get(current_date_str, 0)
                
                # Update soil moisture
                current_moisture += rainfall - etc
                current_moisture = min(current_moisture, self.field_capacity_mm)
                
                # Check if irrigation is needed
                if current_moisture < self.wilting_point_mm + (self.field_capacity_mm - self.wilting_point_mm) * 0.5:
                    irrigation_amount = self.field_capacity_mm - current_moisture
                    
                    schedule.append({
                        'date': current_date_str,
                        'irrigation_mm': irrigation_amount,
                        'crop_stage': stage,
                        'soil_moisture_before': current_moisture - irrigation_amount,
                    })
                    
                    current_moisture = self.field_capacity_mm
            
            current_date += timedelta(days=stage_duration)
        
        return schedule
    
    def calculate_water_use_efficiency(self) -> float:
        """
        Calculate irrigation water use efficiency (%).
        Higher values indicate more efficient water use.
        """
        if not self.irrigation_history:
            return 0.0
        
        total_irrigation = sum(event.water_applied_mm for event in self.irrigation_history)
        effective_use = sum(
            event.water_applied_mm for event in self.irrigation_history
            if event.soil_moisture_after is not None and event.soil_moisture_after > event.soil_moisture_before
        )
        
        if total_irrigation == 0:
            return 0.0
        
        return (effective_use / total_irrigation) * 100
    
    def get_conservation_recommendations(self) -> List[str]:
        """Get recommendations for water conservation."""
        recommendations = []
        efficiency = self.calculate_water_use_efficiency()
        
        if efficiency < 60:
            recommendations.append("Consider drip irrigation to improve water use efficiency")
        
        if efficiency < 50:
            recommendations.append("Increase soil organic matter to improve water retention")
        
        recommendations.append("Schedule irrigation based on soil moisture monitoring")
        recommendations.append("Use mulching to reduce evaporation losses")
        recommendations.append("Collect and store rainwater for supplemental irrigation")
        
        return recommendations


class PrecipitationCollector:
    """Manages rainwater harvesting and runoff collection."""
    
    def __init__(self, catchment_area_sqm: float):
        self.catchment_area_sqm = catchment_area_sqm
        self.storage_capacity_liters = 0
        self.current_storage_liters = 0
        self.monthly_precipitation = {}
    
    def calculate_water_collection(self, precipitation_mm: float) -> float:
        """
        Calculate water collected from precipitation.
        Returns volume in liters.
        """
        # 1 mm of precipitation on 1 m² = 1 liter
        collected_liters = precipitation_mm * self.catchment_area_sqm
        
        self.current_storage_liters = min(
            self.current_storage_liters + collected_liters,
            self.storage_capacity_liters
        )
        
        return collected_liters
    
    def estimate_annual_water_yield(self, annual_precipitation_mm: float) -> float:
        """Estimate annual water yield from rain harvesting in liters."""
        return annual_precipitation_mm * self.catchment_area_sqm