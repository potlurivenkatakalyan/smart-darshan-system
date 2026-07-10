from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import psycopg2

app = Flask(__name__, static_folder="../frontend")
CORS(app)

# Load ML model
model = pickle.load(open("../ml_model/model.pkl", "rb"))

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="temple_db",
    user="postgres",
    password="2004",
    host="localhost",
    port="5432"
)

# ✅ Serve main page
@app.route('/')
def home():
    return send_from_directory('../frontend', 'index.html')

# ✅ IMPORTANT: Serve images & other files
@app.route('/<path:filename>')
def serve_files(filename):
    return send_from_directory('../frontend', filename)

# ✅ Prediction API
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        hour = int(data['hour'])
        day = int(data['day'])

        prediction = model.predict([[hour, day]])

        crowd = int(prediction[0])
        waiting = int(crowd / 10)

        cur = conn.cursor()
        cur.execute(
            "INSERT INTO predictions (hour, day, crowd, waiting) VALUES (%s, %s, %s, %s)",
            (hour, day, crowd, waiting)
        )
        conn.commit()
        cur.close()

        return jsonify({
            "crowd": crowd,
            "waiting": waiting
        })

    except Exception as e:
        print("Error:", e)
        conn.rollback()
        return jsonify({"error": str(e)})

app.run(debug=True)