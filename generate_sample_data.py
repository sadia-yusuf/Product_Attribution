"""
generate_sample_data.py
-----------------------
Generates a realistic mock product dataset for the attribution engine.
Run this first before product_attribution.py.
"""

import pandas as pd
import numpy as np
import json
import os

np.random.seed(42)

# ── Sample product data ──────────────────────────────────────────────────────

PRODUCTS = [
    # Skincare
    ("Nivea Q10 Anti-Wrinkle Day Cream 50ml", "Nivea", "personal care"),
    ("Olay Regenerist Micro-Sculpting Cream", "Olay", "skincare"),
    ("Neutrogena Hydro Boost Water Gel", "Neutrogena", "moisturiser"),
    ("Cetaphil Gentle Skin Cleanser 500ml", "Cetaphil", "face wash"),
    ("Lakme Absolute Skin Natural Mousse", "Lakme", None),
    ("Pond's White Beauty Cream 35g", "Pond's", "skincare"),
    ("Garnier Light Complete Serum Cream", "Garnier", "cream"),
    ("The Body Shop Vitamin E Moisturiser", "The Body Shop", "skin"),
    ("Himalaya Herbals Nourishing Skin Cream", "Himalaya", None),
    ("Biotique Bio Almond Oil Moisturiser", "Biotique", "moisturiser"),

    # Haircare
    ("Head & Shoulders Anti-Dandruff Shampoo 400ml", "P&G", "hair/shampoo"),
    ("Pantene Pro-V Silky Smooth Shampoo", "Pantene", "shampoo"),
    ("Dove Intense Repair Shampoo 340ml", "Dove", "hair care"),
    ("TRESemmé Keratin Smooth Shampoo", "TRESemmé", "hair"),
    ("Sunsilk Stunning Black Shine Shampoo", "Sunsilk", None),
    ("Garnier Ultra Blends Mythic Olive Conditioner", "Garnier", "conditioner"),
    ("Dove Intense Repair Conditioner", "Dove", "hair"),
    ("Parachute Advansed Jasmine Hair Oil 300ml", "Parachute", "hair oil"),
    ("Indulekha Bringha Hair Oil", "Indulekha", None),
    ("Himalaya Anti-Dandruff Hair Cream", "Himalaya", "hair"),

    # Bath & Body
    ("Dove Deeply Nourishing Body Wash 500ml", "Dove", "personal care"),
    ("Lux Velvet Touch Body Wash", "Lux", "body wash"),
    ("Dettol Original Liquid Hand Wash 200ml", "Dettol", "soap/hygiene"),
    ("Lifebuoy Total 10 Body Wash", "Lifebuoy", "hygiene"),
    ("Pears Pure & Gentle Shower Gel", "Pears", "bath"),
    ("Palmolive Naturals Milk & Honey Body Wash", "Palmolive", None),
    ("Fiama Di Wills Peach & Avocado Shower Gel", "Fiama", "body"),
    ("Savlon Moisturising Hand Wash 200ml", "Savlon", "hygiene"),
    ("Biotique Morning Nectar Body Lotion", "Biotique", "lotion"),
    ("Vaseline Intensive Care Body Lotion", "Vaseline", "body lotion"),

    # Oral Care
    ("Colgate MaxFresh Toothpaste 150g", "Colgate", "oral care"),
    ("Sensodyne Rapid Relief Toothpaste", "Sensodyne", "toothpaste"),
    ("Oral-B Pro-Expert Toothbrush", "Oral-B", "dental"),
    ("Colgate 360 Charcoal Gold Toothbrush", "Colgate", "brush"),
    ("Listerine Cool Mint Mouthwash 500ml", "Listerine", None),
    ("Dabur Red Toothpaste Ayurvedic", "Dabur", "oral"),
    ("Pepsodent Germicheck Toothpaste", "Pepsodent", None),
    ("Close Up Deep Action Toothpaste", "Close Up", "toothpaste"),

    # Ambiguous / edge cases
    ("Himalaya Wellness Complete Care", "Himalaya", None),       # brand only
    ("Generic Product 001", "Unknown", None),                   # fully unknown
    ("Dove Men+Care Face Wash", "Dove", "men care"),             # cross-category
    ("Johnson's Baby Powder 200g", "Johnson's", None),           # unclear adult/baby
    ("Vicks VapoRub 50ml", "Vicks", "wellness"),                 # out-of-scope
    ("Gillette Mach3 Razor", "Gillette", "grooming"),            # out of taxonomy
    ("Old Spice After Shave Lotion", "Old Spice", None),         # ambiguous
]

def generate_data():
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    records = []
    for i, (name, brand, raw_cat) in enumerate(PRODUCTS):
        records.append({
            "product_id": f"P{str(i+1).zfill(4)}",
            "product_name": name,
            "brand": brand,
            "raw_category": raw_cat,
            "price_inr": round(np.random.uniform(50, 800), 2),
            "stock_units": np.random.randint(0, 500),
        })

    df = pd.DataFrame(records)

    # Introduce realistic data quality issues
    df.loc[df.sample(5, random_state=1).index, "raw_category"] = None
    df.loc[df.sample(3, random_state=2).index, "brand"] = None
    df.loc[df.sample(2, random_state=3).index, "product_name"] = df.loc[
        df.sample(2, random_state=3).index, "product_name"
    ]  # keep as-is (simulate duplicate names)

    # Add one actual duplicate row
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    df.to_csv("data/raw_products.csv", index=False)
    print(f"Generated {len(df)} product records → data/raw_products.csv")
    print(f"  Null raw_category: {df['raw_category'].isnull().sum()}")
    print(f"  Null brand: {df['brand'].isnull().sum()}")
    print(f"  Duplicates: {df.duplicated().sum()}")


# ── Client taxonomy definition ───────────────────────────────────────────────

TAXONOMY = {
    "Skincare": {
        "keywords": [
            "moisturiser", "moisturizer", "cream", "serum", "cleanser",
            "face wash", "sunscreen", "spf", "toner", "skin", "lotion face",
            "anti-wrinkle", "whitening", "brightening", "gel face"
        ],
        "brands": ["Nivea", "Olay", "Neutrogena", "Cetaphil", "Lakme",
                   "Pond's", "Garnier", "The Body Shop", "Himalaya", "Biotique"]
    },
    "Haircare": {
        "keywords": [
            "shampoo", "conditioner", "hair oil", "hair cream", "hair mask",
            "hair serum", "dandruff", "keratin", "hair", "scalp"
        ],
        "brands": ["Head & Shoulders", "Pantene", "TRESemmé", "Sunsilk",
                   "Parachute", "Indulekha"]
    },
    "Bath & Body": {
        "keywords": [
            "body wash", "shower gel", "hand wash", "soap", "bath",
            "body lotion", "body milk", "hygiene", "liquid wash", "scrub body"
        ],
        "brands": ["Dove", "Lux", "Dettol", "Lifebuoy", "Pears",
                   "Palmolive", "Fiama", "Savlon", "Vaseline"]
    },
    "Oral Care": {
        "keywords": [
            "toothpaste", "toothbrush", "mouthwash", "dental", "teeth",
            "whitening teeth", "oral", "floss", "gum", "brush teeth"
        ],
        "brands": ["Colgate", "Sensodyne", "Oral-B", "Listerine",
                   "Dabur", "Pepsodent", "Close Up"]
    }
}

def save_taxonomy():
    with open("data/client_taxonomy.json", "w") as f:
        json.dump(TAXONOMY, f, indent=2)
    print("Saved taxonomy → data/client_taxonomy.json")


if __name__ == "__main__":
    generate_data()
    save_taxonomy()
