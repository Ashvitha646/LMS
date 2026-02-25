# ai_utils.py

# -------------------------------
# Learning dependency graph
# -------------------------------
graph = {
    "Variables": ["Loops", "Data Types"],
    "Data Types": ["Loops"],
    "Loops": ["Functions"],
    "Functions": ["Modules"],
    "Modules": [],
    "Classes": ["Inheritance"],
    "Inheritance": ["Polymorphism"],
    "Polymorphism": ["OOP Projects"],
    "OOP Projects": []
}

# -------------------------------
# Module contents with detailed study material
# -------------------------------
module_content = {
    "Variables": {
        "content": """
Variables are used to store data in memory. In Python, you can assign a value using '='.
Example:
x = 10
y = 'Hello'

Types:
- int
- float
- str
- bool

Tips:
- Use meaningful variable names
- Python is dynamically typed
""",
        "hours": 2
    },
    "Data Types": {
        "content": """
Python Data Types:

1. Numbers: int, float, complex
2. Strings: str
3. Boolean: bool
4. Lists: mutable sequences
5. Tuples: immutable sequences
6. Dictionaries: key-value mapping
7. Sets: unique collection

Operations:
- Arithmetic operators: +, -, *, /
- Comparison operators: ==, !=, <, >
- Logical operators: and, or, not

Best Practices:
- Choose the correct type for efficiency
- Use lists for ordered collections
""",
        "hours": 2
    },
    "Loops": {
        "content": """
Loops allow you to repeat a block of code.

Types:
1. for loop
   Example:
   for i in range(5):
       print(i)

2. while loop
   Example:
   x = 0
   while x < 5:
       print(x)
       x += 1

Nested Loops:
- Loop inside another loop
- Useful for grids, matrices

Tips:
- Avoid infinite loops
- Use break and continue wisely
""",
        "hours": 2
    },
    "Functions": {
        "content": """
Functions help you organize code into reusable blocks.

Syntax:
def function_name(parameters):
    '''Docstring'''
    # code
    return result

Key Points:
- Functions can return values
- Parameters can be positional or keyword
- Use default arguments for flexibility
- Modular code improves readability
""",
        "hours": 3
    },
    "Modules": {
        "content": """
Modules are files containing Python code. They allow code reuse and organization.

Usage:
- import module_name
- from module_name import function_name

Popular built-in modules:
- math
- random
- datetime
- os
- sys

Tips:
- Use virtual environments for project-specific modules
- Create your own modules for larger projects
""",
        "hours": 2
    },
    "Classes": {
        "content": """
Classes are blueprints for creating objects.

Syntax:
class ClassName:
    def __init__(self, attribute1, attribute2):
        self.attribute1 = attribute1
        self.attribute2 = attribute2

Object creation:
obj = ClassName(value1, value2)

Key Points:
- Encapsulation: hide internal data
- Methods operate on objects
""",
        "hours": 2
    },
    "Inheritance": {
        "content": """
Inheritance allows one class to inherit attributes and methods from another class.

Syntax:
class Parent:
    ...

class Child(Parent):
    ...

Key Points:
- Single inheritance
- Multiple inheritance
- Use super() to call parent methods

Benefits:
- Code reusability
- Organized class hierarchy
""",
        "hours": 2
    },
    "Polymorphism": {
        "content": """
Polymorphism allows methods to behave differently based on the object.

Types:
1. Method Overriding
2. Operator Overloading
3. Duck Typing in Python

Example:
class Animal:
    def sound(self):
        print('Generic sound')

class Dog(Animal):
    def sound(self):
        print('Bark')

Tips:
- Makes code flexible
- Important in OOP design
""",
        "hours": 2
    },
    "OOP Projects": {
        "content": """
Project Ideas:
1. Bank Management System
2. Library Management System
3. Student Record System
4. Simple Game using OOP concepts

Tips:
- Apply Classes, Inheritance, and Polymorphism
- Modularize your code using functions and modules
- Document your code properly
""",
        "hours": 3
    }
}

# -------------------------------
# Track user progress (username -> {course: {module: True/False}})
# -------------------------------
user_progress = {}

# -------------------------------
# Functions
# -------------------------------
def mark_module_complete(username, module, course=None):
    """Mark a module as completed by a specific user."""
    if username not in user_progress:
        user_progress[username] = {}
    if course not in user_progress[username]:
        user_progress[username][course] = {}
    user_progress[username][course][module] = True

def get_completed_modules(username, course=None):
    """Return a list of completed modules for a user."""
    if username not in user_progress:
        return []
    if course:
        return [m for m, done in user_progress[username].get(course, {}).items() if done]
    else:
        all_modules = []
        for cdata in user_progress[username].values():
            all_modules.extend([m for m, done in cdata.items() if done])
        return all_modules

def get_recommendations(username, course=None):
    """Suggest the next module based on prerequisites and user progress."""
    completed = set(get_completed_modules(username, course))
    for module, next_modules in graph.items():
        prerequisites = [m for m, deps in graph.items() if module in deps]
        if all(p in completed for p in prerequisites) and module not in completed:
            return module
    return None
