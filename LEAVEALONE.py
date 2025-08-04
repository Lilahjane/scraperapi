from flask import Flask, request, jsonify
from recipe_scrapers import scrape_html
from flask_cors import CORS
from recipe_scrapers._exceptions import (
    ElementNotFoundInHtml,
    FieldNotProvidedByWebsiteException,
    FillPluginException,
    NoSchemaFoundInWildMode,
    OpenGraphException,
    RecipeSchemaNotFound,
    SchemaOrgException,
    StaticValueException,
    WebsiteNotImplementedError
)

app = Flask(__name__)
CORS(app, origins='*')

def safe_scrape(scraper, func, default=""):
    try:
        result = func()
        return result if result is not None else default
    except (
        ElementNotFoundInHtml,
        FieldNotProvidedByWebsiteException,
        FillPluginException,
        NoSchemaFoundInWildMode,
        OpenGraphException,
        RecipeSchemaNotFound,
        SchemaOrgException,
        StaticValueException,
        WebsiteNotImplementedError,
        AttributeError,
        NotImplementedError
    ):
        return default

@app.route('/scrape-recipe', methods=['POST'])
def scrape_recipe():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        scraper = scrape_html(html=None, org_url=url, online=True, supported_only=True)

        response_data = {
            "author": safe_scrape(scraper, scraper.author),
            "canonical_url": safe_scrape(scraper, scraper.canonical_url),
            "category": safe_scrape(scraper, scraper.category),
            "cook_time": safe_scrape(scraper, scraper.cook_time),
            "cooking_method": safe_scrape(scraper, scraper.cooking_method),
            "cuisine": safe_scrape(scraper, scraper.cuisine),
            "description": safe_scrape(scraper, scraper.description),
            "dietary_restrictions": safe_scrape(scraper, scraper.dietary_restrictions),
            "host": safe_scrape(scraper, scraper.host),
            "image": safe_scrape(scraper, scraper.image),
            "ingredients": safe_scrape(scraper, scraper.ingredients, default=[]),
            # "instructions": safe_scrape(scraper, scraper.instructions),
            "instructions_list": safe_scrape(scraper, scraper.instructions_list, default=[]),
            "keywords": safe_scrape(scraper, scraper.keywords, default=[]),
            "language": safe_scrape(scraper, scraper.language),
            #"links": safe_scrape(scraper, scraper.links, default=[]),
            "nutrients": safe_scrape(scraper, scraper.nutrients, default={}),
            "prep_time": safe_scrape(scraper, scraper.prep_time),
            "ratings": safe_scrape(scraper, scraper.ratings),
            "ratings_count": safe_scrape(scraper, scraper.ratings_count),
            "reviews": safe_scrape(scraper, scraper.reviews, default=[]),
            "site_name": safe_scrape(scraper, scraper.site_name),
            "title": safe_scrape(scraper, scraper.title),
            "total_time": safe_scrape(scraper, scraper.total_time),
            "yields": safe_scrape(scraper, scraper.yields),
            "url": url,
            "error": None
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            "error": str(e),
            "author": "",
            "canonical_url": "",
            "category": "",
            "cook_time": "",
            "cooking_method": "",
            "cuisine": "",
            "description": "",
            "dietary_restrictions": "",
            # "equipment": "",
            "host": "",
            "image": "",
            # "ingredient_groups": [],
            "ingredients": [],
            "instructions": "",
            "instructions_list": [],
            "keywords": [],
            "language": "",
            #"links": [],
            "nutrients": {},
            "prep_time": "",
            "ratings": "",
            "ratings_count": "",
            "reviews": [],
            "site_name": "",
            "title": "",
            "total_time": "",
            "yields": "",
            "url": url
        }), 500

if __name__ == "__main__":
    app.run(debug=True)