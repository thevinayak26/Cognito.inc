"""
RecipeDB API Service
Handles all interactions with RecipeDB API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from config import RECIPEDB_ENDPOINTS, API_TIMEOUT, RECIPEDB_API_KEY


class RecipeDBAPI:
    def __init__(self):
        self.endpoints = RECIPEDB_ENDPOINTS
        self.timeout = API_TIMEOUT
        self.api_key = RECIPEDB_API_KEY
        self._api_failed = False  # Cache failure to skip retries

    def _make_request(self, url, params=None):
        """Generic request handler — skips API after first failure to avoid long waits"""
        if self._api_failed:
            return None

        if params is None:
            params = {}

        try:
            response = requests.get(
                url,
                params={**params, "api_key": self.api_key},
                timeout=self.timeout
            )
            if response.status_code == 200:
                try:
                    return response.json()
                except Exception:
                    return None
        except requests.exceptions.RequestException as e:
            print(f"⚠️ RecipeDB API unreachable, using fallback data: {type(e).__name__}")
            self._api_failed = True
            return None

        return None

    # ==================== RECIPE SEARCH ====================

    def get_all_recipes(self, page=0, limit=10):
        """Fetch recipes with pagination"""
        print(f"📡 Fetching recipes (page={page}, limit={limit})...")
        data = self._make_request(
            self.endpoints["recipes_info"],
            params={"pageSize": limit, "pageNo": page}
        )
        if data:
            if isinstance(data, list):
                print(f"✅ Retrieved {len(data)} recipes")
                return data
            recipes = data.get('recipes', data.get('payload', data))
            if isinstance(recipes, list):
                print(f"✅ Retrieved {len(recipes)} recipes")
                return recipes
        return []

    def search_by_ingredients(self, ingredients):
        """
        Search recipes that use specific ingredients

        Args:
            ingredients: list of ingredient names
        Returns:
            List of matching recipes
        """
        print(f"📡 Searching recipes with ingredients: {ingredients}...")
        results = []

        # Try the ingredient endpoint
        for ingredient in ingredients[:3]:  # Limit to first 3 for speed
            data = self._make_request(
                self.endpoints["recipe_by_ingredient"],
                params={"ingredient": ingredient, "pageSize": 10, "pageNo": 0}
            )
            if data:
                if isinstance(data, list):
                    results.extend(data)
                elif isinstance(data, dict):
                    items = data.get('recipes', data.get('payload', []))
                    if isinstance(items, list):
                        results.extend(items)

        # Deduplicate by recipe_id or title
        seen = set()
        unique = []
        for r in results:
            key = r.get('recipe_id', r.get('Recipe_id', r.get('title', str(r))))
            if key not in seen:
                seen.add(key)
                unique.append(r)

        print(f"✅ Found {len(unique)} unique recipes")
        return unique

    def get_recipes_by_diet(self, diet_type, page=0, limit=10):
        """Get recipes filtered by dietary type"""
        print(f"📡 Fetching {diet_type} recipes...")
        data = self._make_request(
            self.endpoints["recipe_by_diet"],
            params={"diet": diet_type, "pageSize": limit, "pageNo": page}
        )
        if data:
            if isinstance(data, list):
                return data
            recipes = data.get('recipes', data.get('payload', []))
            if isinstance(recipes, list):
                return recipes
        return []

    def get_recipes_by_cuisine(self, cuisine, page=0, limit=10):
        """Get recipes by cuisine type"""
        print(f"📡 Fetching {cuisine} cuisine recipes...")
        data = self._make_request(
            self.endpoints["recipe_by_cuisine"],
            params={"cuisine": cuisine, "pageSize": limit, "pageNo": page}
        )
        if data:
            if isinstance(data, list):
                return data
            recipes = data.get('recipes', data.get('payload', []))
            if isinstance(recipes, list):
                return recipes
        return []

    def get_recipes_by_protein_range(self, min_protein, max_protein):
        """Get recipes within a protein range"""
        print(f"📡 Fetching recipes with protein {min_protein}-{max_protein}g...")
        data = self._make_request(
            self.endpoints["protein_range"],
            params={"min_protein": min_protein, "max_protein": max_protein}
        )
        if data:
            if isinstance(data, list):
                return data
            recipes = data.get('recipes', data.get('payload', []))
            if isinstance(recipes, list):
                return recipes
        return []

    # ==================== NUTRITION DATA ====================

    def get_nutrition_info(self, recipe_id):
        """Get detailed macronutrient information"""
        print(f"📡 Fetching nutrition for recipe {recipe_id}...")
        data = self._make_request(
            self.endpoints["nutrition_info"],
            params={"recipe_id": recipe_id}
        )
        if data:
            return data
        return {}

    def get_micro_nutrition_info(self, recipe_id):
        """Get micronutrient information (vitamins, minerals)"""
        print(f"📡 Fetching micronutrients for recipe {recipe_id}...")
        data = self._make_request(
            self.endpoints["micro_nutrition"],
            params={"recipe_id": recipe_id}
        )
        if data:
            return data
        return {}


# ==================== QUICK TEST ====================

def test_recipedb_api():
    print("\n" + "="*50)
    print("🧪 TESTING RECIPEDB API")
    print("="*50 + "\n")

    api = RecipeDBAPI()

    print("\n--- Test 1: Get All Recipes ---")
    recipes = api.get_all_recipes(limit=3)
    if recipes:
        print(f"Sample recipe: {recipes[0]}")

    print("\n--- Test 2: Search by Ingredient ---")
    results = api.search_by_ingredients(["tomato"])
    if results:
        print(f"Found {len(results)} recipes with tomato")

    print("\n" + "="*50)
    print("✅ RECIPEDB API TESTS COMPLETE")
    print("="*50 + "\n")


if __name__ == "__main__":
    test_recipedb_api()