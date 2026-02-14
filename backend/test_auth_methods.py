"""
Test different authentication methods to find which one works
"""

import requests
from config import API_KEY, RECIPEDB_BASE_URL, FLAVORDB_BASE_URL

print("\n" + "="*70)
print("🔍 TESTING AUTHENTICATION METHODS")
print("="*70)
print(f"API Key: {API_KEY[:15]}..." if API_KEY else "❌ No API key found")
print()

def test_auth_method(url, method_name, headers=None, params=None):
    """Test a specific authentication method"""
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  ✅ SUCCESS - Valid JSON response")
                print(f"  Keys: {list(data.keys())[:3]}")
                return True
            except:
                print(f"  ⚠️ Response is not JSON")
                return False
        elif response.status_code == 401:
            print(f"  ❌ UNAUTHORIZED - Wrong auth method")
            return False
        elif response.status_code == 403:
            print(f"  ❌ FORBIDDEN - API key might be invalid")
            return False
        else:
            print(f"  ⚠️ Unexpected status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"  ❌ TIMEOUT")
        return False
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)[:50]}")
        return False

# ==================== TEST RECIPEDB ====================

print("📦 TESTING RECIPEDB")
print("-" * 70)

test_url = f"{RECIPEDB_BASE_URL}/recipes/recipesinfo?limit=5"

# Method 1: Authorization Header
print("\n1️⃣ Method: Authorization Header (Bearer token)")
success_1 = test_auth_method(
    test_url,
    "header",
    headers={"Authorization": f"Bearer {API_KEY}"}
)

# Method 2: API Key in Query Parameter
print("\n2️⃣ Method: Query Parameter (?api_key=...)")
success_2 = test_auth_method(
    test_url,
    "param",
    params={"api_key": API_KEY}
)

# Method 3: No Authentication
print("\n3️⃣ Method: No Authentication (public endpoint)")
success_3 = test_auth_method(
    test_url,
    "none"
)

# Determine best method for RecipeDB
if success_1:
    recipedb_method = "header"
    print("\n✅ RecipeDB works with: Authorization Header")
elif success_2:
    recipedb_method = "param"
    print("\n✅ RecipeDB works with: Query Parameter")
elif success_3:
    recipedb_method = "none"
    print("\n✅ RecipeDB is public (no auth needed)")
else:
    recipedb_method = None
    print("\n❌ RecipeDB: No working auth method found")

# ==================== TEST FLAVORDB ====================

print("\n" + "="*70)
print("🧬 TESTING FLAVORDB")
print("-" * 70)

test_url = f"{FLAVORDB_BASE_URL}/molecules_data/by-commonName?name=garlic"

# Method 1: Authorization Header
print("\n1️⃣ Method: Authorization Header (Bearer token)")
success_1 = test_auth_method(
    test_url,
    "header",
    headers={"Authorization": f"Bearer {API_KEY}"}
)

# Method 2: API Key in Query Parameter  
print("\n2️⃣ Method: Query Parameter (?api_key=...)")
success_2 = test_auth_method(
    test_url,
    "param",
    params={"name": "garlic", "api_key": API_KEY}
)

# Method 3: No Authentication
print("\n3️⃣ Method: No Authentication (public endpoint)")
success_3 = test_auth_method(
    test_url,
    "none",
    params={"name": "garlic"}
)

# Determine best method for FlavorDB
if success_1:
    flavordb_method = "header"
    print("\n✅ FlavorDB works with: Authorization Header")
elif success_2:
    flavordb_method = "param"
    print("\n✅ FlavorDB works with: Query Parameter")
elif success_3:
    flavordb_method = "none"
    print("\n✅ FlavorDB is public (no auth needed)")
else:
    flavordb_method = None
    print("\n❌ FlavorDB: No working auth method found")

# ==================== SUMMARY ====================

print("\n" + "="*70)
print("📋 AUTHENTICATION SUMMARY")
print("="*70)
print(f"RecipeDB: {recipedb_method or '❌ FAILED'}")
print(f"FlavorDB: {flavordb_method or '❌ FAILED'}")
print()

if recipedb_method and flavordb_method:
    print("✅ BOTH APIs WORKING!")
    print("\n📝 Next step: Update your API service files with the correct auth method")
    print(f"   - RecipeDB uses: {recipedb_method}")
    print(f"   - FlavorDB uses: {flavordb_method}")
else:
    print("⚠️ Some APIs are not working. Possible issues:")
    print("   1. API key might be invalid")
    print("   2. API endpoints might have changed")
    print("   3. APIs might be down")
    print("\n   Try contacting hackathon organizers on Discord/Slack")

print("\n" + "="*70)