# ai_utils.py
from openai import OpenAI

# -----------------------------
# 1️⃣ OpenAI Client Setup
# -----------------------------
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def get_embedding(text):
    """Return the embedding vector for a piece of text."""
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return resp.data[0].embedding

# -----------------------------
# 2️⃣ Directed Graph for Learning Pathways
# -----------------------------
graph = {
    "Arrays": ["Stacks"],
    "Stacks": ["Queues"],
    "Queues": [],
    "Classes": ["Inheritance"],
    "Inheritance": ["Polymorphism"],
    "Polymorphism": [],
    "SQL Basics": ["Normalization"],
    "Normalization": ["Transactions"],
    "Transactions": []
}

# -----------------------------
# 3️⃣ Hash Table to Track Progress
# -----------------------------
user_progress = {}

def mark_module_complete(username, module):
    """Mark a specific module as completed by the user."""
    if username not in user_progress:
        user_progress[username] = {}
    user_progress[username][module] = True

def get_completed_modules(username):
    """Return list of completed modules for a user."""
    return [m for m, done in user_progress.get(username, {}).items() if done]

# -----------------------------
# 4️⃣ Dynamic Programming / DFS for Optimal Path
# -----------------------------
def find_learning_path(start):
    """Find the optimal path from the given module."""
    path = []
    visited = set()

    def dfs(module):
        visited.add(module)
        path.append(module)
        for next_module in graph.get(module, []):
            if next_module not in visited:
                dfs(next_module)

    dfs(start)
    return path

# -----------------------------
# 5️⃣ AI Recommendation (Mock + Embedding-ready)
# -----------------------------
def get_recommendations(username):
    """
    Recommend the next module based on user's completed modules.
    (You can extend this to use embeddings for personalized ranking.)
    """
    completed = set(get_completed_modules(username))
    for module in graph:
        prerequisites = [m for m, nexts in graph.items() if module in nexts]
        if all(p in completed for p in prerequisites) and module not in completed:
            return f"✅ Next recommended module: {module}"
    return "🎉 All modules completed!"

# -----------------------------
# 6️⃣ Optional: Knowledge Tree
# -----------------------------
def build_knowledge_tree():
    roots = [node for node in graph if not any(node in children for children in graph.values())]
    tree = {root: build_subtree(root) for root in roots}
    return tree

def build_subtree(node):
    return {child: build_subtree(child) for child in graph[node]}
