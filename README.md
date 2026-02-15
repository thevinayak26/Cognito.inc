# NutriLogic: Flavor-Constrained Cuisine Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hackathon](https://img.shields.io/badge/Foodoscope-ForkIT%202025-orange.svg)](https://github.com)

> A computational gastronomy engine that transforms leftover ingredients into safe, personalized meal recommendations using molecular flavor science and nutritional intelligence.

**Built for:** Foodoscope ForkIT Challenge 2025
**Hosted by:** IIIT Delhi - CoSy Lab
**Website:** NutriLogic
**Presentation:** [Slides Link](https://www.canva.com/design/DAHAPoibNi4/BlUzHYm1l92CKV9yWty05Q/edit?utm_content=DAHAPoibNi4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

---

## Table of Contents

- [Overview](#overview)
- [Current Status](#current-status)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Scoring Model](#scoring-model)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Verified Test Case](#verified-test-case)
- [API Documentation](#api-documentation)
- [Roadmap](#roadmap)
- [Team](#team)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

**NutriLogic** is a constraint-based culinary optimization engine that goes beyond simple ingredient matching. By combining:

- Nutritional Intelligence (RecipeDB)
- Molecular Flavor Science (FlavorDB)
- Diet and Allergy Filtering
- Macro-based Scoring
- Cuisine-aware Flavor Alignment

We help users reduce food waste while ensuring meals are healthy, safe, and flavor-compatible.

### Why It Matters

- **30% of household food** goes to waste due to "ingredient paralysis"
- **48% of people with dietary restrictions** struggle to find safe recipes
- Traditional recipe apps ignore **molecular flavor compatibility**
- Health-conscious users need **macro-aware recommendations**

---

## Current Status

> **IMPORTANT:** Only the **Standard Mode** flow is fully functional at this time.
> Special modes (Period-Friendly, Stress Mode, Pet-Safe, Medical Report, Doctor Review, Community Kitchen) are available in the UI but have not been fully tested and may not produce reliable results.
>
> **Use the Standard Mode flow:** Landing -> Ingredients -> Health -> Goals -> Preferences -> Advanced -> Results

The external APIs (RecipeDB and FlavorDB hosted at cosylab.iiitd.edu) may be intermittently available. When they are unreachable, the system falls back to a built-in recipe database of 12+ Indian recipes with pre-computed flavor profiles. All core features (scoring, flavor radar charts, nutritional breakdown) work fully with the fallback data.

---

## Problem Statement

Users often have leftover ingredients but struggle to create meals that:

- Fit specific diets (Keto, High-Protein, Low-Carb, Vegan, etc.)
- Meet macro targets (protein, carbs, fat)
- Avoid allergens (dairy, gluten, nuts, etc.)
- Maintain good flavor compatibility
- Align with preferred cuisines

**Most existing platforms only match ingredients without considering:**
- Health constraints
- Molecular flavor science
- Personalized macro requirements
- Explainable recommendations

---

## Solution

Our system performs **multi-constraint optimization** through:

### 1. Ingredient Analysis
Accepts leftover ingredients and validates availability against a known ingredient database.

### 2. Hard Filtering
- **Diet Compliance:** Ensures recipes match selected diet (Keto, Vegan, etc.)
- **Allergen Safety:** Strictly excludes any allergen-containing recipes

### 3. Macro Validation
Validates recipes against user-specified macro targets:
- Calorie range constraints
- Protein range constraints
- Maximum cook time
- Excluded ingredients

### 4. Molecular Flavor Analysis
Uses FlavorDB to compute flavor compatibility across 8 dimensions:
- Sweet, Sour, Bitter, Salty, Umami, Spicy, Fruity, Smoky
- Generates per-recipe **Flavor Dimension Radar Charts**
- Falls back to built-in flavor profiles for 20+ common ingredients

### 5. Cuisine Alignment
Boosts scores for cuisine-typical flavor patterns:
- Punjabi, Bengali, South Indian, Gujarati, Maharashtrian, and more

### 6. Intelligent Ranking
Outputs optimized meal suggestions with **explainable score breakdowns**.

---

## Key Features

### Core Features

| Feature | Description |
|---------|-------------|
| Ingredient Input | Autocomplete ingredient entry from a database of 23 common ingredients |
| Diet Filtering | Keto, Vegan, Vegetarian, High-Protein, Low-Carb, Low-Fat, Gluten-Free, Diabetic-Friendly |
| Allergy Filtering | Dairy, Nuts, Gluten, Soy, Eggs, Shellfish, Fish |
| Health Goals | Muscle Gain, Weight Loss, Diabetic Control, Liver Care, High Energy, Light Digestive, Immune Boost, Skin Health |
| Cuisine Preference | Punjabi, Bengali, South Indian, Gujarati, Maharashtrian, Bihari, UP, No Preference |
| Cooking Style | Gravy, Dry, Roasted, Slow-cooked, Stir-fried, Steamed, Pressure-cooked, Tandoor |
| Advanced Filters | Calorie range, protein range, max cook time, spice tolerance, servings, excluded ingredients |
| Flavor Radar Chart | 8-dimension flavor profile visualization per recipe (Recharts) |
| Score Breakdown | Per-recipe explainable match percentages: Ingredient, Diet, Goal, Cuisine, Mode |
| Flavor Pairings | Suggestions to improve weak flavor dimensions |
| Similar Recipes | "You might also like" section with additional matches |

### Score Breakdown Example

Each recommendation includes a transparent score breakdown:

```
Overall Match: 77/100

  Ingredients Match:  75%  (3 of 4 ingredients overlapping)
  Diet Match:        100%  (Vegetarian + High Protein both satisfied)
  Goal Match:        100%  (Muscle Gain tags present)
  Cuisine Match:      30%  (North Indian region, Punjabi preferred)
  Advanced Match:    100%  (Within calorie, protein, and cook time limits)
```

---

## System Architecture

```
FRONTEND (React + Vite, port 5175)            BACKEND (Flask, port 5000)
+---------------------------------+            +-----------------------------------+
| Landing Page                    |            |                                   |
|   |                             |            |  POST /api/recommend              |
|   v                             |            |    |                               |
| Ingredients Step (Step 1 of 5)  |            |    +-- Fetch from RecipeDB API     |
|   |                             |   POST     |    |     (with fallback)           |
|   v                             | ---------> |    +-- Score all recipes           |
| Health Step (Step 2 of 5)       |            |    |     against user inputs       |
|   |                             |            |    +-- Compute flavor profiles     |
|   v                             |            |    |     via FlavorDB API          |
| Goals Step (Step 3 of 5)        |            |    |     (with built-in fallback)  |
|   |                             |            |    +-- Sort by score, return top 8 |
|   v                             |            |                                   |
| Preferences Step (Step 4 of 5)  |            |  GET /api/recipes/search          |
|   |                             |            |  GET /api/recipes/by-diet         |
|   v                             |            |  GET /api/recipes/by-cuisine      |
| Advanced Step (Step 5 of 5)     |            |  GET /api/flavor/profile/:name    |
|   |                             |            |  GET /api/flavor/compute          |
|   v                             |  <-------  |                                   |
| Results Page                    |   JSON     +-----------------------------------+
|   - Flavor Radar Chart          |
|   - Recipe Cards with Scores    |            External APIs:
|   - Nutrition Breakdown         |            - RecipeDB (cosylab.iiitd.edu)
|   - Flavor Pairings             |            - FlavorDB (cosylab.iiitd.edu.in:6969)
|   - Similar Recipes             |
+---------------------------------+
```

---

## Scoring Model

### Formula (100 points total)

```
Final Score = Ingredient Match (40 pts)
            + Diet Match (20 pts)
            + Goal Match (15 pts)
            + Cuisine Match (10 pts)
            + Advanced Filters (15 pts)
            + Mode Bonus (up to 10 bonus pts)
```

### Component Details

| Component | Max Points | How It Works |
|-----------|-----------|--------------|
| Ingredient Match | 40 | Overlap between user ingredients and recipe ingredients |
| Diet Match | 20 | How many of the user's selected diets match recipe diet tags |
| Goal Match | 15 | Overlap between user health goals and recipe health tags |
| Cuisine Match | 10 | Whether recipe region matches preferred cuisine |
| Advanced Filters | 15 | Penalties for violating calorie range, protein range, cook time, or excluded ingredients |
| Mode Bonus | 10 | Extra points for mode-specific tags (e.g., Period-Friendly, Stress-Friendly) |

Final scores are normalized to 0-100 with a small random variance of +/-3 points for variety.

---

## Tech Stack

### Backend
- **Language:** Python 3.9+
- **Framework:** Flask 3.1.2
- **CORS:** Flask-CORS
- **API Client:** requests
- **Environment:** python-dotenv for API key management

### Frontend
- **Framework:** React 19.2 with Vite
- **Styling:** Tailwind CSS
- **Charts:** Recharts (radar charts)
- **Animations:** Framer Motion
- **Icons:** Lucide React
- **Routing:** React Router DOM 7

### APIs Used
- **RecipeDB API** - Recipe data, nutrition info, diet filtering
  - Base URL: `http://cosylab.iiitd.edu/recipe2-api`
  - Endpoints: `/recipes/recipesinfo`, `/recipes/nutritioninfo`, `/recipes/recipe-diet`, `/recipes/cuisine`, `/recipes/ingredients`

- **FlavorDB API** - Molecular flavor data, pairings, functional groups
  - Base URL: `http://cosylab.iiitd.edu.in:6969/flavordb`
  - Endpoints: `/molecules_data/by-commonName`, `/molecules_data/by-flavorProfile`, `/entity_details`

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm
- API keys from Foodoscope ForkIT Challenge organizers

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/nutrilogic.git
cd nutrilogic
```

#### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install flask flask-cors python-dotenv requests

# Verify .env file exists with API keys:
cat .env
# Should contain:
#   RECIPEDB_API_KEY=your_key_here
#   FLAVORDB_API_KEY=your_key_here
#   FLASK_SECRET_KEY=your_secret_key
#   GOOGLE_CLIENT_ID=your_google_client_id
#   GOOGLE_CLIENT_SECRET=your_google_client_secret
#   GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback
#   FRONTEND_URL=http://localhost:5175
```

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

#### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python3 app.py
# Server starts on http://127.0.0.1:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Server starts on http://localhost:5175
```

**Access the app at:** http://localhost:5175

---

## Verified Test Case

The following test case has been verified to produce a successful output with 8 recipe recommendations.

### Step-by-Step (Standard Mode)

| Step | Page | URL | What to Select |
|------|------|-----|----------------|
| 1 | Ingredients | `/ingredients` | Add: **tomato**, **onion**, **spinach**, **garlic** |
| 2 | Health Profile | `/health` | Diet: **Vegetarian**, **High Protein** |
| 3 | Goals | `/goals` | Select: **Muscle Gain**, **Weight Loss** |
| 4 | Preferences | `/preferences` | Cuisine: **Punjabi** / Style: **Gravy** |
| 5 | Advanced | `/advanced` | Leave defaults, click **Generate Report** |

### Expected Output on Results Page

The system returns 8 ranked recipes:

| Rank | Recipe | Score |
|------|--------|-------|
| 1 | Tandoori Vegetable Kebab | 77 |
| 2 | Lentil and Spinach Dal | 72 |
| 3 | Palak Paneer | 71 |
| 4 | Paneer Tikka Masala | 70 |
| 5 | Chana Masala | 67 |
| 6 | Mushroom Stir-fry | 48 |
| 7 | Aloo Gobi | 48 |
| 8 | Mixed Vegetable Curry | 48 |

Note: Scores may vary by +/-3 points due to randomized variance.

Each recipe card shows:
- Match score badge
- Cook time, servings, calories
- Progress bars for Ingredients, Diet Match, Goal Match, Cuisine match
- Expandable details with flavor radar chart, nutrition breakdown, diet tags, and micronutrients

The results page also includes:
- **Overall Flavor Profile** radar chart across 8 dimensions
- **Flavor Pairing Suggestions** to improve weak flavor dimensions
- **You Might Also Like** section with 4 additional recipe suggestions

### Equivalent cURL Test

You can verify the backend directly with this command:

```bash
curl -s -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "ingredients": ["tomato", "onion", "spinach", "garlic"],
    "diet": ["Vegetarian", "High Protein"],
    "goals": ["Muscle Gain", "Weight Loss"],
    "cuisine": ["Punjabi"],
    "style": ["Gravy"],
    "allergies": [],
    "conditions": [],
    "advanced": {
      "calorieRange": [0, 2000],
      "proteinRange": [0, 100],
      "maxCookTime": 60,
      "spiceTolerance": 3,
      "servings": 2,
      "excludeIngredients": []
    },
    "specialMode": null
  }'
```

Expected response: JSON with `recipes` array (8 items), `overall_flavor_profile`, `flavor_pairings`, and `similar_recipes`.

---

## API Documentation

### Backend Endpoints

#### POST /api/recommend (Main Endpoint)
The primary recommendation engine. Accepts all user inputs, scores recipes, and returns ranked results with flavor data.

```http
POST /api/recommend
Content-Type: application/json
```

**Request Body:**
```json
{
  "ingredients": ["tomato", "onion", "spinach"],
  "diet": ["Vegetarian"],
  "goals": ["Weight Loss"],
  "cuisine": ["South Indian"],
  "style": ["Gravy"],
  "advanced": {
    "calorieRange": [0, 2000],
    "proteinRange": [0, 100],
    "maxCookTime": 60,
    "excludeIngredients": []
  },
  "specialMode": null
}
```

**Response:**
```json
{
  "recipes": [
    {
      "title": "Palak Paneer",
      "cuisine": "Indian",
      "region": "North Indian",
      "description": "Creamy spinach puree with soft paneer cubes...",
      "cook_time": 35,
      "servings": 4,
      "calories": 300,
      "protein": 18,
      "carbs": 12,
      "fat": 20,
      "fiber": 6,
      "ingredients": ["spinach", "paneer", "onion", "garlic", ...],
      "diet_tags": ["Vegetarian", "High Protein", "Low Carb"],
      "health_tags": ["Muscle Gain", "Skin Health", "Immune Boost"],
      "micronutrients": ["Iron", "Calcium", "Vitamin A", ...],
      "score": 77,
      "breakdown": {
        "ingredient_match": 75,
        "diet_match": 100,
        "goal_match": 100,
        "cuisine_match": 30,
        "advanced_match": 100,
        "mode_match": 50
      },
      "flavor_profile": {
        "sweet": 24, "sour": 22, "bitter": 19,
        "salty": 6, "umami": 48, "spicy": 24,
        "fruity": 19, "smoky": 14
      }
    }
  ],
  "total_results": 12,
  "overall_flavor_profile": { ... },
  "flavor_pairings": [ ... ],
  "similar_recipes": [ ... ]
}
```

#### Other Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/recipes/search?ingredients=tomato,onion` | Search recipes by ingredients |
| GET | `/api/recipes/by-diet?diet=Vegetarian` | Get recipes by diet type |
| GET | `/api/recipes/by-cuisine?cuisine=Indian` | Get recipes by cuisine |
| GET | `/api/recipes/all?page=0&limit=10` | Get paginated recipes |
| GET | `/api/recipes/nutrition/<recipe_id>` | Get nutrition info for a recipe |
| GET | `/api/flavor/profile/<ingredient>` | Get flavor profile for an ingredient |
| GET | `/api/flavor/compute?ingredients=tomato,onion` | Compute aggregate flavor profile |
| GET | `/api/flavor/by-profile?profile=spicy` | Get molecules by flavor profile |
| GET | `/api/pet/toxic-foods/<pet_type>` | Get toxic foods for a pet type |
| GET | `/api/community/meals` | Get community surplus meals |

---

## Roadmap

### Completed
- [x] Multi-constraint scoring engine with 5 scoring dimensions
- [x] RecipeDB and FlavorDB API integration with fallback data
- [x] 8-dimension flavor radar chart visualization
- [x] 5-step guided input flow (Standard Mode)
- [x] Explainable score breakdowns per recipe
- [x] Flavor pairing suggestions
- [x] Google OAuth login
- [x] Responsive dark-theme UI

### In Progress
- [ ] Full testing and stabilization of special modes (Period, Stress, Pet, Medical, Doctor, Community)
- [ ] Real-time macro tracking
- [ ] Nutrition timeline visualization

### Planned
- [ ] Integration with fitness wearables
- [ ] Smart grocery list generation
- [ ] Calendar-based meal planning
- [ ] Voice input for ingredients
- [ ] Multi-language support

---

## Team

**[Your Name]** - Project Lead and Backend Developer
**[Teammate 2]** - Frontend Developer and UI/UX
**[Teammate 3]** - Data Science and Algorithm Design
**[Teammate 4]** - API Integration and Testing

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **IIIT Delhi CoSy Lab** - For hosting Foodoscope ForkIT Challenge 2025
- **RecipeDB Team** - For comprehensive recipe and nutrition data
- **FlavorDB Team** - For molecular flavor science research
- **Open Source Community** - Flask, React, Recharts, Tailwind CSS, Framer Motion, Lucide

### Research References

1. Ahn, Y. Y., et al. (2011). "Flavor network and the principles of food pairing." *Scientific Reports*
2. FlavorDB: https://cosylab.iiitd.edu.in/flavordb/
3. RecipeDB: http://cosylab.iiitd.edu/recipe2-api

---

**Event:** Foodoscope ForkIT Challenge 2025
**Date:** February 14-15, 2026
**Location:** IIIT Delhi
**Track:** Computational Gastronomy
