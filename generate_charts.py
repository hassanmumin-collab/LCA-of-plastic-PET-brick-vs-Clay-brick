#!/usr/bin/env python3
"""
Generate LCA charts directly as PNG files without browser automation.
Creates standalone, professional-quality chart images for presentations.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from pathlib import Path

# Configuration
EXPORT_DIR = Path(__file__).parent / "chart_exports"
EXPORT_DIR.mkdir(exist_ok=True)

# Berkeley Colors
BERKELEY_BLUE = "#003262"
BERKELEY_GOLD = "#FDB827"
LIGHT_GRAY = "#E8E8E8"

# Data from LCA analysis
CLIMATE_DATA = {
    "Clay": 0.6861,
    "PET": -0.6642
}

ENERGY_DATA = {
    "Clay": 7.9240,
    "PET": 27.0306
}

WATER_DATA = {
    "Clay": 7.1820,
    "PET": 4.5000
}

CLAY_LIFECYCLE = {
    "Raw Material": 44.2,
    "Transport": 0.1,
    "Manufacturing": 55.0,
    "Use Phase": 0.5,
    "End of Life": 0.2
}

PET_LIFECYCLE = {
    "Raw Material": 32.8,
    "Transport": 1.2,
    "Manufacturing": 15.0,
    "Use Phase": 48.5,
    "End of Life": 2.5
}


def generate_environmental_impact_chart():
    """Create diverging bar chart for environmental impact comparison."""
    print("📊 Generating Environmental Impact Comparison chart...")
    
    fig, ax = plt.subplots(figsize=(11, 7))
    
    categories = ["Climate Change\n(kg CO₂e)", "Energy Demand\n(MJ)", "Water Consumption\n(L)"]
    clay_values = [0.6861, 7.9240, 7.1820]
    pet_values = [-0.6642, 27.0306, 4.5000]
    
    # Diverging bars
    x = np.arange(len(categories))
    width = 0.35
    
    # Clay bars
    bars1 = ax.barh([i - width/2 for i in x], clay_values, width, 
                     label="Clay Brick", color=BERKELEY_BLUE, alpha=0.9)
    
    # PET bars (on other side for diverging effect)
    bars2 = ax.barh([i + width/2 for i in x], pet_values, width,
                     label="PET Brick", color=BERKELEY_GOLD, alpha=0.9)
    
    # Zero line
    ax.axvline(x=0, color='black', linewidth=1.5, linestyle='-')
    
    # Add value labels on bars
    for bar in bars1:
        width_val = bar.get_width()
        ax.text(width_val + 0.5, bar.get_y() + bar.get_height()/2,
                f'{width_val:.2f}', va='center', fontsize=11, fontweight='bold')
    
    for bar in bars2:
        width_val = bar.get_width()
        ax.text(width_val - 0.5 if width_val > 0 else width_val - 1.5, 
                bar.get_y() + bar.get_height()/2,
                f'{width_val:.2f}', va='center', ha='right' if width_val > 0 else 'left',
                fontsize=11, fontweight='bold')
    
    ax.set_yticks(x)
    ax.set_yticklabels(categories, fontsize=12, fontweight='bold')
    ax.set_xlabel('Impact Value', fontsize=12, fontweight='bold')
    ax.set_title('Environmental Impact Comparison\nClay Brick vs. PET Brick', 
                 fontsize=14, fontweight='bold', color=BERKELEY_BLUE, pad=20)
    
    ax.legend(fontsize=11, loc='lower right', framealpha=0.95)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    filepath = EXPORT_DIR / "01_Environmental_Impact_Comparison.png"
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    file_size = filepath.stat().st_size / 1024
    print(f"   ✅ Saved: 01_Environmental_Impact_Comparison.png ({file_size:.1f} KB)")


def generate_lifecycle_donut_charts():
    """Create donut charts for lifecycle stage breakdown."""
    print("📊 Generating Lifecycle Breakdown charts...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Clay brick lifecycle
    clay_labels = list(CLAY_LIFECYCLE.keys())
    clay_values = list(CLAY_LIFECYCLE.values())
    colors_clay = ['#003262', '#FDB827', '#00B0DA', '#C1272D', '#FFB81C']
    
    wedges1, texts1, autotexts1 = ax1.pie(clay_values, labels=clay_labels, autopct='%1.1f%%',
                                           colors=colors_clay, startangle=90,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.set_title('Clay Brick\nLifecycle Stage Breakdown', 
                  fontsize=13, fontweight='bold', color=BERKELEY_BLUE, pad=20)
    
    # Make percentage text more readable
    for autotext in autotexts1:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    # PET brick lifecycle
    pet_labels = list(PET_LIFECYCLE.keys())
    pet_values = list(PET_LIFECYCLE.values())
    colors_pet = ['#003262', '#FDB827', '#00B0DA', '#C1272D', '#FFB81C']
    
    wedges2, texts2, autotexts2 = ax2.pie(pet_values, labels=pet_labels, autopct='%1.1f%%',
                                           colors=colors_pet, startangle=90,
                                           textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('PET Brick\nLifecycle Stage Breakdown', 
                  fontsize=13, fontweight='bold', color=BERKELEY_BLUE, pad=20)
    
    # Make percentage text more readable
    for autotext in autotexts2:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    plt.tight_layout()
    filepath = EXPORT_DIR / "02_Clay_Lifecycle.png"
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    file_size = filepath.stat().st_size / 1024
    print(f"   ✅ Saved: 02_Clay_Lifecycle.png ({file_size:.1f} KB)")
    
    # PET Lifecycle (separate file for clarity)
    fig, ax = plt.subplots(figsize=(8, 7))
    
    wedges, texts, autotexts = ax.pie(pet_values, labels=pet_labels, autopct='%1.1f%%',
                                       colors=colors_pet, startangle=90,
                                       textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_title('PET Brick - Lifecycle Stage Breakdown', 
                 fontsize=13, fontweight='bold', color=BERKELEY_BLUE, pad=20)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    plt.tight_layout()
    filepath = EXPORT_DIR / "03_PET_Lifecycle.png"
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    file_size = filepath.stat().st_size / 1024
    print(f"   ✅ Saved: 03_PET_Lifecycle.png ({file_size:.1f} KB)")


def generate_system_boundaries_diagram():
    """Create system boundaries flowchart."""
    print("📊 Generating System Boundaries diagram...")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'System Boundaries (Cradle-to-Grave)', 
            ha='center', va='top', fontsize=16, fontweight='bold', color=BERKELEY_BLUE)
    
    # Left column - Clay Brick
    ax.text(2.5, 8.5, 'CLAY BRICK', ha='center', fontsize=12, fontweight='bold', color=BERKELEY_BLUE)
    
    stages_clay = [
        (1.5, 7.8, "Raw Material\nExtraction"),
        (1.5, 6.8, "Transport\nto Factory"),
        (1.5, 5.8, "Manufacturing\n(Firing)"),
        (1.5, 4.8, "Transport\nto Site"),
        (1.5, 3.8, "Use Phase\n(Mortar)"),
        (1.5, 2.8, "End of Life\n(Landfill/Reuse)")
    ]
    
    for x, y, label in stages_clay:
        box = FancyBboxPatch((x-0.6, y-0.35), 1.2, 0.7,
                             boxstyle="round,pad=0.05", 
                             edgecolor=BERKELEY_BLUE, facecolor=BERKELEY_BLUE, 
                             alpha=0.7, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=9,
                fontweight='bold', color='white')
        
        # Arrows
        if y > 2.8:
            ax.arrow(x, y-0.4, 0, -0.5, head_width=0.15, head_length=0.1,
                    fc=BERKELEY_BLUE, ec=BERKELEY_BLUE, alpha=0.5)
    
    # Right column - PET Brick
    ax.text(7.5, 8.5, 'PET BRICK', ha='center', fontsize=12, fontweight='bold', color=BERKELEY_GOLD)
    
    stages_pet = [
        (7.5, 7.8, "Raw Material\n(PET Resin)"),
        (7.5, 6.8, "Transport\nto Factory"),
        (7.5, 5.8, "Manufacturing\n(Molding)"),
        (7.5, 4.8, "Transport\nto Site"),
        (7.5, 3.8, "Use Phase\n(Installation)"),
        (7.5, 2.8, "End of Life\n(Reuse - 0 GHG)")
    ]
    
    for x, y, label in stages_pet:
        box = FancyBboxPatch((x-0.6, y-0.35), 1.2, 0.7,
                             boxstyle="round,pad=0.05",
                             edgecolor=BERKELEY_GOLD, facecolor=BERKELEY_GOLD,
                             alpha=0.7, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, label, ha='center', va='center', fontsize=9,
                fontweight='bold', color='#333')
        
        # Arrows
        if y > 2.8:
            ax.arrow(x, y-0.4, 0, -0.5, head_width=0.15, head_length=0.1,
                    fc=BERKELEY_GOLD, ec=BERKELEY_GOLD, alpha=0.5)
    
    # Scope label
    ax.text(5, 1.5, 'Functional Unit: 1 Brick (Clay: 3.5 kg | PET: 1.8 kg)', 
            ha='center', fontsize=10, style='italic', color=BERKELEY_BLUE)
    
    # Legend
    clay_patch = mpatches.Patch(color=BERKELEY_BLUE, alpha=0.7, label='Clay Brick System')
    pet_patch = mpatches.Patch(color=BERKELEY_GOLD, alpha=0.7, label='PET Brick System')
    ax.legend(handles=[clay_patch, pet_patch], loc='lower center', 
             fontsize=10, framealpha=0.95, ncol=2)
    
    plt.tight_layout()
    filepath = EXPORT_DIR / "04_System_Boundaries.png"
    plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    
    file_size = filepath.stat().st_size / 1024
    print(f"   ✅ Saved: 04_System_Boundaries.png ({file_size:.1f} KB)")


def main():
    """Generate all charts."""
    print("\n" + "="*60)
    print("🎨 LCA CHARTS GENERATION - DIRECT PNG OUTPUT")
    print("="*60)
    print(f"\n📁 Export directory: {EXPORT_DIR}\n")
    
    try:
        generate_environmental_impact_chart()
        generate_lifecycle_donut_charts()
        generate_system_boundaries_diagram()
        
        print("\n" + "="*60)
        print("✅ ALL CHARTS GENERATED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📁 Files saved to: {EXPORT_DIR}")
        print("\n📊 Generated files:")
        print("   1. 01_Environmental_Impact_Comparison.png")
        print("   2. 02_Clay_Lifecycle.png")
        print("   3. 03_PET_Lifecycle.png")
        print("   4. 04_System_Boundaries.png")
        print("\n💡 Ready for PowerPoint presentations!")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
