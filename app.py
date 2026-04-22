from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Default route - welcome message
@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Events API"})

# GET /events - Return all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])

# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Get JSON data from request body
    data = request.get_json()

    # Validate that title exists in the request
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Generate a new unique ID
    new_id = max(event.id for event in events) + 1 if events else 1

    # Create and store the new event
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    # Return the new event with 201 Created status
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<id> - Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Get JSON data from request body
    data = request.get_json()

    # Search for the event by ID
    for event in events:
        if event.id == event_id:
            # Update the title if provided
            if "title" in data:
                event.title = data["title"]
            return jsonify(event.to_dict()), 200

    # Event not found
    return jsonify({"error": "Event not found"}), 404

# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Search for the event by ID
    for event in events:
        if event.id == event_id:
            events.remove(event)
            # Return 204 No Content on success
            return "", 204

    # Event not found
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)