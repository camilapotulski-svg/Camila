"""
Biodiversity Tracking Module
Monitors and promotes biodiversity in agricultural systems to maintain
ecosystem services and environmental resilience.
"""

from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class SpeciesType(Enum):
    """Types of species in agricultural ecosystems."""
    POLLINATOR = "pollinator"
    PREDATOR = "predator"
    SOIL_ORGANISM = "soil_organism"
    PLANT = "plant"
    PEST = "pest"


@dataclass
class Species:
    """Represents a species found in agricultural system."""
    species_id: str
    common_name: str
    scientific_name: str
    species_type: SpeciesType
    ecosystem_value: float  # 0-1 scale
    abundance_index: int  # Population indicator
    threat_status: str  # "stable", "declining", "increasing"


@dataclass
class BiodiversityObservation:
    """Records a biodiversity observation."""
    observation_id: str
    date: datetime
    field_id: str
    species: Species
    quantity: int
    location_gps: Optional[tuple] = None  # (latitude, longitude)
    habitat_type: Optional[str] = None


class BiodiversityMonitor:
    """Monitors and tracks biodiversity in agricultural fields."""
    
    def __init__(self, field_id: str):
        self.field_id = field_id
        self.observations: List[BiodiversityObservation] = []
        self.species_index: Dict[str, Species] = {}
        
        # Ideal species diversity targets
        self.target_pollinator_species = 5
        self.target_predator_species = 3
        self.target_soil_organisms = 10
    
    def add_observation(self, observation: BiodiversityObservation) -> bool:
        """Record a biodiversity observation."""
        self.observations.append(observation)
        
        # Update species index
        if observation.species.species_id not in self.species_index:
            self.species_index[observation.species.species_id] = observation.species
        
        return True
    
    def get_species_diversity_index(self) -> float:
        """
        Calculate Shannon Diversity Index (0-5 scale).
        Higher values indicate greater species diversity.
        """
        if not self.observations:
            return 0.0
        
        # Count observations by species
        species_counts = {}
        total_observations = 0
        
        for obs in self.observations:
            species_id = obs.species.species_id
            species_counts[species_id] = species_counts.get(species_id, 0) + obs.quantity
            total_observations += obs.quantity
        
        if total_observations == 0:
            return 0.0
        
        # Calculate Shannon Index
        shannon_index = 0.0
        for count in species_counts.values():
            if count > 0:
                proportion = count / total_observations
                shannon_index -= proportion * (proportion ** 0.5)  # Simplified
        
        return shannon_index
    
    def get_ecosystem_health_score(self) -> float:
        """
        Calculate ecosystem health score (0-100).
        Based on species diversity, presence of key species, and trends.
        """
        if not self.observations:
            return 0.0
        
        # Get species counts by type
        species_by_type = {}
        for species in self.species_index.values():
            type_key = species.species_type.value
            if type_key not in species_by_type:
                species_by_type[type_key] = 0
            species_by_type[type_key] += 1
        
        # Score based on species diversity targets
        pollinator_score = min(
            (species_by_type.get('pollinator', 0) / self.target_pollinator_species) * 25,
            25
        )
        predator_score = min(
            (species_by_type.get('predator', 0) / self.target_predator_species) * 25,
            25
        )
        soil_score = min(
            (species_by_type.get('soil_organism', 0) / self.target_soil_organisms) * 25,
            25
        )
        
        # Diversity bonus
        diversity_index = self.get_species_diversity_index()
        diversity_score = min((diversity_index / 5) * 25, 25)
        
        total_score = pollinator_score + predator_score + soil_score + diversity_score
        
        return min(100, max(0, total_score / 4))
    
    def get_biodiversity_recommendations(self) -> List[str]:
        """Get recommendations to improve biodiversity."""
        recommendations = []
        species_by_type = {}
        
        for species in self.species_index.values():
            type_key = species.species_type.value
            if type_key not in species_by_type:
                species_by_type[type_key] = 0
            species_by_type[type_key] += 1
        
        # Check pollinator diversity
        if species_by_type.get('pollinator', 0) < self.target_pollinator_species:
            recommendations.append("Plant native flowering plants to attract pollinators")
            recommendations.append("Create bee-friendly habitats with diverse flowering periods")
        
        # Check predator diversity
        if species_by_type.get('predator', 0) < self.target_predator_species:
            recommendations.append("Maintain field margins with native vegetation for predators")
            recommendations.append("Reduce pesticide use to support natural pest control")
        
        # Check soil organisms
        if species_by_type.get('soil_organism', 0) < self.target_soil_organisms:
            recommendations.append("Increase soil organic matter to support soil biodiversity")
            recommendations.append("Practice reduced tillage to preserve soil structure")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Maintain current biodiversity-friendly practices")
        else:
            recommendations.append("Establish wildlife corridors between field patches")
            recommendations.append("Avoid monoculture; diversify crop rotations")
        
        return recommendations


class PollotectionService:
    """Monitors and protects pollinator populations."""
    
    def __init__(self):
        self.pollinator_populations: Dict[str, int] = {}
        self.flowering_resources: List[str] = []
        self.nesting_sites: List[str] = []
    
    def calculate_pollinator_health_index(self, 
                                         population_trend: float,
                                         resource_availability: float,
                                         nesting_availability: float) -> float:
        """
        Calculate pollinator health index (0-100).
        
        Args:
            population_trend: -1 to 1 scale (-1 declining, 0 stable, 1 increasing)
            resource_availability: 0-1 scale (food resources)
            nesting_availability: 0-1 scale (nesting sites)
        
        Returns:
            Health index score
        """
        population_score = (population_trend + 1) / 2 * 40  # 0-40 points
        resource_score = resource_availability * 30  # 0-30 points
        nesting_score = nesting_availability * 30  # 0-30 points
        
        return population_score + resource_score + nesting_score
    
    def recommend_flowering_plants(self, bloom_period: str) -> List[Dict]:
        """
        Recommend flowering plants for specific bloom periods.
        
        Args:
            bloom_period: "spring", "summer", "autumn", "winter"
        
        Returns:
            List of recommended plants with characteristics
        """
        plants_database = {
            'spring': [
                {'name': 'Dandelion', 'height_cm': 30, 'nectar_value': 'high'},
                {'name': 'Clover', 'height_cm': 10, 'nectar_value': 'high'},
                {'name': 'Wildflower mix', 'height_cm': 45, 'nectar_value': 'medium'},
            ],
            'summer': [
                {'name': 'Sunflower', 'height_cm': 150, 'nectar_value': 'high'},
                {'name': 'Lavender', 'height_cm': 60, 'nectar_value': 'high'},
                {'name': 'Borage', 'height_cm': 45, 'nectar_value': 'high'},
            ],
            'autumn': [
                {'name': 'Aster', 'height_cm': 60, 'nectar_value': 'medium'},
                {'name': 'Goldenrod', 'height_cm': 90, 'nectar_value': 'medium'},
            ],
            'winter': [
                {'name': 'Winter flowering shrubs', 'height_cm': 200, 'nectar_value': 'low'},
            ]
        }
        
        return plants_database.get(bloom_period, [])


class PestManagementIntegrated:
    """Implements integrated pest management with biodiversity considerations."""
    
    def __init__(self):
        self.pest_records: List[Dict] = []
    
    def evaluate_pest_control_strategy(self, pest_type: str,
                                      population_threshold: int,
                                      natural_enemies_present: bool) -> str:
        """
        Recommend pest control strategy prioritizing biodiversity.
        
        Returns:
            Recommended strategy
        """
        if natural_enemies_present and population_threshold < 100:
            return "Monitor and support natural predators - no action needed"
        
        if natural_enemies_present:
            return "Encourage natural enemy populations through habitat management"
        
        if population_threshold < 50:
            return "Monitor pest population - consider cultural practices"
        
        return "Consider biological control or targeted organic pesticides as last resort"
    
    def calculate_biodiversity_impact_score(self, 
                                           pesticide_type: str,
                                           application_rate: float) -> float:
        """
        Calculate potential impact of pest management on biodiversity.
        Lower scores indicate less harm to non-target organisms.
        """
        # Pesticide impact factors
        toxicity_factors = {
            'neonicotinoid': 0.9,
            'pyrethroid': 0.7,
            'organophosphate': 0.8,
            'biological': 0.2,
            'mechanical': 0.0,
        }
        
        base_impact = toxicity_factors.get(pesticide_type, 0.5)
        impact_score = base_impact * application_rate
        
        return min(1.0, impact_score)