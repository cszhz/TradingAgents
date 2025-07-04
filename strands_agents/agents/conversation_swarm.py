from concurrent.futures import ThreadPoolExecutor, as_completed

class ConversationSwarm:
    def __init__(self,agents,summarizer_agent,coordination='hybrid'):
        self.agents = agents
        self.summarizer_agent = summarizer_agent
        self.coordination = coordination
        
    def run(self, task):
        
        #Init message dict
        messages = {}
        messages[self.summarizer_agent.name]=[]
        for i, agent in enumerate(self.agents):
            messages[agent.name]=[]
        # Phase 1 Initial analysis by each specialized agent (parallel)
        with ThreadPoolExecutor(max_workers=len(self.agents)) as executor:
            future_to_agent = {executor.submit(agent, task): agent for agent in self.agents}
            
            for future in as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    result = future.result()
                    for key in messages.keys():
                        if not key == agent.name:
                            messages[key].append(f"# From {agent.name}: \n{result}")
                except Exception as exc:
                    print(f'Agent {agent.name} generated an exception: {exc}')
        
        # Phase 2: Each agent refines based on input from others
        if self.coordination == "collaborative":
            role = f"you are Collaborative Agent - Focus on building upon others' insights"
        elif self.coordination == "competitive":
            role = f"you are Competitive Agent- Focus on finding unique solutions"
        else:  # hybrid
            role = f"you are Hybrid Agent- Balance cooperation and innovation"
        for i, agent in enumerate(self.agents):
            prompt = f"{task}\n\n{role}\nConsider these messages from other agents:\n" + "\n\n".join(messages[agent.name])
            result = agent(prompt)
            messages[self.summarizer_agent.name].append(f"# From {agent.name} (Phase 2):\n{result}")
            
        # Final phase: Summarizer creates the final solution
        summarizer_prompt = f"""
Original query: {task}

Please synthesize the following inputs from all agents into a comprehensive final solution:

{"\n\n".join(messages[self.summarizer_agent.name])}

Create a well-structured final answer that incorporates the research findings, 
creative ideas, and addresses the critical feedback.
"""
        print(f"-------summarizer_prompt-------------:\n{summarizer_prompt}")
        final_solution = self.summarizer_agent(summarizer_prompt)

        return final_solution