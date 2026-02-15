"""
FlavorDB API Service
Handles all interactions with FlavorDB API for molecular flavor data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import FLAVORDB_ENDPOINTS, API_TIMEOUT, FLAVORDB_API_KEY


class FlavorDBAPI:
    def __init__(self):
        self.endpoints = FLAVORDB_ENDPOINTS
        self.timeout = API_TIMEOUT
        self.api_key = FLAVORDB_API_KEY
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
            print(f"⚠️ FlavorDB API unreachable, using fallback data: {type(e).__name__}")
            self._api_failed = True
            return None

        return None

    # ==================== MOLECULE SEARCH ====================

    def get_molecules_by_flavor_profile(self, flavor_profile):
        """Get molecules associated with a flavor profile (fruity, floral, spicy, etc.)"""
        print(f"📡 Fetching molecules with {flavor_profile} profile...")
        data = self._make_request(
            self.endpoints["by_flavor_profile"],
            params={"flavorProfile": flavor_profile}
        )
        if data:
            if isinstance(data, list):
                return data
            molecules = data.get('molecules', data.get('payload', []))
            return molecules if isinstance(molecules, list) else []
        return []

    def get_molecules_by_common_name(self, ingredient_name):
        """Get flavor molecules for a specific ingredient"""
        print(f"📡 Fetching flavor molecules for {ingredient_name}...")
        data = self._make_request(
            self.endpoints["by_common_name"],
            params={"name": ingredient_name}
        )
        if data:
            if isinstance(data, list):
                return data
            molecules = data.get('molecules', data.get('payload', []))
            return molecules if isinstance(molecules, list) else []
        return []

    def get_entity_details(self, entity_id):
        """Get detailed entity info from FlavorDB"""
        print(f"📡 Fetching entity details for {entity_id}...")
        data = self._make_request(
            f"{self.endpoints['entity_details']}/{entity_id}"
        )
        return data or {}

    def get_all_entities(self, page=0, limit=20):
        """List all food entities"""
        print(f"📡 Fetching entities (page={page})...")
        data = self._make_request(
            self.endpoints["all_entities"],
            params={"pageNo": page, "pageSize": limit}
        )
        if data:
            if isinstance(data, list):
                return data
            return data.get('entities', data.get('payload', []))
        return []

    def get_molecules_by_functional_groups(self, functional_group):
        """Get molecules with specific functional groups"""
        print(f"📡 Fetching molecules with {functional_group} group...")
        data = self._make_request(
            self.endpoints["by_functional_groups"],
            params={"functional_group": functional_group}
        )
        if data:
            if isinstance(data, list):
                return data
            molecules = data.get('molecules', data.get('payload', []))
            return molecules if isinstance(molecules, list) else []
        return []

    # ==================== FLAVOR PROFILE COMPUTATION ====================

    # Flavor dimension categories and their associated keywords/profiles
    FLAVOR_DIMENSIONS = {
        "sweet": ["sweet", "caramel", "honey", "vanilla", "sugary", "fruity"],
        "sour": ["sour", "acidic", "tart", "citrus", "vinegar"],
        "bitter": ["bitter", "astringent", "roasted", "burnt"],
        "salty": ["salty", "briny", "mineral"],
        "umami": ["umami", "savory", "meaty", "brothy", "fermented"],
        "spicy": ["spicy", "pungent", "hot", "pepper", "sharp"],
        "fruity": ["fruity", "floral", "berry", "tropical", "apple"],
        "smoky": ["smoky", "woody", "earthy", "toasted", "nutty"],
    }

    # Fallback flavor profiles for common ingredients
    INGREDIENT_FLAVOR_MAP = {
        "tomato": {"sweet": 40, "sour": 55, "bitter": 10, "salty": 5, "umami": 70, "spicy": 5, "fruity": 50, "smoky": 10},
        "onion": {"sweet": 35, "sour": 15, "bitter": 15, "salty": 5, "umami": 40, "spicy": 30, "fruity": 10, "smoky": 15},
        "garlic": {"sweet": 10, "sour": 10, "bitter": 15, "salty": 5, "umami": 60, "spicy": 55, "fruity": 5, "smoky": 20},
        "potato": {"sweet": 20, "sour": 5, "bitter": 5, "salty": 5, "umami": 25, "spicy": 0, "fruity": 5, "smoky": 10},
        "spinach": {"sweet": 10, "sour": 10, "bitter": 35, "salty": 10, "umami": 20, "spicy": 5, "fruity": 10, "smoky": 15},
        "carrot": {"sweet": 55, "sour": 10, "bitter": 10, "salty": 5, "umami": 15, "spicy": 5, "fruity": 30, "smoky": 10},
        "capsicum": {"sweet": 35, "sour": 10, "bitter": 15, "salty": 5, "umami": 10, "spicy": 40, "fruity": 25, "smoky": 15},
        "mushroom": {"sweet": 10, "sour": 5, "bitter": 10, "salty": 10, "umami": 80, "spicy": 5, "fruity": 5, "smoky": 35},
        "paneer": {"sweet": 15, "sour": 10, "bitter": 5, "salty": 15, "umami": 30, "spicy": 0, "fruity": 5, "smoky": 5},
        "cauliflower": {"sweet": 20, "sour": 5, "bitter": 20, "salty": 5, "umami": 15, "spicy": 5, "fruity": 10, "smoky": 20},
        "cabbage": {"sweet": 20, "sour": 10, "bitter": 25, "salty": 5, "umami": 10, "spicy": 10, "fruity": 10, "smoky": 10},
        "broccoli": {"sweet": 15, "sour": 5, "bitter": 30, "salty": 5, "umami": 20, "spicy": 5, "fruity": 10, "smoky": 15},
        "ginger": {"sweet": 10, "sour": 10, "bitter": 10, "salty": 0, "umami": 5, "spicy": 75, "fruity": 15, "smoky": 10},
        "cumin": {"sweet": 5, "sour": 5, "bitter": 15, "salty": 5, "umami": 20, "spicy": 40, "fruity": 5, "smoky": 55},
        "turmeric": {"sweet": 5, "sour": 5, "bitter": 35, "salty": 0, "umami": 10, "spicy": 30, "fruity": 5, "smoky": 30},
        "coriander": {"sweet": 15, "sour": 10, "bitter": 10, "salty": 0, "umami": 10, "spicy": 15, "fruity": 35, "smoky": 10},
        "lemon": {"sweet": 15, "sour": 85, "bitter": 15, "salty": 5, "umami": 5, "spicy": 5, "fruity": 65, "smoky": 0},
        "chili": {"sweet": 5, "sour": 5, "bitter": 10, "salty": 0, "umami": 10, "spicy": 90, "fruity": 15, "smoky": 20},
        "rice": {"sweet": 20, "sour": 0, "bitter": 5, "salty": 0, "umami": 15, "spicy": 0, "fruity": 5, "smoky": 10},
        "lentil": {"sweet": 10, "sour": 5, "bitter": 10, "salty": 5, "umami": 40, "spicy": 5, "fruity": 5, "smoky": 20},
        "chickpea": {"sweet": 15, "sour": 5, "bitter": 10, "salty": 5, "umami": 30, "spicy": 5, "fruity": 10, "smoky": 20},
    }

    def compute_flavor_profile(self, ingredients):
        """
        Compute aggregate flavor dimensions for a list of ingredients.
        Tries the API first, falls back to built-in flavor map.

        Args:
            ingredients: list of ingredient names

        Returns:
            dict with flavor dimension scores (0-100):
            {sweet, sour, bitter, salty, umami, spicy, fruity, smoky}
        """
        dimension_scores = {dim: [] for dim in self.FLAVOR_DIMENSIONS}

        for ingredient in ingredients:
            ingredient_lower = ingredient.lower().strip()

            # Try API first
            molecules = self.get_molecules_by_common_name(ingredient_lower)

            if molecules and len(molecules) > 0:
                # Parse molecule flavor profiles
                for molecule in molecules:
                    flavor_profile = (
                        molecule.get('flavor_profile', '') or
                        molecule.get('flavorProfile', '') or
                        molecule.get('taste', '') or ''
                    ).lower()

                    for dim, keywords in self.FLAVOR_DIMENSIONS.items():
                        for kw in keywords:
                            if kw in flavor_profile:
                                dimension_scores[dim].append(60 + len(molecules) * 2)
                                break
            else:
                # Fallback to built-in map
                if ingredient_lower in self.INGREDIENT_FLAVOR_MAP:
                    fallback = self.INGREDIENT_FLAVOR_MAP[ingredient_lower]
                    for dim in dimension_scores:
                        dimension_scores[dim].append(fallback.get(dim, 10))
                else:
                    # Unknown ingredient gets moderate baseline
                    for dim in dimension_scores:
                        dimension_scores[dim].append(20)

        # Average across ingredients
        result = {}
        for dim, scores in dimension_scores.items():
            if scores:
                result[dim] = min(100, round(sum(scores) / len(scores)))
            else:
                result[dim] = 15

        return result

    def get_flavor_pairings(self, ingredients):
        """
        Suggest ingredient pairings that complement the current flavor profile.

        Args:
            ingredients: list of current ingredient names

        Returns:
            list of pairing suggestions with reasoning
        """
        current_profile = self.compute_flavor_profile(ingredients)

        # Find weakest dimensions
        sorted_dims = sorted(current_profile.items(), key=lambda x: x[1])
        weak_dims = sorted_dims[:3]  # 3 weakest

        pairing_suggestions = {
            "sweet": ["honey", "jaggery", "coconut", "sweet potato", "dates"],
            "sour": ["lemon", "tamarind", "yogurt", "raw mango", "vinegar"],
            "bitter": ["fenugreek", "bitter gourd", "turmeric", "mustard greens", "neem"],
            "salty": ["rock salt", "soy sauce", "miso", "seaweed", "olives"],
            "umami": ["mushroom", "soy sauce", "tomato paste", "parmesan", "miso"],
            "spicy": ["chili", "black pepper", "ginger", "wasabi", "horseradish"],
            "fruity": ["mango", "pineapple", "apple", "orange zest", "raisins"],
            "smoky": ["smoked paprika", "chipotle", "charcoal-grilled veggies", "liquid smoke", "roasted cumin"],
        }

        suggestions = []
        ingredient_set = set(i.lower() for i in ingredients)

        for dim, score in weak_dims:
            candidates = [p for p in pairing_suggestions.get(dim, []) if p.lower() not in ingredient_set]
            if candidates:
                suggestions.append({
                    "dimension": dim,
                    "current_score": score,
                    "suggestion": candidates[0],
                    "reason": f"Adding {candidates[0]} would boost the {dim} dimension (currently {score}/100)",
                    "alternatives": candidates[1:3]
                })

        return suggestions

    def get_ingredient_flavor_profile(self, ingredient_name):
        """Get comprehensive flavor profile for a single ingredient"""
        molecules = self.get_molecules_by_common_name(ingredient_name)

        if not molecules:
            # Use fallback
            flavor = self.INGREDIENT_FLAVOR_MAP.get(
                ingredient_name.lower(),
                {dim: 20 for dim in self.FLAVOR_DIMENSIONS}
            )
            return {
                "ingredient": ingredient_name,
                "molecule_count": 0,
                "flavor_profile": flavor,
                "molecules": [],
                "source": "fallback"
            }

        molecule_ids = [m.get('molecule_id') or m.get('id') for m in molecules]
        flavor = self.compute_flavor_profile([ingredient_name])

        return {
            "ingredient": ingredient_name,
            "molecule_count": len(molecules),
            "molecule_ids": molecule_ids,
            "flavor_profile": flavor,
            "molecules": molecules[:10],  # Limit for performance
            "source": "api"
        }


# ==================== QUICK TEST ====================

def test_flavordb_api():
    print("\n" + "="*50)
    print("🧪 TESTING FLAVORDB API")
    print("="*50 + "\n")

    api = FlavorDBAPI()

    print("\n--- Test 1: Get Garlic Flavor Profile ---")
    garlic_data = api.get_ingredient_flavor_profile("garlic")
    print(f"Garlic: {garlic_data['flavor_profile']}")

    print("\n--- Test 2: Compute Profile for Multiple Ingredients ---")
    profile = api.compute_flavor_profile(["tomato", "onion", "garlic"])
    print(f"Combined profile: {profile}")

    print("\n--- Test 3: Get Flavor Pairings ---")
    pairings = api.get_flavor_pairings(["tomato", "onion", "garlic"])
    for p in pairings:
        print(f"  {p['dimension']}: Add {p['suggestion']} ({p['reason']})")

    print("\n" + "="*50)
    print("✅ FLAVORDB API TESTS COMPLETE")
    print("="*50 + "\n")


if __name__ == "__main__":
    test_flavordb_api()