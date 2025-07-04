#!/usr/bin/env python3
"""
Memory Inspector for TradingAgents System

This script provides comprehensive tools to inspect, analyze, and manage
the memories stored in the ChromaDB collections used by the TradingAgents
reflection system.
"""

import sys
import os
from pathlib import Path
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd

# Add the parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from strands_agents.tools.memory import FinancialSituationMemory
from strands_agents.default_config import DEFAULT_CONFIG
import chromadb
from chromadb.config import Settings


class MemoryInspector:
    """
    Comprehensive memory inspection tool for TradingAgents system.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the memory inspector."""
        self.config = config or DEFAULT_CONFIG.copy()
        self.chroma_client = chromadb.Client(Settings(allow_reset=True))
        self.memory_collections = {}
        
        # Standard memory collection names used in TradingAgents
        self.standard_collections = [
            "bull_memory",
            "bear_memory", 
            "trader_memory",
            "invest_judge_memory",
            "risk_manager_memory"
        ]
    
    def discover_collections(self) -> List[str]:
        """Discover all available ChromaDB collections."""
        try:
            collections = self.chroma_client.list_collections()
            collection_names = [col.name for col in collections]
            print(f"Found {len(collection_names)} collections:")
            for name in collection_names:
                print(f"  - {name}")
            return collection_names
        except Exception as e:
            print(f"Error discovering collections: {e}")
            return []
    
    def load_collection(self, collection_name: str) -> Optional[Any]:
        """Load a specific collection."""
        try:
            collection = self.chroma_client.get_collection(name=collection_name)
            self.memory_collections[collection_name] = collection
            print(f"✅ Loaded collection: {collection_name}")
            return collection
        except Exception as e:
            print(f"❌ Failed to load collection {collection_name}: {e}")
            return None
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """Get statistics for a collection."""
        try:
            if collection_name not in self.memory_collections:
                self.load_collection(collection_name)
            
            collection = self.memory_collections.get(collection_name)
            if not collection:
                return {}
            
            count = collection.count()
            
            # Get a sample of data to analyze
            sample_data = collection.get(limit=min(count, 100))
            
            stats = {
                "name": collection_name,
                "total_memories": count,
                "sample_size": len(sample_data.get("documents", [])),
                "has_embeddings": bool(sample_data.get("embeddings")),
                "has_metadata": bool(sample_data.get("metadatas")),
                "embedding_dimensions": len(sample_data["embeddings"][0]) if sample_data.get("embeddings") else 0,
            }
            
            # Analyze document lengths
            if sample_data.get("documents"):
                doc_lengths = [len(doc) for doc in sample_data["documents"]]
                stats.update({
                    "avg_document_length": sum(doc_lengths) / len(doc_lengths),
                    "min_document_length": min(doc_lengths),
                    "max_document_length": max(doc_lengths),
                })
            
            # Analyze metadata
            if sample_data.get("metadatas"):
                metadata_keys = set()
                for meta in sample_data["metadatas"]:
                    if meta:
                        metadata_keys.update(meta.keys())
                stats["metadata_keys"] = list(metadata_keys)
            
            return stats
            
        except Exception as e:
            print(f"Error getting stats for {collection_name}: {e}")
            return {"name": collection_name, "error": str(e)}
    
    def inspect_collection_content(self, collection_name: str, limit: int = 10) -> Dict[str, Any]:
        """Inspect the actual content of a collection."""
        try:
            if collection_name not in self.memory_collections:
                self.load_collection(collection_name)
            
            collection = self.memory_collections.get(collection_name)
            if not collection:
                return {}
            
            # Get data with all components
            data = collection.get(
                limit=limit,
                include=["documents", "metadatas", "embeddings", "distances"]
            )
            
            content = {
                "collection_name": collection_name,
                "retrieved_count": len(data.get("documents", [])),
                "memories": []
            }
            
            # Process each memory
            for i in range(len(data.get("documents", []))):
                memory = {
                    "id": data.get("ids", [None])[i],
                    "situation": data.get("documents", [None])[i],
                    "recommendation": data.get("metadatas", [{}])[i].get("recommendation", ""),
                    "embedding_preview": data.get("embeddings", [[]])[i][:5] if data.get("embeddings") else [],
                    "situation_length": len(data.get("documents", [""])[i]),
                    "recommendation_length": len(data.get("metadatas", [{}])[i].get("recommendation", "")),
                }
                content["memories"].append(memory)
            
            return content
            
        except Exception as e:
            print(f"Error inspecting content for {collection_name}: {e}")
            return {"collection_name": collection_name, "error": str(e)}
    
    def search_memories(self, collection_name: str, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Search for memories in a collection using semantic similarity."""
        try:
            # Create a memory instance to use its search functionality
            memory = FinancialSituationMemory(collection_name, self.config)
            results = memory.get_memories(query, n_matches=n_results)
            
            search_results = {
                "collection_name": collection_name,
                "query": query,
                "results_count": len(results),
                "results": []
            }
            
            for result in results:
                search_results["results"].append({
                    "similarity_score": result.get("similarity_score", 0),
                    "matched_situation": result.get("matched_situation", "")[:200] + "..." if len(result.get("matched_situation", "")) > 200 else result.get("matched_situation", ""),
                    "recommendation": result.get("recommendation", "")[:200] + "..." if len(result.get("recommendation", "")) > 200 else result.get("recommendation", ""),
                    "full_situation_length": len(result.get("matched_situation", "")),
                    "full_recommendation_length": len(result.get("recommendation", "")),
                })
            
            return search_results
            
        except Exception as e:
            print(f"Error searching memories in {collection_name}: {e}")
            return {"collection_name": collection_name, "query": query, "error": str(e)}
    
    def analyze_memory_patterns(self, collection_name: str) -> Dict[str, Any]:
        """Analyze patterns in the stored memories."""
        try:
            content = self.inspect_collection_content(collection_name, limit=100)
            
            if "error" in content:
                return content
            
            memories = content.get("memories", [])
            
            analysis = {
                "collection_name": collection_name,
                "total_analyzed": len(memories),
                "patterns": {}
            }
            
            # Analyze situation patterns
            situations = [mem["situation"] for mem in memories if mem.get("situation")]
            recommendations = [mem["recommendation"] for mem in memories if mem.get("recommendation")]
            
            # Common words in situations
            situation_words = []
            for situation in situations:
                situation_words.extend(situation.lower().split())
            
            word_freq = {}
            for word in situation_words:
                if len(word) > 3:  # Skip short words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Top words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            analysis["patterns"]["common_situation_words"] = top_words
            
            # Analyze recommendation patterns
            recommendation_words = []
            for rec in recommendations:
                recommendation_words.extend(rec.lower().split())
            
            rec_word_freq = {}
            for word in recommendation_words:
                if len(word) > 3:
                    rec_word_freq[word] = rec_word_freq.get(word, 0) + 1
            
            top_rec_words = sorted(rec_word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            analysis["patterns"]["common_recommendation_words"] = top_rec_words
            
            # Length analysis
            if situations:
                analysis["patterns"]["situation_lengths"] = {
                    "avg": sum(len(s) for s in situations) / len(situations),
                    "min": min(len(s) for s in situations),
                    "max": max(len(s) for s in situations),
                }
            
            if recommendations:
                analysis["patterns"]["recommendation_lengths"] = {
                    "avg": sum(len(r) for r in recommendations) / len(recommendations),
                    "min": min(len(r) for r in recommendations),
                    "max": max(len(r) for r in recommendations),
                }
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing patterns for {collection_name}: {e}")
            return {"collection_name": collection_name, "error": str(e)}
    
    def export_memories(self, collection_name: str, output_file: str = None) -> str:
        """Export memories to a JSON file."""
        try:
            content = self.inspect_collection_content(collection_name, limit=1000)
            
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"memories_export_{collection_name}_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Exported {collection_name} memories to {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error exporting memories: {e}")
            return ""
    
    def compare_collections(self, collection_names: List[str]) -> Dict[str, Any]:
        """Compare multiple collections."""
        comparison = {
            "collections": collection_names,
            "comparison_date": datetime.now().isoformat(),
            "stats": {},
            "summary": {}
        }
        
        total_memories = 0
        total_collections = 0
        
        for name in collection_names:
            stats = self.get_collection_stats(name)
            comparison["stats"][name] = stats
            
            if "total_memories" in stats:
                total_memories += stats["total_memories"]
                total_collections += 1
        
        comparison["summary"] = {
            "total_collections": total_collections,
            "total_memories_across_all": total_memories,
            "avg_memories_per_collection": total_memories / total_collections if total_collections > 0 else 0,
        }
        
        return comparison
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate a comprehensive memory inspection report."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if not output_file:
                output_file = f"memory_inspection_report_{timestamp}.json"
            
            # Discover all collections
            collections = self.discover_collections()
            
            report = {
                "report_date": datetime.now().isoformat(),
                "total_collections": len(collections),
                "collections": collections,
                "detailed_stats": {},
                "content_samples": {},
                "pattern_analysis": {},
                "comparison": {}
            }
            
            # Get detailed stats for each collection
            for collection_name in collections:
                print(f"\nAnalyzing {collection_name}...")
                
                # Get stats
                stats = self.get_collection_stats(collection_name)
                report["detailed_stats"][collection_name] = stats
                
                # Get content sample
                content = self.inspect_collection_content(collection_name, limit=5)
                report["content_samples"][collection_name] = content
                
                # Analyze patterns
                patterns = self.analyze_memory_patterns(collection_name)
                report["pattern_analysis"][collection_name] = patterns
            
            # Generate comparison
            if collections:
                comparison = self.compare_collections(collections)
                report["comparison"] = comparison
            
            # Save report
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Generated comprehensive report: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return ""


def interactive_memory_inspector():
    """Interactive command-line interface for memory inspection."""
    inspector = MemoryInspector()
    
    print("🔍 TradingAgents Memory Inspector")
    print("=" * 50)
    
    while True:
        print("\nAvailable commands:")
        print("1. discover - Discover all collections")
        print("2. stats <collection_name> - Get collection statistics")
        print("3. inspect <collection_name> [limit] - Inspect collection content")
        print("4. search <collection_name> <query> - Search memories")
        print("5. analyze <collection_name> - Analyze memory patterns")
        print("6. export <collection_name> [filename] - Export memories")
        print("7. compare - Compare all collections")
        print("8. report [filename] - Generate comprehensive report")
        print("9. quit - Exit inspector")
        
        try:
            command = input("\nEnter command: ").strip().split()
            
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == "quit":
                break
            elif cmd == "discover":
                inspector.discover_collections()
            elif cmd == "stats" and len(command) > 1:
                stats = inspector.get_collection_stats(command[1])
                print(json.dumps(stats, indent=2))
            elif cmd == "inspect" and len(command) > 1:
                limit = int(command[2]) if len(command) > 2 else 10
                content = inspector.inspect_collection_content(command[1], limit)
                print(json.dumps(content, indent=2))
            elif cmd == "search" and len(command) > 2:
                query = " ".join(command[2:])
                results = inspector.search_memories(command[1], query)
                print(json.dumps(results, indent=2))
            elif cmd == "analyze" and len(command) > 1:
                analysis = inspector.analyze_memory_patterns(command[1])
                print(json.dumps(analysis, indent=2))
            elif cmd == "export" and len(command) > 1:
                filename = command[2] if len(command) > 2 else None
                inspector.export_memories(command[1], filename)
            elif cmd == "compare":
                collections = inspector.discover_collections()
                comparison = inspector.compare_collections(collections)
                print(json.dumps(comparison, indent=2))
            elif cmd == "report":
                filename = command[1] if len(command) > 1 else None
                inspector.generate_report(filename)
            else:
                print("Invalid command or missing arguments")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main function with command-line argument support."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TradingAgents Memory Inspector")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    parser.add_argument("--discover", "-d", action="store_true", help="Discover all collections")
    parser.add_argument("--stats", "-s", help="Get stats for a specific collection")
    parser.add_argument("--inspect", help="Inspect content of a specific collection")
    parser.add_argument("--limit", type=int, default=10, help="Limit for content inspection")
    parser.add_argument("--search", nargs=2, metavar=("COLLECTION", "QUERY"), help="Search memories")
    parser.add_argument("--analyze", "-a", help="Analyze patterns in a collection")
    parser.add_argument("--export", "-e", help="Export memories from a collection")
    parser.add_argument("--report", "-r", nargs="?", const="auto", help="Generate comprehensive report")
    parser.add_argument("--output", "-o", help="Output filename")
    
    args = parser.parse_args()
    
    inspector = MemoryInspector()
    
    if args.interactive:
        interactive_memory_inspector()
    elif args.discover:
        inspector.discover_collections()
    elif args.stats:
        stats = inspector.get_collection_stats(args.stats)
        print(json.dumps(stats, indent=2))
    elif args.inspect:
        content = inspector.inspect_collection_content(args.inspect, args.limit)
        print(json.dumps(content, indent=2))
    elif args.search:
        results = inspector.search_memories(args.search[0], args.search[1])
        print(json.dumps(results, indent=2))
    elif args.analyze:
        analysis = inspector.analyze_memory_patterns(args.analyze)
        print(json.dumps(analysis, indent=2))
    elif args.export:
        inspector.export_memories(args.export, args.output)
    elif args.report:
        filename = args.output if args.output else None
        inspector.generate_report(filename)
    else:
        # Default: show quick overview
        print("🔍 TradingAgents Memory Inspector - Quick Overview")
        print("=" * 60)
        
        collections = inspector.discover_collections()
        
        if collections:
            print(f"\nFound {len(collections)} collections. Quick stats:")
            for collection_name in collections:
                stats = inspector.get_collection_stats(collection_name)
                memories_count = stats.get("total_memories", 0)
                print(f"  📁 {collection_name}: {memories_count} memories")
        
        print(f"\nUse --help for more options or --interactive for interactive mode")


if __name__ == "__main__":
    main()
