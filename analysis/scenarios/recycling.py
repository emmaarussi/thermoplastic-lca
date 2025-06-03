##Calculate emissions and energy consumption for different recycling scenarios.

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy import stats

class RecyclingScenario:
    def __init__(self, name, granulator_energy_mj, pelletizing_energy_mj, de_grid_co2_per_mj=0.161):
        self.name = name
        self.granulator_energy_mj = granulator_energy_mj
        self.pelletizing_energy_mj = pelletizing_energy_mj
        self.de_grid_co2_per_mj = de_grid_co2_per_mj
        self.pa6_co2_per_kg = 4.45   # kg CO2 per kg material
        self.peek_co2_per_kg = 13.70  # kg CO2 per kg material
        self.pps_co2_per_kg = 2.13   # kg CO2 per kg material (estimated)

    def calculate_emissions_with_material(self, final_weight_kg, scrap_percentage=100, material_type='PA6'):
        """Calculate emissions for given weight and scrap percentage with specified material."""
        # Calculate total energy
        total_energy_mj = (self.granulator_energy_mj + self.pelletizing_energy_mj) * final_weight_kg
        
        # Calculate emissions from energy
        energy_emissions = total_energy_mj * self.de_grid_co2_per_mj
        
        # Calculate material emissions based on material type
        if material_type == 'PA6':
            material_co2_per_kg = self.pa6_co2_per_kg
        elif material_type == 'PEEK':
            material_co2_per_kg = self.peek_co2_per_kg
        elif material_type == 'PPS':
            material_co2_per_kg = self.pps_co2_per_kg
        else:
            raise ValueError(f'Unknown material type: {material_type}')
        
        material_emissions = (100 - scrap_percentage) / 100 * material_co2_per_kg * final_weight_kg
        
        return {
            'total_energy_mj': total_energy_mj,
            'energy_emissions': energy_emissions,
            'material_emissions': material_emissions,
            'total_emissions': energy_emissions + material_emissions
        }

    def calculate_emissions(self, final_weight_kg, scrap_percentage=100):
        """Calculate emissions for given weight and scrap percentage."""
        # Calculate total energy
        total_energy_mj = self.granulator_energy_mj + self.pelletizing_energy_mj
        
        # Calculate emissions from energy
        energy_emissions = total_energy_mj * self.de_grid_co2_per_mj
        
        # Calculate material emissions (if using virgin PA6)
        virgin_pa6_percentage = (100 - scrap_percentage) / 100
        material_emissions = virgin_pa6_percentage * self.pa6_co2_per_kg
        
        # Total emissions per kg
        total_emissions_per_kg = energy_emissions + material_emissions
        
        # Scale to final weight
        total_emissions = total_emissions_per_kg * final_weight_kg
        
        return {
            'total_energy_mj': total_energy_mj * final_weight_kg,
            'energy_emissions': energy_emissions * final_weight_kg,
            'material_emissions': material_emissions * final_weight_kg,
            'total_emissions': total_emissions
        }

def print_scenario_results(scenario, weights, scrap_percentages):
    """Print results for a scenario with different weights and scrap percentages."""
    print(f"\n=== {scenario.name} ===")
    print(f"Base energy consumption: {scenario.granulator_energy_mj + scenario.pelletizing_energy_mj:.3f} MJ/kg")
    
    for weight in weights:
        print(f"\nResults for {weight:.3f} kg final material:")
        for scrap in scrap_percentages:
            results = scenario.calculate_emissions(weight, scrap)
            print(f"\n{scrap}% scrap material:")
            print(f"Total energy: {results['total_energy_mj']:.6f} MJ")
            print(f"Energy emissions: {results['energy_emissions']:.6f} kg CO2")
            print(f"Material emissions: {results['material_emissions']:.6f} kg CO2")
            print(f"Total emissions: {results['total_emissions']:.6f} kg CO2")

def create_materials_comparison_plot(scenarios):
    """Create a bar plot comparing different materials for 1kg production."""
    plt.style.use('default')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle('CO₂ Emissions Comparison for Different Materials\n(1 kg Material)', fontsize=14, y=0.95)
    
    # Calculate emissions for each scenario and material combination
    emissions_100 = [s.calculate_emissions_with_material(1.0, 100, 'PA6')['total_emissions'] for s in scenarios]
    emissions_70_pa6 = [s.calculate_emissions_with_material(1.0, 70, 'PA6')['total_emissions'] for s in scenarios]
    emissions_70_peek = [s.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions'] for s in scenarios]
    emissions_70_pps = [s.calculate_emissions_with_material(1.0, 70, 'PPS')['total_emissions'] for s in scenarios]
    
    # Set up bar positions
    x = np.arange(len(scenarios))
    width = 0.2
    
    # Create bars
    ax.bar(x - width*1.5, emissions_100, width, label='100% Scrap', color='#2ecc71')
    ax.bar(x - width*0.5, emissions_70_pa6, width, label='70% Scrap + 30% PA6', color='#000000')
    ax.bar(x + width*0.5, emissions_70_peek, width, label='70% Scrap + 30% PEEK', color='#ff7f0e')
    ax.bar(x + width*1.5, emissions_70_pps, width, label='70% Scrap + 30% PPS', color='#808080')
    
    # Customize plot
    ax.set_ylabel('CO₂ Emissions (kg)', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels([s.name for s in scenarios], rotation=45, ha='right')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Add legend
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    
    # Save plot
    plt.savefig('materials_comparison.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_comparison_plots(scenarios, weights, scrap_percentages):
    """Create bar plots comparing scenarios."""
    # Set style for better readability
    plt.style.use('default')
    
    # Prepare data
    scenario_names = [s.name for s in scenarios]
    n_scenarios = len(scenarios)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), height_ratios=[1, 1.5])
    fig.suptitle('Comparison of Recycling Scenarios (1 kg Material)', fontsize=14, y=0.95)
    
    # Common styling function
    def style_axis(ax, title):
        ax.set_title(title, pad=20, fontsize=12)
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        for label in ax.get_xticklabels():
            label.set_horizontalalignment('right')
    
    # Plot 1: Energy consumption per kg
    energies = [s.granulator_energy_mj + s.pelletizing_energy_mj for s in scenarios]
    ax1.bar(range(n_scenarios), energies, color='#808080')
    ax1.set_xticks(range(n_scenarios))
    ax1.set_xticklabels(scenario_names)
    ax1.set_ylabel('Energy (MJ/kg)', fontsize=11)
    style_axis(ax1, 'Total Energy Consumption per kg')
    
    # Plot 2: CO2 emissions for 1kg (100%, 70% PA6, 70% PEEK)
    emissions_100 = [s.calculate_emissions_with_material(1.0, 100, 'PA6')['total_emissions'] for s in scenarios]
    emissions_70_pa6 = [s.calculate_emissions_with_material(1.0, 70, 'PA6')['total_emissions'] for s in scenarios]
    emissions_70_peek = [s.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions'] for s in scenarios]
    
    x = np.arange(n_scenarios)
    width = 0.25
    
    # Use orange, black, and green color scheme
    ax2.bar(x - width, emissions_100, width, label='100% Scrap', color='#2ecc71')
    ax2.bar(x, emissions_70_pa6, width, label='70% Scrap + 30% PA6', color='#000000')
    ax2.bar(x + width, emissions_70_peek, width, label='70% Scrap + 30% PEEK', color='#ff7f0e')
    
    ax2.set_xticks(x)
    ax2.set_xticklabels(scenario_names)
    ax2.set_ylabel('CO2 Emissions (kg)', fontsize=11)
    style_axis(ax2, 'CO2 Emissions for 1kg Material')
    
    # Adjust legend position and style
    ax2.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    
    # Save with high quality
    plt.savefig('recycling_scenarios_comparison.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_cascade_plot(scenario, n_cycles=10):
    """Create a plot showing emissions over multiple recycling cycles."""
    plt.style.use('default')
    
    # Calculate emissions for initial production (70% recycled + 30% virgin PEEK)
    initial_emissions = scenario.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions']
    
    # Calculate emissions for subsequent cycles (100% recycled, using spiral grinding)
    cycle_emissions = []
    cumulative_emissions = [initial_emissions]
    
    # Create recycling scenario with spiral grinding
    spiral_scenario = RecyclingScenario(
        "Spiral Grinding + Sphera Pelletization",
        granulator_energy_mj=0.05,  # Spiral grinding energy
        pelletizing_energy_mj=1.1    # Sphera pelletization energy
    )
    
    # Calculate emissions for each cycle
    for cycle in range(1, n_cycles):
        cycle_emission = spiral_scenario.calculate_emissions_with_material(1.0, 100, 'PEEK')['total_emissions']
        cycle_emissions.append(cycle_emission)
        cumulative_emissions.append(cumulative_emissions[-1] + cycle_emission)
    
    # Calculate average emissions per cycle
    average_emissions = [cum_em / (i + 1) for i, cum_em in enumerate(cumulative_emissions)]
    
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), height_ratios=[1, 1.5])
    fig.suptitle('PEEK Cascading Recycling Analysis\n(1 kg Material)', fontsize=14, y=0.95)
    
    # Plot cumulative emissions
    cycles = range(n_cycles)
    ax1.plot(cycles, cumulative_emissions, marker='o', color='#ff7f0e', linewidth=2)
    ax1.set_ylabel('Cumulative CO₂ Emissions (kg)', fontsize=11)
    ax1.set_xlabel('Number of Recycling Cycles', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_title('Cumulative CO₂ Emissions Over Recycling Cycles', pad=20, fontsize=12)
    
    # Plot average emissions per cycle
    ax2.plot(cycles, average_emissions, marker='s', color='#2ecc71', linewidth=2)
    ax2.set_ylabel('Average CO₂ Emissions per Cycle (kg)', fontsize=11)
    ax2.set_xlabel('Number of Recycling Cycles', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_title('Average CO₂ Emissions per Recycling Cycle', pad=20, fontsize=12)

def create_cascade_plot_2(scenario, n_cycles=10):
    """Create a plot showing emissions over multiple recycling cycles, with cumulative graph starting at 0."""
    plt.style.use('default')
    
    # Calculate emissions for initial production (70% recycled + 30% virgin PEEK)
    initial_emissions = scenario.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions']
    
    # Calculate emissions for subsequent cycles (100% recycled, using spiral grinding)
    cycle_emissions = [initial_emissions]  # Start with initial emissions
    cumulative_emissions = [initial_emissions]  # Start with initial emissions
    
    # Create recycling scenario with spiral grinding
    spiral_scenario = RecyclingScenario(
        "Spiral Grinding + Sphera Pelletization",
        granulator_energy_mj=0.05,  # Spiral grinding energy
        pelletizing_energy_mj=1.1    # Sphera pelletization energy
    )
    
    # Calculate emissions for each cycle
    for cycle in range(1, n_cycles):
        cycle_emission = spiral_scenario.calculate_emissions_with_material(1.0, 100, 'PEEK')['total_emissions']
        cycle_emissions.append(cycle_emission)
        cumulative_emissions.append(cumulative_emissions[-1] + cycle_emission)
    
    # Calculate average emissions per cycle
    average_emissions = [cum_em / (i + 1) for i, cum_em in enumerate(cumulative_emissions)]
    
    # Create the visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), height_ratios=[1, 1.5])
    fig.suptitle('PEEK Cascading Recycling Analysis\n(1 kg Material) - Version 2', fontsize=14, y=0.95)
    
    # Plot cumulative emissions
    cycles = range(n_cycles)
    ax1.plot(cycles, cumulative_emissions, marker='o', color='#ff7f0e', linewidth=2)
    ax1.set_ylabel('Cumulative CO₂ Emissions (kg)', fontsize=11)
    ax1.set_xlabel('Number of Recycling Cycles', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_ylim(bottom=0)  # Force y-axis to start at 0
    ax1.set_title('Cumulative CO₂ Emissions Over Recycling Cycles (Starting at 0)', pad=20, fontsize=12)
    
    # Plot average emissions per cycle
    ax2.plot(cycles, average_emissions, marker='s', color='#2ecc71', linewidth=2)
    ax2.set_ylabel('Average CO₂ Emissions per Cycle (kg)', fontsize=11)
    ax2.set_xlabel('Number of Recycling Cycles', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.set_title('Average CO₂ Emissions per Recycling Cycle', pad=20, fontsize=12)
    
    # Add text box with key information
    info_text = f'Initial cycle (30% virgin PEEK): {initial_emissions:.3f} kg CO₂\n'
    info_text += f'Subsequent cycles (100% recycled): {cycle_emissions[0]:.3f} kg CO₂\n'
    info_text += f'Average emissions after {n_cycles} cycles: {average_emissions[-1]:.3f} kg CO₂'
    
    plt.figtext(0.15, 0.02, info_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    
    # Save plot
    plt.savefig('peek_cascade_recycling2.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_recycling_process_diagram():
    """Create a circular diagram showing the recycling process steps."""
    plt.style.use('default')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': 'polar'})
    fig.patch.set_facecolor('white')
    
    # Define the steps
    steps = [
        'Collection of\nRecyclable Materials',
        'Breaking Down\ninto Fragments',
        'Sorting by\nProperties',
        'Reprocessing into\nRaw Materials',
        'New Product\nManufacturing'
    ]
    
    # Calculate angles for each step
    n_steps = len(steps)
    angles = np.linspace(0, 2*np.pi, n_steps, endpoint=False)
    
    # Define colors
    colors = ['#2ecc71', '#000000', '#ff7f0e', '#2ecc71', '#000000']
    
    # Plot connecting arrows in a circle
    radius = 0.8
    arrow_length = 2*np.pi/n_steps * 0.8
    
    for i, (angle, step) in enumerate(zip(angles, steps)):
        # Plot step number
        number_angle = angle - 0.2
        ax.text(number_angle, 1.3, f'{i+1}', 
                ha='center', va='center', fontsize=12,
                bbox=dict(facecolor='white', edgecolor=colors[i], boxstyle='circle'))
        
        # Plot step text
        text_angle = angle
        ax.text(text_angle, 1.1, step, 
                ha='center', va='center', fontsize=10,
                bbox=dict(facecolor='white', edgecolor=colors[i], 
                         boxstyle='round,pad=0.5', alpha=0.9))
        
        # Plot arrow
        next_angle = angles[(i + 1) % n_steps]
        arrow_start = angle + arrow_length * 0.1
        arrow_end = next_angle - arrow_length * 0.1
        
        arrow = patches.FancyArrowPatch(
            (arrow_start, radius), (arrow_end, radius),
            transform=ax.transData,
            color=colors[i],
            arrowstyle='->,head_length=0.7,head_width=0.3',
            connectionstyle=f'arc3,rad=0.3',
            linewidth=2
        )
        ax.add_patch(arrow)
    
    # Add title
    plt.title('Circular Recycling Process', y=1.4, fontsize=14, pad=20)
    
    # Remove axis and grid
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['polar'].set_visible(False)
    
    # Save the plot
    plt.savefig('recycling_process.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_energy_comparison_plot(scenarios):
    """Create a bar plot comparing energy consumption for different processes."""
    plt.style.use('default')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.suptitle('Energy Consumption Comparison\n(1 kg Material)', fontsize=14, y=0.95)
    
    # Get energy data
    granulator_energy = [s.granulator_energy_mj for s in scenarios]
    pelletizing_energy = [s.pelletizing_energy_mj for s in scenarios]
    total_energy = [g + p for g, p in zip(granulator_energy, pelletizing_energy)]
    
    # Set up bar positions
    x = np.arange(len(scenarios))
    width = 0.25
    
    # Create stacked bars with different shades of green
    ax.bar(x, granulator_energy, width, label='Granulator', color='#2ecc71')
    ax.bar(x, pelletizing_energy, width, bottom=granulator_energy, label='Pelletizing', color='#27ae60')
    
    # Add total energy values on top of bars
    for i, total in enumerate(total_energy):
        ax.text(i, total + 0.1, f'{total:.2f}', ha='center', va='bottom', fontsize=10)
    
    # Customize plot
    ax.set_ylabel('Energy Consumption (MJ/kg)', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels([s.name for s in scenarios], rotation=45, ha='right')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Add legend
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    
    # Save plot
    plt.savefig('energy_consumption.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.close()

def main():
    # Define scenarios with shorter names for better plot readability
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
    
    # Define weights to analyze
    weights = [1.0, 0.07]  # 1 kg and 0.07 kg
    scrap_percentages = [100, 70]  # 100% scrap and 70% scrap
    
    scenario5 = RecyclingScenario(
        "Incineration",
        granulator_energy_mj=2.9/0.0581,  # Convert CO2 emissions back to energy using grid factor
        pelletizing_energy_mj=0.0
    )
    
    # Calculate and print results for each scenario
    scenarios = [scenario1, scenario2, scenario3, scenario4, scenario5]
    for scenario in scenarios:
        print_scenario_results(scenario, weights, scrap_percentages)
    
    # Create visualizations
    create_comparison_plots(scenarios, weights, scrap_percentages)
    create_cascade_plot(scenario3)
    create_recycling_process_diagram()
    create_materials_comparison_plot(scenarios)
    create_energy_comparison_plot(scenarios)
    create_pa6_comparison_plot(scenarios)
    create_hybrid_process_analysis(scenario3)

def create_pa6_comparison_plot(scenarios):
    """Create a bar plot comparing only PA6 scenarios (100% recyclate vs 70% recyclate + 30% virgin)."""
    plt.style.use('default')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.suptitle('CO₂ Emissions Comparison: 100% Recyclate vs. 70% Recyclate + 30% Virgin PA6\n(1 kg Material)', 
                 fontsize=14, y=0.95)
    
    # Calculate emissions for each scenario
    emissions_100 = [s.calculate_emissions_with_material(1.0, 100, 'PA6')['total_emissions'] for s in scenarios]
    emissions_70_pa6 = [s.calculate_emissions_with_material(1.0, 70, 'PA6')['total_emissions'] for s in scenarios]
    
    # Set up bar positions
    x = np.arange(len(scenarios))
    width = 0.35
    
    # Create bars
    ax.bar(x - width/2, emissions_100, width, label='100% Recyclate', color='#2ecc71')
    ax.bar(x + width/2, emissions_70_pa6, width, label='70% Recyclate + 30% Virgin PA6', color='#000000')
    
    # Customize plot
    ax.set_ylabel('CO₂ Emissions (kg)', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels([s.name for s in scenarios], rotation=45, ha='right')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Add legend
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    
    # Save plot
    plt.savefig('pa6_comparison.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_hybrid_process_analysis(scenario):
    """Create a detailed analysis plot for the hybrid process (scenario 3) showing energy, CO2, and cascading scheme."""
    plt.style.use('default')
    
    # Create figure with three subplots
    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.2])
    ax1 = fig.add_subplot(gs[0, 0])  # Energy consumption
    ax2 = fig.add_subplot(gs[0, 1])  # CO2 emissions
    ax3 = fig.add_subplot(gs[1, :])  # Cascading scheme
    
    # Data preparation
    materials = ['100% Scrap', '70% + PEEK', '70% + PA6', '70% + PPS']
    energy_values = [
        scenario.granulator_energy_mj + scenario.pelletizing_energy_mj,
        scenario.granulator_energy_mj + scenario.pelletizing_energy_mj,
        scenario.granulator_energy_mj + scenario.pelletizing_energy_mj,
        scenario.granulator_energy_mj + scenario.pelletizing_energy_mj
    ]
    
    co2_values = [
        scenario.calculate_emissions_with_material(1.0, 100, 'PA6')['total_emissions'],
        scenario.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions'],
        scenario.calculate_emissions_with_material(1.0, 70, 'PA6')['total_emissions'],
        scenario.calculate_emissions_with_material(1.0, 70, 'PPS')['total_emissions']
    ]
    
    # Colors
    colors = ['#2ecc71', '#ff7f0e', '#000000', '#808080']
    
    # Plot 1: Energy consumption
    bars1 = ax1.bar(range(len(materials)), energy_values, color=colors)
    ax1.set_title('Energy Consumption', pad=20, fontsize=12)
    ax1.set_ylabel('Energy (MJ/kg)', fontsize=11)
    ax1.set_xticks(range(len(materials)))
    ax1.set_xticklabels(materials, rotation=45, ha='right')
    ax1.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Plot 2: CO2 emissions
    bars2 = ax2.bar(range(len(materials)), co2_values, color=colors)
    ax2.set_title('CO₂ Emissions', pad=20, fontsize=12)
    ax2.set_ylabel('CO₂ Emissions (kg/kg)', fontsize=11)
    ax2.set_xticks(range(len(materials)))
    ax2.set_xticklabels(materials, rotation=45, ha='right')
    ax2.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Plot 3: Cascading scheme
    n_cycles = 5
    x = range(n_cycles)
    
    # Calculate emissions for each material over cycles
    emissions_100 = [scenario.calculate_emissions_with_material(1.0, 100, 'PA6')['total_emissions']] * n_cycles
    emissions_peek = [scenario.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions']] * n_cycles
    emissions_pa6 = [scenario.calculate_emissions_with_material(1.0, 70, 'PA6')['total_emissions']] * n_cycles
    emissions_pps = [scenario.calculate_emissions_with_material(1.0, 70, 'PPS')['total_emissions']] * n_cycles
    
    ax3.plot(x, emissions_100, 'o-', color=colors[0], label='100% Scrap', linewidth=2)
    ax3.plot(x, emissions_peek, 's-', color=colors[1], label='70% + PEEK', linewidth=2)
    ax3.plot(x, emissions_pa6, '^-', color=colors[2], label='70% + PA6', linewidth=2)
    ax3.plot(x, emissions_pps, 'D-', color=colors[3], label='70% + PPS', linewidth=2)
    
    ax3.set_title('Emissions Over Multiple Cycles', pad=20, fontsize=12)
    ax3.set_xlabel('Cycle Number', fontsize=11)
    ax3.set_ylabel('CO₂ Emissions (kg/kg)', fontsize=11)
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    
    # Add value labels on bars
    def autolabel(rects, ax):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width()/2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', rotation=0)
    
    autolabel(bars1, ax1)
    autolabel(bars2, ax2)
    
    # Main title
    fig.suptitle(f'Detailed Analysis of {scenario.name}\n(1 kg Material)', fontsize=14, y=0.95)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])
    
    # Save plot
    plt.savefig('hybrid_process_analysis.png',
                dpi=300,
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.close()

def create_spiral_vs_sphera_comparison():
    """Create a bar plot comparing electricity expenditure between spiral and Sphera processes."""
    plt.style.use('default')
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Define the processes and their energy values (MJ/kg)
    processes = ['Spiral Process', 'Sphera Aggregated']
    energy_values = [1.15, 2.650]  # Spiral process vs Sphera aggregated
    
    # Create bars
    x = np.arange(len(processes))
    bars = ax.bar(x, energy_values, width=0.5, color='green')
    
    # Customize the plot
    ax.set_ylabel('Electricity Consumption (MJ/kg)', fontsize=12)
    ax.set_title('Electricity Expenditure Comparison:\nSpiral vs Sphera Source', fontsize=14, pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(processes, fontsize=10)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f} MJ/kg',
                ha='center', va='bottom')
    
    # Add grid for better readability
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('spiral_vs_sphera_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Create the spiral vs Sphera comparison plot
    create_spiral_vs_sphera_comparison()
    main()
