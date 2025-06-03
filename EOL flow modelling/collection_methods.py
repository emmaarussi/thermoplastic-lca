import pandas as pd
from pathlib import Path

# Define collection method options with descriptions and categories
collection_methods = pd.DataFrame([
    {"Method Category": "Formal Process", "Collection Method": "Scheduled In-House Dismantling", "Description": "Planned removal of components by internal staff"},
    {"Method Category": "Formal Process", "Collection Method": "Third-Party Contractor", "Description": "Outsourced disassembly and collection"},
    {"Method Category": "Formal Process", "Collection Method": "On-Site Sorting and Segregation", "Description": "Material is sorted and stored separately at the source"},
    {"Method Category": "Informal/Ad Hoc", "Collection Method": "Disposed as Mixed Waste", "Description": "Discarded without segregation or recovery"},
    {"Method Category": "Informal/Ad Hoc", "Collection Method": "Stored with No Clear Strategy", "Description": "Material stored or stockpiled without a recycling or disposal plan"},
    {"Method Category": "Informal/Ad Hoc", "Collection Method": "Untracked Removal", "Description": "Material is removed or disappears without clear documentation"},
    {"Method Category": "Other", "Collection Method": "Other", "Description": "Unspecified or emerging methods"}
])

# Save to CSV in the project directory
collection_file_path = Path(__file__).parent.parent / "collection_methods.csv"
collection_methods.to_csv(collection_file_path, index=False)
print(f"Saved collection methods to {collection_file_path}")
