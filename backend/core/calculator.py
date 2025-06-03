from sqlalchemy.orm import Session
from models import Material, Process, GridMix
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ManufacturingScenario:
    material_name: str
    process_name: str
    grid_mix_name: str
    mass_kg: float

class EmissionsCalculator:
    def __init__(self, db_session: Session):
        self.session = db_session

    def calculate_scenario_emissions(self, scenario: ManufacturingScenario) -> Dict:
        """Calculate total emissions for a given manufacturing scenario."""
        # Get required data from database
        material = self.session.query(Material).filter(Material.name == scenario.material_name).first()
        process = self.session.query(Process).filter(Process.name == scenario.process_name).first()
        grid_mix = self.session.query(GridMix).filter(GridMix.name == scenario.grid_mix_name).first()

        if not all([material, process, grid_mix]):
            raise ValueError("One or more components not found in database")

        # Calculate emissions
        material_emissions = material.production_emissions * scenario.mass_kg
        process_energy = process.energy_consumption * scenario.mass_kg
        process_emissions = (process_energy * grid_mix.emissions_factor) + \
                          (process.emissions_factor * scenario.mass_kg if process.emissions_factor else 0)
        
        total_emissions = material_emissions + process_emissions

        return {
            "total_emissions_kg_co2e": total_emissions,
            "breakdown": {
                "material_production_emissions": material_emissions,
                "process_emissions": process_emissions,
                "grid_mix_emissions_factor": grid_mix.emissions_factor,
                "process_energy_consumption_kwh": process_energy
            },
            "scenario_details": {
                "material": material.name,
                "material_type": material.type.value,
                "process": process.name,
                "grid_mix": grid_mix.name,
                "mass_kg": scenario.mass_kg
            }
        }

    def compare_scenarios(self, scenarios: List[ManufacturingScenario]) -> List[Dict]:
        """Compare multiple manufacturing scenarios."""
        results = []
        for scenario in scenarios:
            result = self.calculate_scenario_emissions(scenario)
            results.append(result)
        return results
