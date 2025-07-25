# crew_manager.py
from crewai import Crew, Process
from agents.search_agent import SearchAgents
from agents.summarizer_agent import SummarizerAgents
from agents.verifier_agent import VerifierAgents
from agents.coordinator_agent import CoordinatorAgents
from tasks.intelligence_tasks import IntelligenceTasks
import os
from dotenv import load_dotenv

load_dotenv() # Ensure env vars are loaded

class IntelligenceCrew:
    def __init__(self, product_topic: str):
        self.product_topic = product_topic
        self.search_agents = SearchAgents()
        self.summarizer_agents = SummarizerAgents()
        self.verifier_agents = VerifierAgents()
        self.coordinator_agents = CoordinatorAgents()
        self.tasks = IntelligenceTasks()

    def run(self):
        # Define agents
        search_agent = self.search_agents.search_agent()
        summarizer_agent = self.summarizer_agents.summarizer_agent()
        verifier_agent = self.verifier_agents.verifier_agent()
        coordinator_agent = self.coordinator_agents.coordinator_agent()

        # Define tasks and assign them to agents
        # Note: CrewAI tasks are often designed to be passed between agents dynamically,
        # but for a linear flow, you can chain them explicitly in the Coordinator.

        # Task 1: Search for URLs
        search_task = self.tasks.search_for_updates(
            agent=search_agent,
            topic=self.product_topic
        )

        # Task 2: Summarize content from URLs (output of search_task)
        # The output of the previous task is automatically passed as input to the next task's tool if chained
        summarize_task = self.tasks.summarize_content(
            agent=summarizer_agent,
            url_list=search_task # CrewAI handles passing outputs if tasks are chained or explicitly referenced
        )

        # Task 3: Verify and filter summaries (output of summarize_task)
        verify_task = self.tasks.verify_and_filter_summaries(
            agent=verifier_agent,
            summaries_json=summarize_task,
            original_topic=self.product_topic
        )

        # Task 4: Generate final report (output of verify_task)
        final_report_task = self.tasks.generate_final_report(
            agent=coordinator_agent,
            validated_summaries_json=verify_task,
            topic=self.product_topic
        )

        # Create the Crew
        crew = Crew(
            agents=[
                search_agent,
                summarizer_agent,
                verifier_agent,
                coordinator_agent
            ],
            tasks=[
                search_task,
                summarize_task,
                verify_task,
                final_report_task
            ],
            verbose=2, # Increased verbosity for detailed logs
            process=Process.sequential # Execute tasks in defined order
        )

        print("## Starting the Competitive Intelligence Crew ##")
        result = crew.kickoff()
        print("\n## Competitive Intelligence Crew Finished ##")
        return result