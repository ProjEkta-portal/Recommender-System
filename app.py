from fastapi import FastAPI, HTTPException, Request
import httpx

app = FastAPI()

# You don't need the dotenv library in FastAPI. Environment variables can be accessed directly.

# data = httpx.get("http://localhost:5000/api/projects")
# projects = data.json()

@app.post("/recommend-projects")
async def get_projects(request: Request):
    # Get JSON body from request
    json_body = await request.json()

    # Extract skills from JSON body
    skills = json_body["skills"]
    projects = []
    unique_project_names = set()

    # Make a GET request to the backend API to fetch project data
    backend_api_url = "https://eager-bass-sombrero.cyclic.cloud/api/projects"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(backend_api_url)

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
        raise HTTPException(status_code=500, detail="Failed to fetch project data from the backend API")

    # Return the list of projects
    return {"recommended_projects": projects}
