# Thermoplastic Life Cycle Assessment Tool

A comprehensive tool for analyzing the life cycle and environmental impact of thermoplastic and composite materials, with a focus on end-of-life (EOL) stakeholder management and material flow tracking.

## Project Structure

```
thermoplastic-lca/
├── backend/            # Core backend functionality
│   ├── api/           # FastAPI routes
│   ├── core/          # Core business logic
│   └── db/            # Database operations
├── analysis/          # Analysis modules
│   ├── scenarios/     # Recycling scenarios
│   ├── visualizations/# Plotting modules
│   └── utils/         # Common utilities
├── EOL flow modelling/# End-of-Life tracking
│   ├── flow_app.py    # Streamlit interface
│   └── *.csv         # Stakeholder and flow data
├── notebooks/         # Jupyter notebooks
└── results/           # Analysis outputs
    ├── plots/         # Generated plots
    └── reports/       # Analysis reports
```

## Features

- Material and process database
- Emissions calculation engine
- Recycling scenario analysis
- Visualization tools
- API endpoints for integration
- Stakeholder interview tracking
- Material flow monitoring
- End-of-Life chain assessment
- Risk factor evaluation

## Setup

1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure database:
   - Update database settings in `backend/db/connection.py`
   - Run database migrations
   - Seed initial data using `backend/db/seed_data.py`

3. Run the API:
   ```bash
   uvicorn backend.api.routes:app --reload
   ```

4. Launch the EOL Flow Tracking Interface:
   ```bash
   cd "EOL flow modelling"
   streamlit run flow_app.py
   ```

## Usage

### Analysis and Calculations
Refer to the notebooks in the `notebooks/` directory for example usage and analysis workflows.

### EOL Flow Tracking
The Streamlit interface provides tools for:
- Recording stakeholder interviews
- Tracking material flows between organizations
- Assessing End-of-Life chain activities
- Evaluating risk factors
- Monitoring value chain responsibilities

## License

MIT
