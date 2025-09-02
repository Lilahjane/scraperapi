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

def scrape_single_recipe(url):
    try:
        scraper = scrape_html(html=None, org_url=url, online=True, supported_only=True)

        return {
            "author": str(safe_scrape(scraper, scraper.author)),
            "canonical_url": str(safe_scrape(scraper, scraper.canonical_url)),
            "category": str(safe_scrape(scraper, scraper.category)),
            "cook_time": str(safe_scrape(scraper, scraper.cook_time)),
            "cooking_method": str(safe_scrape(scraper, scraper.cooking_method)),
            "cuisine": str(safe_scrape(scraper, scraper.cuisine)),
            "description": str(safe_scrape(scraper, scraper.description)),
            "dietary_restrictions": str(safe_scrape(scraper, scraper.dietary_restrictions)),
            "host": str(safe_scrape(scraper, scraper.host)),
            "image": str(safe_scrape(scraper, scraper.image)),
            "ingredients": safe_scrape(scraper, scraper.ingredients, default=[]),
            "instructions_list": safe_scrape(scraper, scraper.instructions_list, default=[]),
            "keywords": safe_scrape(scraper, scraper.keywords, default=[]),
            "language": safe_scrape(scraper, scraper.language),
            "nutrients": safe_scrape(scraper, scraper.nutrients, default={}),
            "prep_time": str(safe_scrape(scraper, scraper.prep_time)),
            "ratings": str(safe_scrape(scraper, scraper.ratings)),
            "ratings_count": str(safe_scrape(scraper, scraper.ratings_count)),
            "reviews": safe_scrape(scraper, scraper.reviews, default=[]),
            "site_name": str(safe_scrape(scraper, scraper.site_name)),
            "title": str(safe_scrape(scraper, scraper.title)),
            "total_time": str(safe_scrape(scraper, scraper.total_time)),
            "yields": str(safe_scrape(scraper, scraper.yields)),
            "url": url,
            "error": None
        }
    except Exception as e:
        return {
            "error": str(e),
            "author": "",
            "canonical_url": "",
            "category": "",
            "cook_time": "",
            "cooking_method": "",
            "cuisine": "",
            "description": "",
            "dietary_restrictions": "",
            "host": "",
            "image": "",
            "ingredients": [],
            "instructions_list": [],
            "keywords": [],
            "language": "",
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
        }

@app.route('/scrape-recipe', methods=['POST'])
def scrape_recipe():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        result = scrape_single_recipe(url)
        return jsonify(result), 200 if not result["error"] else 500

    except Exception as e:
        return jsonify({
            "error": str(e),
            "url": url if 'url' in locals() else None
        }), 500

@app.route('/bulk-scrape', methods=['POST'])
def bulk_scrape():
    try:
        data = request.get_json()
        urls = data.get('urls', [])

        if not urls or not isinstance(urls, list):
            return jsonify({"error": "No URLs array provided"}), 400

        results = []
        for url in urls:
            if url:  # Only process non-empty URLs
                results.append(scrape_single_recipe(url))

        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({
            "error": str(e),
            "results": []
        }), 500

if __name__ == "__main__":
    app.run(debug=True)