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
        """Calculates the total impact for each category."""
        totals: Dict[str, Dict[str, float or str]] = {}
        for stage in self.stages:
            for impact in stage.impacts:
                if impact.category not in totals:
                    totals[impact.category] = {}
                totals[impact.category]["value"] += impact.value
        return totals

    def get_impact_breakdown(self) -> Dict[str, Dict[str, float]]:
        """Creates a breakdown of impacts by category and life cycle stage."""
        breakdown: Dict[str, Dict[str, float]] = {}
        for stage in self.stages:
            for impact in stage.impacts:
                if impact.category not in breakdown:
                    breakdown[impact.category] = {}
                breakdown[impact.category][stage.name] = impact.value
        return breakdown


class LcaCalculator:
    """
    A tool to load, process, and calculate Life Cycle Assessment data for different products.
    """

    def __init__(self, data_path: Path):
        """
        Initializes the calculator with the path to the data file.
        """
        self.data_path = data_path
        self.raw_data: Dict = {}
        self.bricks: List[Brick] = []
        self.results: Dict = {}
        
        self.load_data()
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

    def process_data(self):
        """Processes the loaded raw data into structured Brick objects."""
        if not self.raw_data:
            raise ValueError("Data not loaded. Please run load_data() first.")

        self.bricks = []
        for brick_name, brick_data in self.raw_data.items():
            brick_stages = []
            for stage_name, stage_data in brick_data["stages"].items():
                stage_impacts = []
                for impact_category, impact_details in stage_data["impacts"].items():
                    impact = Impact(
                        category=impact_category,
                        value=impact_details["value"],
                        unit=impact_details["unit"]
                    )
                    stage_impacts.append(impact)
                
                stage = LifeCycleStage(name=stage_name, impacts=stage_impacts)
                brick_stages.append(stage)
            
            brick = Brick(name=brick_name, stages=brick_stages)
            self.bricks.append(brick)

    def get_results(self) -> Dict[str, Dict[str, Dict[str, float or str]]]:
        """Calculates and returns both total impacts and stage-by-stage breakdowns."""
        if not self.bricks:
            raise ValueError("Data not processed. Call process_data() first.")

        all_results = {}
        for brick in self.bricks:
            all_results[brick.name] = {
                "total_impacts": brick.get_total_impact(),
                "impact_breakdown": brick.get_impact_breakdown()
            }
        return all_results

    def print_summary(self):
        """Prints a summary of the total impacts for each brick."""
        if not self.bricks:
            raise ValueError("Data not processed. Please run process_data() first.")

        print("\n--- LCA Results Summary ---")
        for name, result_data in self.results.items():
            print(f"\nResults for: {name}")
            for category, data in result_data["total_impacts"].items():
                # Round the value to 4 decimal places for cleaner output
                rounded_value = round(data['value'], 4)
                print(f"  - Total {category}: {rounded_value} {data['unit']}")
        print("\n--------------------------")

    def print_impact_breakdown(self):
        """Prints a detailed breakdown of impacts by life cycle stage."""
        if not self.results:
            raise ValueError("Results not calculated. Call get_results() first.")

        print("\n--- Detailed Impact Breakdown ---")
        for name, result_data in self.results.items():
            print(f"\n--- {name} ---")
            for category, stages in result_data["impact_breakdown"].items():
                print(f"\nImpact Category: {category}")
                # Find the unit for the current category
                unit = result_data["total_impacts"][category]['unit']
                for stage, value in stages.items():
                    print(f"  - {stage}: {value} {unit}")
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
