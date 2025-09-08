"""
Conversation Swarm

This module implements a multi-agent conversation system that coordinates debates
and discussions between different trading agents. It supports various coordination
modes for different types of agent interactions.
"""

import logging
from strands.multiagent import Swarm


# Enable debug logs and print them to stderr
logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)


class ConversationSwarm:
    """
    A multi-agent conversation system for coordinating debates and discussions.
    
    This class manages interactions between multiple agents, allowing them to
    collaborate, compete, or use hybrid approaches to analyze trading scenarios
    and reach consensus decisions.
    """
    
    def __init__(self, agents, summarizer_agent, coordination='hybrid'):
        """
        Initialize the ConversationSwarm with agents and coordination strategy.
        
        Args:
            agents (list): List of agent instances to participate in discussions
            summarizer_agent: Agent responsible for synthesizing final decisions
            coordination (str): Coordination mode - 'collaborative', 'competitive', or 'hybrid'
        """
        self.agents = agents
        self.summarizer_agent = summarizer_agent
        self.coordination = coordination
        
    def run(self, task):
        """
        Execute a multi-phase conversation between agents to analyze a task.
        
        The conversation follows a structured approach:
        1. Initial parallel analysis by all agents
        2. Refinement phase where agents respond to each other's insights
        3. Final synthesis by the summarizer agent
        
        Args:
            task (str): The trading task or question to analyze
            
        Returns:
            tuple: (final_solution, messages_dict) containing the synthesized
                   decision and all conversation messages
        """
        
        # Initialize message dictionary to track all agent communications
        messages = {}
        messages[self.summarizer_agent.name] = []
        for agent in self.agents:
            messages[agent.name] = []
        
        print(f"Starting {self.coordination} conversation with {len(self.agents)} agents...")
        # Create a swarm with these agents
        swarm = Swarm(
            self.agents,
            max_handoffs=10,
            max_iterations=10,
            execution_timeout=2400.0,  # 15 minutes
            node_timeout=600.0,       # 5 minutes per agent
            repetitive_handoff_detection_window=8,  # There must be >= 3 unique agents in the last 8 handoffs
            repetitive_handoff_min_unique_agents=5
        )

        # Execute the swarm on a task
        print("Phase 1: Swarm conversation between bull reseacher and bear reseacher...")
        result = swarm(task)

        # Access the final result
        print(f"Status: {result.status}")
        print(f"Node history: {[node.node_id for node in result.node_history]}")

        bull_history, bear_history = None, None
        for message in self.agents[0].messages[::-1]:
            if message["role"] != "assistant" or len(message["content"]) == 0:
                continue
            else:
                print(message["content"])
                for item in message["content"]:
                    if "text" in item:
                        bull_history = item["text"]
                break

        for message in self.agents[1].messages[::-1]:
            if message["role"] != "assistant" or len(message["content"]) == 0:
                continue
            else:
                print(message["content"])
                for item in message["content"]:
                    if "text" in item:
                        bear_history = item["text"]
                        # bear_history = message["content"]["text"]
                break
        print("Phase 2: Final synthesis and decision...")
        
        # Prepare all messages for the summarizer
        # all_messages = "\n\n".join(messages[self.summarizer_agent.name])
        
        summarizer_prompt = f"""
Original Investment Analysis Task:
<query>
{task}
</query>

You have received comprehensive analyses from the research team. Please synthesize 
these inputs into a final investment decision and strategy:

<team_analyses>
Bull Reseacher: 
{bull_history}

Bear Reseacher:
{bear_history}
</team_analyses>

Your synthesis should:
1. Evaluate the strength of arguments from both bull and bear perspectives
2. Identify the most compelling evidence and reasoning
3. Make a clear investment recommendation (Buy, Sell, or Hold)
4. Provide a detailed rationale for your decision
5. Outline specific implementation strategies
6. Address key risks and mitigation approaches

Create a comprehensive final investment plan that incorporates the best insights 
from the team while addressing any concerns or contradictions in their analyses.
"""

        print("Generating final synthesis...")
        final_solution = self.summarizer_agent(summarizer_prompt)
        
        print("Conversation completed successfully!")
        
        return final_solution, bull_history, bear_history