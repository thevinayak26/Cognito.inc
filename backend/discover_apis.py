"""
Discover correct API endpoints
"""

import requests

API_KEY = "vApEsmdFGGTs-nLyeFTlpIrho2yGovDI3AWP0eExmGAuN0cQ"

print("\n" + "="*70)
print("🔍 DISCOVERING API ENDPOINTS")
print("="*70 + "\n")

# Test if the main websites load
sites = [
    "https://cosylab.iiitd.edu.in/recipedb",
    "https://cosylab.iiitd.edu.in/flavordb",
]

for site in sites:
    try:
        print(f"Testing: {site}")
        response = requests.get(site, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✅ Website is UP")
            # Check if it's an API or web interface
            content_type = response.headers.get('content-type', '')
            if 'json' in content_type:
                print(f"  📋 Returns JSON - this is an API!")
            elif 'html' in content_type:
                print(f"  🌐 Returns HTML - this is a web interface")
                print(f"  💡 Need to find the actual API endpoints")
        
        print()
    except Exception as e:
        print(f"  ❌ Error: {e}\n")

# Check for API documentation
docs_urls = [
    "https://cosylab.iiitd.edu.in/recipedb/api-docs",
    "https://cosylab.iiitd.edu.in/recipedb/docs",
    "https://cosylab.iiitd.edu.in/recipedb/swagger",
    "https://cosylab.iiitd.edu.in/flavordb/api-docs",
    "https://cosylab.iiitd.edu.in/flavordb/docs",
    "https://cosylab.iiitd.edu.in/flavordb/swagger",
]

print("="*70)
print("🔍 LOOKING FOR API DOCUMENTATION")
print("="*70 + "\n")

for url in docs_urls:
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ FOUND: {url}")
            print(f"   This might have API documentation!\n")
    except:
        pass

print("\n" + "="*70)
print("DISCOVERY COMPLETE")
print("="*70)
print("\n💡 NEXT STEPS:")
print("   1. Check the hackathon portal for API documentation")
print("   2. Ask organizers on Discord/Slack")
print("   3. Or use the web interface directly")