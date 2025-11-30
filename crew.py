# crew.py
from dotenv import load_dotenv
load_dotenv()

import os
import yaml
from crewai import Agent, Crew, Process, Task, llms

# === LOAD YOUR YAML FILES ===
with open('config/agents.yaml', 'r', encoding='utf-8') as f:
    agents_config = yaml.safe_load(f)

with open('config/tasks.yaml', 'r', encoding='utf-8') as f:
    tasks_config = yaml.safe_load(f)

# === GEMINI MODEL (FREE!) ===
GEMINI_MODEL = "gemini/gemini-2.5-flash"

class FridgeToFeastCrew:
    def __init__(self):
        # All agents use FREE Gemini model
        self.ingredient_understander = Agent(
            config=agents_config['ingredient_understander'],
            llm=GEMINI_MODEL,
            verbose=True
        )
        self.recipe_brainstormer = Agent(
            config=agents_config['recipe_brainstormer'],
            llm=GEMINI_MODEL,
            verbose=True
        )
        self.zero_waste_optimizer = Agent(
            config=agents_config['zero_waste_optimizer'],
            llm=GEMINI_MODEL,
            verbose=True
        )
        self.substitution_agent = Agent(
            config=agents_config['substitution_agent'],
            tools=[],
            llm=GEMINI_MODEL,
            verbose=True
        )
        self.step_by_step_cooking = Agent(
            config=agents_config['step_by_step_cooking'],
            llm=GEMINI_MODEL,
            verbose=True
        )
        self.flavor_texture_agent = Agent(
            config=agents_config['flavor_texture_agent'],
            llm=GEMINI_MODEL,
            verbose=True
        )
        self.nutrition_health_agent = Agent(
            config=agents_config['nutrition_health_agent'],
            llm=GEMINI_MODEL,
            verbose=True
        )
        self.cost_saving_agent = Agent(
            config=agents_config['cost_saving_agent'],
            llm=GEMINI_MODEL,
            verbose=True
        )
        self.safety_hygiene_agent = Agent(
            config=agents_config['safety_hygiene_agent'],
            llm=GEMINI_MODEL,
            verbose=True
        )
        self.final_synthesizer = Agent(
            config=agents_config['final_synthesizer'],
            llm=GEMINI_MODEL,
            verbose=True
        )

        # === TASKS ===
        self.understand_ingredients = Task(
            description=tasks_config['understand_ingredients']['description'].replace("{ingredients}", "{ingredients}"),
            expected_output=tasks_config['understand_ingredients']['expected_output'],
            agent=self.ingredient_understander
        )
        self.brainstorm_recipes = Task(
            description=tasks_config['brainstorm_recipes']['description'],
            expected_output=tasks_config['brainstorm_recipes']['expected_output'],
            agent=self.recipe_brainstormer,
            context=[self.understand_ingredients]
        )
        self.optimize_zero_waste = Task(
            description=tasks_config['optimize_zero_waste']['description'],
            expected_output=tasks_config['optimize_zero_waste']['expected_output'],
            agent=self.zero_waste_optimizer,
            context=[self.brainstorm_recipes]
        )
        self.handle_substitutions = Task(
            description=tasks_config['handle_substitutions']['description'],
            expected_output=tasks_config['handle_substitutions']['expected_output'],
            agent=self.substitution_agent,
            context=[self.optimize_zero_waste]
        )
        self.write_cooking_steps = Task(
            description=tasks_config['write_cooking_steps']['description'],
            expected_output=tasks_config['write_cooking_steps']['expected_output'],
            agent=self.step_by_step_cooking,
            context=[self.optimize_zero_waste, self.handle_substitutions]
        )
        self.balance_flavor_texture = Task(
            description=tasks_config['balance_flavor_texture']['description'],
            expected_output=tasks_config['balance_flavor_texture']['expected_output'],
            agent=self.flavor_texture_agent,
            context=[self.write_cooking_steps]
        )
        self.add_nutrition_insights = Task(
            description=tasks_config['add_nutrition_insights']['description'],
            expected_output=tasks_config['add_nutrition_insights']['expected_output'],
            agent=self.nutrition_health_agent,
            context=[self.write_cooking_steps]
        )
        self.calculate_cost_savings = Task(
            description=tasks_config['calculate_cost_savings']['description'],
            expected_output=tasks_config['calculate_cost_savings']['expected_output'],
            agent=self.cost_saving_agent,
            context=[self.write_cooking_steps]
        )
        self.ensure_safety = Task(
            description=tasks_config['ensure_safety']['description'],
            expected_output=tasks_config['ensure_safety']['expected_output'],
            agent=self.safety_hygiene_agent,
            context=[self.write_cooking_steps]
        )
        self.create_final_recipe = Task(
            description=tasks_config['create_final_recipe']['description'],
            expected_output=tasks_config['create_final_recipe']['expected_output'],
            agent=self.final_synthesizer,
            context=[self.optimize_zero_waste, self.write_cooking_steps, self.balance_flavor_texture,
                     self.add_nutrition_insights, self.calculate_cost_savings, self.ensure_safety,
                     self.handle_substitutions],
            output_file="output/final_recipe.md"
        )

    def run(self, ingredients):
        crew = Crew(
            agents=[self.ingredient_understander, self.recipe_brainstormer, self.zero_waste_optimizer,
                    self.substitution_agent, self.step_by_step_cooking, self.flavor_texture_agent,
                    self.nutrition_health_agent, self.cost_saving_agent, self.safety_hygiene_agent,
                    self.final_synthesizer],
            tasks=[self.understand_ingredients, self.brainstorm_recipes, self.optimize_zero_waste,
                   self.handle_substitutions, self.write_cooking_steps, self.balance_flavor_texture,
                   self.add_nutrition_insights, self.calculate_cost_savings, self.ensure_safety,
                   self.create_final_recipe],
            verbose=True,
            process=Process.sequential
        )
        return crew.kickoff(inputs={"ingredients": ingredients})