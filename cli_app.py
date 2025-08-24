from crewai import Crew, LLM
from trip_agents import TripAgents
from trip_tasks import TripTasks
from datetime import datetime, timedelta
import argparse
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os

class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.cities = cities
        self.origin = origin
        self.interests = interests
        self.date_range = date_range
        #self.llm = LLM(model="groq/deepseek-r1-distill-llama-70b")
        self.llm = LLM(model="gemini/gemini-2.0-flash")




    def run(self):
        try:
            agents = TripAgents(llm=self.llm)
            tasks = TripTasks()

            city_selector_agent = agents.city_selection_agent()
            local_expert_agent = agents.local_expert()
            travel_concierge_agent = agents.travel_concierge()

            identify_task = tasks.identify_task(
                city_selector_agent,
                self.origin,
                self.cities,
                self.interests,
                self.date_range
            )

            gather_task = tasks.gather_task(
                local_expert_agent,
                self.origin,
                self.interests,
                self.date_range
            )

            plan_task = tasks.plan_task(
                travel_concierge_agent,
                self.origin,
                self.interests,
                self.date_range
            )

            crew = Crew(
                agents=[
                    city_selector_agent, local_expert_agent, travel_concierge_agent
                ],
                tasks=[identify_task, gather_task, plan_task],
                verbose=True
            )

            result = crew.kickoff()
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format. Please use YYYY-MM-DD")