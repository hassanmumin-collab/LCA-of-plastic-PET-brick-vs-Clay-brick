📁 USER DATA INPUT FOLDER
========================

This folder is where you upload your verified LCA data.

## How to Provide Your Data:

### Option 1: CSV Format (Recommended - Easy to Edit)
1. Create a CSV file with columns:
   - Life Cycle Stage
   - Impact Category
   - Value
   - Unit
   - Source
   - Notes

2. Name it: `clay_brick_data.csv` or `pet_brick_data.csv`

3. Example format (see template below):
   ```
   Life Cycle Stage,Impact Category,Value,Unit,Source,Notes
   Raw Material Acquisition,Climate Change,0.002,kg CO2e/kg,Olweny et al. (2017),Excavation emissions
   Raw Material Acquisition,Energy Demand,0.03,MJ/kg,Christoforou et al. (2016),Excavation machinery
   Manufacturing,Climate Change,0.35,kg CO2e/kg,Koroneos & Dompros (2007),Kiln firing
   ```

### Option 2: Excel Format
1. Create .xlsx file with same columns
2. Sheet 1: Clay Brick data
3. Sheet 2: PET Brick data (optional)

### Option 3: JSON Format
1. Provide a JSON file matching data.json structure
2. Keep the nested format with stages and impact categories

## Steps:

1. ✅ Prepare your data file (CSV, Excel, or JSON)
2. ✅ Save it to this folder: `user_data_input/`
3. ✅ Tell me the filename
4. ✅ I will read it and update data.json

## File Location:
```
C:\Users\hasan\OneDrive\Documents\LCA-of-plastic-PET-brick-vs-Clay-brick\user_data_input\
```

Save your file here and let me know when it's ready!
