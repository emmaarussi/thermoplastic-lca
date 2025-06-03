import matplotlib.pyplot as plt
import numpy as np
from recycling_scenarios import RecyclingScenario

def create_co2_emissions_comparison():
    """Create a comparison plot of CO2 emissions for different scenarios."""
    # Define scenarios with the correct values
    scenario1 = RecyclingScenario(
        "Aggregated Process\n(Sphera)",
        granulator_energy_mj=2.65,
        pelletizing_energy_mj=0.0
    )
    
    scenario2 = RecyclingScenario(
        "Separate Processes\n(Sphera)",
        granulator_energy_mj=0.33,
        pelletizing_energy_mj=1.1
    )
    
    scenario3 = RecyclingScenario(
        "Hybrid Process\n(Spiral + Sphera)",
        granulator_energy_mj=0.05,
        pelletizing_energy_mj=1.1
    )
    
    scenario4 = RecyclingScenario(
        "Alternative Process\n(Sphera + PIE)",
        granulator_energy_mj=0.33,
        pelletizing_energy_mj=2.2716
    )
    
    scenario5 = RecyclingScenario(
        "Incineration",
        granulator_energy_mj=2.9/0.0581,  # Convert CO2 emissions back to energy using grid factor
        pelletizing_energy_mj=0.0
    )
    
    scenarios = [scenario1, scenario2, scenario3, scenario4, scenario5]
    
    # Calculate emissions for different material combinations
    emissions_100_pa6 = [s.calculate_emissions_with_material(1.0, 100, 'PA6')['total_emissions'] for s in scenarios]
    emissions_70_pa6 = [s.calculate_emissions_with_material(1.0, 70, 'PA6')['total_emissions'] for s in scenarios]
    emissions_70_peek = [s.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions'] for s in scenarios]
    emissions_70_pps = [s.calculate_emissions_with_material(1.0, 70, 'PPS')['total_emissions'] for s in scenarios]

    # Create figure
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set up bar positions
    x = np.arange(len(scenarios))
    width = 0.2
    
    # Create bars
    ax.bar(x - width*1.5, emissions_100_pa6, width, label='100% Recyclate', color='#2ecc71')
    ax.bar(x - width*0.5, emissions_70_pa6, width, label='70% Recyclate + 30% PA6', color='#000000')
    ax.bar(x + width*0.5, emissions_70_peek, width, label='70% Recyclate + 30% PEEK', color='#ff7f0e')
    ax.bar(x + width*1.5, emissions_70_pps, width, label='70% Recyclate + 30% PPS', color='#808080')
    
    # Customize plot
    ax.set_ylabel('CO₂ Emissions (kg)', fontsize=11)
    ax.set_title('CO₂ Emissions Comparison for Different Processing Routes\n(1 kg Material)', fontsize=14, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([s.name for s in scenarios], rotation=45, ha='right')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Add legend
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    
    # Save plot
    plt.savefig('co2_emissions_comparison.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.close()

if __name__ == "__main__":
    create_co2_emissions_comparison()
