"""
Data Inventory Updater
Converts user-provided CSV/Excel data to data.json format
"""

import json
import csv
from pathlib import Path


def read_csv_data(csv_file):
    """Read data from CSV file"""
    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def read_json_data(json_file):
    """Read from JSON file"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def csv_to_data_json(csv_data, brick_type='clay'):
    """Convert CSV data to data.json structure"""
    
    # Map stage names to snake_case keys
    stage_map = {
        'Raw Material Acquisition': 'raw_material_acquisition',
        'Material Processing': 'material_processing',
        'Manufacturing': 'manufacturing',
        'Transportation': 'transportation',
        'Packaging': 'packaging',
        'Use Phase': 'use_phase',
    }
    
    # Map impact category names to snake_case keys
    impact_map = {
        'Climate Change': 'climate_change',
        'Energy Demand': 'energy_demand',
        'Water Depletion': 'water_depletion',
        'Particulate Matter': 'particulate_matter',
        'Land Use': 'land_use',
    }
    
    # Initialize structure
    structure = {
        "stages": {}
    }
    
    # Organize data by stage
    for row in csv_data:
        stage_name = row['Life Cycle Stage'].strip()
        impact_name = row['Impact Category'].strip()
        
        stage_key = stage_map.get(stage_name)
        impact_key = impact_map.get(impact_name)
        
        if not stage_key or not impact_key:
            print(f"⚠️ Warning: Unknown stage '{stage_name}' or impact '{impact_name}'")
            continue
        
        # Initialize stage if needed
        if stage_key not in structure["stages"]:
            structure["stages"][stage_key] = {}
        
        # Add impact data
        structure["stages"][stage_key][impact_key] = {
            "value": float(row['Value']),
            "unit": row['Unit'].strip(),
            "source": row['Source'].strip(),
            "notes": row['Notes'].strip()
        }
    
    return structure


def update_data_json(csv_file, output_file='data.json', brick_type='clay'):
    """Read CSV and update data.json"""
    
    print(f"📖 Reading {csv_file}...")
    csv_data = read_csv_data(csv_file)
    
    print(f"🔄 Converting to data.json format for {brick_type} brick...")
    new_data = csv_to_data_json(csv_data, brick_type)
    
    # Read existing data.json
    print(f"📁 Reading existing {output_file}...")
    with open(output_file, 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    # Update the appropriate brick type
    if brick_type == 'clay':
        full_data['clay_brick'] = new_data
    elif brick_type == 'pet':
        full_data['pet_brick'] = new_data
    
    # Write back to file
    print(f"✍️ Updating {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, indent=2)
    
    print(f"✅ Successfully updated {output_file}")
    print(f"   Entries updated: {sum(len(stage.keys()) for stage in new_data['stages'].values())}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("📊 DATA UPDATER - Convert CSV to data.json")
        print("=" * 50)
        print("\nUsage: python update_data_inventory.py <csv_file> [brick_type] [output_file]")
        print("\nExamples:")
        print("  python update_data_inventory.py clay_brick_data.csv clay")
        print("  python update_data_inventory.py pet_brick_data.csv pet ../data/data.json")
        print("\nArguments:")
        print("  csv_file      - CSV file with your data")
        print("  brick_type    - 'clay' or 'pet' (default: 'clay')")
        print("  output_file   - Path to data.json (default: ../data/data.json)")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    brick_type = sys.argv[2] if len(sys.argv) > 2 else 'clay'
    output_file = sys.argv[3] if len(sys.argv) > 3 else '../data/data.json'
    
    update_data_json(csv_file, output_file, brick_type)
