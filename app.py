from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os


app = Flask(__name__)
app.secret_key = "kenhub_secret"

# --- KenChat data ---
chatrooms = {"general": []}
MAX_MESSAGES = 6
MAX_USERNAME = 20
MAX_TEXT = 100

# --- KenWiki setup ---
WIKI_PASSWORD = "kenbotizdead"
ENTRIES_FILE = "entries.json"
ADMIN_PASSWORD = "ilovemarkxdialeryaoi"

if not os.path.exists(ENTRIES_FILE):
    with open(ENTRIES_FILE, "w") as f:
        json.dump({}, f)

def load_entries():
    with open(ENTRIES_FILE, "r") as f:
        return json.load(f)

def save_entries(entries):
    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=4)

# --- Routes ---
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/kenchat")
def kenchat():
    username = request.args.get("username", "")
    room = request.args.get("room", "general")
    if room not in chatrooms:
        chatrooms[room] = []
    messages = chatrooms[room]
    return render_template("kenchat.html", messages=messages, username=username, room=room, rooms=list(chatrooms.keys()))

@app.route("/send_win98", methods=["POST"])
def send_win98():
    user = request.form.get("user", "Anon")[:MAX_USERNAME]
    text = request.form.get("text", "")[:MAX_TEXT]
    room = request.form.get("room", "general")
    if room not in chatrooms:
        chatrooms[room] = []
    if text.strip():
        if text.lower().startswith("oevhwEHIUWEVHOUWEHWUEVHUWEGHhhfjfuehejjjj "):
            query = text[8:].strip()
            chatrooms[room].append({"user": user, "text": query})
            bot_reply = chat_with_bot(query)
            chatrooms[room].append({"user": "KenBot", "text": bot_reply})
        else:
            chatrooms[room].append({"user": user, "text": text})
        if len(chatrooms[room]) > MAX_MESSAGES:
            chatrooms[room].pop(0)
    return redirect(url_for("kenchat", username=user, room=room))



# --- Wiki routes ---
@app.route("/wiki")
def wiki_home():
    entries = load_entries()
    return render_template("wiki_index.html", entries=entries)

@app.route("/wiki/entry/<title>")
def wiki_entry(title):
    entries = load_entries()
    content = entries.get(title)
    if content is None:
        return f"Entry '{title}' not found.", 404
    return render_template("wiki_view.html", title=title, content=content)

@app.route("/wiki/login", methods=["GET","POST"])
def wiki_login():
    if request.method=="POST":
        if request.form.get("password") == WIKI_PASSWORD:
            session["wiki_logged_in"] = True
            flash("Logged in! You can create/edit/delete entries.", "success")
            return redirect(url_for("wiki_home"))
        else:
            flash("Wrong password!", "danger")
    return render_template("wiki_login.html")

@app.route("/wiki/logout")
def wiki_logout():
    session.pop("wiki_logged_in", None)
    flash("Logged out!", "info")
    return redirect(url_for("wiki_home"))

@app.route("/wiki/create", methods=["GET","POST"])
def wiki_create():
    if not session.get("wiki_logged_in"):
        flash("You must log in to create entries.", "warning")
        return redirect(url_for("wiki_login"))
    if request.method=="POST":
        title = request.form.get("title")
        content = request.form.get("content")
        entries = load_entries()
        if title in entries:
            flash("Entry exists!", "danger")
        else:
            entries[title] = content
            save_entries(entries)
            flash(f"Entry '{title}' created!", "success")
            return redirect(url_for("wiki_entry", title=title))
    return render_template("wiki_create.html")

@app.route("/wiki/edit/<title>", methods=["GET","POST"])
def wiki_edit(title):
    if not session.get("wiki_logged_in"):
        flash("You must log in to edit entries.", "warning")
        return redirect(url_for("wiki_login"))
    entries = load_entries()
    content = entries.get(title)
    if content is None:
        flash(f"Entry '{title}' not found!", "danger")
        return redirect(url_for("wiki_home"))
    if request.method=="POST":
        new_content = request.form.get("content")
        entries[title] = new_content
        save_entries(entries)
        flash(f"Entry '{title}' updated!", "success")
        return redirect(url_for("wiki_entry", title=title))
    return render_template("wiki_edit.html", title=title, content=content)

@app.route("/wiki/delete/<title>", methods=["POST"])
def wiki_delete(title):
    if not session.get("wiki_logged_in"):
        flash("You must log in to delete entries.", "warning")
        return redirect(url_for("wiki_login"))
    entries = load_entries()
    if title in entries:
        del entries[title]
        save_entries(entries)
        flash(f"Entry '{title}' deleted!", "success")
    return redirect(url_for("wiki_home"))

# --- KenChat Admin ---
@app.route("/admin", methods=["GET","POST"])
def admin_panel():
    if request.method=="POST":
        if request.form.get("password")==ADMIN_PASSWORD:
            session["admin_logged_in"]=True
            flash("Admin logged in!", "success")
            return redirect(url_for("admin_panel"))
        else:
            flash("Wrong password!", "danger")
    if not session.get("admin_logged_in"):
        return render_template("kenchat_admin_login.html")
    return render_template("kenchat_admin.html", rooms=list(chatrooms.keys()))

@app.route("/create_room", methods=["POST"])
def create_room():
    if not session.get("admin_logged_in"):
        flash("You must log in as admin.", "warning")
        return redirect(url_for("admin_panel"))
    room_name = request.form.get("new_room")
    if room_name and room_name not in chatrooms:
        chatrooms[room_name] = []
    return redirect(url_for("admin_panel"))

@app.route("/delete_room", methods=["POST"])
def delete_room():
    if not session.get("admin_logged_in"):
        flash("You must log in as admin.", "warning")
        return redirect(url_for("admin_panel"))
    room_name = request.form.get("room_name")
    if room_name in chatrooms and room_name != "general":
        del chatrooms[room_name]
    return redirect(url_for("admin_panel"))

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Admin logged out!", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


