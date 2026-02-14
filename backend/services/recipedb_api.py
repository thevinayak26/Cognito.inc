"""
RecipeDB API Service
Handles all interactions with RecipeDB API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from config import RECIPEDB_ENDPOINTS, API_TIMEOUT


class RecipeDBAPI:
    def __init__(self):
        self.endpoints = RECIPEDB_ENDPOINTS
        self.timeout = API_TIMEOUT
    
    def _make_request(self, url, params=None):
        """
        Generic request handler with error handling
        """
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()  # Raise error for 4xx/5xx
            return response.json()
        except requests.exceptions.Timeout:
            print(f"❌ Timeout error for {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None
    
    # ==================== RECIPE SEARCH ====================
    
    def get_all_recipes(self, limit=100):
        """
        Fetch basic information about recipes
        
        Returns:
            List of recipes with basic info
        """
        print("📡 Fetching recipes from RecipeDB...")
        data = self._make_request(
            self.endpoints["recipes_info"],
            params={"limit": limit}
        )
        
        if data:
            print(f"✅ Retrieved {len(data.get('recipes', []))} recipes")
            return data.get('recipes', [])
        return []
    
    def get_recipes_by_diet(self, diet_type):
        """
        Get recipes filtered by dietary type
        
        Args:
            diet_type: "keto", "vegan", "high-protein", etc.
        
        Returns:
            List of recipes matching diet
        """
        print(f"📡 Fetching {diet_type} recipes...")
        data = self._make_request(
            self.endpoints["recipe_by_diet"],
            params={"diet": diet_type}
        )
        
        if data:
            recipes = data.get('recipes', [])
            print(f"✅ Found {len(recipes)} {diet_type} recipes")
            return recipes
        return []
    
    def get_recipes_by_protein_range(self, min_protein, max_protein):
        """
        Get recipes within a protein range
        
        Args:
            min_protein: Minimum protein (grams)
            max_protein: Maximum protein (grams)
        
        Returns:
            List of recipes
        """
        print(f"📡 Fetching recipes with protein {min_protein}-{max_protein}g...")
        data = self._make_request(
            self.endpoints["protein_range"],
            params={
                "min_protein": min_protein,
                "max_protein": max_protein
            }
        )
        
        if data:
            recipes = data.get('recipes', [])
            print(f"✅ Found {len(recipes)} recipes in protein range")
            return recipes
        return []
    
    # ==================== NUTRITION DATA ====================
    
    def get_nutrition_info(self, recipe_id):
        """
        Get detailed macronutrient information
        
        Args:
            recipe_id: Recipe identifier
        
        Returns:
            Dict with calories, protein, carbs, fat
        """
        print(f"📡 Fetching nutrition for recipe {recipe_id}...")
        data = self._make_request(
            self.endpoints["nutrition_info"],
            params={"recipe_id": recipe_id}
        )
        
        if data:
            print(f"✅ Nutrition data retrieved")
            return data
        return {}
    
    def get_micro_nutrition_info(self, recipe_id):
        """
        Get micronutrient information (vitamins, minerals)
        
        Args:
            recipe_id: Recipe identifier
        
        Returns:
            Dict with vitamin/mineral data
        """
        print(f"📡 Fetching micronutrients for recipe {recipe_id}...")
        data = self._make_request(
            self.endpoints["micro_nutrition"],
            params={"recipe_id": recipe_id}
        )
        
        if data:
            print(f"✅ Micronutrient data retrieved")
            return data
        return {}
    
    # ==================== INGREDIENT DATA ====================
    
    def get_ingredients_by_flavor(self, flavor_profile):
        """
        Get ingredients with specific flavor profile
        
        Args:
            flavor_profile: e.g., "sweet", "spicy", "umami"
        
        Returns:
            List of ingredients
        """
        print(f"📡 Fetching ingredients with {flavor_profile} flavor...")
        url = f"{self.endpoints['ingredients_by_flavor']}/{flavor_profile}"
        data = self._make_request(url)
        
        if data:
            ingredients = data.get('ingredients', [])
            print(f"✅ Found {len(ingredients)} ingredients")
            return ingredients
        return []


# ==================== QUICK TEST FUNCTION ====================

def test_recipedb_api():
    """
    Test function to verify API connectivity
    """
    print("\n" + "="*50)
    print("🧪 TESTING RECIPEDB API")
    print("="*50 + "\n")
    
    api = RecipeDBAPI()
    
    # Test 1: Get some recipes
    print("\n--- Test 1: Get All Recipes ---")
    recipes = api.get_all_recipes(limit=5)
    if recipes:
        print(f"Sample recipe: {recipes[0].get('title', 'N/A')}")
    
    # Test 2: Get keto recipes
    print("\n--- Test 2: Get Keto Recipes ---")
    keto_recipes = api.get_recipes_by_diet("keto")
    if keto_recipes:
        print(f"Sample keto recipe: {keto_recipes[0].get('title', 'N/A')}")
    
    # Test 3: Get high-protein recipes
    print("\n--- Test 3: Get High-Protein Recipes ---")
    protein_recipes = api.get_recipes_by_protein_range(25, 50)
    if protein_recipes:
        print(f"Sample high-protein recipe: {protein_recipes[0].get('title', 'N/A')}")
    
    # Test 4: Get nutrition for first recipe
    if recipes:
        print("\n--- Test 4: Get Nutrition Info ---")
        recipe_id = recipes[0].get('id')
        nutrition = api.get_nutrition_info(recipe_id)
        print(f"Nutrition data keys: {list(nutrition.keys())}")
    
    print("\n" + "="*50)
    print("✅ RECIPEDB API TESTS COMPLETE")
    print("="*50 + "\n")


if __name__ == "__main__":
    test_recipedb_api()