"""
FlavorDB API Service
Handles all interactions with FlavorDB API for molecular flavor data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import FLAVORDB_ENDPOINTS, API_TIMEOUT


class FlavorDBAPI:
    def __init__(self):
        self.endpoints = FLAVORDB_ENDPOINTS
        self.timeout = API_TIMEOUT
    
    def _make_request(self, url, params=None):
        """
        Generic request handler with error handling
        """
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"❌ Timeout error for {url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None
    
    # ==================== MOLECULE SEARCH ====================
    
    def get_molecules_by_flavor_profile(self, flavor_profile):
        """
        Get molecules associated with a flavor profile
        
        Args:
            flavor_profile: e.g., "fruity", "floral", "spicy"
        
        Returns:
            List of molecules
        """
        print(f"📡 Fetching molecules with {flavor_profile} profile...")
        data = self._make_request(
            self.endpoints["by_flavor_profile"],
            params={"flavor_profile": flavor_profile}
        )
        
        if data:
            molecules = data.get('molecules', [])
            print(f"✅ Found {len(molecules)} molecules")
            return molecules
        return []
    
    def get_molecules_by_common_name(self, ingredient_name):
        """
        Get flavor molecules for a specific ingredient
        
        Args:
            ingredient_name: e.g., "garlic", "tomato", "basil"
        
        Returns:
            List of molecules with their properties
        """
        print(f"📡 Fetching flavor molecules for {ingredient_name}...")
        data = self._make_request(
            self.endpoints["by_common_name"],
            params={"name": ingredient_name}
        )
        
        if data:
            molecules = data.get('molecules', [])
            print(f"✅ Found {len(molecules)} molecules in {ingredient_name}")
            return molecules
        return []
    
    def get_molecules_by_functional_groups(self, functional_group):
        """
        Get molecules with specific functional groups
        
        Args:
            functional_group: e.g., "alcohol", "aldehyde", "ester"
        
        Returns:
            List of molecules
        """
        print(f"📡 Fetching molecules with {functional_group} group...")
        data = self._make_request(
            self.endpoints["by_functional_groups"],
            params={"functional_group": functional_group}
        )
        
        if data:
            molecules = data.get('molecules', [])
            print(f"✅ Found {len(molecules)} molecules")
            return molecules
        return []
    
    def get_molecules_by_aroma_threshold(self, min_threshold, max_threshold):
        """
        Get molecules within aroma threshold range
        
        Args:
            min_threshold: Minimum threshold (ppb)
            max_threshold: Maximum threshold (ppb)
        
        Returns:
            List of molecules
        """
        print(f"📡 Fetching molecules with aroma threshold {min_threshold}-{max_threshold}...")
        data = self._make_request(
            self.endpoints["by_aroma_threshold"],
            params={
                "min": min_threshold,
                "max": max_threshold
            }
        )
        
        if data:
            molecules = data.get('molecules', [])
            print(f"✅ Found {len(molecules)} molecules")
            return molecules
        return []
    
    def filter_molecules_by_weight_range(self, min_weight, max_weight):
        """
        Filter molecules by molecular weight
        
        Args:
            min_weight: Minimum molecular weight (g/mol)
            max_weight: Maximum molecular weight (g/mol)
        
        Returns:
            List of molecules
        """
        print(f"📡 Filtering molecules by weight {min_weight}-{max_weight}...")
        data = self._make_request(
            self.endpoints["filter_by_weight"],
            params={
                "min_weight": min_weight,
                "max_weight": max_weight
            }
        )
        
        if data:
            molecules = data.get('molecules', [])
            print(f"✅ Found {len(molecules)} molecules")
            return molecules
        return []
    
    # ==================== HELPER FUNCTIONS ====================
    
    def get_ingredient_flavor_profile(self, ingredient_name):
        """
        Get comprehensive flavor profile for an ingredient
        
        Args:
            ingredient_name: Name of ingredient
        
        Returns:
            Dict with molecule IDs, names, and properties
        """
        molecules = self.get_molecules_by_common_name(ingredient_name)
        
        if not molecules:
            return {
                "ingredient": ingredient_name,
                "molecule_count": 0,
                "molecules": []
            }
        
        # Extract molecule IDs for matching
        molecule_ids = [m.get('molecule_id') or m.get('id') for m in molecules]
        
        return {
            "ingredient": ingredient_name,
            "molecule_count": len(molecules),
            "molecule_ids": molecule_ids,
            "molecules": molecules
        }


# ==================== QUICK TEST FUNCTION ====================

def test_flavordb_api():
    """
    Test function to verify FlavorDB API connectivity
    """
    print("\n" + "="*50)
    print("🧪 TESTING FLAVORDB API")
    print("="*50 + "\n")
    
    api = FlavorDBAPI()
    
    # Test 1: Get molecules for garlic
    print("\n--- Test 1: Get Garlic Flavor Molecules ---")
    garlic_data = api.get_ingredient_flavor_profile("garlic")
    print(f"Garlic has {garlic_data['molecule_count']} flavor molecules")
    if garlic_data['molecules']:
        print(f"Sample molecule: {garlic_data['molecules'][0]}")
    
    # Test 2: Get molecules for tomato
    print("\n--- Test 2: Get Tomato Flavor Molecules ---")
    tomato_data = api.get_ingredient_flavor_profile("tomato")
    print(f"Tomato has {tomato_data['molecule_count']} flavor molecules")
    
    # Test 3: Get molecules with fruity profile
    print("\n--- Test 3: Get Fruity Profile Molecules ---")
    fruity_molecules = api.get_molecules_by_flavor_profile("fruity")
    print(f"Found {len(fruity_molecules)} fruity molecules")
    
    # Test 4: Get molecules by functional group
    print("\n--- Test 4: Get Alcohol Group Molecules ---")
    alcohol_molecules = api.get_molecules_by_functional_groups("alcohol")
    print(f"Found {len(alcohol_molecules)} alcohol-based molecules")
    
    print("\n" + "="*50)
    print("✅ FLAVORDB API TESTS COMPLETE")
    print("="*50 + "\n")


if __name__ == "__main__":
    test_flavordb_api()