# app.py - Beautiful Flask Web App
from flask import Flask, render_template, request, jsonify
from crew import FridgeToFeastCrew
import threading
import time
import os

app = Flask(__name__)
current_result = None
is_running = False

def run_crew(ingredients):
    global current_result, is_running
    is_running = True
    try:
        crew = FridgeToFeastCrew()
        result = crew.run(ingredients)
        current_result = result
    except Exception as e:
        current_result = f"Error: {str(e)}"
    finally:
        is_running = False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    global is_running, current_result
    data = request.json
    ingredients = data.get("ingredients", "").strip()
    
    if not ingredients:
        return jsonify({"error": "Please enter some ingredients!"})
    
    if is_running:
        return jsonify({"error": "Already cooking... please wait!"})

    # 🧹 DELETE OLD FINAL RECIPE (safe absolute path)
    try:
        import os

        # Build correct absolute path to /output/final_recipe.md
        output_path = os.path.join(os.path.dirname(__file__), "output", "final_recipe.md")

        if os.path.exists(output_path):
            os.remove(output_path)
            print("Old recipe deleted ✔️", output_path)

    except Exception as e:
        print("Error deleting file:", e)

    
    # Run in background so page stays responsive
    thread = threading.Thread(target=run_crew, args=(ingredients,))
    thread.start()
    
    return jsonify({"status": "cooking"})

@app.route("/status")
def status():
    global is_running, current_result
    if is_running:
        return jsonify({"status": "cooking"})
    if current_result:
        try:
            with open("output/final_recipe.md", "r", encoding="utf-8") as f:
                recipe = f.read()
            return jsonify({"status": "done", "recipe": recipe})
        except:
            return jsonify({"status": "done", "recipe": str(current_result)})
    return jsonify({"status": "waiting"})

startup_cleanup_done = False

@app.before_request
def cleanup_on_start():
    global startup_cleanup_done
    
    if not startup_cleanup_done:
        import os
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "output", "final_recipe.md")

        print("🧹 Startup Cleanup Running…")
        print("DEBUG - Startups Path:", output_path)

        if os.path.exists(output_path):
            os.remove(output_path)
            print("Old recipe deleted at startup!")
        else:
            print("No recipe found at startup.")

        startup_cleanup_done = True



if __name__ == "__main__":
    print("Your Zero-Waste Chef is ready at http://127.0.0.1:5000")
    app.run(debug=True)