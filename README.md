# Product Attribution & Category Mapping Engine

## Overview

A rule-based + confidence-scored product attribution system that maps raw product data to structured client-defined category taxonomies. Built to simulate real-world data operations work where each client defines their own category structure differently.

This project demonstrates:
- Judgment-driven data classification under ambiguity
- Confidence scoring to flag products needing manual review
- Scalable, documented mapping logic
- Data quality reporting

## Business Context

In retail and e-commerce analytics, raw product data rarely comes pre-labelled to a client's specification. A client selling FMCG products may define "Haircare" differently from another — one includes styling products, another does not. This engine handles that ambiguity systematically.

## Project Structure

```
project1_product_attribution/
│
├── README.md                     ← This file
├── product_attribution.py        ← Main attribution engine
├── generate_sample_data.py       ← Sample dataset generator

├── data/
│   ├── raw_products.csv          ← Input: raw product data
│   └── client_taxonomy.json      ← Input: client's category definitions
└── output/
    ├── attributed_products.csv   ← Output: mapped + confidence scored
   
```

## How It Works

### Step 1 — Load and audit raw data
```python
df = pd.read_csv("data/raw_products.csv")
# Always audit first: nulls, duplicates, type issues
```

### Step 2 — Apply keyword-based mapping rules
Each category in the client taxonomy has associated keywords. Products are scored against each category.

### Step 3 — Assign confidence level
| Confidence | Meaning |
|---|---|
| HIGH | Direct keyword match in product name |
| MEDIUM | Brand-level inference or partial match |
| LOW | Fallback — needs manual review |

### Step 4 — Generate report
Summary of category distribution, confidence breakdown, and flagged items.

## Sample Output

| product_id | product_name | brand | mapped_category | confidence |
|---|---|---|---|---|
| P001 | Dove Body Wash 500ml | Dove | Bath & Body | HIGH |
| P002 | Nivea Q10 Moisturiser | Nivea | Skincare | HIGH |
| P003 | Unknown Hair Thing | Generic | Haircare | MEDIUM |
| P004 | Product XYZ | Unknown | NEEDS_REVIEW | LOW |

## Key Skills Demonstrated
- Pandas: data loading, cleaning, apply/map operations
- String matching: regex, fuzzy matching logic
- Structured output: confidence scoring, reporting
- Business judgment: documented assumptions and edge case handling

## How to Run

```bash
pip install -r requirements.txt
python generate_sample_data.py    # creates data/raw_products.csv
python product_attribution.py     # runs engine, writes output/
```

## Assumptions & Design Decisions

1. Products with NULL category AND NULL brand are flagged as LOW confidence — not silently dropped
2. Brand-level inference is used only when keyword match fails — reduces false positives
3. A product can match multiple categories; the highest-scoring one wins
4. Thresholds (keyword score ≥ 2 = HIGH) are configurable in the taxonomy JSON

