"""
Configuration file for API endpoints and constants
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (use explicit path)
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Get API Keys from environment
RECIPEDB_API_KEY = os.getenv('RECIPEDB_API_KEY')
FLAVORDB_API_KEY = os.getenv('FLAVORDB_API_KEY')

if not RECIPEDB_API_KEY:
    print("⚠️ WARNING: RECIPEDB_API_KEY not found in .env file")
else:
    print(f"✅ RecipeDB API Key loaded: {RECIPEDB_API_KEY[:10]}...")

if not FLAVORDB_API_KEY:
    print("⚠️ WARNING: FLAVORDB_API_KEY not found in .env file")
else:
    print(f"✅ FlavorDB API Key loaded: {FLAVORDB_API_KEY[:10]}...")

# API Base URLs
RECIPEDB_BASE_URL = "http://cosylab.iiitd.edu/recipe2-api"
FLAVORDB_BASE_URL = "http://cosylab.iiitd.edu.in:6969/flavordb"

# API Endpoints - RecipeDB
RECIPEDB_ENDPOINTS = {
    "recipes_info": f"{RECIPEDB_BASE_URL}/recipes/recipesinfo",
    "nutrition_info": f"{RECIPEDB_BASE_URL}/recipes/nutritioninfo",
    "micro_nutrition": f"{RECIPEDB_BASE_URL}/recipes/micronutritioninfo",
    "ingredients_by_flavor": f"{RECIPEDB_BASE_URL}/ingredients",
    "recipe_by_diet": f"{RECIPEDB_BASE_URL}/recipes/recipe-diet",
    "protein_range": f"{RECIPEDB_BASE_URL}/recipes/protein-range",
    "recipe_by_cuisine": f"{RECIPEDB_BASE_URL}/recipes/cuisine",
    "recipe_by_ingredient": f"{RECIPEDB_BASE_URL}/recipes/ingredients",
}

# API Endpoints - FlavorDB
FLAVORDB_ENDPOINTS = {
    "by_flavor_profile": f"{FLAVORDB_BASE_URL}/molecules_data/by-flavorProfile",
    "by_functional_groups": f"{FLAVORDB_BASE_URL}/molecules_data/by-functionalGroups",
    "by_aroma_threshold": f"{FLAVORDB_BASE_URL}/properties/by-aromaThresholdValues",
    "filter_by_weight": f"{FLAVORDB_BASE_URL}/molecules_data/filter-by-weight-range",
    "by_common_name": f"{FLAVORDB_BASE_URL}/molecules_data/by-commonName",
    "entity_details": f"{FLAVORDB_BASE_URL}/entity_details",
    "all_entities": f"{FLAVORDB_BASE_URL}/entities",
}

# Request settings
API_TIMEOUT = 3
ENABLE_CACHE = True
CACHE_EXPIRY = 3600  # 1 hour

# Authentication methods
AUTH_METHODS = {
    "header": True,
    "param": True,
    "none": True
}