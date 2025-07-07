#!/usr/bin/env python3
"""
Simple Memory Viewer for TradingAgents System

A straightforward script to quickly view and analyze the memories
stored in the TradingAgents reflection system.
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add the parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from strands_agents.tools.memory import FinancialSituationMemory
from strands_agents.default_config import DEFAULT_CONFIG
import chromadb
from chromadb.config import Settings
config = DEFAULT_CONFIG.copy()


def view_all_collections():
    """View all available memory collections and their basic info."""
    print("🔍 TradingAgents Memory Collections")
    print("=" * 50)
    try:
        client = chromadb.PersistentClient(path=config["chromadb_path"],settings=Settings(allow_reset=True))
        collections = client.list_collections()
        
        if not collections:
            print("No memory collections found.")
            return
        
        print(f"Found {len(collections)} memory collections:\n")
        
        for collection in collections:
            try:
                count = collection.count()
                print(f"📁 {collection.name}")
                print(f"   └── {count} memories stored")
                
                # Get a sample to show what's inside
                if count > 0:
                    sample = collection.get(limit=1, include=["documents", "metadatas"])
                    if sample.get("documents"):
                        doc_preview = sample["documents"][0][:100] + "..." if len(sample["documents"][0]) > 100 else sample["documents"][0]
                        print(f"   └── Sample: {doc_preview}")
                print()
                
            except Exception as e:
                print(f"   └── Error reading collection: {e}")
                print()
    
    except Exception as e:
        print(f"Error accessing ChromaDB: {e}")


def view_collection_details(collection_name: str):
    """View detailed information about a specific collection."""
    print(f"📋 Collection Details: {collection_name}")
    print("=" * 50)
    
    try:
        memory = FinancialSituationMemory(collection_name, DEFAULT_CONFIG)
        
        # Get collection stats
        client = chromadb.PersistentClient(path=config["chromadb_path"],settings=Settings(allow_reset=True))
        collection = client.get_collection(name=collection_name)
        count = collection.count()
        
        print(f"Total memories: {count}")
        
        if count == 0:
            print("No memories stored in this collection.")
            return
        
        # Get all data
        data = collection.get(
            limit=min(count, 50),  # Limit to first 50 for display
            include=["documents", "metadatas", "embeddings"]
        )
        
        print(f"Showing first {len(data.get('documents', []))} memories:\n")
        
        for i, (doc, meta) in enumerate(zip(data.get("documents", []), data.get("metadatas", []))):
            print(f"Memory #{i+1}:")
            print(f"  📄 Situation: {doc[:200]}{'...' if len(doc) > 200 else ''}")
            
            recommendation = meta.get("recommendation", "") if meta else ""
            print(f"  💡 Recommendation: {recommendation[:200]}{'...' if len(recommendation) > 200 else ''}")
            
            # Fix the array ambiguity issue
            embeddings = data.get("embeddings")
            if embeddings is not None and len(embeddings) > i:
                try:
                    embedding_preview = embeddings[i][:5] if len(embeddings[i]) > 5 else embeddings[i]
                    print(f"  🔢 Embedding preview: {embedding_preview}")
                except (IndexError, TypeError):
                    print(f"  🔢 Embedding: Available but cannot preview")
            
            print(f"  📏 Lengths: Situation={len(doc)}, Recommendation={len(recommendation)}")
            print("-" * 60)
    
    except Exception as e:
        print(f"Error viewing collection {collection_name}: {e}")


def search_memories(collection_name: str, query: str, n_results: int = 5):
    """Search for memories using semantic similarity."""
    print(f"🔍 Searching '{query}' in {collection_name}")
    print("=" * 50)
    
    try:
        memory = FinancialSituationMemory(collection_name, DEFAULT_CONFIG)
        results = memory.get_memories(query, n_matches=n_results)
        
        if not results:
            print("No matching memories found.")
            return
        
        print(f"Found {len(results)} matching memories:\n")
        
        for i, result in enumerate(results, 1):
            similarity = result.get("similarity_score", 0)
            situation = result.get("matched_situation", "")
            recommendation = result.get("recommendation", "")
            
            print(f"Result #{i} (Similarity: {similarity:.3f})")
            print(f"  📄 Situation: {situation[:300]}{'...' if len(situation) > 300 else ''}")
            print(f"  💡 Recommendation: {recommendation[:300]}{'...' if len(recommendation) > 300 else ''}")
            print("-" * 60)
    
    except Exception as e:
        print(f"Error searching memories: {e}")


def analyze_collection_patterns(collection_name: str):
    """Analyze patterns in a memory collection."""
    print(f"📊 Pattern Analysis: {collection_name}")
    print("=" * 50)
    
    try:
        client = chromadb.PersistentClient(path=config["chromadb_path"],settings=Settings(allow_reset=True))
        collection = client.get_collection(name=collection_name)
        count = collection.count()
        
        if count == 0:
            print("No memories to analyze.")
            return
        
        # Get data for analysis
        data = collection.get(
            limit=min(count, 100),
            include=["documents", "metadatas"]
        )
        
        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])
        
        print(f"Analyzing {len(documents)} memories...\n")
        
        # Length analysis
        doc_lengths = [len(doc) for doc in documents]
        rec_lengths = [len(meta.get("recommendation", "")) for meta in metadatas if meta]
        
        print("📏 Length Statistics:")
        print(f"  Situations - Avg: {sum(doc_lengths)/len(doc_lengths):.0f}, Min: {min(doc_lengths)}, Max: {max(doc_lengths)}")
        if rec_lengths:
            print(f"  Recommendations - Avg: {sum(rec_lengths)/len(rec_lengths):.0f}, Min: {min(rec_lengths)}, Max: {max(rec_lengths)}")
        
        # Word frequency analysis
        print("\n🔤 Common Words in Situations:")
        all_words = []
        for doc in documents:
            words = doc.lower().split()
            all_words.extend([word for word in words if len(word) > 3 and word.isalpha()])
        
        word_freq = {}
        for word in all_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        for word, freq in top_words:
            print(f"  {word}: {freq} times")
        
        # Recommendation analysis
        print("\n💡 Common Words in Recommendations:")
        rec_words = []
        for meta in metadatas:
            if meta and meta.get("recommendation"):
                words = meta["recommendation"].lower().split()
                rec_words.extend([word for word in words if len(word) > 3 and word.isalpha()])
        
        if rec_words:
            rec_word_freq = {}
            for word in rec_words:
                rec_word_freq[word] = rec_word_freq.get(word, 0) + 1
            
            top_rec_words = sorted(rec_word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            for word, freq in top_rec_words:
                print(f"  {word}: {freq} times")
        
    except Exception as e:
        print(f"Error analyzing collection: {e}")


def export_collection(collection_name: str, output_file: str = None):
    """Export a collection to JSON file."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{collection_name}_export_{timestamp}.json"
    
    print(f"📤 Exporting {collection_name} to {output_file}")
    print("=" * 50)
    
    try:
        client = chromadb.PersistentClient(path=config["chromadb_path"],settings=Settings(allow_reset=True))
        collection = client.get_collection(name=collection_name)
        
        # Get all data
        data = collection.get(include=["documents", "metadatas", "embeddings"])
        
        export_data = {
            "collection_name": collection_name,
            "export_date": datetime.now().isoformat(),
            "total_memories": len(data.get("documents", [])),
            "memories": []
        }
        
        # Process each memory
        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])
        embeddings = data.get("embeddings", [])
        ids = data.get("ids", [])
        
        for i in range(len(documents)):
            # Safely handle embeddings which might be numpy arrays
            embedding_data = []
            if embeddings is not None and len(embeddings) > 0 and i < len(embeddings):
                try:
                    # Convert to list if it's a numpy array or similar
                    embedding_data = list(embeddings[i]) if embeddings[i] is not None else []
                except (TypeError, ValueError):
                    embedding_data = []
            
            memory = {
                "id": ids[i] if i < len(ids) else None,
                "situation": documents[i] if i < len(documents) else "",
                "recommendation": metadatas[i].get("recommendation", "") if i < len(metadatas) and metadatas[i] else "",
                "embedding": embedding_data
            }
            export_data["memories"].append(memory)
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully exported {len(export_data['memories'])} memories to {output_file}")
        
    except Exception as e:
        print(f"❌ Error exporting collection: {e}")


def clear_collection(collection_name: str, confirm: bool = False, backup: bool = False):
    """Clear all memories from a collection."""
    print(f"🗑️  Clearing collection: {collection_name}")
    print("=" * 50)
    
    try:
        client = chromadb.PersistentClient(path=config["chromadb_path"],settings=Settings(allow_reset=True))
        
        # Check if collection exists
        try:
            collection = client.get_collection(name=collection_name)
        except Exception:
            print(f"❌ Collection '{collection_name}' not found.")
            return
        
        # Get current count
        current_count = collection.count()
        
        if current_count == 0:
            print(f"📭 Collection '{collection_name}' is already empty.")
            return
        
        print(f"⚠️  This will permanently delete {current_count} memories from '{collection_name}'")
        
        # Create backup if requested
        if backup:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{collection_name}_backup_before_clear_{timestamp}.json"
            print(f"💾 Creating backup: {backup_file}")
            export_collection(collection_name, backup_file)
            print()
        
        if not confirm:
            response = input("Are you sure you want to continue? (yes/no): ").lower().strip()
            if response not in ['yes', 'y']:
                print("❌ Operation cancelled.")
                return
        
        # Delete the collection and recreate it (this clears all data)
        client.delete_collection(name=collection_name)
        client.create_collection(name=collection_name)
        
        print(f"✅ Successfully cleared {current_count} memories from '{collection_name}'")
        print(f"📁 Collection '{collection_name}' is now empty and ready for new memories.")
        
    except Exception as e:
        print(f"❌ Error clearing collection: {e}")


def main():
    """Main function with simple command-line interface."""
    if len(sys.argv) == 1:
        # No arguments - show overview
        view_all_collections()
        print("\nUsage examples:")
        print(f"  python {sys.argv[0]} view <collection_name>     # View collection details")
        print(f"  python {sys.argv[0]} search <collection_name> <query>  # Search memories")
        print(f"  python {sys.argv[0]} analyze <collection_name>  # Analyze patterns")
        print(f"  python {sys.argv[0]} export <collection_name>   # Export to JSON")
        print(f"  python {sys.argv[0]} clear <collection_name>    # Clear all memories")
        return
    
    command = sys.argv[1].lower()
    
    if command == "view" and len(sys.argv) > 2:
        view_collection_details(sys.argv[2])
    
    elif command == "search" and len(sys.argv) > 3:
        collection_name = sys.argv[2]
        query = " ".join(sys.argv[3:])
        search_memories(collection_name, query)
    
    elif command == "analyze" and len(sys.argv) > 2:
        analyze_collection_patterns(sys.argv[2])
    
    elif command == "export" and len(sys.argv) > 2:
        collection_name = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else None
        export_collection(collection_name, output_file)
    
    elif command == "clear" and len(sys.argv) > 2:
        collection_name = sys.argv[2]
        # Check for --force flag to skip confirmation
        force = "--force" in sys.argv or "-f" in sys.argv
        # Check for --backup flag to create backup before clearing
        backup = "--backup" in sys.argv or "-b" in sys.argv
        clear_collection(collection_name, confirm=force, backup=backup)
    
    elif command == "list":
        view_all_collections()
    
    else:
        print("Invalid command or missing arguments.")
        print("\nAvailable commands:")
        print("  list                                    # List all collections")
        print("  view <collection_name>                  # View collection details")
        print("  search <collection_name> <query>       # Search memories")
        print("  analyze <collection_name>               # Analyze patterns")
        print("  export <collection_name> [filename]     # Export to JSON")
        print("  clear <collection_name> [--force] [--backup] # Clear all memories (use --force to skip confirmation, --backup to create backup)")


if __name__ == "__main__":
    main()
