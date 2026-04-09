"""
LCA Data Extraction Tool from PDF Papers
Extracts environmental impact data from research papers using OCR and text analysis
"""

import os
import sys
import re
from pathlib import Path
import json

# Try to import PDF libraries
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ PyPDF2 not installed. Run: pip install PyPDF2")

try:
    from PIL import Image
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    print("⚠️ pytesseract/PIL not installed. Run: pip install pytesseract pillow")

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    print("⚠️ pdfplumber not installed. Run: pip install pdfplumber")


class LCADataExtractor:
    """Extract LCA data from PDF research papers"""
    
    # Impact categories we're looking for
    IMPACT_CATEGORIES = {
        'climate': ['kg CO2e', 'kg co2e', 'kg CO2-eq', 'GWP', 'global warming'],
        'energy': ['MJ', 'kWh', 'GJ', 'energy demand'],
        'water': ['L/kg', 'liters', 'L ', 'water depletion', 'water consumption'],
        'particulate': ['PM2.5', 'g PM2.5', 'particulate matter'],
        'land_use': ['m²a', 'm2a', 'land use', 'land occupation']
    }
    
    # Life cycle stages
    STAGES = [
        'raw material',
        'material processing', 
        'manufacturing',
        'transportation',
        'packaging',
        'use phase',
        'end of life'
    ]
    
    def __init__(self, pdf_path):
        """Initialize with PDF file path"""
        self.pdf_path = Path(pdf_path)
        self.text = ""
        self.tables = []
        self.extracted_data = {}
        
    def extract_text_pdfplumber(self):
        """Extract text from PDF using pdfplumber"""
        if not PDFPLUMBER_AVAILABLE:
            return False
            
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                print(f"📄 Extracting text from {len(pdf.pages)} pages...")
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        self.text += f"\n--- PAGE {i+1} ---\n{text}"
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        self.tables.extend(tables)
                        print(f"   Found {len(tables)} table(s) on page {i+1}")
            
            print(f"✓ Extracted {len(self.text)} characters of text")
            return True
        except Exception as e:
            print(f"❌ Error extracting text: {e}")
            return False
    
    def extract_text_pypdf2(self):
        """Fallback: Extract text using PyPDF2"""
        if not PDF_AVAILABLE:
            return False
            
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                print(f"📄 Extracting text from {len(reader.pages)} pages (PyPDF2)...")
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        self.text += f"\n--- PAGE {i+1} ---\n{text}"
            
            print(f"✓ Extracted {len(self.text)} characters of text")
            return True
        except Exception as e:
            print(f"❌ Error with PyPDF2: {e}")
            return False
    
    def find_impact_values(self):
        """Search text for impact category values"""
        results = {}
        
        for category, keywords in self.IMPACT_CATEGORIES.items():
            results[category] = self._search_values(category, keywords)
        
        return results
    
    def _search_values(self, category, keywords):
        """Search for specific impact values in text"""
        found_values = []
        
        # Pattern to find numbers with units
        patterns = [
            r'(\d+\.?\d*)\s*(kg|g|L|MJ|m²a|m2a)',  # Number + unit
            r'(\d+\.?\d*)\s*±\s*(\d+\.?\d*)',  # Number with range
        ]
        
        for keyword in keywords:
            # Search within context (50 chars before/after keyword)
            if keyword.lower() in self.text.lower():
                for match in re.finditer(rf'.{{0,100}}{re.escape(keyword)}.{{0,100}}', 
                                        self.text, re.IGNORECASE):
                    context = match.group(0)
                    # Extract numbers from context
                    for pattern in patterns:
                        for num_match in re.finditer(pattern, context):
                            value = num_match.group(1)
                            found_values.append({
                                'value': float(value),
                                'keyword': keyword,
                                'context': context[:100] + "..." if len(context) > 100 else context
                            })
        
        return found_values
    
    def find_stage_impacts(self):
        """Find impacts associated with specific life cycle stages"""
        stage_data = {}
        
        for stage in self.STAGES:
            stage_data[stage] = self._search_stage_context(stage)
        
        return stage_data
    
    def _search_stage_context(self, stage):
        """Find values in context of a specific stage"""
        results = []
        
        pattern = rf'.{{0,200}}{re.escape(stage)}.{{0,200}}'
        for match in re.finditer(pattern, self.text, re.IGNORECASE):
            context = match.group(0)
            # Extract all numbers from stage context
            numbers = re.findall(r'(\d+\.?\d*)', context)
            if numbers:
                results.append({
                    'stage': stage,
                    'numbers_found': [float(n) for n in numbers],
                    'context': context
                })
        
        return results
    
    def display_tables(self):
        """Display extracted tables"""
        if not self.tables:
            print("No tables found in PDF")
            return
        
        print(f"\n📊 Found {len(self.tables)} table(s):")
        for i, table in enumerate(self.tables):
            print(f"\n--- TABLE {i+1} ---")
            for row in table[:10]:  # Show first 10 rows
                print(row)
            if len(table) > 10:
                print(f"... ({len(table) - 10} more rows)")
    
    def extract_and_display(self):
        """Run full extraction and display results"""
        print(f"\n📖 Opening {self.pdf_path.name}...")
        
        # Try preferred method first
        success = self.extract_text_pdfplumber()
        if not success:
            success = self.extract_text_pypdf2()
        
        if not success:
            print("❌ Could not extract text from PDF")
            return False
        
        print("\n🔍 Searching for impact category values...")
        impacts = self.find_impact_values()
        
        print("\n📈 FOUND VALUES BY IMPACT CATEGORY:")
        for category, values in impacts.items():
            if values:
                print(f"\n{category.upper()}:")
                for val in values[:5]:  # Show top 5
                    print(f"  • {val['value']} - from: {val['keyword']}")
                    print(f"    Context: ...{val['context'][:80]}...")
        
        print("\n📍 Searching for life cycle stage values...")
        stages = self.find_stage_impacts()
        
        print("\n📍 FOUND VALUES BY LIFE CYCLE STAGE:")
        for stage, data in stages.items():
            if data:
                print(f"\n{stage.upper()}:")
                for item in data[:3]:  # Show top 3
                    print(f"  • Numbers: {item['numbers_found']}")
                    print(f"    Context: ...{item['context'][:80]}...")
        
        print("\n📊 TABLES FOUND:")
        self.display_tables()
        
        return True
    
    def export_summary(self, output_file='extracted_data.json'):
        """Export extracted data to JSON"""
        data = {
            'source_file': str(self.pdf_path),
            'impacts': self.find_impact_values(),
            'stages': self.find_stage_impacts(),
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"\n✓ Summary exported to {output_file}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("\n📚 LCA DATA EXTRACTOR")
        print("=" * 50)
        print("\nUsage: python pdf_data_extractor.py <path_to_pdf>")
        print("\nExample: python pdf_data_extractor.py papers/koroneos_2007.pdf")
        print("\nThe tool will:")
        print("  1. Extract text from the PDF")
        print("  2. Search for LCA impact values (CO2e, MJ, L, PM2.5, m²a)")
        print("  3. Find values associated with life cycle stages")
        print("  4. Display tables found in the paper")
        print("  5. Export extracted data to JSON")
        return
    
    pdf_file = sys.argv[1]
    
    if not os.path.exists(pdf_file):
        print(f"❌ File not found: {pdf_file}")
        return
    
    extractor = LCADataExtractor(pdf_file)
    extractor.extract_and_display()
    extractor.export_summary()


if __name__ == "__main__":
    main()
