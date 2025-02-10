from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Material, Process

# Database connection
DATABASE_URL = 'postgresql://postgres:postgres@localhost/thermoplastic_lca'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Function to create the database tables
def create_tables():
    Base.metadata.create_all(engine)

# Function to seed data
def seed_data():
    session = Session()
    # Example data
    materials = [
        Material(name='Polypropylene (PP)', type=MaterialType.thermoplastic, density=0.9, production_emissions=2.5),
        Material(name='Carbon Fiber Reinforced Polymer (CFRP)', type=MaterialType.composite, density=1.6, production_emissions=15.0)
    ]
    processes = [
        Process(name='Injection Molding for PP', type=ProcessType.injection_molding, energy_consumption=0.5, emissions_factor=0.2)
    ]
    session.add_all(materials)
    session.add_all(processes)
    session.commit()
    session.close()
