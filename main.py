# #!/usr/bin/env python
# # from FRIDGE_TO_FEAST.crew import FridgeToFeastCrew
# from crew import FridgeToFeastCrew

# def run():
#     print("🍳 Welcome to Fridge-to-Feast Zero-Waste Kitchen Assistant!\n")
#     ingredients = input("Enter your leftover ingredients (comma-separated):\n> ")
    
#     inputs = {
#         'ingredients': ingredients.strip()
#     }

#     try:
#         result = FridgeToFeastCrew().crew().kickoff(inputs=inputs)
#         print("\n" + "="*60)
#         print("🍽️ YOUR ZERO-WASTE MASTERPIECE IS READY!")
#         print("="*60)
#         print("Check: output/final_recipe.md")
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     run()


#!/usr/bin/env python
from crew import FridgeToFeastCrew

print("Welcome to Fridge-to-Feast Zero-Waste Kitchen Assistant!\n")
ingredients = input("Enter your leftover ingredients (comma-separated):\n> ")

crew = FridgeToFeastCrew()
result = crew.run(ingredients)

print("\n" + "="*60)
print("YOUR ZERO-WASTE RECIPE IS READY!")
print("="*60)
print("Check: output/final_recipe.md")