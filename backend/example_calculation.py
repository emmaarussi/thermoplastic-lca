from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from emissions_calculator import EmissionsCalculator, ManufacturingScenario

# Database connection
DATABASE_URL = 'postgresql://postgres:localhost@localhost/thermoplastic_lca'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def main():
    calculator = EmissionsCalculator(session)

    # Define different manufacturing scenarios
    scenarios = [
        ManufacturingScenario(
            material_name='Polypropylene (PP)',
            process_name='Injection Molding for PP',
            grid_mix_name='DE grid mix',
            mass_kg=1.0
        ),
        ManufacturingScenario(
            material_name='Polypropylene (PP)',
            process_name='Injection Molding for PP',
            grid_mix_name='NL grid mix',
            mass_kg=1.0
        ),
        ManufacturingScenario(
            material_name='Carbon Fiber Reinforced Polymer (CFRP)',
            process_name='Injection Molding for PP',  # Note: In real scenario, you'd use appropriate CFRP process
            grid_mix_name='DE grid mix',
            mass_kg=1.0
        )
    ]

    try:
        # Compare different scenarios
        results = calculator.compare_scenarios(scenarios)
        
        # Print results
        print("\nEmissions Comparison Results:")
        print("=" * 50)
        for i, result in enumerate(results, 1):
            print(f"\nScenario {i}:")
            print(f"Material: {result['scenario_details']['material']}")
            print(f"Process: {result['scenario_details']['process']}")
            print(f"Grid Mix: {result['scenario_details']['grid_mix']}")
            print(f"Total Emissions: {result['total_emissions_kg_co2e']:.2f} kg CO2e")
            print("\nBreakdown:")
            print(f"- Material Production: {result['breakdown']['material_production_emissions']:.2f} kg CO2e")
            print(f"- Process Emissions: {result['breakdown']['process_emissions']:.2f} kg CO2e")
            print(f"- Energy Consumption: {result['breakdown']['process_energy_consumption_kwh']:.2f} kWh")
            print("-" * 30)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
