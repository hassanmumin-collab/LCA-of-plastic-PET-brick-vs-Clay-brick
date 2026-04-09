# LCA Paper Data Extraction Tools

This toolkit helps you verify and extract environmental impact data directly from research papers.

## Two Ways to Extract Data

### **Method 1: Python Command Line (Recommended for accuracy)**

#### Installation:
```bash
pip install pdfplumber PyPDF2 pytesseract pillow
```

#### Usage:
```bash
cd lca_tool
python pdf_data_extractor.py path/to/paper.pdf
```

#### Example:
```bash
python pdf_data_extractor.py papers/koroneos_2007.pdf
```

The tool will:
1. ✓ Extract all text from the PDF
2. ✓ Search for impact values (kg CO2e, MJ, L, g PM2.5, m²a)
3. ✓ Find values in context of life cycle stages
4. ✓ Extract and display any tables
5. ✓ Export results to `extracted_data.json`

#### Output Example:
```
📖 Opening koroneos_2007.pdf...
✓ Extracted 45000 characters of text
🔍 Searching for impact category values...

CLIMATE CHANGE:
  • 0.35 - from: kg CO2e
    Context: ...manufacturing stage emissions from brick kiln firing...

ENERGY DEMAND:
  • 4.5 - from: MJ
    Context: ...thermal energy requirements for clay firing...

WATER DEPLETION:
  • 1.5 - from: L
    Context: ...water for clay mixing and preparation...
```

---

### **Method 2: HTML Web Interface (Easier for batch uploads)**

#### How to Use:
1. Open `lca_tool/paper_extraction_interface.html` in a browser
2. Drag and drop PDF files into the upload area
3. Click "Extract Data" button
4. Review the extracted values
5. Click "✓ Confirm" on values that match your data.json

#### Visual Workflow:
```
Upload Paper → Extract Text → Search for Values → Review Results → Confirm for data.json
```

---

## What It Searches For

### Impact Categories:
- **Climate Change**: kg CO2e/kg, kg CO2-eq/kg, GWP
- **Energy Demand**: MJ/kg, kWh/kg, GJ/kg
- **Water Depletion**: L/kg, liters/kg, water consumption
- **Particulate Matter**: g PM2.5/kg, PM2.5 emissions
- **Land Use**: m²a/kg, m2a/kg, land occupation

### Life Cycle Stages:
- Raw material acquisition
- Material processing
- Manufacturing  
- Transportation
- Packaging
- Use phase
- End of life

---

## Workflow for Verification

### Step 1: Gather Papers
Collect PDFs for the papers cited in data.json:
- Koroneos & Dompros (2007)
- Shen et al. (2010)
- Olweny et al. (2017)
- Lange (2021)
- Prateep Na Talang et al. (2017)
- etc.

### Step 2: Extract Data
```bash
# Extract from first paper
python pdf_data_extractor.py papers/koroneos_2007.pdf

# Extract from next paper
python pdf_data_extractor.py papers/shen_2010.pdf

# Continue for all papers...
```

### Step 3: Review and Confirm
For each extracted value, check if it:
- ✓ Matches the value in data.json
- ✓ Is from the correct life cycle stage
- ✓ Is in the correct units
- ✓ Has proper attribution

### Step 4: Update data.json
Once verified, update the `notes` field with the exact table/page reference:

```json
"manufacturing": {
  "climate_change": {
    "value": 0.35,
    "source": "Koroneos & Dompros (2007)",
    "notes": "From Table 3, Page 156: Fired clay brick manufacturing emissions. Original value: 0.38 kg CO2e/kg (adjusted for kiln efficiency)"
  }
}
```

---

## Troubleshooting

### "Module not found" errors:
```bash
pip install pdfplumber PyPDF2 pytesseract pillow
```

### PDF extraction fails:
- Check file is valid PDF
- Try opening in Adobe Reader first
- Some encrypted PDFs won't extract text

### Values not found:
- The table might be an image (scanned PDF)
- Try searching manually in paper for specific numbers
- Check if values are in appendix or supplementary materials

---

## Output Files

After running the Python tool, you'll get:

### `extracted_data.json`
Contains all found values organized by:
- Impact category
- Life cycle stage
- Keywords used to find them
- Surrounding context

### Example format:
```json
{
  "source_file": "papers/koroneos_2007.pdf",
  "impacts": {
    "climate": [
      {
        "value": 0.35,
        "keyword": "kg CO2e",
        "context": "...brick manufacturing kiln firing emissions..."
      }
    ]
  },
  "stages": {
    "manufacturing": [
      {
        "numbers_found": [0.35, 0.38, 400],
        "context": "...thermal energy for firing causes 0.35 kg CO2e per kg..."
      }
    ]
  }
}
```

---

## Next Steps

1. **Identify Papers**: Which papers do you have access to?
2. **Extract Data**: Run the tool on each paper
3. **Verify Values**: Check extracted values against data.json
4. **Update Citations**: Add page/table references to notes
5. **Confirm Sources**: Mark as verified in documentation

Would you like to start with a specific paper? I can help you interpret the extraction results.
