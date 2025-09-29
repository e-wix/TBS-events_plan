from flask import Flask, render_template, request, redirect
import shelve

app = Flask(__name__)
DB_NAME = "events.db"

def get_events():
    with shelve.open(DB_NAME) as db:
        return dict(db)  

@app.route("/")
def home():
    events = get_events()
    return render_template("index.html", events=events)

@app.route("/add_event", methods=["POST"])
def add_event():
    title = request.form["title"]
    description = request.form["description"]
    date = request.form["date"]

    with shelve.open(DB_NAME, writeback=True) as db:
        event_id = str(len(db) + 1)
        db[event_id] = {"title": title, "description": description, "date": date, "votes": []}

    return redirect("/")

@app.route("/vote/<event_id>", methods=["POST"])
def vote(event_id):
    email = request.form["email"]

    with shelve.open(DB_NAME, writeback=True) as db:
        event = db[event_id]
        if email not in event["votes"]: 
            event["votes"].append(email)
        db[event_id] = event

    return redirect("/")

@app.route("/calendar")
def calendar():
    headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    days = [{"name": str(i), "enabled": True} for i in range(1, 31)]

    items = []
    events = get_events()
    for event_id, event in events.items():
        try:
            day = int(event["date"].split("-")[2])  
        except:
            continue

        item = {
            "title": event["title"],
            "className": "task--info",
            "startCol": (day % 7) + 1,  
            "startRow": 1,
            "len": 1,
            "isBottom": False,
            "detailHeader": event["title"],
            "detailContent": event["description"]
        }
        items.append(item)

    return render_template("calendar.html", headers=headers, days=days, items=items)

if __name__ == "__main__":
    app.run(debug=True)
