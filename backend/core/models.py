from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class MaterialType(enum.Enum):
    thermoplastic = "thermoplastic"
    composite = "composite"
    fiber = "fiber"
    additive = "additive"
    filler = "filler"

class ProcessType(enum.Enum):
    injection_molding = "injection_molding"
    extrusion = "extrusion"
    thermoforming = "thermoforming"
    blow_molding = "blow_molding"

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(Enum(MaterialType), nullable=False)
    density = Column(Float)  # kg/m3
    production_emissions = Column(Float)  # kg CO2e/kg
    processing_temp_min = Column(Float)  # °C
    processing_temp_max = Column(Float)  # °C
    properties = Column(JSON)  # Additional properties

class Process(Base):
    __tablename__ = "processes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Enum(ProcessType), nullable=False)
    energy_consumption = Column(Float)  # kWh/kg
    emissions_factor = Column(Float)  # kg CO2e/kg

class GridMix(Base):
    __tablename__ = "grid_mix"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    emissions_factor = Column(Float)  # kg CO2e/kWh
    country_code = Column(String(2))  # Two-letter country code
