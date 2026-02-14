"""
Configuration file for API endpoints and constants
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API Key from environment
API_KEY = os.getenv('FOODOSCOPE_API_KEY')

if not API_KEY:
    print("⚠️ WARNING: FOODOSCOPE_API_KEY not found in .env file")
else:
    print(f"✅ API Key loaded: {API_KEY[:10]}...")

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
    "protein_range": f"{RECIPEDB_BASE_URL}/recipes/protein-range"
}

# API Endpoints - FlavorDB
FLAVORDB_ENDPOINTS = {
    "by_flavor_profile": f"{FLAVORDB_BASE_URL}/molecules_data/by-flavorProfile",
    "by_functional_groups": f"{FLAVORDB_BASE_URL}/molecules_data/by-functionalGroups",
    "by_aroma_threshold": f"{FLAVORDB_BASE_URL}/properties/by-aromaThresholdValues",
    "filter_by_weight": f"{FLAVORDB_BASE_URL}/molecules_data/filter-by-weight-range",
    "by_common_name": f"{FLAVORDB_BASE_URL}/molecules_data/by-commonName"
}

# Request settings
API_TIMEOUT = 10
ENABLE_CACHE = True
CACHE_EXPIRY = 3600  # 1 hour

# Authentication methods to try (we'll detect which works)
AUTH_METHODS = {
    "header": True,      # Try Authorization: Bearer <token>
    "param": True,       # Try ?api_key=<token>
    "none": True         # Try without auth (if public)
}