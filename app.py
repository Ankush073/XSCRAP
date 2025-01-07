# Import necessary libraries
from flask import Flask, jsonify, request, render_template  # Flask web framework components
from pymongo import MongoClient  # MongoDB database connector
import subprocess  # For executing external scripts
import sys  # For system-level operations
import os  # For environment variable access
from dotenv import load_dotenv  # Environment variable loader

# Initialize Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# MongoDB connection configuration
# Retrieve connection string from environment variables for security
MONGO_URI = os.getenv('MONGODB_URL')
client = MongoClient(MONGO_URI)
db = client.get_database("mydatabase")
collection = db.get_collection("trending_topics")

# Route for serving the main page
@app.route("/")
def index():
    return render_template("index.html")

# Route for executing the Selenium script
@app.route("/run-script", methods=["POST"])
def run_script():
    try:
        # Execute the selenium_script.py using the same Python interpreter as the main application
        # check=True ensures that subprocess.CalledProcessError is raised for non-zero exit status
        subprocess.run([sys.executable, "selenium_script.py"], check=True)
        return jsonify({"message": "Script executed successfully"})
    except subprocess.CalledProcessError as e:
        # Handle and return any errors that occur during script execution
        return jsonify({"message": "Script execution failed", "error": str(e)})

# Route for retrieving trend data from MongoDB
@app.route("/get-trends")
def get_trends():
    # Query MongoDB for the most recent trend data
    # Sort by datetime in descending order (-1) to get the latest entry
    data = collection.find_one(sort=[("datetime", -1)])
    
    if not data:
        return jsonify({"message": "No trends available yet."})
    
    # Convert MongoDB ObjectId to string to make it JSON serializable
    data["_id"] = str(data["_id"])
    return jsonify(data)

# Run the Flask application in debug mode if executed directly
if __name__ == "__main__":
    app.run(debug=True)