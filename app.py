from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import requests
import os
load_dotenv()

# PASSWORD = os.getenv('PASS')
app = Flask(__name__)


# data = requests.get("http://localhost:5000/api/projects")
# projects = data.json()
# Get HTTP request from frontend
@app.route("/recommend-projects", methods=["POST"])
def get_projects():
#   # Get JSON body from request
  json_body = request.get_json()

  # Extract skills from JSON body
  skills = json_body["skills"]
  projects = []
  unique_project_names = set()

  # Make a GET request to the backend API to fetch project data
  # backend_api_url = "http://localhost:5000/api/projects"
  backend_api_url = "https://eager-bass-sombrero.cyclic.cloud/api/projects"
  response = requests.get(backend_api_url)

  # Check if the API request was successful
  if response.status_code == 200:
      project_data = response.json()
      # Iterate through the skills and find 3 projects for each skill
      for skill in skills:
          skill_projects = [project for project in project_data if skill in project["tags"]]
          skill_projects = skill_projects[:3]  # Limit to 3 projects per skill

          # Add the projects to the list, making sure to avoid duplicates
          for project in skill_projects:
              if project["name"] not in unique_project_names:
                  projects.append(project)
                  unique_project_names.add(project["name"])
  else:
      # return 0
      return jsonify({"error": "Failed to fetch project data from the backend API"}), 500

  # Return the list of projects
  return jsonify({"recommended_projects": projects})

if __name__ == "__main__":
  app.run(debug=True)