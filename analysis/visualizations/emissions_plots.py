"""Emissions visualization module for thermoplastic LCA analysis."""

import matplotlib.pyplot as plt
import numpy as np
from ..scenarios.recycling import RecyclingScenario
from ..utils.plotting import setup_plot_style, add_value_labels, setup_grid, save_plot

def create_co2_emissions_comparison():
    """Create a comparison plot of CO2 emissions for different scenarios."""
    # Define scenarios
    scenarios = [
        RecyclingScenario("Aggregated Process\n(Sphera)", 2.65, 0.0),
        RecyclingScenario("Separate Processes\n(Sphera)", 0.33, 1.1),
        RecyclingScenario("Hybrid Process\n(Spiral + Sphera)", 0.05, 1.1),
        RecyclingScenario("Alternative Process\n(Sphera + PIE)", 0.33, 2.2716),
        RecyclingScenario("Incineration", 2.9/0.0581, 0.0)
    ]
    
    # Calculate emissions
    emissions_data = {
        '100% Recyclate': [s.calculate_emissions_with_material(1.0, 100, 'PA6')['total_emissions'] for s in scenarios],
        '70% Recyclate + 30% PA6': [s.calculate_emissions_with_material(1.0, 70, 'PA6')['total_emissions'] for s in scenarios],
        '70% Recyclate + 30% PEEK': [s.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions'] for s in scenarios],
        '70% Recyclate + 30% PPS': [s.calculate_emissions_with_material(1.0, 70, 'PPS')['total_emissions'] for s in scenarios]
    }
    
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(12, 8))
    
    x = np.arange(len(scenarios))
    width = 0.2
    multiplier = 0
    
    for attribute, measurement in emissions_data.items():
        offset = width * multiplier
        bars = ax.bar(x + offset, measurement, width, label=attribute)
        multiplier += 1
    
    ax.set_ylabel('CO₂ Emissions (kg)')
    ax.set_title('CO₂ Emissions Comparison for Different Processing Routes\n(1 kg Material)')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels([s.name for s in scenarios], rotation=45, ha='right')
    setup_grid(ax)
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    save_plot(fig, 'results/plots/emissions/co2_emissions_comparison.png')

def create_co2_bar_comparison():
    """Create a bar plot comparison of CO2 emissions with logarithmic scale."""
    spiral_process = RecyclingScenario(
        "Hybrid Process\n(Spiral + Sphera)",
        granulator_energy_mj=0.05,
        pelletizing_energy_mj=1.1
    )
    
    # Calculate emissions
    values = [
        spiral_process.calculate_emissions_with_material(1.0, 100, 'PEEK')['total_emissions'],
        spiral_process.calculate_emissions_with_material(1.0, 70, 'PEEK')['total_emissions'],
        2.9,  # Incineration emissions
        30.0  # CF-PEEK virgin production
    ]
    
    labels = [
        'Spiral Process\n(100% Scrap)',
        'Spiral Process\n(70% Scrap + 30% PEEK)',
        'Incineration\n(1 kg TP Scrap)',
        'CF-PEEK\nVirgin Production'
    ]
    
    colors = ['green', '#2ecc71', '#ff7f0e', '#FF5000']
    
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(np.arange(len(labels)), values, color=colors)
    
    ax.set_ylabel('CO₂-eq Emissions (kg)')
    ax.set_title('CO₂-eq Emissions Comparison\nClimate Change, Global Warming Potential (GWP100)\nDeclared Unit: 1 kg Material')
    ax.set_ylim(bottom=0)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    
    setup_grid(ax, alpha=0.3)
    add_value_labels(ax, bars)
    
    plt.tight_layout()
    save_plot(fig, 'results/plots/emissions/co2_bar_comparison.png')

if __name__ == "__main__":
    create_co2_emissions_comparison()
    create_co2_bar_comparison()
