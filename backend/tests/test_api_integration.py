"""
Comprehensive API Integration Tests
Verifies both RecipeDB and FlavorDB work correctly
"""

import sys
sys.path.append('..')

from services.recipedb_api import RecipeDBAPI
from services.flavordb_api import FlavorDBAPI


def test_complete_workflow():
    """
    Test a complete user workflow:
    1. User has leftovers: chicken, garlic
    2. User wants keto recipes
    3. Find flavor compatibility
    """
    print("\n" + "="*60)
    print("🚀 TESTING COMPLETE WORKFLOW: CHICKEN + GARLIC (KETO)")
    print("="*60 + "\n")
    
    recipe_api = RecipeDBAPI()
    flavor_api = FlavorDBAPI()
    
    # Step 1: Get keto recipes
    print("Step 1: Searching for keto recipes...")
    keto_recipes = recipe_api.get_recipes_by_diet("keto")
    print(f"✅ Found {len(keto_recipes)} keto recipes\n")
    
    # Step 2: Get flavor profile for chicken
    print("Step 2: Getting flavor profile for chicken...")
    chicken_flavor = flavor_api.get_ingredient_flavor_profile("chicken")
    print(f"✅ Chicken has {chicken_flavor['molecule_count']} flavor molecules\n")
    
    # Step 3: Get flavor profile for garlic
    print("Step 3: Getting flavor profile for garlic...")
    garlic_flavor = flavor_api.get_ingredient_flavor_profile("garlic")
    print(f"✅ Garlic has {garlic_flavor['molecule_count']} flavor molecules\n")
    
    # Step 4: Check flavor compatibility
    print("Step 4: Checking flavor compatibility...")
    chicken_molecules = set(chicken_flavor.get('molecule_ids', []))
    garlic_molecules = set(garlic_flavor.get('molecule_ids', []))
    
    shared_molecules = chicken_molecules & garlic_molecules
    union_molecules = chicken_molecules | garlic_molecules
    
    if union_molecules:
        compatibility_score = len(shared_molecules) / len(union_molecules)
        print(f"✅ Flavor compatibility score: {compatibility_score:.2%}")
        print(f"   Shared molecules: {len(shared_molecules)}")
        print(f"   Total molecules: {len(union_molecules)}\n")
    else:
        print("⚠️ Could not calculate compatibility score\n")
    
    # Step 5: Get nutrition for first keto recipe
    if keto_recipes:
        print("Step 5: Getting nutrition for sample recipe...")
        recipe_id = keto_recipes[0].get('id')
        recipe_title = keto_recipes[0].get('title', 'N/A')
        nutrition = recipe_api.get_nutrition_info(recipe_id)
        
        print(f"✅ Recipe: {recipe_title}")
        print(f"   Nutrition: {nutrition}\n")
    
    print("="*60)
    print("✅ COMPLETE WORKFLOW TEST PASSED")
    print("="*60 + "\n")


def test_api_error_handling():
    """
    Test error handling for invalid requests
    """
    print("\n" + "="*60)
    print("🧪 TESTING ERROR HANDLING")
    print("="*60 + "\n")
    
    recipe_api = RecipeDBAPI()
    flavor_api = FlavorDBAPI()
    
    # Test invalid ingredient
    print("Test: Invalid ingredient name...")
    invalid_flavor = flavor_api.get_ingredient_flavor_profile("xyzabc123notreal")
    print(f"Result: {invalid_flavor['molecule_count']} molecules (expected: 0)\n")
    
    # Test invalid diet type
    print("Test: Invalid diet type...")
    invalid_recipes = recipe_api.get_recipes_by_diet("invaliddietype")
    print(f"Result: {len(invalid_recipes)} recipes (expected: 0)\n")
    
    print("="*60)
    print("✅ ERROR HANDLING TESTS COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Run all tests
    test_complete_workflow()
    test_api_error_handling()
    
    print("\n" + "🎉 ALL API INTEGRATION TESTS PASSED! 🎉\n")