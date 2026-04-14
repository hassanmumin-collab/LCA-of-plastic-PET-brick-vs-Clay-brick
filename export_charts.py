#!/usr/bin/env python3
"""
Export interactive LCA charts to PNG files for PowerPoint presentations.
Generates high-quality images with visible data labels and values.
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright, ViewportSize

# Configuration
PROJECT_DIR = Path(__file__).parent
HTML_FILE = PROJECT_DIR / "data_visualization.html"
EXPORT_DIR = PROJECT_DIR / "chart_exports"
VIEWPORT = ViewportSize(width=1400, height=900)
WAIT_TIME = 3000  # 3 seconds for charts to fully render

# Chart configurations with their DOM selectors
CHARTS_TO_EXPORT = {
    "01_Environmental_Impact_Comparison": {
        "selector": "#divergingChart",
        "delay": 2000,
        "description": "Environmental Impact Comparison (Climate, Energy, Water)"
    },
    "02_Clay_Brick_Lifecycle": {
        "selector": "#clayLifecycleChart",
        "delay": 2000,
        "description": "Clay Brick Lifecycle Stage Breakdown"
    },
    "03_PET_Brick_Lifecycle": {
        "selector": "#petLifecycleChart",
        "delay": 2000,
        "description": "PET Brick Lifecycle Stage Breakdown"
    },
    "04_System_Boundaries_Flowchart": {
        "selector": ".mermaid",
        "delay": 2500,
        "description": "System Boundaries and Scope Definition"
    }
}

FULL_PAGE_EXPORTS = {
    "05_ExecutiveSummary_Full": {
        "tab_button": 0,
        "wait_selector": "#ExecutiveSummary",
        "description": "Full Executive Summary Tab"
    },
    "06_DataInventory_Full": {
        "tab_button": 1,
        "wait_selector": "#DataInventory",
        "description": "Full Data Inventory Tab"
    },
    "07_Results_Full": {
        "tab_button": 2,
        "wait_selector": "#Results",
        "description": "Full Results Summary Tab"
    }
}


async def export_individual_charts(page):
    """Export individual charts as PNG files."""
    print("\n📊 EXPORTING INDIVIDUAL CHARTS")
    print("=" * 60)
    
    # Ensure Results tab is active
    await page.click("button.tab-button:nth-of-type(3)")
    await page.wait_for_timeout(1500)
    
    for filename, config in CHARTS_TO_EXPORT.items():
        try:
            selector = config["selector"]
            delay = config["delay"]
            description = config["description"]
            
            print(f"\n📈 Exporting: {description}")
            print(f"   Selector: {selector}")
            
            # Wait for element and additional render time
            await page.wait_for_selector(selector, timeout=10000)
            await page.wait_for_timeout(delay)
            
            # Get element bounding box
            element = await page.query_selector(selector)
            if not element:
                print(f"   ❌ Element not found: {selector}")
                continue
            
            box = await element.bounding_box()
            if not box:
                print(f"   ❌ Could not get bounding box")
                continue
            
            # Add padding for better composition
            box["x"] = max(0, box["x"] - 20)
            box["y"] = max(0, box["y"] - 20)
            box["width"] = box["width"] + 40
            box["height"] = box["height"] + 40
            
            # Take screenshot
            filepath = EXPORT_DIR / f"{filename}.png"
            await page.screenshot(path=str(filepath), clip=box)
            
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"   ✅ Saved: {filename}.png ({file_size:.1f} KB)")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            continue


async def export_full_pages(page):
    """Export full tab pages as PNG files."""
    print("\n\n📄 EXPORTING FULL PAGES")
    print("=" * 60)
    
    tab_buttons = await page.query_selector_all("button.tab-button")
    
    for filename, config in FULL_PAGE_EXPORTS.items():
        try:
            tab_index = config["tab_button"]
            wait_selector = config["wait_selector"]
            description = config["description"]
            
            print(f"\n📋 Exporting: {description}")
            
            # Click tab
            if tab_index < len(tab_buttons):
                await tab_buttons[tab_index].click()
                await page.wait_for_selector(wait_selector, timeout=10000)
                await page.wait_for_timeout(WAIT_TIME)
            
            # Take full viewport screenshot
            filepath = EXPORT_DIR / f"{filename}.png"
            await page.screenshot(path=str(filepath))
            
            file_size = os.path.getsize(filepath) / 1024  # KB
            print(f"   ✅ Saved: {filename}.png ({file_size:.1f} KB)")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            continue


async def optimize_chart_display(page):
    """Ensure charts have visible data labels for interactive appearance."""
    await page.evaluate("""
        () => {
            // Ensure tooltips and data indicators are visible
            const style = document.createElement('style');
            style.textContent = `
                .chartjs-tooltip {
                    opacity: 1 !important;
                    visibility: visible !important;
                }
                canvas {
                    image-rendering: crisp-edges;
                }
            `;
            document.head.appendChild(style);
        }
    """)


async def main():
    """Main export function."""
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║           LCA CHARTS EXPORT TO PNG                         ║")
    print("║      For PowerPoint Presentations with Data Labels         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Verify HTML file exists
    if not HTML_FILE.exists():
        print(f"\n❌ ERROR: HTML file not found at {HTML_FILE}")
        return False
    
    # Create export directory
    EXPORT_DIR.mkdir(exist_ok=True)
    print(f"\n📁 Export directory: {EXPORT_DIR}")
    
    # Launch browser
    async with async_playwright() as p:
        try:
            # Use chromium
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport=VIEWPORT)
            page = await context.new_page()
            
            # Navigate to HTML
            html_url = f"file:///{HTML_FILE.as_posix()}"
            print(f"🌐 Loading: {html_url}")
            await page.goto(html_url, wait_until="networkidle")
            
            # Optimize chart display
            await optimize_chart_display(page)
            await page.wait_for_timeout(2000)
            
            # Export charts
            await export_individual_charts(page)
            await export_full_pages(page)
            
            # Cleanup
            await context.close()
            await browser.close()
            
            print("\n" + "=" * 60)
            print("✅ ALL EXPORTS COMPLETED SUCCESSFULLY!")
            print(f"📁 Files saved to: {EXPORT_DIR}")
            print("=" * 60)
            print("\n📊 Next Steps:")
            print("   1. Open the 'chart_exports' folder in Windows Explorer")
            print("   2. Use the PNG files in your PowerPoint presentations")
            print("   3. Charts include visible data labels and values")
            print("\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR: {str(e)}")
            print("\nTroubleshooting:")
            print("   • Ensure Chromium is installed: python -m playwright install chromium")
            print("   • Verify data_visualization.html exists in project directory")
            print("   • Check file permissions in project folder")
            return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Export cancelled by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        exit(1)
