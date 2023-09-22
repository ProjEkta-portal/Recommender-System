# from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

PASSWORD = os.getenv('PASS')
# app = Flask(__name__)

# Connect to MongoDB Atlas cloud database
URI = f"mongodb+srv://neerajjm12345:{PASSWORD}@cluster0.hdq7yc2.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(URI)
db = client["db"]["projects"]

# Get HTTP request from frontend
# @app.route("/projects", methods=["POST"])
# def get_projects():
#   # Get JSON body from request
#   json_body = request.get_json()

  # Extract skills from JSON body
# skills = json_body["skills"]
skills = ["Web Development", "Programming", "Algorithms"]
# Create a set to store unique project names
unique_project_names = set()

# Iterate over skills and extract 3 projects for each skill
projects = []
output = {}
for skill in skills:
    # Find 3 projects for the skill
  skill_projects = db.find({"skills": skill}).limit(10)
# Add the projects to the list, making sure to avoid duplicates
  for project in skill_projects:
      # if project["name"] not in unique_project_names:
      if project["_id"] not in unique_project_names:
          projects.append(project)
          output.update({project["_id"] : project["skills"]})
          # output[project] = project["skills"]
          unique_project_names.add(project["_id"])

  # Return the list of projects
# print(projects)
print(output)
# return jsonify({"projects": projects})

# if __name__ == "__main__":
  # app.run(debug=True)
