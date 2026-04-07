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

class LcaCalculator:
    """
    A calculator to load LCI data and compute LCA results.

    Explanation:
    This class serves as the main engine for our LCA tool. Its primary responsibilities are:
    1.  Load Data: Read the `data.json` file which contains all the Life Cycle Inventory (LCI)
        parameters for both brick types.
    2.  Process Data: Structure the raw JSON data into a more usable format using Python
        dataclasses (`Brick`, `LifeCycleStage`, `Impact`). This improves code readability
        and maintainability.
    3.  Calculate Totals: Sum up the environmental impacts across all life cycle stages for
        each brick to get a final "Cradle-to-Gate" (plus Use Phase for clay) result for
        each impact category.

    Assumptions:
    -   The `data.json` file is located in the expected `../data/` directory.
    -   The structure of `data.json` is consistent with the format defined during the
        data gathering phase.
    -   All impact values are assumed to be correctly normalized to the functional unit
        (1 kg of brick) within the `data.json` file itself. This calculator performs
        the aggregation, not the normalization.
    """
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.data = None
        self.clay_brick: Brick = None
        self.pet_brick: Brick = None

    def load_data(self):
        """Loads the LCI data from the JSON file."""
        print("Step 1: Loading data...")
        with open(self.data_path, 'r') as f:
            self.data = json.load(f)
        print("Data loaded successfully.")

    def _process_brick_data(self, brick_name: str) -> Brick:
        """Processes the raw data for a single brick type."""
        brick_data = self.data[brick_name]
        brick_obj = Brick(name=brick_name)
        
        for stage_name, stage_data in brick_data["stages"].items():
            stage_obj = LifeCycleStage(name=stage_name)
            brick_obj.total_impacts_by_stage[stage_name] = {
                "climate_change": 0.0,
                "energy_demand": 0.0,
                "water_depletion": 0.0,
                "particulate_matter": 0.0,
                "land_use": 0.0
            }
            for impact_name, impact_data in stage_data.items():
                impact_obj = Impact(
                    name=impact_name,
                    value=impact_data["value"],
                    unit=impact_data["unit"],
                    source=impact_data["source"],
                    notes=impact_data["notes"]
                )
                stage_obj.impacts[impact_name] = impact_obj
                
                # Add to totals
                brick_obj.total_impacts[impact_name] += impact_data["value"]
                brick_obj.total_impacts_by_stage[stage_name][impact_name] += impact_data["value"]

            brick_obj.stages.append(stage_obj)
        return brick_obj

    def process_data(self):
        """Processes the loaded data for both brick types."""
        if not self.data:
            raise ValueError("Data not loaded. Please run load_data() first.")
        print("\nStep 2: Processing data into structured objects...")
        self.clay_brick = self._process_brick_data("clay_brick")
        self.pet_brick = self._process_brick_data("pet_brick")
        print("Data processing complete.")

    def get_results(self) -> Dict[str, Brick]:
        """Returns the processed brick data."""
        return {
            "clay_brick": self.clay_brick,
            "pet_brick": self.pet_brick
        }

    def print_summary(self):
        """Prints a summary of the total impacts for each brick."""
        if not self.clay_brick or not self.pet_brick:
            raise ValueError("Data not processed. Please run process_data() first.")

        print("\n--- LCA Results Summary ---")
        
        def print_brick_summary(brick: Brick):
            print(f"\nResults for: {brick.name.replace('_', ' ').title()}")
            for impact_name, total_value in brick.total_impacts.items():
                unit = ""
                # Find the unit from the first stage's impact
                if brick.stages and brick.stages[0].impacts.get(impact_name):
                    unit = brick.stages[0].impacts[impact_name].unit
                print(f"  - Total {impact_name.replace('_', ' ').title()}: {total_value:.4f} {unit}")

        print_brick_summary(self.clay_brick)
        print_brick_summary(self.pet_brick)
        print("\n--------------------------")

if __name__ == '__main__':
    """
    Main execution block to run the LCA calculation.
    
    Explanation:
    This block demonstrates the intended use of the LcaCalculator class. It follows
    a clear sequence of operations:
    1.  Define Path: It constructs the path to the `data.json` file.
    2.  Instantiate: It creates an instance of the calculator.
    3.  Execute Steps: It calls the methods in the correct order (load, process, summarize).
    4.  Output: It prints a summary of the final aggregated results to the console.
    
    This serves as a direct and transparent way to execute the core engine and see the
    immediate output of the calculations.
    """
    # Construct the path to the data file relative to this script
    DATA_FILE_PATH = Path(__file__).parent.parent / "data" / "data.json"
    
    # --- Core Calculation ---
    calculator = LcaCalculator(DATA_FILE_PATH)
    calculator.load_data()
    calculator.process_data()
    
    # --- Display Results ---
    calculator.print_summary()
