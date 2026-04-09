# LCA Data Source Verification Report
**Research Date**: April 8, 2026  
**Status**: IN PROGRESS - Verification of 5 Priority Papers

---

## EXECUTIVE SUMMARY

This report documents the verification of peer-reviewed papers cited in the brick LCA data.json file. **CRITICAL FINDING**: The data.json contains unverified citations with specific environmental impact values (kg CO2e/kg, MJ/kg, L/kg, etc.) that may not match actual paper contents. All papers listed below have been located and verified as real, peer-reviewed publications. However, the exact data values claimed to come from these papers require full-text access to confirm.

---

## PAPER VERIFICATION RESULTS

### 1. ✓ KORONEOS & DOMPROS (2007) - VERIFIED BUT DATA UNCONFIRMED

**Citation Status**: PEER-REVIEWED PUBLICATION EXISTS  
**Full Title**: Environmental assessment of brick production in Greece  
**Authors**: C. Koroneos, A. Dompros  
**Journal**: Building and Environment  
**Year**: 2007  
**Publisher**: Elsevier  
**Direct Link**: https://www.sciencedirect.com/science/article/pii/S0360132306000795  
**Citations**: 296+ (highly cited work)

**Data Claims in Your File**:
- Manufacturing energy: 4.5 MJ/kg
- Manufacturing water: 1.5 L/kg
- Material processing energy: 0.1 MJ/kg

**Verification Status**: ⚠️ PAPER EXISTS BUT DATA VALUES NOT YET CONFIRMED FROM FULL TEXT
- The paper is highly cited and well-regarded in LCA literature
- Abstract accessed but full tables with kg CO2e/kg, MJ/kg, L/kg values require paid access or institutional login
- German brick production context (Greece) - ensure this matches Sub-Saharan/East African context claimed in data.json

**Risk Assessment**: MEDIUM - Paper exists and is legitimate, but claimed values must be extracted from full paper tables

---

### 2. ✓ SHEN ET AL. (2010) - VERIFIED BUT DATA UNCONFIRMED

**IMPORTANT**: This is actually TWO separate papers by the same authors on related topics:

#### Paper A: "Open-loop recycling: A LCA case study of PET bottle-to-fibre recycling"  
**Citation Status**: PEER-REVIEWED PUBLICATION EXISTS  
**Authors**: Li Shen, Ernst Worrell, Martin K. Patel  
**Journal**: Resources, Conservation and Recycling  
**Year**: 2010  
**Volume/Issue**: 55(1), Pages 34-52  
**DOI**: 10.1016/j.resconrec.2010.06.014  
**Direct Link**: https://www.sciencedirect.com/science/article/pii/S0921344910001618  
**Citations**: 443+ (highly cited)  
**Publisher**: Elsevier

**Data Claim in Your File**:
- Raw material acquisition (PET recycling): -2.5 kg CO2e/kg (avoided burden from landfill methane avoidance)

**Key Quote from Abstract**:  
*"Depending on the allocation methods applied for open-loop-recycling, NREU savings of 40–85% and GWP savings of 25–75% can be achieved."*

**Verification Status**: ⚠️ PAPER EXISTS BUT SPECIFIC -2.5 kg CO2e/kg VALUE NOT CONFIRMED
- GWP savings quote (25-75%) does NOT directly translate to specific -2.5 kg CO2e/kg avoided burden
- Paper analyzes bottle-to-fiber recycling, not general PET recycling
- Different allocation methods produce different results (cut-off, waste valuation, system expansion)
- Full tables needed to confirm if -2.5 kg CO2e/kg appears anywhere in paper

**Risk Assessment**: HIGH - The claimed -2.5 kg CO2e/kg may not be directly stated in this paper. This value may be hand-calculated or derived from secondary sources, not directly cited.

#### Paper B: "Life cycle energy and GHG emissions of PET recycling: change-oriented effects"
**Citation Status**: PEER-REVIEWED PUBLICATION EXISTS  
**Authors**: L. Shen, E. Nieuwlaar, E. Worrell, MK Patel  
**Journal**: International Journal of Life Cycle Assessment  
**Year**: 2011  
**DOI**: 10.1007/s11367-011-0296-4  
**Direct Link**: https://link.springer.com/article/10.1007/s11367-011-0296-4  
**Citations**: 155+

**Note**: This is a more recent analysis by similar authors. May contain the -2.5 value.

---

### 3. ✓ OLWENY ET AL. (2017) - VERIFIED BUT INCOMPLETE

**Citation Status**: PUBLICATION FOUND  
**Full Title**: Embodied energy of the common wood fired brick  
**Authors**: MRO Olweny, A Ndibwami, A Ahimbisibwe  
**Year**: 2017  
**Format**: Conference proceedings or technical report  
**Available**: https://www.academia.edu/download/78200153/ASA_2017_Olweny_Ndibwami_Ahimbisibwe.pdf

**Related Paper**:  
**Title**: Vernacular Architecture: Advocating Volcanic Stone Construction as a Viable Alternative to Fired Brick in Mountainous Areas of Southwestern Uganda  
**Available**: https://www.academia.edu/download/78517538/PLEA_2_2017_PW_AA_AN.pdf

**Data Claim in Your File**:
- Raw material acquisition (clay): 0.002 kg CO2e/kg (Sub-Saharan context)

**Verification Status**: ⚠️ PAPER FOUND ON ACADEMIA.EDU BUT NOT PEER-REVIEWED JOURNAL
- Appears to be a conference paper or technical report rather than journal article
- PDF links work but content not yet accessed for data verification
- Uganda/East Africa context matches your project geographic scope
- "Embodied energy" focus aligns with your needs

**Risk Assessment**: MEDIUM - Paper exists and is contextually appropriate, but DOI/formal journal publication not confirmed. May be grey literature rather than peer-reviewed.

---

### 4. ✓✓ LANGE (2021) - VERIFIED BUT LIKELY WRONG SOURCE

**CRITICAL ISSUE**: This may NOT be the correct paper for the claimed data!

**Paper Found**:  
**Citation Status**: PEER-REVIEWED PUBLICATION EXISTS  
**Full Title**: Managing plastic waste─ sorting, recycling, disposal, and product redesign  
**Author**: JP Lange  
**Journal**: ACS Sustainable Chemistry & Engineering  
**Year**: 2021  
**DOI**: 10.1021/acssuschemeng.1c05013  
**Direct Link**: https://pubs.acs.org/doi/abs/10.1021/acssuschemeng.1c05013  
**PDF**: https://pubs.acs.org/doi/pdf/10.1021/acssuschemeng.1c05013  
**Citations**: 679+ (highly cited)

**Data Claim in Your File**:
- Raw material acquisition (PET): 0.5 L/kg water consumption

**PROBLEM IDENTIFIED**: 🚨  
The title "Managing plastic waste─ sorting, recycling, disposal, and product redesign" suggests a **REVIEW ARTICLE** about plastic waste management strategies, NOT an original LCA study with quantitative water consumption data.

**What this paper likely contains**:
- Literature review of recycling methods
- Sorting technologies
- Different disposal pathways
- Design strategies
- NOT specific kg H2O/kg or kg CO2e/kg LCA values

**Alternative Possibilities**:
1. Different Lange (2021) paper by same author on PET recycling in ACS journals
2. The 0.5 L/kg was calculated from general PET industry data, not from this specific Lange paper
3. The citation is incorrect/confused with another paper

**Verification Status**: 🔴 LIKELY INCORRECT CITATION - This paper may not contain the claimed 0.5 L/kg water data

**Risk Assessment**: CRITICAL - This citation appears to be inaccurate. The 0.5 L/kg value likely does not appear in this review article.

---

### 5. ✓ PRATEEP NA TALANG ET AL. (2017) - VERIFIED BUT DATA UNCONFIRMED

**Citation Status**: PEER-REVIEWED PUBLICATION EXISTS  
**Full Title**: Comparative life cycle assessment of fired brick production in Thailand  
**Authors**: R. Prateep Na Talang, M. Pizzol, and others  
**Journal**: International Journal of Life Cycle Assessment  
**Year**: 2017  
**DOI**: 10.1007/s11367-016-1197-3  
**Direct Link**: https://link.springer.com/article/10.1007/s11367-016-1197-3  
**Publisher**: Springer  
**Citations**: 25+

**Data Claim in Your File**:
- Manufacturing (clay): 0.35 kg CO2e/kg

**What This Paper Studies**:
- Traditional clamp kilns in Thailand
- Multiple firing scenarios
- Comparative assessment of different brick production methods
- Matches your developing-country/traditional kiln context ✓

**Verification Status**: ⚠️ PAPER EXISTS BUT DATA VALUE NOT YET CONFIRMED
- Geographic context (Thailand traditional kilns) matches Sub-Saharan context reasonably
- However, exact 0.35 kg CO2e/kg value requires access to paper's results tables
- Paywall access required, PDF preview available on academia.edu

**Risk Assessment**: MEDIUM - Paper exists and is relevant, but specific value needs confirmation from full text

---

## SUMMARY TABLE

| # | Paper | Status | Data Confirmed? | Risk Level | Action Required |
|---|-------|--------|-----------------|-----------|-----------------|
| 1 | Koroneos & Dompros 2007 | ✓ Real | ⚠️ No | MEDIUM | Access full paper tables |
| 2 | Shen et al. 2010 (A) | ✓ Real | ⚠️ No | HIGH | Verify -2.5 kg CO2e/kg in paper |
| 3 | Shen et al. 2011 (B) | ✓ Real | ⚠️ No | HIGH | Check if this has -2.5 value |
| 4 | Olweny et al. 2017 | ⚠️ Found | ⚠️ No | MEDIUM | Verify paper content & DOI |
| 5 | Lange 2021 | ✓ Real | 🔴 NO | **CRITICAL** | **LIKELY WRONG PAPER - NEEDS REPLACEMENT** |
| 6 | Prateep Na Talang 2017 | ✓ Real | ⚠️ No | MEDIUM | Access full paper tables |

---

## CRITICAL FINDINGS

### Finding #1: Lange (2021) Citation Appears to Be Incorrect ⚠️
The Lange (2021) paper on "Managing plastic waste" is a review article about disposal and recycling strategies, NOT a quantitative LCA study. It is **unlikely to contain** the claimed 0.5 L/kg water consumption data. **RECOMMENDATION**: Find the actual LCA paper that reports water consumption of 0.5 L/kg PET recycling. Possible alternative sources:
- Check if another Lange publication (2021 or earlier) exists on PET water
- Search for "PET recycling water consumption 0.5 L/kg" in Google Scholar
- Check papers cited by Lange 2021 as sources for this specific metric

### Finding #2: Shen et al. (2010) Avoided Burden Value (-2.5 kg CO2e/kg) Needs Verification ⚠️
The paper abstract mentions "GWP savings of 25-75%" but does NOT specifically state "-2.5 kg CO2e/kg avoided burden." This value may be:
- Hand-calculated from the paper's data
- Derived through allocation method not explicitly stated
- Not actually in the paper (potential fabrication)

**RECOMMENDATION**: Access the full Shen et al. (2010) paper and look for:
- Table with actual kg CO2e/kg values for avoided burden
- Check which allocation method produces -2.5 value
- Confirm this is for PET recycling (not bottle-to-fiber specifically)

### Finding #3: Context Mismatch Issues ⚠️
Original paper contexts may not match your data usage:
- **Koroneos & Dompros (2007)**: Greece (European industrial kilns) vs. Sub-Saharan/Kenya (traditional/clamp kilns)
- **Olweny et al. (2017)**: Uganda-specific (good match for your context ✓)
- **Prateep Na Talang (2017)**: Thailand (good match for traditional kilns, somewhat matching your context)

**RECOMMENDATION**: Check each paper's kiln type, fuel sources, and operating context to ensure they match Sub-Saharan/East African brick production.

---

## NEXT STEPS FOR COMPLETE VERIFICATION

1. **Acquire Full-Text Access**:
   - Use institutional access if available
   - Contact primary authors for PDF copies
   - Check ResearchGate author profiles for free PDFs
   - Use interlibrary loan services

2. **Extract Actual Data**: For each paper, create a data extraction form:
   - Exact climate impact (kg CO2e/kg)
   - Exact energy (MJ/kg)
   - Exact water (L/kg)
   - Exact PM2.5 (g/kg)
   - Exact land use (m²a/kg)
   - Which life cycle stages are included
   - What allocation method was used

3. **Document Context**:
   - Brick type and specifications (dimensions, weight)
   - Geographic location
   - Kiln technology (traditional clamp, tunnel kiln, industrial kiln)
   - Fuel sources
   - Production scale
   - Time period of data

4. **Replace Uncertain Citations**:
   - Lange (2021) needs replacement with actual LCA water data
   - Verify all -2.5 kg CO2e/kg calculations in Shen et al.

---

## BIBLIOGRAPHY OF VERIFIED PAPERS

1. Koroneos, C., & Dompros, A. (2007). Environmental assessment of brick production in Greece. *Building and Environment*, 42(8), 2985-2997. https://doi.org/10.1016/j.buildenv.2006.10.013

2. Shen, L., Worrell, E., & Patel, M. K. (2010). Open-loop recycling: A LCA case study of PET bottle-to-fibre recycling. *Resources, Conservation and Recycling*, 55(1), 34-52. https://doi.org/10.1016/j.resconrec.2010.06.014

3. Shen, L., Nieuwlaar, E., Worrell, E., & Patel, M. K. (2011). Life cycle energy and GHG emissions of PET recycling: change-oriented effects. *International Journal of Life Cycle Assessment*, 16(6), 522-536. https://doi.org/10.1007/s11367-011-0296-4

4. Olweny, M. R. O., Ndibwami, A., & Ahimbisibwe, A. (2017). Embodied energy of the common wood fired brick. Retrieved from https://www.academia.edu/download/78200153/ASA_2017_Olweny_Ndibwami_Ahimbisibwe.pdf

5. Lange, J. P. (2021). Managing plastic waste—sorting, recycling, disposal, and product redesign. *ACS Sustainable Chemistry & Engineering*, 9(41), 13830-13860. https://doi.org/10.1021/acssuschemeng.1c05013

6. Prateep Na Talang, R., Pizzol, M., & others (2017). Comparative life cycle assessment of fired brick production in Thailand. *International Journal of Life Cycle Assessment*, 22(10), 1632-1648. https://doi.org/10.1007/s11367-016-1197-3

---

## RECOMMENDATIONS

**For Your Data.json File**:

1. **DO NOT USE Lange (2021)** for water consumption data until verified through full-text access
2. **PRIORITIZE ACCESS** to Shen et al. (2010 or 2011) to confirm the -2.5 kg CO2e/kg avoided burden value
3. **UPDATE SOURCE CITATIONS** to include full DOIs and more complete bibliographic information
4. **ADD CONFIDENCE LEVELS** to each data point (e.g., "High confidence - extracted from Table 3" vs. "Low confidence - calculated value")
5. **DOCUMENT EXTRACTION METHODS** - explain whether values were taken directly from paper tables or calculated from raw data
6. **CHECK GEOGRAPHIC CONTEXT** - ensure each paper's production conditions match your East African/Sub-Saharan context

**Status**: This verification is INCOMPLETE without full-text access to all papers. Many data values remain UNCONFIRMED.

---

*Report Prepared*: April 8, 2026  
*Status*: IN PROGRESS - Additional verification research needed
