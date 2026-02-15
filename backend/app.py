import os
os.environ["FLASK_SKIP_DOTENV"] = "1"

from dotenv import load_dotenv
load_dotenv()

import requests
import random
from flask import Flask, jsonify, request, session
from flask_cors import CORS

from auth import auth_bp, login_required
from services.recipedb_api import RecipeDBAPI
from services.flavordb_api import FlavorDBAPI

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Enable CORS with credentials
CORS(app,
     origins=["http://localhost:5175", "http://localhost:5174", "http://localhost:5173", "http://localhost:3000"],
     supports_credentials=True)

# Register authentication blueprint
app.register_blueprint(auth_bp)

# Initialize API services
recipe_api = RecipeDBAPI()
flavor_api = FlavorDBAPI()


# ---------- RECIPE ENDPOINTS ----------

@app.route("/api/recipes/search")
def search_recipes():
    """Search recipes by ingredients (comma-separated)"""
    ingredients = request.args.get("ingredients", "")
    ingredient_list = [i.strip() for i in ingredients.split(",") if i.strip()]

    if not ingredient_list:
        return jsonify({"error": "No ingredients provided"}), 400

    recipes = recipe_api.search_by_ingredients(ingredient_list)
    return jsonify({"recipes": recipes, "count": len(recipes)})


@app.route("/api/recipes/by-diet")
def recipes_by_diet():
    """Get recipes filtered by diet type"""
    diet = request.args.get("diet", "")
    if not diet:
        return jsonify({"error": "No diet type provided"}), 400

    recipes = recipe_api.get_recipes_by_diet(diet)
    return jsonify({"recipes": recipes, "count": len(recipes)})


@app.route("/api/recipes/by-cuisine")
def recipes_by_cuisine():
    """Get recipes by cuisine"""
    cuisine = request.args.get("cuisine", "")
    if not cuisine:
        return jsonify({"error": "No cuisine provided"}), 400

    recipes = recipe_api.get_recipes_by_cuisine(cuisine)
    return jsonify({"recipes": recipes, "count": len(recipes)})


@app.route("/api/recipes/all")
def all_recipes():
    """Get paginated recipes"""
    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit", 10))
    recipes = recipe_api.get_all_recipes(page=page, limit=limit)
    return jsonify({"recipes": recipes, "count": len(recipes)})


@app.route("/api/recipes/nutrition/<recipe_id>")
def recipe_nutrition(recipe_id):
    """Get nutrition info for a recipe"""
    nutrition = recipe_api.get_nutrition_info(recipe_id)
    micro = recipe_api.get_micro_nutrition_info(recipe_id)
    return jsonify({"nutrition": nutrition, "micronutrients": micro})


# ---------- FLAVOR ENDPOINTS ----------

@app.route("/api/flavor/profile/<ingredient>")
def flavor_profile(ingredient):
    """Get flavor profile for an ingredient"""
    data = flavor_api.get_ingredient_flavor_profile(ingredient)
    return jsonify(data)


@app.route("/api/flavor/by-profile")
def flavor_by_profile():
    """Get molecules by flavor profile"""
    profile = request.args.get("profile", "")
    if not profile:
        return jsonify({"error": "No profile provided"}), 400

    molecules = flavor_api.get_molecules_by_flavor_profile(profile)
    return jsonify({"molecules": molecules, "count": len(molecules)})


@app.route("/api/flavor/compute")
def compute_flavor():
    """Compute aggregate flavor profile for ingredients"""
    ingredients = request.args.get("ingredients", "")
    ingredient_list = [i.strip() for i in ingredients.split(",") if i.strip()]

    if not ingredient_list:
        return jsonify({"error": "No ingredients provided"}), 400

    profile = flavor_api.compute_flavor_profile(ingredient_list)
    pairings = flavor_api.get_flavor_pairings(ingredient_list)

    return jsonify({
        "ingredients": ingredient_list,
        "flavor_profile": profile,
        "pairings": pairings
    })


# ---------- RECOMMENDATION ENGINE ----------

# Predefined recipe templates for robust results
RECIPE_TEMPLATES = [
    {
        "title": "Lentil & Spinach Dal",
        "cuisine": "Indian",
        "region": "North Indian",
        "description": "A hearty and nutritious lentil dal enriched with fresh spinach, tempered with aromatic spices.",
        "cook_time": 35,
        "servings": 4,
        "ingredients": ["lentil", "spinach", "onion", "tomato", "garlic", "ginger", "cumin", "turmeric"],
        "calories": 280,
        "protein": 18,
        "carbs": 42,
        "fat": 4,
        "fiber": 12,
        "micronutrients": ["Iron", "Folate", "Vitamin A", "Vitamin C", "Magnesium", "Potassium"],
        "diet_tags": ["Vegetarian", "Vegan", "High Protein", "Low Fat", "Gluten-Free"],
        "health_tags": ["Diabetic-Friendly", "Heart Health", "High Energy"],
    },
    {
        "title": "Paneer Tikka Masala",
        "cuisine": "Indian",
        "region": "Punjabi",
        "description": "Succulent tandoor-grilled paneer cubes in a rich, creamy tomato-based gravy with aromatic spices.",
        "cook_time": 45,
        "servings": 4,
        "ingredients": ["paneer", "tomato", "onion", "capsicum", "garlic", "ginger", "cream", "cumin"],
        "calories": 380,
        "protein": 22,
        "carbs": 18,
        "fat": 24,
        "fiber": 4,
        "micronutrients": ["Calcium", "Vitamin A", "Phosphorus", "Vitamin B12", "Riboflavin"],
        "diet_tags": ["Vegetarian", "High Protein", "Keto"],
        "health_tags": ["Muscle Gain", "Skin Health"],
    },
    {
        "title": "Vegetable Biryani",
        "cuisine": "Indian",
        "region": "South Indian",
        "description": "Fragrant basmati rice layered with seasonal vegetables, saffron, and whole spices.",
        "cook_time": 60,
        "servings": 6,
        "ingredients": ["rice", "carrot", "potato", "cauliflower", "onion", "tomato", "cumin", "coriander"],
        "calories": 320,
        "protein": 8,
        "carbs": 58,
        "fat": 6,
        "fiber": 6,
        "micronutrients": ["Vitamin A", "Vitamin C", "Iron", "Potassium", "Manganese"],
        "diet_tags": ["Vegetarian", "Vegan", "Low Fat"],
        "health_tags": ["High Energy", "Light Digestive"],
    },
    {
        "title": "Mushroom Stir-fry",
        "cuisine": "Indian",
        "region": "Bengali",
        "description": "Quick stir-fried mushrooms with garlic, bell peppers, and a hint of soy sauce.",
        "cook_time": 15,
        "servings": 2,
        "ingredients": ["mushroom", "capsicum", "garlic", "onion", "ginger", "soy sauce"],
        "calories": 120,
        "protein": 8,
        "carbs": 10,
        "fat": 6,
        "fiber": 3,
        "micronutrients": ["Vitamin D", "Selenium", "Niacin", "Potassium", "Copper"],
        "diet_tags": ["Vegetarian", "Vegan", "Low Carb", "Low Fat", "Keto", "Gluten-Free"],
        "health_tags": ["Weight Loss", "Diabetic Control", "Immune Boost"],
    },
    {
        "title": "Aloo Gobi",
        "cuisine": "Indian",
        "region": "Punjabi",
        "description": "Classic dry-cooked potato and cauliflower curry with turmeric and cumin seeds.",
        "cook_time": 30,
        "servings": 4,
        "ingredients": ["potato", "cauliflower", "onion", "tomato", "turmeric", "cumin", "coriander", "ginger"],
        "calories": 200,
        "protein": 5,
        "carbs": 35,
        "fat": 6,
        "fiber": 6,
        "micronutrients": ["Vitamin C", "Vitamin B6", "Potassium", "Manganese", "Folate"],
        "diet_tags": ["Vegetarian", "Vegan", "Gluten-Free"],
        "health_tags": ["Light Digestive", "High Energy"],
    },
    {
        "title": "Chana Masala",
        "cuisine": "Indian",
        "region": "North Indian",
        "description": "Spiced chickpea curry in a tangy tomato-onion gravy with warming spices.",
        "cook_time": 40,
        "servings": 4,
        "ingredients": ["chickpea", "tomato", "onion", "garlic", "ginger", "cumin", "coriander", "chili"],
        "calories": 310,
        "protein": 15,
        "carbs": 48,
        "fat": 6,
        "fiber": 14,
        "micronutrients": ["Iron", "Folate", "Manganese", "Phosphorus", "Zinc", "Vitamin B6"],
        "diet_tags": ["Vegetarian", "Vegan", "High Protein", "Gluten-Free"],
        "health_tags": ["Muscle Gain", "Heart Health", "High Energy", "Diabetic Control"],
    },
    {
        "title": "Palak Paneer",
        "cuisine": "Indian",
        "region": "North Indian",
        "description": "Creamy spinach puree with soft paneer cubes, seasoned with garlic and aromatic spices.",
        "cook_time": 35,
        "servings": 4,
        "ingredients": ["spinach", "paneer", "onion", "garlic", "ginger", "tomato", "cream", "cumin"],
        "calories": 300,
        "protein": 18,
        "carbs": 12,
        "fat": 20,
        "fiber": 6,
        "micronutrients": ["Iron", "Calcium", "Vitamin A", "Vitamin K", "Folate", "Vitamin C"],
        "diet_tags": ["Vegetarian", "High Protein", "Low Carb"],
        "health_tags": ["Muscle Gain", "Skin Health", "Immune Boost"],
    },
    {
        "title": "Mixed Vegetable Curry",
        "cuisine": "Indian",
        "region": "South Indian",
        "description": "A medley of seasonal vegetables simmered in a coconut-based curry with curry leaves.",
        "cook_time": 30,
        "servings": 4,
        "ingredients": ["carrot", "potato", "broccoli", "capsicum", "onion", "tomato", "coconut milk"],
        "calories": 220,
        "protein": 6,
        "carbs": 28,
        "fat": 10,
        "fiber": 8,
        "micronutrients": ["Vitamin A", "Vitamin C", "Vitamin K", "Potassium", "Iron"],
        "diet_tags": ["Vegetarian", "Vegan", "Gluten-Free"],
        "health_tags": ["Weight Loss", "Light Digestive", "Heart Health"],
    },
    {
        "title": "Tandoori Vegetable Kebab",
        "cuisine": "Indian",
        "region": "North Indian",
        "description": "Marinated mixed vegetables grilled tandoori-style with yogurt and aromatic spices.",
        "cook_time": 25,
        "servings": 4,
        "ingredients": ["capsicum", "onion", "mushroom", "paneer", "tomato", "garlic", "ginger"],
        "calories": 180,
        "protein": 12,
        "carbs": 14,
        "fat": 9,
        "fiber": 4,
        "micronutrients": ["Vitamin C", "Calcium", "Iron", "Vitamin B12", "Selenium"],
        "diet_tags": ["Vegetarian", "High Protein", "Low Carb"],
        "health_tags": ["Weight Loss", "Muscle Gain", "Skin Health"],
    },
    {
        "title": "Cabbage Poriyal",
        "cuisine": "Indian",
        "region": "South Indian",
        "description": "A simple, quick South Indian stir-fry of shredded cabbage with mustard seeds and coconut.",
        "cook_time": 15,
        "servings": 3,
        "ingredients": ["cabbage", "onion", "coconut", "mustard seeds", "curry leaves", "chili"],
        "calories": 110,
        "protein": 3,
        "carbs": 12,
        "fat": 6,
        "fiber": 4,
        "micronutrients": ["Vitamin C", "Vitamin K", "Folate", "Manganese"],
        "diet_tags": ["Vegetarian", "Vegan", "Low Carb", "Gluten-Free", "Low Fat"],
        "health_tags": ["Weight Loss", "Light Digestive", "Diabetic Control"],
    },
    {
        "title": "Broccoli & Garlic Stir-fry",
        "cuisine": "Indian",
        "region": "Maharashtrian",
        "description": "Crisp broccoli florets tossed with golden garlic, sesame seeds, and a touch of soy.",
        "cook_time": 12,
        "servings": 2,
        "ingredients": ["broccoli", "garlic", "onion", "capsicum", "sesame", "soy sauce"],
        "calories": 130,
        "protein": 7,
        "carbs": 12,
        "fat": 6,
        "fiber": 5,
        "micronutrients": ["Vitamin C", "Vitamin K", "Folate", "Chromium", "Sulforaphane"],
        "diet_tags": ["Vegetarian", "Vegan", "Low Carb", "Gluten-Free", "Keto"],
        "health_tags": ["Weight Loss", "Immune Boost", "Liver Care", "Diabetic Control"],
    },
    {
        "title": "Carrot Halwa",
        "cuisine": "Indian",
        "region": "Punjabi",
        "description": "A classic Indian dessert of grated carrots slow-cooked in milk with cardamom and nuts.",
        "cook_time": 50,
        "servings": 6,
        "ingredients": ["carrot", "milk", "sugar", "cardamom", "ghee", "cashew"],
        "calories": 350,
        "protein": 6,
        "carbs": 52,
        "fat": 14,
        "fiber": 3,
        "micronutrients": ["Vitamin A", "Calcium", "Vitamin D", "Potassium"],
        "diet_tags": ["Vegetarian"],
        "health_tags": ["High Energy", "Skin Health"],
    },
]

# Period-friendly recipe templates
PERIOD_RECIPES = [
    {
        "title": "Iron-Boost Spinach & Beetroot Soup",
        "cuisine": "Indian", "region": "North Indian",
        "description": "A warm, iron-rich soup that helps replenish what your body loses during menstruation.",
        "cook_time": 25, "servings": 2,
        "ingredients": ["spinach", "beetroot", "tomato", "garlic", "ginger", "cumin"],
        "calories": 150, "protein": 8, "carbs": 22, "fat": 3, "fiber": 7,
        "micronutrients": ["Iron", "Folate", "Vitamin C", "Magnesium"],
        "diet_tags": ["Vegetarian", "Vegan", "Low Fat", "Gluten-Free"],
        "health_tags": ["Period-Friendly", "Iron-Rich", "Anti-Inflammatory"],
    },
    {
        "title": "Dark Chocolate & Banana Smoothie Bowl",
        "cuisine": "Indian", "region": "Modern Fusion",
        "description": "Satisfies chocolate cravings with magnesium-rich dark cacao and potassium-loaded banana.",
        "cook_time": 10, "servings": 1,
        "ingredients": ["banana", "cacao", "oats", "almond milk", "honey"],
        "calories": 320, "protein": 10, "carbs": 52, "fat": 10, "fiber": 8,
        "micronutrients": ["Magnesium", "Potassium", "Iron", "Vitamin B6"],
        "diet_tags": ["Vegetarian", "High Energy"],
        "health_tags": ["Period-Friendly", "Craving Satisfier", "Mood Boost"],
    },
    {
        "title": "Turmeric Ginger Anti-Cramp Tea",
        "cuisine": "Indian", "region": "Ayurvedic",
        "description": "A warming anti-inflammatory drink that helps ease menstrual cramps naturally.",
        "cook_time": 8, "servings": 1,
        "ingredients": ["turmeric", "ginger", "cinnamon", "honey", "black pepper"],
        "calories": 45, "protein": 1, "carbs": 10, "fat": 1, "fiber": 1,
        "micronutrients": ["Curcumin", "Gingerol", "Iron", "Manganese"],
        "diet_tags": ["Vegetarian", "Vegan", "Low Calorie"],
        "health_tags": ["Period-Friendly", "Anti-Inflammatory", "Cramp Relief"],
    },
]

# Stress-friendly recipe templates
STRESS_RECIPES = [
    {
        "title": "Gentle Khichdi",
        "cuisine": "Indian", "region": "Ayurvedic",
        "description": "The ultimate comfort food — easy to digest, warm, and grounding. Perfect when appetite is low.",
        "cook_time": 25, "servings": 2,
        "ingredients": ["rice", "moong dal", "ghee", "cumin", "turmeric", "ginger"],
        "calories": 220, "protein": 10, "carbs": 38, "fat": 4, "fiber": 5,
        "micronutrients": ["Iron", "Zinc", "Magnesium", "B Vitamins"],
        "diet_tags": ["Vegetarian", "Gluten-Free", "Low Fat"],
        "health_tags": ["Stress-Friendly", "Light Digestive", "Comfort Food"],
    },
    {
        "title": "Warm Banana Oatmeal",
        "cuisine": "Indian", "region": "Modern Fusion",
        "description": "Soft, warm, and mildly sweet oatmeal that's easy to eat even with no appetite.",
        "cook_time": 10, "servings": 1,
        "ingredients": ["oats", "banana", "milk", "cinnamon", "honey"],
        "calories": 280, "protein": 8, "carbs": 48, "fat": 6, "fiber": 6,
        "micronutrients": ["Tryptophan", "Vitamin B6", "Magnesium", "Potassium"],
        "diet_tags": ["Vegetarian", "Low Fat"],
        "health_tags": ["Stress-Friendly", "Mood Boost", "Light Digestive"],
    },
]

# Pet toxic ingredients database
PET_TOXIC_FOODS = {
    "dog": ["chocolate", "grapes", "raisins", "onion", "garlic", "xylitol", "macadamia", "avocado", "alcohol", "caffeine"],
    "cat": ["onion", "garlic", "chocolate", "grapes", "raisins", "caffeine", "alcohol", "xylitol"],
    "bird": ["avocado", "chocolate", "caffeine", "onion", "garlic", "alcohol", "mushroom", "salt"],
    "rabbit": ["chocolate", "avocado", "onion", "garlic", "potato", "rhubarb", "bread", "pasta"],
}

# Community meals sample data
COMMUNITY_MEALS = [
    {"id": 1, "restaurant": "Green Bowl Kitchen", "items": ["Dal Makhani", "Jeera Rice", "Mixed Raita"], "servings": 12, "expiresIn": "3 hours", "location": "Sector 15, Noida", "price": 30, "tags": ["Vegetarian", "High Protein"]},
    {"id": 2, "restaurant": "Spice Garden Cafe", "items": ["Paneer Butter Masala", "Naan", "Green Salad"], "servings": 8, "expiresIn": "2 hours", "location": "Connaught Place, Delhi", "price": 45, "tags": ["Vegetarian"]},
    {"id": 3, "restaurant": "Fresh Bites Tiffin", "items": ["Rajma Chawal", "Pickle", "Buttermilk"], "servings": 20, "expiresIn": "4 hours", "location": "Lajpat Nagar, Delhi", "price": 25, "tags": ["Vegan Option", "Budget"]},
]


def score_recipe(recipe, user_inputs):
    """
    Score a recipe based on user inputs.
    Returns a score 0-100 and detailed breakdown.
    """
    score = 0
    max_score = 0
    breakdown = {}

    # 1. Ingredient match (40 points)
    max_score += 40
    user_ingredients = set(i.lower() for i in user_inputs.get("ingredients", []))
    recipe_ingredients = set(i.lower() for i in recipe.get("ingredients", []))
    if user_ingredients and recipe_ingredients:
        overlap = user_ingredients & recipe_ingredients
        ingredient_score = (len(overlap) / max(len(user_ingredients), 1)) * 40
    else:
        ingredient_score = 20
    score += ingredient_score
    breakdown["ingredient_match"] = round(ingredient_score / 40 * 100)

    # 2. Diet match (20 points)
    max_score += 20
    user_diets = set(i.lower() for i in user_inputs.get("diet", []))
    recipe_diets = set(i.lower() for i in recipe.get("diet_tags", []))
    if user_diets:
        diet_overlap = sum(1 for d in user_diets if any(d in rd for rd in recipe_diets))
        diet_score = (diet_overlap / max(len(user_diets), 1)) * 20
    else:
        diet_score = 15
    score += diet_score
    breakdown["diet_match"] = round(diet_score / 20 * 100)

    # 3. Goal match (15 points)
    max_score += 15
    user_goals = set(i.lower() for i in user_inputs.get("goals", []))
    recipe_health = set(i.lower() for i in recipe.get("health_tags", []))
    if user_goals:
        goal_overlap = sum(1 for g in user_goals if any(g in rh for rh in recipe_health))
        goal_score = (goal_overlap / max(len(user_goals), 1)) * 15
    else:
        goal_score = 10
    score += goal_score
    breakdown["goal_match"] = round(goal_score / 15 * 100)

    # 4. Cuisine match (10 points)
    max_score += 10
    user_cuisines = set(i.lower() for i in user_inputs.get("cuisine", []))
    recipe_region = recipe.get("region", "").lower()
    if user_cuisines:
        cuisine_match = any(c in recipe_region for c in user_cuisines) or "no preference" in user_cuisines
        cuisine_score = 10 if cuisine_match else 3
    else:
        cuisine_score = 7
    score += cuisine_score
    breakdown["cuisine_match"] = round(cuisine_score / 10 * 100)

    # 5. Advanced filters (15 points)
    max_score += 15
    advanced = user_inputs.get("advanced", {})
    adv_score = 15  # Start with full, subtract for violations

    # Calorie range
    cal_range = advanced.get("calorieRange", [0, 2000])
    if isinstance(cal_range, list) and len(cal_range) == 2:
        if not (cal_range[0] <= recipe.get("calories", 300) <= cal_range[1]):
            adv_score -= 5

    # Protein range
    prot_range = advanced.get("proteinRange", [0, 100])
    if isinstance(prot_range, list) and len(prot_range) == 2:
        if not (prot_range[0] <= recipe.get("protein", 10) <= prot_range[1]):
            adv_score -= 4

    # Cook time
    max_time = advanced.get("maxCookTime", 180)
    if recipe.get("cook_time", 30) > max_time:
        adv_score -= 4

    # Excluded ingredients
    excluded = set(i.lower() for i in advanced.get("excludeIngredients", []))
    if excluded & recipe_ingredients:
        adv_score -= 10

    score += max(0, adv_score)
    breakdown["advanced_match"] = round(max(0, adv_score) / 15 * 100)

    # 6. Special mode scoring (10 bonus points)
    mode = user_inputs.get("specialMode")
    mode_score = 0
    if mode == "period":
        period_tags = {"period-friendly", "iron-rich", "anti-inflammatory", "cramp relief", "mood boost"}
        if period_tags & recipe_health:
            mode_score = 10
        elif {"iron", "magnesium", "vitamin c"} & set(n.lower() for n in recipe.get("micronutrients", [])):
            mode_score = 7
        # Penalize bloating triggers
        bloat_triggers = {"chickpea", "broccoli", "cabbage", "cauliflower"}
        period_data = user_inputs.get("periodData", {})
        if "bloating" in period_data.get("symptoms", []) and bloat_triggers & recipe_ingredients:
            mode_score -= 5
    elif mode == "stress":
        stress_tags = {"stress-friendly", "light digestive", "comfort food", "mood boost"}
        if stress_tags & recipe_health:
            mode_score = 10
        stress_data = user_inputs.get("stressData", {})
        if stress_data.get("appetite") in ["none", "very_low"]:
            if recipe.get("cook_time", 30) <= 15:
                mode_score += 3
            if recipe.get("calories", 300) <= 250:
                mode_score += 2
    elif mode == "pet":
        pet_data = user_inputs.get("petData", {})
        pet_type = pet_data.get("petType")
        if pet_type and pet_data.get("filterEnabled", True):
            toxic = set(PET_TOXIC_FOODS.get(pet_type, []))
            if toxic & recipe_ingredients:
                mode_score = -20  # Heavily penalize toxic recipes
            else:
                mode_score = 8
    elif mode == "medical":
        med_data = user_inputs.get("medicalData", {})
        restrictions = [r.lower() for r in med_data.get("restrictions", [])]
        for r in restrictions:
            if "low fat" in r and recipe.get("fat", 10) > 15:
                mode_score -= 5
            if "low sodium" in r:
                mode_score -= 2
            if "low glycemic" in r and recipe.get("carbs", 30) > 40:
                mode_score -= 5

    score += mode_score
    breakdown["mode_match"] = max(0, min(100, 50 + mode_score * 5))

    # Normalize to 0-100
    final_score = round((score / (max_score + 10)) * 100) if max_score > 0 else 50

    # Add slight randomness for variety (±3 points)
    final_score = max(10, min(99, final_score + random.randint(-3, 3)))

    return final_score, breakdown


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    Main recommendation endpoint.
    Accepts all user inputs, scores recipes, enriches with flavor data.
    """
    data = request.get_json() or {}

    ingredients = data.get("ingredients", [])
    diet = data.get("diet", [])
    goals = data.get("goals", [])
    cuisine = data.get("cuisine", [])
    style = data.get("style", [])
    advanced = data.get("advanced", {})
    special_mode = data.get("specialMode")

    user_inputs = {
        "ingredients": ingredients,
        "diet": diet,
        "goals": goals,
        "cuisine": cuisine,
        "style": style,
        "advanced": advanced,
        "specialMode": special_mode,
        "periodData": data.get("periodData", {}),
        "medicalData": data.get("medicalData", {}),
        "petData": data.get("petData", {}),
        "stressData": data.get("stressData", {}),
        "doctorData": data.get("doctorData", {}),
    }

    # --- Fetch recipes from API ---
    api_recipes = []
    try:
        if ingredients:
            api_recipes = recipe_api.search_by_ingredients(ingredients[:5])
        if not api_recipes and cuisine:
            api_recipes = recipe_api.get_recipes_by_cuisine(cuisine[0])
        if not api_recipes and diet:
            api_recipes = recipe_api.get_recipes_by_diet(diet[0])
        if not api_recipes:
            api_recipes = recipe_api.get_all_recipes(page=0, limit=15)
    except Exception as e:
        print(f"⚠️ API fetch error: {e}")

    # --- Merge with template recipes for robustness ---
    all_recipes = list(RECIPE_TEMPLATES)

    # Inject mode-specific templates
    if special_mode == "period":
        all_recipes.extend(PERIOD_RECIPES)
    elif special_mode == "stress":
        all_recipes.extend(STRESS_RECIPES)

    # Convert API recipes to our format
    for r in api_recipes[:10]:
        template = {
            "title": r.get("title") or r.get("Recipe_title") or r.get("name", "Unknown Recipe"),
            "cuisine": r.get("cuisine") or r.get("Cuisine", "Indian"),
            "region": r.get("region") or r.get("Region") or r.get("Sub_region", ""),
            "description": r.get("description") or r.get("instructions", "")[:150] or "A delicious recipe from RecipeDB",
            "cook_time": r.get("cook_time") or r.get("Total_time") or 30,
            "servings": r.get("servings") or r.get("Servings") or 4,
            "ingredients": r.get("ingredients") or [],
            "calories": r.get("calories") or r.get("Calories") or 250,
            "protein": r.get("protein") or r.get("Protein") or 10,
            "carbs": r.get("carbs") or r.get("Carbohydrate") or 30,
            "fat": r.get("fat") or r.get("Total_fat") or 8,
            "fiber": r.get("fiber") or r.get("Dietary_fiber") or 4,
            "micronutrients": ["Vitamin A", "Vitamin C", "Iron", "Calcium"],
            "diet_tags": r.get("diet_tags", ["Vegetarian"]),
            "health_tags": r.get("health_tags", ["High Energy"]),
        }
        all_recipes.append(template)

    # --- Score all recipes ---
    scored = []
    for recipe in all_recipes:
        score, breakdown = score_recipe(recipe, user_inputs)
        scored.append({
            **recipe,
            "score": score,
            "breakdown": breakdown,
        })

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    # Take top 8
    top_recipes = scored[:8]

    # --- Compute flavor profiles ---
    all_recipe_ingredients = set()
    for r in top_recipes:
        all_recipe_ingredients.update(r.get("ingredients", []))

    # Compute overall flavor profile from user's ingredients
    flavor_ingredients = ingredients if ingredients else list(all_recipe_ingredients)[:5]
    overall_flavor = flavor_api.compute_flavor_profile(flavor_ingredients)

    # Compute per-recipe flavor profiles
    for recipe in top_recipes:
        recipe_ingrs = recipe.get("ingredients", [])[:5]
        if recipe_ingrs:
            recipe["flavor_profile"] = flavor_api.compute_flavor_profile(recipe_ingrs)
        else:
            recipe["flavor_profile"] = overall_flavor

    # --- Flavor pairings ---
    pairings = flavor_api.get_flavor_pairings(flavor_ingredients)

    # --- Similar recipes (next 4 after top 8) ---
    similar = scored[8:12] if len(scored) > 8 else []
    for s in similar:
        s_ingrs = s.get("ingredients", [])[:3]
        if s_ingrs:
            s["flavor_profile"] = flavor_api.compute_flavor_profile(s_ingrs)
        else:
            s["flavor_profile"] = overall_flavor

    # --- Build response ---
    response = {
        "recipes": top_recipes,
        "total_results": len(scored),
        "overall_flavor_profile": overall_flavor,
        "flavor_pairings": pairings,
        "similar_recipes": similar,
        "user_inputs_summary": {
            "ingredients": len(ingredients),
            "diets": diet,
            "goals": goals,
            "cuisines": cuisine,
        },
    }

    return jsonify(response)


# ---------- MODE-SPECIFIC ENDPOINTS ----------

@app.route("/api/pet/toxic-foods/<pet_type>")
def pet_toxic_foods(pet_type):
    """Get toxic foods list for a pet type"""
    toxic = PET_TOXIC_FOODS.get(pet_type.lower(), [])
    return jsonify({"pet_type": pet_type, "toxic_foods": toxic})


@app.route("/api/community/meals")
def community_meals():
    """Get available community meals"""
    return jsonify({"meals": COMMUNITY_MEALS, "count": len(COMMUNITY_MEALS)})


@app.route("/api/community/list", methods=["POST"])
def list_surplus():
    """List surplus food from a restaurant"""
    data = request.get_json() or {}
    # In production, save to database
    return jsonify({"status": "listed", "message": "Surplus food listed successfully"})


@app.route("/api/medical/parse-qr", methods=["POST"])
def parse_medical_qr():
    """Parse medical report QR code data"""
    data = request.get_json() or {}
    # Simulated parsing — in production, decode QR and extract data
    conditions_map = {
        "diabetes": {"restrictions": ["Low Glycemic Index", "No Added Sugar"], "nutrients": ["Chromium", "Magnesium", "Fiber"]},
        "hypertension": {"restrictions": ["Low Sodium", "No Processed Foods"], "nutrients": ["Potassium", "Calcium", "Omega-3"]},
        "cholesterol": {"restrictions": ["Low Saturated Fat", "High Fiber"], "nutrients": ["Omega-3", "Soluble Fiber"]},
    }
    qr_data = data.get("qr_data", "").lower()
    for condition, info in conditions_map.items():
        if condition in qr_data:
            return jsonify({"condition": condition, **info})
    return jsonify({"condition": "general", "restrictions": [], "nutrients": []})


# ---------- LEGACY TEST ROUTES ----------

@app.route("/test-recipedb")
def test_recipedb():
    recipes = recipe_api.get_all_recipes(limit=5)
    return jsonify({"recipes": recipes})

@app.route("/test-flavordb")
def test_flavordb():
    profile = flavor_api.get_ingredient_flavor_profile("garlic")
    return jsonify(profile)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
