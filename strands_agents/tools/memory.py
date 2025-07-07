
from strands import tool,Agent
import chromadb
from typing import List,Dict,Any
from chromadb.config import Settings
from openai import OpenAI
import boto3
import json
from pydantic_core import core_schema
class FinancialSituationMemory:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.any_schema()

    def __init__(self, name, config):
        self.config = config
        self.embedding_provider = config.get("embedding_provider", "openai")
        
        if config["backend_url"] == "http://localhost:11434/v1":
            self.embedding = "nomic-embed-text"
            self.embedding_provider = "ollama"
        else:
            self.embedding = config.get("embedding_model")
        
        # Initialize clients based on embedding provider
        if self.embedding_provider == "bedrock":
            # Initialize Bedrock client for embeddings
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=config.get("aws_region", "us-east-1")
            )
        else:
            # Use OpenAI client for embeddings
            self.client = OpenAI(base_url=config["backend_url"])
        
        self.chroma_client = chromadb.PersistentClient(path=config['chromadb_path'], settings=Settings(allow_reset=True))
        self.situation_collection = self.chroma_client.get_or_create_collection(name=name)

    def get_embedding(self, text):
        """Get embedding for a text using the configured provider"""
        
        if self.embedding_provider == "bedrock":
            return self._get_bedrock_embedding(text)
        else:
            return self._get_openai_embedding(text)
    
    def _get_bedrock_embedding(self, text):
        """Get embedding using Amazon Bedrock Titan model"""
        try:
            # Prepare the request body for Titan embedding model
            body = json.dumps({
                "inputText": text[:8192], # Titan v2 supports up to 8192
                "dimensions": 1024,  # Titan v2 supports up to 1024 dimensions
                "normalize": True
            })
            
            # Call Bedrock
            response = self.bedrock_client.invoke_model(
                modelId=self.embedding,
                body=body,
                contentType='application/json',
                accept='application/json'
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            embedding = response_body.get('embedding')
            
            if not embedding:
                raise ValueError("No embedding returned from Bedrock")
                
            return embedding
            
        except Exception as e:
            print(f"Error getting Bedrock embedding: {e}")
            # Fallback to OpenAI if Bedrock fails and OpenAI client is available
            if hasattr(self, 'client'):
                print("Falling back to OpenAI embedding...")
                return self._get_openai_embedding(text)
            else:
                raise e
    
    def _get_openai_embedding(self, text):
        """Get embedding using OpenAI-compatible API"""
        response = self.client.embeddings.create(
            model=self.embedding, input=text
        )
        return response.data[0].embedding

    def add_situations(self, situations_and_advice):
        """Add financial situations and their corresponding advice. Parameter is a list of tuples (situation, rec)"""
        print(f"\n----------add_situations called with {len(situations_and_advice)} items\n")
        situations = []
        advice = []
        ids = []
        embeddings = []

        offset = self.situation_collection.count()

        for i, (situation, recommendation) in enumerate(situations_and_advice):
            situations.append(situation)
            advice.append(recommendation)
            ids.append(str(offset + i))
            embeddings.append(self.get_embedding(situation))

        self.situation_collection.add(
            documents=situations,
            metadatas=[{"recommendation": rec} for rec in advice],
            embeddings=embeddings,
            ids=ids,
        )

    def get_memories(self, current_situation, n_matches=1):
        """Find matching recommendations using configured embedding provider"""
        query_embedding = self.get_embedding(current_situation)

        results = self.situation_collection.query(
            query_embeddings=[query_embedding],
            n_results=n_matches,
            include=["metadatas", "documents", "distances"],
        )

        matched_results = []
        for i in range(len(results["documents"][0])):
            matched_results.append(
                {
                    "matched_situation": results["documents"][0][i],
                    "recommendation": results["metadatas"][0][i]["recommendation"],
                    "similarity_score": 1 - results["distances"][0][i],
                }
            )

        return matched_results
    
@tool
def get_financial_situation_memories(current_situation: str, n_matches: int,agent: Agent):
    """Get memories from the financial situation memory. they are past reflections on mistakes
    
    Args:
        current_situation (str):  A detail description of current financial situation, including whatever information you have about the company and market, use this value to sementic search the memory bank to retrieve past reflections on mistakes
        n_matches (int): defaut is 1
    """
    memory_name = agent.state.get("memory_name")
    config = agent.state.get("config")
    memory = FinancialSituationMemory(memory_name,config)
    return memory.get_memories(current_situation, n_matches) if memory else ""

@tool
def add_financial_situation_memories(situations_and_advice: List[Dict[str,str]],agent: Agent):
    """Add memories to the financial situation memory. they are past reflections on mistakes
    
    Args:
        situations_and_advice (list): list, Parameter is a list of tuples (situation, rec), financial situations and their corresponding recommendation advice. The situation is a detail description of current financial situation, including whatever information you have about the company and market,
    """
    memory_name = agent.state.get("memory_name")
    config = agent.state.get("config")
    memory = FinancialSituationMemory(memory_name,config)
    memory.add_situations(situations_and_advice)
