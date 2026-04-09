"""
Core Calculation Engine for the Life Cycle Assessment.

This module is responsible for loading the inventory data, processing it,
and calculating the total impacts for each brick type across all life cycle stages.
"""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Impact:
    """Represents a single environmental impact category."""
    name: str
    value: float
    unit: str
    source: str
    notes: str

@dataclass
class LifeCycleStage:
    """Represents a single stage in the brick's life cycle."""
    name: str
    impacts: Dict[str, Impact] = field(default_factory=dict)

@dataclass
class Brick:
    """Represents a type of brick and its complete life cycle."""
    name: str
    stages: List[LifeCycleStage] = field(default_factory=list)
    total_impacts: Dict[str, float] = field(default_factory=lambda: {
        "climate_change": 0.0,
        "energy_demand": 0.0,
        "water_depletion": 0.0,
        "particulate_matter": 0.0,
        "land_use": 0.0
    })
    total_impacts_by_stage: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def get_total_impact(self) -> Dict[str, Dict[str, float or str]]:
        """Calculates the total impact for each category across all stages."""
        totals: Dict[str, Dict[str, float or str]] = {}
        for stage in self.stages:
            for impact in stage.impacts:
                if impact.name not in totals:
                    totals[impact.name] = {
                        "value": 0.0,
                        "unit": impact.unit
                    }
                totals[impact.name]["value"] += impact.value
        return totals

    def get_impact_breakdown(self) -> Dict[str, Dict[str, float]]:
        """Creates a breakdown of impacts by category and life cycle stage."""
        breakdown: Dict[str, Dict[str, float]] = {}
        for stage in self.stages:
            for impact in stage.impacts:
                if impact.name not in breakdown:
                    breakdown[impact.name] = {}
                breakdown[impact.name][stage.name] = impact.value
        return breakdown


class LcaCalculator:
    """
    A tool to load, process, and calculate Life Cycle Assessment data for different products.
    Converts per-kg values to per-brick values using brick weights.
    """

    def __init__(self, data_path: Path):
        """
        Initializes the calculator with the path to the data file.
        """
        self.data_path = data_path
        self.raw_data: Dict = {}
        self.brick_weights: Dict[str, float] = {}
        self.bricks: List[Brick] = []
        self.results: Dict = {}
        
        self.load_data()
        self.extract_brick_weights()
        self.process_data()
        self.results = self.get_results()

    def load_data(self):
        """Loads data from the specified JSON file."""
        try:
            with open(self.data_path, 'r') as f:
                self.raw_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Data file not found at {self.data_path}")
            raise
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.data_path}")
            raise

    def extract_brick_weights(self):
        """Extracts brick weights from the functional_unit section."""
        try:
            functional_unit = self.raw_data.get("functional_unit", {})
            brick_weights = functional_unit.get("brick_weights", {})
            
            # Map brick type data names to brick type names
            if "clay_brick" in brick_weights:
                self.brick_weights["clay_brick"] = brick_weights["clay_brick"]["weight_kg"]
            if "pet_brick" in brick_weights:
                self.brick_weights["pet_brick"] = brick_weights["pet_brick"]["weight_kg"]
                
            if not self.brick_weights:
                raise ValueError("No brick weights found in data file")
        except Exception as e:
            print(f"Error extracting brick weights: {e}")
            raise

    def process_data(self):
        """Processes the loaded raw data into structured Brick objects with per-brick calculations."""
        if not self.raw_data:
            raise ValueError("Data not loaded. Please run load_data() first.")

        self.bricks = []
        
        # Process clay brick and pet brick from the data
        for brick_type in ["clay_brick", "pet_brick"]:
            if brick_type not in self.raw_data:
                continue
                
            brick_data = self.raw_data[brick_type]
            brick_weight = self.brick_weights.get(brick_type, 1.0)
            
            # Convert brick type name for display (clay_brick -> Clay Brick)
            display_name = " ".join(word.capitalize() for word in brick_type.split("_"))
            
            brick_stages = []
            for stage_name, stage_data in brick_data["stages"].items():
                stage_impacts = []
                for impact_category, impact_details in stage_data.items():
                    # Multiply per-kg value by brick weight to get per-brick value
                    per_kg_value = impact_details["value"]
                    per_brick_value = per_kg_value * brick_weight
                    
                    impact = Impact(
                        name=impact_category,
                        value=per_brick_value,
                        unit=impact_details["unit"],
                        source=impact_details.get("source", "N/A"),
                        notes=impact_details.get("notes", "")
                    )
                    stage_impacts.append(impact)
                
                stage = LifeCycleStage(name=stage_name, impacts=stage_impacts)
                brick_stages.append(stage)
            
            brick = Brick(name=display_name, stages=brick_stages)
            self.bricks.append(brick)

    def get_results(self) -> Dict[str, Dict[str, Dict[str, float or str]]]:
        """Calculates and returns both total impacts and stage-by-stage breakdowns."""
        if not self.bricks:
            raise ValueError("Data not processed. Call process_data() first.")

        all_results = {}
        for brick in self.bricks:
            all_results[brick.name] = {
                "total_impacts": brick.get_total_impact(),
                "impact_breakdown": brick.get_impact_breakdown(),
                "brick_weight": self.brick_weights.get(brick.name.lower().replace(" ", "_"), 1.0)
            }
        return all_results

    def print_summary(self):
        """Prints a summary of the total impacts for each brick (per-brick values)."""
        if not self.bricks:
            raise ValueError("Data not processed. Please run process_data() first.")

        print("\n--- LCA Results Summary (Per Brick) ---")
        for brick in self.bricks:
            print(f"\nResults for: {brick.name}")
            total_impacts = brick.get_total_impact()
            for category, data in total_impacts.items():
                # Round the value to 4 decimal places for cleaner output
                rounded_value = round(data['value'], 4)
                unit = data['unit']
                print(f"  - Total {category}: {rounded_value} {unit}")
        print("\n--------------------------")

    def print_impact_breakdown(self):
        """Prints a detailed breakdown of impacts by life cycle stage (per-brick values)."""
        if not self.bricks:
            raise ValueError("Results not calculated. Call get_results() first.")

        print("\n--- Detailed Impact Breakdown (Per Brick) ---")
        for brick in self.bricks:
            print(f"\n--- {brick.name} ---")
            total_impacts = brick.get_total_impact()
            impact_breakdown = brick.get_impact_breakdown()
            
            for category, stages in impact_breakdown.items():
                unit = total_impacts[category]['unit']
                print(f"\n{category.replace('_', ' ').title()}: ({unit})")
                total = 0
                for stage, value in stages.items():
                    rounded_value = round(value, 4)
                    print(f"  - {stage}: {rounded_value}")
                    total += value
                print(f"  - TOTAL: {round(total, 4)}")
        print("\n---------------------------------")


def main():
    """
    Main function to run the LCA calculation and print summaries.
    """
    try:
        # Correctly locate the data file relative to the script's location
        data_path = Path(__file__).resolve().parent.parent / 'data' / 'data.json'
        
        calculator = LcaCalculator(data_path)

        # Step 3: Print results
        print("\n--- LCA Results Summary ---")
        calculator.print_summary()
        
        print("\n--- Detailed Impact Breakdown ---")
        calculator.print_impact_breakdown()

    except FileNotFoundError:
        # This is now handled inside the LcaCalculator
        pass
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")


if __name__ == '__main__':
    main()
