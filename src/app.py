"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports Activities
    "Basketball Team": {
        "description": "Competitive basketball training and inter-school tournaments",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Soccer skills development and friendly matches",
        "schedule": "Tuesdays and Fridays, 3:45 PM - 5:15 PM",
        "max_participants": 22,
        "participants": ["maria@mergington.edu", "carlos@mergington.edu"]
    },
    # Artistic Activities
    "Drama Club": {
        "description": "Theater performances, acting workshops, and script writing",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["isabella@mergington.edu", "james@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, sculpture, and mixed media art projects",
        "schedule": "Thursdays, 3:00 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["lily@mergington.edu"]
    },
    # Intellectual Activities
    "Debate Society": {
        "description": "Public speaking, argumentation skills, and competitive debates",
        "schedule": "Mondays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["nathan@mergington.edu", "grace@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Competitive science events covering biology, chemistry, physics, and engineering",
        "schedule": "Saturdays, 9:00 AM - 12:00 PM",
        "max_participants": 20,
        "participants": ["ethan@mergington.edu", "zoe@mergington.edu", "ryan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if student is already registered
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail=f"Student {email} is already registered for {activity_name}")

    # Check if activity is at capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail=f"Activity {activity_name} is full (max {activity['max_participants']} participants)")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Successfully signed up {email} for {activity_name}"}
