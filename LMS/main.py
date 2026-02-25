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
# Course Data with Expanded Modules
# ---------------------------------------------------
courses = {
    "Python Basics": ["Variables", "Data Types", "Loops", "Functions", "Modules"],
    "OOP": ["Classes", "Inheritance", "Polymorphism", "OOP Projects"]
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
    module_names = courses.get(cname, [])
    from ai_utils import module_content
    modules = {m: module_content[m] for m in module_names if m in module_content}
    return render_template("modules.html", course=cname, modules=modules)

# ---------------------------------------------------
# Module Content Page
# ---------------------------------------------------
@app.route("/course/<cname>/<mname>")
def module_content_page(cname, mname):
    username = session.get("username")
    if not username:
        return redirect("/")
    from ai_utils import module_content
    details = module_content.get(mname)
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

    module_questions = {
        "Variables": [
            "What are variables and why are they used in Python?",
            "Give an example of declaring and using a variable."
        ],
        "Data Types": [
            "Explain the different data types in Python.",
            "How would you convert between different data types?"
        ],
        "Loops": [
            "Describe the types of loops in Python and their uses.",
            "Write an example of a 'for' loop iterating over a list."
        ],
        "Functions": [
            "What is a function and why are functions important?",
            "Demonstrate a simple function with parameters and return value."
        ],
        "Modules": [
            "What is a Python module and how do you use it?",
            "Give an example of importing and using a module."
        ],
        "Classes": [
            "Explain the concept of a class in OOP.",
            "Create a simple class with attributes and methods."
        ],
        "Inheritance": [
            "What is inheritance in OOP?",
            "Provide an example of a parent and child class in Python."
        ],
        "Polymorphism": [
            "Define polymorphism and its types in OOP.",
            "Give an example demonstrating method overriding."
        ],
        "OOP Projects": [
            "Explain how OOP concepts are applied in a real project.",
            "Describe one small project you can implement using classes."
        ]
    }

    questions = module_questions.get(module, [
        "Explain the key concept of this module.",
        "Give an example related to this module."
    ])

    if request.method == "POST":
        mark_module_complete(username, module)
        next_module = get_recommendations(username)
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
    from ai_utils import module_content
    scores = {m: 80 for m in courses[course_name]}
    hours = sum(module_content[m]["hours"] for m in courses[course_name])
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
# Progress Chart Page
# ---------------------------------------------------
@app.route('/progress/<course_name>')
def progress_chart(course_name):
    username = session.get("username", "Student")
    scores = {m: 80 for m in courses[course_name]}
    return render_template('progress.html', course_name=course_name, scores=scores)

# ---------------------------------------------------
# Logout
# ---------------------------------------------------
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

# ---------------------------------------------------
# Run the app
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
