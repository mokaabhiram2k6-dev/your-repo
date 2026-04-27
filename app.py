from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Data from your datasheet: Soil_pH_Urea_Datasheet.xlsx
PH_DATA = [
    {
        "range": "< 5.5",
        "label": "Strong Acidic",
        "min": 0,
        "max": 5.5,
        "nitrogen": "Very Low",
        "urea": "40–50 kg/acre",
        "efficiency": "Low",
        "additional": "Lime (CaCO3)",
    },
    {
        "range": "5.5 – 6.5",
        "label": "Moderately Acidic",
        "min": 5.5,
        "max": 6.5,
        "nitrogen": "Medium",
        "urea": "35–45 kg/acre",
        "efficiency": "Medium",
        "additional": "Lime (small qty)",
    },
    {
        "range": "6.5 – 7.5",
        "label": "Neutral",
        "min": 6.5,
        "max": 7.5,
        "nitrogen": "High (Optimal)",
        "urea": "25–35 kg/acre",
        "efficiency": "High",
        "additional": "None required",
    },
    {
        "range": "7.5 – 8.5",
        "label": "Moderately Alkaline",
        "min": 7.5,
        "max": 8.5,
        "nitrogen": "Medium",
        "urea": "30–40 kg/acre",
        "efficiency": "Medium",
        "additional": "Gypsum/Sulfur",
    },
    {
        "range": "> 8.5",
        "label": "Strong Alkaline",
        "min": 8.5,
        "max": 14,
        "nitrogen": "Low",
        "urea": "35–45 kg/acre",
        "efficiency": "Low",
        "additional": "Sulfur + Organic",
    },
]


def get_ph_recommendation(avg_ph):
    for entry in PH_DATA:
        if entry["min"] <= avg_ph < entry["max"]:
            return entry
    # Edge case: exactly 14
    return PH_DATA[-1]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    ph_values = data.get("ph_values", [])

    if len(ph_values) != 7:
        return jsonify({"error": "Please provide exactly 7 pH values."}), 400

    try:
        ph_floats = [float(v) for v in ph_values]
    except ValueError:
        return jsonify({"error": "All pH values must be valid numbers."}), 400

    for v in ph_floats:
        if v < 0 or v > 14:
            return jsonify({"error": f"pH value {v} is out of range (0–14)."}), 400

    avg_ph = round(sum(ph_floats) / len(ph_floats), 2)
    rec = get_ph_recommendation(avg_ph)

    return jsonify({
        "average_ph": avg_ph,
        "ph_range": rec["range"],
        "soil_type": rec["label"],
        "nitrogen_availability": rec["nitrogen"],
        "urea_recommendation": rec["urea"],
        "efficiency": rec["efficiency"],
        "additional_input": rec["additional"],
    })


if __name__ == "__main__":
    app.run(debug=True)
