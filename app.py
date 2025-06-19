# arzeonxyl/pahlawan-bm25/pahlawan-bm25-8ebf1d8ad63d6ecca710d88fc830f10dab0dd18b/app.py
from flask import Flask, request, jsonify, render_template
from search_logic import perform_search # Impor fungsi search_logic

# Kasih tahu Flask template folder-nya "views"
app = Flask(__name__, template_folder='views')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/run-python", methods=["POST"])
def run_python():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query tidak boleh kosong!"}), 400

    try:
        # Panggil fungsi perform_search secara langsung
        result_json_string = perform_search(query)
        return jsonify({"output": result_json_string})
    except Exception as e:
        return jsonify({"error": "Internal error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
