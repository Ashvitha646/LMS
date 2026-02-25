from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from ai_utils import get_recommendations, mark_module_complete, get_completed_modules
import google.generativeai as genai

# ---------------------------------------------------
# Initialize Flask
# ---------------------------------------------------
app = Flask(__name__)
app.secret_key = "secret123"

# ---------------------------------------------------
# Configure Gemini AI
# ---------------------------------------------------
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")  # Replace with your Gemini API key
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------------------------------------------
# Course Data
# ---------------------------------------------------
courses = {
    "Python Basics": {
        "Variables": {"content": "Learn about Python variables, types, and memory allocation.", "hours": 1},
        "Loops": {"content": "Understand Python loops: for, while, and nested loops.", "hours": 2},
        "Functions": {"content": "Explore Python functions, parameters, and return types.", "hours": 2},
    },
    "OOP": {
        "Classes": {"content": "Learn object-oriented concepts: classes and objects.", "hours": 2},
        "Inheritance": {"content": "Understand inheritance and code reusability in Python.", "hours": 2},
        "Polymorphism": {"content": "Explore polymorphism and method overriding in Python.", "hours": 2},
    }
}

# ---------------------------------------------------
# AI Response (Hybrid Mode)
# ---------------------------------------------------
def get_ai_response(prompt):
    """Returns an AI-generated or fallback response."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("⚠️ Gemini AI Error:", e)
        return "🤖 I couldn’t connect to AI, but here’s something basic:\n" \
               f"{prompt.split('.')[0]} — this is an important concept. Let’s study it together!"

# ---------------------------------------------------
# Login Page
# ---------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
        return redirect("/courses")
    return render_template("login.html", error=None)

# ---------------------------------------------------
# Courses Page
# ---------------------------------------------------
@app.route("/courses")
def courses_page():
    username = session.get("username")
    if not username:
        return redirect("/")
    return render_template("courses.html", courses=courses.keys())

# ---------------------------------------------------
# Modules Page
# ---------------------------------------------------
@app.route("/course/<cname>")
def modules_page(cname):
    username = session.get("username")
    if not username:
        return redirect("/")
    modules = courses.get(cname)
    return render_template("modules.html", course=cname, modules=modules)

# ---------------------------------------------------
# Module Content Page
# ---------------------------------------------------
@app.route("/course/<cname>/<mname>")
def module_content(cname, mname):
    username = session.get("username")
    if not username:
        return redirect("/")
    details = courses[cname][mname]
    mark_module_complete(username, mname)
    recommendation = get_recommendations(username)
    return render_template(
        "module_content.html",
        course=cname,
        module=mname,
        details=details,
        recommendation=recommendation,
        username=username
    )

# ---------------------------------------------------
# AI Chat (AJAX)
# ---------------------------------------------------
@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    data = request.get_json()
    user_message = data.get("message", "")
    response = get_ai_response(user_message)
    return jsonify({"response": response})

# ---------------------------------------------------
# Quiz Page
# ---------------------------------------------------
@app.route("/quiz/<course>/<module>", methods=["GET", "POST"])
def quiz(course, module):
    username = session.get("username")
    if not username:
        return redirect("/")

    from ai_utils import module_content

    # Generate questions dynamically based on module content
    details = module_content.get(module, {})
    topic = details.get("content", "")
    
    questions = [
        f"Explain the key concept of '{module}'.",
        f"Give an example or application related to '{module}'.",
        f"Why is '{module}' important in {course}?",
        f"Summarize the main points of '{module}'."
    ]

    if request.method == "POST":
        # Optionally, you can capture answers from form here
        answers = {f"answer_{i+1}": request.form.get(f"answer_{i+1}") for i in range(len(questions))}
        mark_module_complete(username, module, course=course)
        next_module = get_recommendations(username, course=course)
        if next_module:
            return redirect(url_for("module_content_page", cname=course, mname=next_module))
        else:
            return redirect(url_for("summary", course_name=course))

    return render_template("quiz.html", course=course, module=module, questions=questions)
# ---------------------------------------------------
# Summary Page
# ---------------------------------------------------
@app.route("/summary/<course_name>")
def summary(course_name):
    username = session.get("username")
    if not username:
        return redirect("/")
    scores = {m: 80 for m in courses[course_name]}
    hours = sum(courses[course_name][m]["hours"] for m in courses[course_name])
    recommendation = get_recommendations(username)
    return render_template(
        "summary.html",
        username=username,
        course_name=course_name,
        scores=scores,
        hours=hours,
        recommendation=recommendation
    )

# ---------------------------------------------------
# Logout
# ---------------------------------------------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")
@app.route('/progress/<cname>')
def progress_chart(cname):
    username = "ashvitha"  # or fetch dynamically
    scores = {
        "Variables": 80,
        "Data Types": 80,
        "Loops": 80,
        "Functions": 80,
        "Modules": 80
    }
    return render_template('progress.html', course_name=cname, scores=scores)


# ---------------------------------------------------
# Run
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
