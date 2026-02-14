# NutriLogic: Flavor-Constrained Cuisine Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hackathon](https://img.shields.io/badge/Foodoscope-ForkIT%202025-orange.svg)](https://github.com)

> A computational gastronomy engine that transforms leftover ingredients into safe, personalized meal recommendations using molecular flavor science and nutritional intelligence.

**Built for:** Foodoscope ForkIT Challenge 2025  
**Hosted by:** IIIT Delhi – CoSy Lab  
**Website:** NutriLogic  
**Demo:** [Live Demo Link] | **Presentation:** [Slides Link](https://www.canva.com/design/DAHAPoibNi4/BlUzHYm1l92CKV9yWty05Q/edit?utm_content=DAHAPoibNi4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Scoring Model](#scoring-model)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Screenshots](#screenshots)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Team](#team)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

**NutriLogic** is a constraint-based culinary optimization engine that goes beyond simple ingredient matching. By combining:

- Nutritional Intelligence (RecipeDB)
- Molecular Flavor Science (FlavorDB)
- Diet & Allergy Filtering
- Macro-based Scoring
- Cuisine-aware Flavor Alignment

We help users reduce food waste while ensuring meals are healthy, safe, and flavor-compatible.

### Why It Matters

- **30% of household food** goes to waste due to "ingredient paralysis"
- **48% of people with dietary restrictions** struggle to find safe recipes
- Traditional recipe apps ignore **molecular flavor compatibility**
- Health-conscious users need **macro-aware recommendations**

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
Accepts leftover ingredients and validates availability.

### 2. Hard Filtering
- **Diet Compliance:** Ensures recipes match selected diet (Keto, Vegan, etc.)
- **Allergen Safety:** Strictly excludes any allergen-containing recipes

### 3. Macro Validation
Validates recipes against user-specified macro targets:
- Minimum protein requirements
- Carbohydrate limits
- Fat constraints

### 4. Molecular Flavor Analysis
Uses FlavorDB to compute flavor compatibility:
- Identifies shared flavor molecules between ingredients
- Evaluates functional groups
- Considers aroma threshold values
- Generates **Flavor Harmony Score**

### 5. Cuisine Alignment
Boosts scores for cuisine-typical flavor patterns:
- Indian: cumin, turmeric, coriander
- Italian: basil, oregano, garlic
- Thai: lemongrass, galangal, fish sauce

### 6. Intelligent Ranking
Outputs optimized meal suggestions with **explainable reasoning**.

---

## Key Features

### Core Features

#### 1. Ingredient Input
- Natural language ingredient entry
- Comma-separated or autocomplete interface
- Smart ingredient recognition

#### 2. Diet & Allergy Filtering
Hard filters ensure safety:
- **Diets:** Keto, Vegan, Vegetarian, Paleo, High-Protein, Low-Carb, Mediterranean
- **Allergens:** Dairy, Gluten, Nuts, Soy, Eggs, Shellfish, Fish

#### 3. Macro Optimization
Specify your macro targets:
```
Protein: 25-35g per meal
Carbs: < 30g (for Keto)
Fat: 15-25g
```
Recipes are scored based on macro fit.

#### 4. Flavor Compatibility Scoring
Using FlavorDB molecular data:
- **Shared Molecules:** Identifies common flavor compounds
- **Functional Groups:** Analyzes chemical similarity
- **Aroma Thresholds:** Weighs impact on flavor perception
- **Output:** Flavor Harmony Score (0-100)

#### 5. Cuisine Alignment
Preference-aware scoring:
- Boosts cuisine-typical flavor patterns
- Adjusts ingredient compatibility weights
- Suggests authentic ingredient combinations

#### 6. Leftover Utilization Score
Maximizes use of available ingredients:
```
Leftover Usage = (Matched Ingredients / Total Available) × 100
```

#### 7. Explainable Output
Each recommendation includes:

**Score Breakdown:**
```
Overall Score: 87/100
├─ Flavor Harmony: 92/100 (High molecular overlap)
├─ Macro Fit: 85/100 (Protein: 28g ✓, Carbs: 22g ✓)
├─ Cuisine Alignment: 88/100 (Italian flavor profile)
└─ Leftover Utilization: 83/100 (5/6 ingredients used)
```

**Molecular Explanation:**
```
Why this pairing works:
• Tomato + Basil share 12 flavor molecules
• Chicken + Garlic: Compatible functional groups
• Overall harmony: Strong (8 shared compounds)
```

**Suggested Substitutes:**
```
Missing: Mozzarella
Molecular alternatives:
• Ricotta (0.89 similarity)
• Feta (0.82 similarity)
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  • Leftover Ingredients                                     │
│  • Diet Selection (Keto, Vegan, etc.)                       │
│  • Allergens to Avoid                                       │
│  • Macro Targets (Protein, Carbs, Fat)                      │
│  • Cuisine Preference (Optional)                            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     PROCESSING LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  1. Recipe Retrieval (RecipeDB API)                         │
│     └─ Fetch recipes by ingredients & diet                  │
│                                                             │
│  2. Hard Filtering                                          │
│     ├─ Diet Compliance Filter                               │
│     └─ Allergen Safety Filter                               │
│                                                             │
│  3. Nutritional Validation (RecipeDB)                       │
│     └─ Validate macro ranges                                │
│                                                             │
│  4. Molecular Flavor Analysis (FlavorDB)                    │
│     ├─ Fetch flavor molecules for each ingredient           │
│     ├─ Calculate molecular overlap                          │
│     ├─ Evaluate functional group compatibility              │
│     └─ Generate Flavor Harmony Score                        │
│                                                             │
│  5. Cuisine Pattern Matching                                │
│     └─ Boost scores for cuisine-typical combinations        │
│                                                             │
│  6. Multi-Constraint Scoring Engine                         │
│     └─ Weighted scoring across all dimensions               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       OUTPUT LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  • Top N Ranked Recipes (Sorted by Overall Score)           │
│  • Score Breakdown (Explainable)                            │
│  • Molecular Explanation                                    │
│  • Nutritional Summary                                      │
│  • Suggested Ingredient Substitutes                         │
│  • Flavor Profile Visualization                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Scoring Model

Our multi-constraint scoring system uses weighted optimization:

### Formula

```
Final Score = w₁ × Flavor_Score + w₂ × Macro_Fit + w₃ × Cuisine_Alignment + w₄ × Leftover_Utilization

Where:
w₁ = 0.35 (Flavor weight)
w₂ = 0.30 (Nutrition weight)
w₃ = 0.20 (Cuisine weight)
w₄ = 0.15 (Utilization weight)
```

### Component Calculations

#### 1. Flavor Harmony Score (0-100)
```python
shared_molecules = count_shared_flavor_compounds(ingredient_set)
functional_similarity = calculate_functional_group_overlap(ingredient_set)
aroma_impact = weighted_aroma_threshold_score(ingredient_set)

Flavor_Score = (0.5 × shared_molecules_normalized + 
                0.3 × functional_similarity + 
                0.2 × aroma_impact) × 100
```

#### 2. Macro Fit Score (0-100)
```python
protein_deviation = abs(actual_protein - target_protein) / target_protein
carb_deviation = abs(actual_carbs - target_carbs) / target_carbs
fat_deviation = abs(actual_fat - target_fat) / target_fat

Macro_Fit = 100 - (protein_deviation + carb_deviation + fat_deviation) / 3 × 100
```

#### 3. Cuisine Alignment Score (0-100)
```python
cuisine_typical_ingredients = get_cuisine_profile(cuisine_type)
matched_typical = count_matches(recipe_ingredients, cuisine_typical_ingredients)

Cuisine_Alignment = (matched_typical / len(cuisine_typical_ingredients)) × 100
```

#### 4. Leftover Utilization Score (0-100)
```python
Leftover_Utilization = (ingredients_used / ingredients_available) × 100
```

### Example Calculation

**Input:**
- Ingredients: chicken, tomatoes, basil, garlic, onion
- Diet: Mediterranean
- Macros: Protein 30g, Carbs 25g, Fat 20g
- Cuisine: Italian

**Recipe: Chicken Cacciatore**

```
Flavor Score:
  • Shared molecules: 14 (tomato-basil: 12, garlic-onion: 8)
  • Functional similarity: 0.87
  • Aroma impact: 0.92
  → Flavor_Score = 91/100

Macro Fit:
  • Protein: 32g (deviation: 6.7%)
  • Carbs: 23g (deviation: 8.0%)
  • Fat: 18g (deviation: 10.0%)
  → Macro_Fit = 91.8/100

Cuisine Alignment:
  • Italian typical ingredients matched: 4/5 (80%)
  → Cuisine_Alignment = 88/100

Leftover Utilization:
  • Ingredients used: 5/5 (100%)
  → Leftover_Utilization = 100/100

Final Score = 0.35 × 91 + 0.30 × 91.8 + 0.20 × 88 + 0.15 × 100
            = 31.85 + 27.54 + 17.6 + 15
            = 91.99/100
```

---

## Tech Stack

### Backend
- **Language:** Python 3.12.10+
- **Framework:** Flask 
- **API Client:** RecipeDB + FlavorDB
- **Data Processing:** Native Python (dictionaries, sets)
- **Environment:** python-dotenv for API key management

### Frontend
- **Framework:** React.js with Vite
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Icons:** Lucide React 

### APIs Used
- **RecipeDB API** - Recipe data, nutrition info, diet filtering
  - Base URL: `http://cosylab.iiitd.edu/recipe2-api`
  - Endpoints: `/recipesinfo`, `/nutritioninfo`, `/recipe-diet`, `/protein-range`

- **FlavorDB API** - Molecular flavor data, pairings, functional groups
  - Base URL: `http://cosylab.iiitd.edu.in:6969/flavordb`
  - Endpoints: `/by-alias`, `/by-femaFlavorProfile`, `/by-natural-source`

### Development Tools
- **Version Control:** Git + GitHub
- **API Testing:** Postman
- **Linting:** ESLint (JS), Black (Python)
- **Documentation:** Swagger / OpenAPI

---

## Getting Started

### Prerequisites

```bash
# Required
- Python 3.8 or higher
- Node.js 14+ (for frontend)
- API keys from Foodoscope ForkIT Challenge organizers

# Optional
- Redis (for caching)
- Docker (for containerization)
```

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/nutrilogic.git
cd nutrilogic
```

#### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your API keys:
# RECIPEDB_API_KEY=your_key_here
# FLAVORDB_API_KEY=your_key_here
```

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
# Add backend API URL
```

#### 4. Run the Application

**Backend:**
```bash
# Development mode
python app.py

# Or with Flask
flask run

# Or with Gunicorn (production)
gunicorn -w 4 app:app
```

**Frontend:**
```bash
cd frontend
npm run dev
```

**Access the app:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

---

## API Documentation

### Backend Endpoints

#### 1. Optimize Recipes
```http
POST /api/optimize
Content-Type: application/json

{
  "ingredients": ["chicken", "tomatoes", "basil"],
  "diet": "mediterranean",
  "allergens": ["gluten", "dairy"],
  "macros": {
    "protein_min": 25,
    "protein_max": 35,
    "carbs_max": 30,
    "fat_min": 15,
    "fat_max": 25
  },
  "cuisine": "italian",
  "top_n": 5
}
```

**Response:**
```json
{
  "status": "success",
  "results": [
    {
      "recipe": {
        "id": "12345",
        "name": "Chicken Cacciatore",
        "ingredients": [...],
        "instructions": [...],
        "nutrition": {
          "calories": 420,
          "protein": 32,
          "carbs": 23,
          "fat": 18
        }
      },
      "scores": {
        "overall": 91.99,
        "flavor_harmony": 91,
        "macro_fit": 91.8,
        "cuisine_alignment": 88,
        "leftover_utilization": 100
      },
      "explanation": {
        "molecular_matches": [
          {"pair": "tomato-basil", "shared_molecules": 12},
          {"pair": "garlic-onion", "shared_molecules": 8}
        ],
        "macro_analysis": "Excellent protein match, low carbs suitable for Mediterranean diet",
        "cuisine_notes": "Authentic Italian flavor profile"
      },
      "substitutes": [...]
    }
  ],
  "metadata": {
    "total_analyzed": 150,
    "filtered_out": 145,
    "processing_time_ms": 234
  }
}
```

#### 2. Get Flavor Analysis
```http
GET /api/flavor-analysis?ingredients=tomato,basil,garlic
```

#### 3. Suggest Substitutes
```http
GET /api/substitutes?ingredient=mozzarella&cuisine=italian
```

---

## Usage Examples

### Example 1: Keto Meal with Leftover Chicken

**Input:**
```javascript
{
  ingredients: ["chicken breast", "broccoli", "cream", "cheese"],
  diet: "keto",
  allergens: [],
  macros: {
    protein_min: 30,
    carbs_max: 10,
    fat_min: 20
  }
}
```

**Output:**
```
Top Recommendation: Creamy Garlic Chicken with Broccoli
Score: 94/100

Flavor Harmony: 89/100
  - Cream + Garlic: 8 shared molecules
  - Chicken + Broccoli: Compatible functional groups

Macro Fit: 96/100
  - Protein: 35g (meets target)
  - Carbs: 7g (meets target)
  - Fat: 24g (meets target)

Keto Compliant: Yes
Allergen Safe: Yes
Leftover Use: 100% (4/4 ingredients)
```

### Example 2: Vegan Meal with Indian Cuisine Preference

**Input:**
```javascript
{
  ingredients: ["chickpeas", "spinach", "tomatoes", "onion", "garlic"],
  diet: "vegan",
  allergens: ["nuts"],
  macros: {
    protein_min: 15,
    carbs_max: 45,
    fat_max: 10
  },
  cuisine: "indian"
}
```

**Output:**
```
Top Recommendation: Chana Palak (Chickpea Spinach Curry)
Score: 92/100

Flavor Harmony: 95/100
  - High molecular overlap in Indian spice profile
  - Spinach + Garlic: 10 shared aroma compounds

Macro Fit: 88/100
  - Protein: 18g (meets target)
  - Carbs: 42g (meets target)
  - Fat: 8g (meets target)

Cuisine Alignment: 94/100
  - Authentic Indian flavor pattern
  - Typical ingredient combinations

Suggested Addition: Cumin (molecular similarity: 0.91)
```

---

## Screenshots

### Main Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Recipe Results with Score Breakdown
![Results](docs/screenshots/results.png)

### Flavor Analysis Visualization
![Flavor Analysis](docs/screenshots/flavor-analysis.png)

### Molecular Explanation
![Molecular View](docs/screenshots/molecular-view.png)

---

## Roadmap

### Phase 1: Core Features (Completed)
- [x] Multi-constraint optimization engine
- [x] RecipeDB & FlavorDB integration
- [x] Scoring system implementation
- [x] Basic UI/UX

### Phase 2: Enhanced Intelligence (In Progress)
- [ ] Machine learning-based flavor prediction
- [ ] Adaptive learning from user preferences
- [ ] Real-time macro tracking
- [ ] Nutrition timeline visualization

### Phase 3: Smart Integrations (Planned)
- [ ] Integration with fitness wearables (Fitbit, Apple Watch)
- [ ] Smart grocery list generation
- [ ] Calendar-based meal planning
- [ ] Voice input for ingredients
- [ ] Barcode scanner for packaged foods

### Phase 4: Advanced Features (Future)
- [ ] Computer vision for ingredient recognition
- [ ] Collaborative filtering recommendations
- [ ] Social features (share recipes, meal plans)
- [ ] Offline mode with cached recipes
- [ ] Multi-language support
- [ ] Restaurant menu analysis

---

## Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Write meaningful commit messages
- Add tests for new features
- Update documentation

### Areas for Contribution

- Bug fixes
- New features
- Documentation improvements
- UI/UX enhancements
- Testing coverage
- Translations

---

## Team

### Core Team

**[Your Name]** - Project Lead & Backend Developer  
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/YOUR-USERNAME)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://linkedin.com/in/YOUR-PROFILE)

**[Teammate 2]** - Frontend Developer & UI/UX  
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/TEAMMATE-2)

**[Teammate 3]** - Data Science & Algorithm Design  
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/TEAMMATE-3)

**[Teammate 4]** - API Integration & Testing  
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?logo=github)](https://github.com/TEAMMATE-4)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 NutriLogic Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Acknowledgments

### Special Thanks

- **IIIT Delhi CoSy Lab** - For hosting Foodoscope ForkIT Challenge 2025
- **RecipeDB Team** - For providing comprehensive recipe and nutrition data
- **FlavorDB Team** - For groundbreaking molecular flavor science research
- **Hackathon Mentors** - For guidance and support throughout the event
- **Open Source Community** - For amazing tools and libraries

### Research References

1. Ahn, Y. Y., et al. (2011). "Flavor network and the principles of food pairing." *Scientific Reports*
2. FlavorDB Research: [https://cosylab.iiitd.edu.in/flavordb/](https://cosylab.iiitd.edu.in/flavordb/)
3. RecipeDB Documentation: [http://cosylab.iiitd.edu/recipe2-api](http://cosylab.iiitd.edu/recipe2-api)

### Technologies

Built with amazing open-source technologies:
- [Flask](https://flask.palletsprojects.com/)
- [React](https://reactjs.org/)
- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- And many more...

---

## Contact & Support

### Questions or Feedback?

- **Email:** contact@nutrilogic.com
- **GitHub Issues:** [Report a bug or request a feature](https://github.com/YOUR-USERNAME/nutrilogic/issues)
- **Website:** [NutriLogic](https://nutrilogic.com)

### Project Links

- **Documentation:** [Full Docs](https://docs.nutrilogic.com)
- **Live Demo:** [Try it now](https://demo.nutrilogic.com)
- **Presentation:** [Slides](https://your-slides-link.com)
- **Video Demo:** [YouTube](https://youtube.com/your-video)

---

## Project Stats

![GitHub stars](https://img.shields.io/github/stars/YOUR-USERNAME/nutrilogic?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR-USERNAME/nutrilogic?style=social)
![GitHub issues](https://img.shields.io/github/issues/YOUR-USERNAME/nutrilogic)
![GitHub pull requests](https://img.shields.io/github/issues-pr/YOUR-USERNAME/nutrilogic)

---

## Hackathon Details

**Event:** Foodoscope ForkIT Challenge 2025  
**Date:** February 14-15, 2026  
**Location:** IIIT Delhi  
**Track:** Computational Gastronomy  
**Award:** [If applicable]

---

<div align="center">

**Star this repo if you find it helpful!**

Made with passion during Foodoscope ForkIT Challenge 2025

[Report Bug](https://github.com/YOUR-USERNAME/nutrilogic/issues) · [Request Feature](https://github.com/YOUR-USERNAME/nutrilogic/issues) · [Documentation](https://docs.nutrilogic.com)

</div>
