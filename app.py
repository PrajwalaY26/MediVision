from flask import Flask, request, jsonify, render_template
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename
import subprocess
import os
from flask import Flask, jsonify


app = Flask(__name__)

# Set up the upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load the trained model
model = tf.keras.models.load_model("medicine_model.h5")  # Load your saved model

# Metadata for Paracetamol
metadata = {
    "paracetamol": {
        "name": "Paracetamol",
        "dosage": "500mg",
        "usage": [
            "Pain relief",
            "Fever reduction",
            "Post-surgery pain relief",
            "Cold and flu symptom relief"
        ],
        "side_effects": [
            "Allergic reactions (rash, itching)",
            "Stomach upset",
            "Nausea and vomiting"
        ],
        "benefits": [
            "Effective for mild to moderate pain",
            "Safe for people with stomach issues",
            "Widely available and affordable"
        ],
        "summary": "Paracetamol is a widely used pain reliever and fever reducer, effective for headaches, muscle aches, and colds. It is safer for those with stomach issues compared to NSAIDs and has fewer side effects. However, overdosing can lead to severe liver damage, so it should be taken as directed."
    }
}


# Function to process the image and predict
def predict_image(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize

    prediction = model.predict(img_array)
    
    if prediction[0] > 0.5:
        return metadata["paracetamol"]
    else:
        return {"error": "Medicine not recognized"}

# Route to render the webpage
@app.route("/")
def upload_page():
    return render_template("home.html")

@app.route("/medicine")
def medicine_page():
    return render_template("medicinepage.html")




@app.route('/run_app2', methods=['POST'])
def run_app2():
    try:
        # Get the absolute path of app2.py
        script_path = os.path.abspath("app2.py")

        # Different command for Windows & Linux/Mac
        if os.name == "nt":  # Windows
            command = f"start cmd /k streamlit run {script_path}"
        else:  # Linux/Mac
            command = f"gnome-terminal -- streamlit run {script_path}"

        # Run the command in a new terminal window
        subprocess.Popen(command, shell=True)

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})




# Default users (email: password)
users = {
    "yash@gmail.com": "123",
    "hash@gmail.com": "143"
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users and users[email] == password:
            return render_template("home.html", error="Error")
        else:
            return render_template("index.html", error="Invalid email or password")

    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users:
            return render_template("signup.html", error="User already exists")
        else:
            users[email] = password
            return render_template("home.html", error="Error")

    return render_template("signup.html")











# Route to handle image upload and prediction
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"})
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Predict the medicine
    result = predict_image(filepath)
    
    return jsonify(result)




@app.route("/reprocess", methods=["POST"])
def reprocess():
    data = request.json
    image_name = data.get("image")

    if not image_name:
        return jsonify({"error": "No image provided"})

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_name)
    
    # Re-run the model on the same image
    result = predict_image(image_path)
    
    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)
