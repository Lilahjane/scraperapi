from flask import Flask, request, jsonify
from recipe_scrapers import scrape_html
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*')

@app.route('/scrape-recipe', methods=['POST'])
def scrape_recipe():
    try:
        # Parse the JSON request
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Scrape the recipe
        scraper = scrape_html(html=None, org_url=url, online=True, supported_only=True)

        # Build the response data
        response_data = {
            "URL": url,
            "Recipe_Name": scraper.title(),
            "Recipe_photo": scraper.image(),
            "Macros": scraper.nutrients(),
            "Total_Time": scraper.total_time(),
            "ingredients": scraper.ingredients()
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
