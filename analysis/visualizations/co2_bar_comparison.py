import matplotlib.pyplot as plt
import numpy as np
from recycling_scenarios import RecyclingScenario

def create_co2_bar_comparison():
    """Create a bar plot comparison of CO2 emissions with logarithmic scale."""
    # Create the spiral process scenario
    spiral_process = RecyclingScenario(
        "Hybrid Process\n(Spiral + Sphera)",
        granulator_energy_mj=0.05,
        pelletizing_energy_mj=1.1
    )
    
    # Calculate emissions for different scenarios
    spiral_100_scrap = spiral_process.calculate_emissions_with_material(1.0, 100, 'PEEK')['total_emissions']
    spiral_70_peek = spiral_process.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions']
    
    # Incineration emissions (direct value)
    incineration_emissions = 2.9  # kg CO2 eq.
    
    # CF-PEEK virgin production value
    cf_peek_virgin = 30.0  # kg CO2 eq.
    
    # Prepare data for bar plot
    values = [spiral_100_scrap, spiral_70_peek, incineration_emissions, cf_peek_virgin]
    labels = ['Spiral Process\n(100% Scrap)',
             'Spiral Process\n(70% Scrap + 30% PEEK)',
             'Incineration\n(1 kg TP Scrap)',
             'CF-PEEK\nVirgin Production']
    colors = ['green', '#2ecc71', '#ff7f0e', '#FF5000']  # More vibrant orange for CF-PEEK
    
    # Create figure
    plt.style.use('default')
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create bars
    x = np.arange(len(labels))
    bars = ax.bar(x, values, color=colors)
    
    # Customize plot
    ax.set_ylabel('CO₂-eq Emissions (kg)', fontsize=11)
    ax.set_title('CO₂-eq Emissions Comparison\nClimate Change, Global Warming Potential (GWP100)\nDeclared Unit: 1 kg Material', fontsize=14, pad=20)
    
    # Set y-axis to start at 0
    ax.set_ylim(bottom=0)
    
    # Set x-tick labels
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    
    # Add grid for better readability
    ax.grid(True, axis='y', linestyle='--', alpha=0.3, color='gray')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save plot
    plt.savefig('co2_emissions_comparison.png',
                dpi=300,
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.close()

if __name__ == "__main__":
    create_co2_bar_comparison()
