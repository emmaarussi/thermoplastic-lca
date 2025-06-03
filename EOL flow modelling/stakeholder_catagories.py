import pandas as pd
from pathlib import Path

# Define stakeholder category data again after reset
stakeholder_categories = pd.DataFrame([
    {"Category Group": "Supplier", "Category Name": "Airline (EoL Supplier)", "Description": "Fleet operators discarding TPCs"},
    {"Category Group": "Supplier", "Category Name": "Aircraft Manufacturer", "Description": "Companies that produce aircraft using TPCs"},
    {"Category Group": "Supplier", "Category Name": "MRO Facility", "Description": "Maintenance, Repair, and Overhaul facilities"},
    {"Category Group": "Supplier", "Category Name": "Airport Waste/Logistics", "Description": "Airport services managing TPC waste"},
    {"Category Group": "Logistics & Processing", "Category Name": "Recycler", "Description": "Companies recycling thermoplastic composites"},
    {"Category Group": "Logistics & Processing", "Category Name": "Transport Company", "Description": "Companies transporting composite waste"},
    {"Category Group": "Logistics & Processing", "Category Name": "Regulator", "Description": "Bodies overseeing aviation/environmental compliance"},
    {"Category Group": "End Use", "Category Name": "End User - Construction", "Description": "Users of recycled TPCs in infrastructure/building"},
    {"Category Group": "End Use", "Category Name": "End User - Consumer Goods", "Description": "Users in furniture, appliances, etc."},
    {"Category Group": "End Use", "Category Name": "End User - Electronics", "Description": "Casings or components for electronics"},
    {"Category Group": "End Use", "Category Name": "End User - Sports/Leisure", "Description": "Users in equipment like bikes, boards, helmets"},
    {"Category Group": "Other", "Category Name": "Other", "Description": "Catch-all for unique or emerging roles"}
])

# Save to CSV in the project directory
category_file_path = Path(__file__).parent.parent / "stakeholder_categories.csv"
stakeholder_categories.to_csv(category_file_path, index=False)
print(f"Saved categories to {category_file_path}")

category_file_path