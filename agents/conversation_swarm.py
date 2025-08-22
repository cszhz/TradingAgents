"""
Conversation Swarm

This module implements a multi-agent conversation system that coordinates debates
and discussions between different trading agents. It supports various coordination
modes for different types of agent interactions.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed


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
        
        # Phase 1: Initial parallel analysis by each specialized agent
        print("Phase 1: Initial analysis by all agents...")
        with ThreadPoolExecutor(max_workers=1) as executor:  # Avoid API throttling
            # Submit tasks to all agents in parallel
            future_to_agent = {executor.submit(agent, task): agent for agent in self.agents}
            
            # Collect results as they complete
            for future in as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    result = future.result()
                    # Share this agent's result with all other agents
                    for key in messages.keys():
                        if key != agent.name:
                            message = f"# Analysis from {agent.name}:\n<input>\n{result}\n</input>"
                            messages[key].append(message)
                            print(f"Shared {agent.name}'s analysis with {key}")
                except Exception as exc:
                    print(f'Agent {agent.name} generated an exception: {exc}')
        
        # Phase 2: Refinement phase - agents respond to each other's insights
        print("Phase 2: Agent refinement and debate...")
        
        # Set coordination role based on strategy
        if self.coordination == "collaborative":
            role = "You are a Collaborative Agent - Focus on building upon others' insights and finding common ground"
        elif self.coordination == "competitive":
            role = "You are a Competitive Agent - Focus on challenging others' views and presenting unique solutions"
        else:  # hybrid
            role = "You are a Hybrid Agent - Balance cooperation and innovation, both supporting and challenging ideas"
        
        # Each agent refines their analysis based on others' input
        for i, agent in enumerate(self.agents):
            print(f"Agent {agent.name} refining analysis...")
            
            # Prepare prompt with original task and other agents' messages
            other_messages = "\n\n".join(messages[agent.name])
            prompt = (
                f"{task}\n\n"
                f"{role}\n\n"
                f"Consider these analyses from other agents:\n"
                f"<messages>\n{other_messages}\n</messages>\n\n"
                f"Provide your refined analysis, addressing their points and strengthening your position."
            )
            
            # Get refined analysis from agent
            result = agent(prompt)
            
            # Share refined analysis with other agents and summarizer
            for key in messages.keys():
                if key != agent.name:
                    refined_message = f"# Refined analysis from {agent.name}:\n<input>\n{result}\n</input>"
                    messages[key].append(refined_message)
            
            print(f"Agent {agent.name} completed refinement")
        
        # Phase 3: Final synthesis by summarizer agent
        print("Phase 3: Final synthesis and decision...")
        
        # Prepare all messages for the summarizer
        all_messages = "\n\n".join(messages[self.summarizer_agent.name])
        
        summarizer_prompt = f"""
Original Investment Analysis Task:
<query>
{task}
</query>

You have received comprehensive analyses from the research team. Please synthesize 
these inputs into a final investment decision and strategy:

<team_analyses>
{all_messages}
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
        
        return final_solution, messages