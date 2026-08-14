"""
seed_sample_data.py — inserts a small set of placeholder/showcase records into the
'fermented_beverages' collection so the UI has something to render immediately.

This is NOT a substitute for your real 17-file dataset. Fields like "Evidence Source"
are marked as placeholders on purpose -- replace this collection's contents with your
real CSV import (scripts/import_csv.py) when your sourced data is ready. Easiest way to
clear it first: drop_seed_data() at the bottom, or just delete the collection in Atlas.

Usage:
    cd backend
    python scripts/seed_sample_data.py
"""
import sys
from pathlib import Path

from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.config import settings  # noqa: E402

COLLECTION_NAME = "fermented_beverages"

PLACEHOLDER_NOTE = "Sample/placeholder — replace with verified citation before publishing"

SAMPLE_RECORDS = [
    {
        "Beverage Name": "Handia",
        "Tribe / Ethnic Group (major consumers)": "Munda; Ho; Santhal",
        "Region / State (typical)": "Jharkhand",
        "Longitude (avg)": "85.3", "Latitude (avg)": "22.8", "Altitude (m, avg)": "300",
        "Temperature (°C, annual avg)": "26", "Humidity (% RH, annual avg)": "70",
        "Humidity (%) (typical range)": "60-80",
        "Starter Name": "Bakhar",
        "Microorganisms Used (dominant reported)": "Saccharomyces cerevisiae; Lactobacillus spp.",
        "Evidence Source (paper/book/URL/DOI)": PLACEHOLDER_NOTE,
        "Components (GC-MS/LC-MS derived)": "Ethanol; Lactic acid; Esters",
        "Components Sources (URL/DOI)": PLACEHOLDER_NOTE,
        "Fermentation Type": "Solid-state (rice-based)",
        "Fermentation Time (days)": "3-5",
        "Fermentation Vessel": "Earthen pot",
        "pH (reported range)": "3.8-4.5",
        "Alcohol Content (% v/v)": "4-6",
        "Major Microorganisms": "Saccharomyces cerevisiae; Rhizopus spp.",
        "Starter Culture Type": "Back-slopping (dry cake)",
        "Dominant Microbial Group": "Yeast-LAB consortium",
        "Fermentation Temperature (°C)": "25-30",
        "Primary Metabolites": "Ethanol; Organic acids; CO2",
        "Probiotic Potential": "Moderate",
        "Documentation Status": "Partially documented",
        "Research Gap / Remarks": "Limited strain-level data",
        "Carbohydrate Source": "Rice",
        "Enzymatic Activity Involved": "Amylolytic; Alcoholic",
        "Organic Acids Reported": "Lactic acid; Acetic acid",
        "Redox Nature of Fermentation": "Anaerobic",
        "Microbial Safety Concern": "Low if hygienic prep",
        "Shelf Life (Traditional)": "2-3 days",
        "Consumption Mode": "Direct drink",
        "Age Group of Consumers": "Adults",
        "Occasion of Consumption": "Festivals; social gatherings",
        "Knowledge Transmission Mode": "Oral (family lineage)",
        "Data Confidence Level": "Medium",
        "Preparation Steps (Traditional)": "Steam rice; cool; mix bakhar; ferment in pot",
        "Taste Profile": "Sour-sweet, mild alcoholic",
        "Aroma Description": "Yeasty, tangy",
        "Color / Appearance": "Cloudy off-white",
        "Serving Method": "Served in bamboo cup",
        "Medicinal Use (Traditional)": "Used for digestive issues",
        "Current Popularity Status": "Declining among youth",
        "Risk of Knowledge Loss": "High",
    },
    {
        "Beverage Name": "Apong",
        "Tribe / Ethnic Group (major consumers)": "Mishing",
        "Region / State (typical)": "Assam",
        "Longitude (avg)": "94.6", "Latitude (avg)": "27.5", "Altitude (m, avg)": "100",
        "Temperature (°C, annual avg)": "24", "Humidity (% RH, annual avg)": "78",
        "Humidity (%) (typical range)": "65-85",
        "Starter Name": "Epop / Epab",
        "Microorganisms Used (dominant reported)": "Saccharomyces cerevisiae; Mucor spp.",
        "Evidence Source (paper/book/URL/DOI)": PLACEHOLDER_NOTE,
        "Components (GC-MS/LC-MS derived)": "Ethanol; Higher alcohols; Organic acids",
        "Components Sources (URL/DOI)": PLACEHOLDER_NOTE,
        "Fermentation Type": "Solid-state (rice-based)",
        "Fermentation Time (days)": "2-4",
        "Fermentation Vessel": "Bamboo container / earthen pot",
        "pH (reported range)": "3.5-4.2",
        "Alcohol Content (% v/v)": "5-8",
        "Major Microorganisms": "Saccharomyces cerevisiae; Mucor circinelloides",
        "Starter Culture Type": "Back-slopping (herbal cake)",
        "Dominant Microbial Group": "Yeast-mold consortium",
        "Fermentation Temperature (°C)": "26-30",
        "Primary Metabolites": "Ethanol; CO2; Esters",
        "Probiotic Potential": "Moderate",
        "Documentation Status": "Partially documented",
        "Research Gap / Remarks": "Regional variation (Nahoxing vs Poro types) underexplored",
        "Carbohydrate Source": "Glutinous rice",
        "Enzymatic Activity Involved": "Amylolytic; Alcoholic",
        "Organic Acids Reported": "Lactic acid; Citric acid",
        "Redox Nature of Fermentation": "Anaerobic",
        "Microbial Safety Concern": "Low if hygienic prep",
        "Shelf Life (Traditional)": "3-4 days",
        "Consumption Mode": "Direct drink",
        "Age Group of Consumers": "Adults",
        "Occasion of Consumption": "Daily; festivals (Ali-Aye-Ligang)",
        "Knowledge Transmission Mode": "Oral (family lineage)",
        "Data Confidence Level": "Medium",
        "Preparation Steps (Traditional)": "Cook rice; cool; mix epop; ferment 2-4 days",
        "Taste Profile": "Sweet-sour, mildly alcoholic",
        "Aroma Description": "Fruity, fermented rice",
        "Color / Appearance": "Milky white to pale yellow",
        "Serving Method": "Served in bamboo mug",
        "Medicinal Use (Traditional)": "Believed to aid stamina",
        "Current Popularity Status": "Stable within community, low outside",
        "Risk of Knowledge Loss": "Medium",
    },
    {
        "Beverage Name": "Chhang",
        "Tribe / Ethnic Group (major consumers)": "Bhutia; Lepcha",
        "Region / State (typical)": "Sikkim / Himachal Pradesh",
        "Longitude (avg)": "88.5", "Latitude (avg)": "27.3", "Altitude (m, avg)": "1800",
        "Temperature (°C, annual avg)": "14", "Humidity (% RH, annual avg)": "65",
        "Humidity (%) (typical range)": "50-75",
        "Starter Name": "Marcha / Phab",
        "Microorganisms Used (dominant reported)": "Saccharomyces cerevisiae; Pichia spp.",
        "Evidence Source (paper/book/URL/DOI)": PLACEHOLDER_NOTE,
        "Components (GC-MS/LC-MS derived)": "Ethanol; Acetaldehyde; Fusel alcohols",
        "Components Sources (URL/DOI)": PLACEHOLDER_NOTE,
        "Fermentation Type": "Solid-state (millet/barley-based)",
        "Fermentation Time (days)": "5-7",
        "Fermentation Vessel": "Wooden or bamboo vessel",
        "pH (reported range)": "3.6-4.3",
        "Alcohol Content (% v/v)": "3-5",
        "Major Microorganisms": "Saccharomyces cerevisiae; Lactobacillus spp.",
        "Starter Culture Type": "Back-slopping (dry cake, marcha)",
        "Dominant Microbial Group": "Yeast-LAB consortium",
        "Fermentation Temperature (°C)": "18-24",
        "Primary Metabolites": "Ethanol; Organic acids",
        "Probiotic Potential": "Low-Moderate",
        "Documentation Status": "Well documented regionally",
        "Research Gap / Remarks": "Strain diversity across Himalayan belt not mapped",
        "Carbohydrate Source": "Finger millet / barley",
        "Enzymatic Activity Involved": "Amylolytic; Alcoholic",
        "Organic Acids Reported": "Lactic acid",
        "Redox Nature of Fermentation": "Anaerobic",
        "Microbial Safety Concern": "Low",
        "Shelf Life (Traditional)": "5-7 days (refrigerated)",
        "Consumption Mode": "Sipped through bamboo straw (tongba style) or direct",
        "Age Group of Consumers": "Adults",
        "Occasion of Consumption": "Daily; winter warming drink; festivals",
        "Knowledge Transmission Mode": "Oral (family lineage)",
        "Data Confidence Level": "Medium-High",
        "Preparation Steps (Traditional)": "Cook millet; cool; mix marcha; ferment in cool storage",
        "Taste Profile": "Mildly sour, warm, slightly sweet",
        "Aroma Description": "Malty, fermented grain",
        "Color / Appearance": "Pale beige, cloudy",
        "Serving Method": "Tongba (bamboo vessel with straw), hot water added",
        "Medicinal Use (Traditional)": "Believed to provide warmth at high altitude",
        "Current Popularity Status": "Popular, some commercialization as tongba",
        "Risk of Knowledge Loss": "Low-Medium",
    },
    {
        "Beverage Name": "Judima",
        "Tribe / Ethnic Group (major consumers)": "Dimasa",
        "Region / State (typical)": "Assam (Dima Hasao)",
        "Longitude (avg)": "93.0", "Latitude (avg)": "25.5", "Altitude (m, avg)": "500",
        "Temperature (°C, annual avg)": "22", "Humidity (% RH, annual avg)": "80",
        "Humidity (%) (typical range)": "70-90",
        "Starter Name": "Humao",
        "Microorganisms Used (dominant reported)": "Saccharomyces cerevisiae; Rhizopus spp.",
        "Evidence Source (paper/book/URL/DOI)": PLACEHOLDER_NOTE,
        "Components (GC-MS/LC-MS derived)": "Ethanol; Phenolics; Organic acids",
        "Components Sources (URL/DOI)": PLACEHOLDER_NOTE,
        "Fermentation Type": "Solid-state (rice-based, GI tagged)",
        "Fermentation Time (days)": "7-15",
        "Fermentation Vessel": "Earthen pot",
        "pH (reported range)": "3.4-4.0",
        "Alcohol Content (% v/v)": "6-9",
        "Major Microorganisms": "Saccharomyces cerevisiae; Rhizopus oryzae",
        "Starter Culture Type": "Back-slopping (humao cake with local herbs)",
        "Dominant Microbial Group": "Yeast-mold consortium",
        "Fermentation Temperature (°C)": "24-28",
        "Primary Metabolites": "Ethanol; Antioxidant phenolics",
        "Probiotic Potential": "High (reported antioxidant activity)",
        "Documentation Status": "Documented (GI tag holder, 2022)",
        "Research Gap / Remarks": "Antioxidant/health claims need clinical validation",
        "Carbohydrate Source": "Glutinous rice",
        "Enzymatic Activity Involved": "Amylolytic; Alcoholic",
        "Organic Acids Reported": "Lactic acid; Gallic acid",
        "Redox Nature of Fermentation": "Anaerobic",
        "Microbial Safety Concern": "Low",
        "Shelf Life (Traditional)": "Weeks (improves with age)",
        "Consumption Mode": "Direct drink",
        "Age Group of Consumers": "Adults",
        "Occasion of Consumption": "Festivals; rituals; guest hospitality",
        "Knowledge Transmission Mode": "Oral (family lineage)",
        "Data Confidence Level": "Medium-High",
        "Preparation Steps (Traditional)": "Cook rice; cool; mix humao with herbs; ferment weeks in pot",
        "Taste Profile": "Sweet, wine-like, mildly tart",
        "Aroma Description": "Fruity, wine-like",
        "Color / Appearance": "Reddish-brown, clear after settling",
        "Serving Method": "Served in cups, sometimes strained",
        "Medicinal Use (Traditional)": "Believed to have antioxidant, health benefits",
        "Current Popularity Status": "Rising (GI tag driving commercial interest)",
        "Risk of Knowledge Loss": "Low (actively promoted)",
    },
    {
        "Beverage Name": "Zutho",
        "Tribe / Ethnic Group (major consumers)": "Angami Naga",
        "Region / State (typical)": "Nagaland",
        "Longitude (avg)": "94.1", "Latitude (avg)": "25.7", "Altitude (m, avg)": "1400",
        "Temperature (°C, annual avg)": "18", "Humidity (% RH, annual avg)": "75",
        "Humidity (%) (typical range)": "60-85",
        "Starter Name": "Traditional rice-based inoculum (unnamed, household-specific)",
        "Microorganisms Used (dominant reported)": "Saccharomyces cerevisiae; Lactobacillus spp.",
        "Evidence Source (paper/book/URL/DOI)": PLACEHOLDER_NOTE,
        "Components (GC-MS/LC-MS derived)": "Ethanol; Lactic acid",
        "Components Sources (URL/DOI)": PLACEHOLDER_NOTE,
        "Fermentation Type": "Liquid-state (rice beer)",
        "Fermentation Time (days)": "5-7",
        "Fermentation Vessel": "Earthen pot / bamboo vessel",
        "pH (reported range)": "3.7-4.4",
        "Alcohol Content (% v/v)": "4-6",
        "Major Microorganisms": "Saccharomyces cerevisiae",
        "Starter Culture Type": "Back-slopping (household inoculum)",
        "Dominant Microbial Group": "Yeast-LAB consortium",
        "Fermentation Temperature (°C)": "22-26",
        "Primary Metabolites": "Ethanol; Organic acids",
        "Probiotic Potential": "Moderate",
        "Documentation Status": "Partially documented",
        "Research Gap / Remarks": "Household-level variation poorly characterized",
        "Carbohydrate Source": "Rice",
        "Enzymatic Activity Involved": "Amylolytic; Alcoholic",
        "Organic Acids Reported": "Lactic acid",
        "Redox Nature of Fermentation": "Anaerobic",
        "Microbial Safety Concern": "Low",
        "Shelf Life (Traditional)": "3-5 days",
        "Consumption Mode": "Direct drink",
        "Age Group of Consumers": "Adults",
        "Occasion of Consumption": "Daily; festivals (Sekrenyi)",
        "Knowledge Transmission Mode": "Oral (family lineage)",
        "Data Confidence Level": "Low-Medium",
        "Preparation Steps (Traditional)": "Cook rice; cool; ferment in liquid form days",
        "Taste Profile": "Sour, mildly alcoholic, milky",
        "Aroma Description": "Sour rice, yeasty",
        "Color / Appearance": "Milky white",
        "Serving Method": "Served in bamboo mug",
        "Medicinal Use (Traditional)": "Believed to be nutritious, energy-giving",
        "Current Popularity Status": "Stable within community",
        "Risk of Knowledge Loss": "Medium",
    },
]


def seed():
    client = MongoClient(settings.mongodb_uri)
    db = client[settings.mongodb_db_name]
    collection = db[COLLECTION_NAME]

    existing = collection.count_documents({})
    if existing > 0:
        print(f"'{COLLECTION_NAME}' already has {existing} documents.")
        confirm = input("Insert sample records anyway? (y/N): ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            client.close()
            return

    result = collection.insert_many(SAMPLE_RECORDS)
    print(f"Inserted {len(result.inserted_ids)} sample records into "
          f"'{COLLECTION_NAME}' in database '{settings.mongodb_db_name}'.")
    print("These are placeholder records for UI showcase -- replace with your real, "
          "cited CSV data via scripts/import_csv.py when ready.")
    client.close()


def drop_seed_data():
    """Utility: wipe the collection clean before loading your real data."""
    client = MongoClient(settings.mongodb_uri)
    db = client[settings.mongodb_db_name]
    result = db[COLLECTION_NAME].delete_many({})
    print(f"Deleted {result.deleted_count} documents from '{COLLECTION_NAME}'.")
    client.close()


if __name__ == "__main__":
    seed()
