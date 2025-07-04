# TradingAgents Memory Inspection Guide

This guide explains how to inspect, analyze, and manage the memories stored in the TradingAgents reflection system using the provided inspection tools.

## Overview

The TradingAgents system stores trading reflections and lessons learned in ChromaDB collections. Each trading component (bull researcher, bear researcher, trader, etc.) has its own memory collection where it stores past experiences and insights.

## Available Tools

### 1. Simple Memory Viewer (`view_memories.py`)
Quick and easy tool for basic memory inspection.

### 2. Comprehensive Memory Inspector (`inspect_memories.py`)
Advanced tool with detailed analysis capabilities.

### 3. Memory Inspection Demo (`memory_inspection_demo.py`)
Demonstration script showing all capabilities.

## Quick Start

### View All Collections
```bash
python view_memories.py
```
This shows an overview of all memory collections and their basic statistics.

### View Specific Collection
```bash
python view_memories.py view trader_memory
```
Shows detailed content of the trader's memory collection.

### Search Memories
```bash
python view_memories.py search bull_memory "NVDA technical analysis"
```
Searches for memories related to NVDA technical analysis in the bull researcher's memory.

## Detailed Usage

### Simple Memory Viewer Commands

#### List All Collections
```bash
python view_memories.py list
```

#### View Collection Details
```bash
python view_memories.py view <collection_name>
```
Example:
```bash
python view_memories.py view trader_memory
```

#### Search Memories
```bash
python view_memories.py search <collection_name> <query>
```
Example:
```bash
python view_memories.py search risk_manager_memory "position sizing"
```

#### Analyze Patterns
```bash
python view_memories.py analyze <collection_name>
```
Example:
```bash
python view_memories.py analyze bull_memory
```

#### Export Memories
```bash
python view_memories.py export <collection_name> [filename]
```
Example:
```bash
python view_memories.py export trader_memory trader_memories_backup.json
```

### Comprehensive Memory Inspector

#### Interactive Mode
```bash
python inspect_memories.py --interactive
```
Launches an interactive command-line interface with these commands:
- `discover` - Find all collections
- `stats <collection>` - Get detailed statistics
- `inspect <collection> [limit]` - View content
- `search <collection> <query>` - Search memories
- `analyze <collection>` - Pattern analysis
- `export <collection> [filename]` - Export data
- `compare` - Compare all collections
- `report [filename]` - Generate comprehensive report

#### Command Line Options
```bash
# Quick overview
python inspect_memories.py

# Discover collections
python inspect_memories.py --discover

# Get collection statistics
python inspect_memories.py --stats trader_memory

# Inspect collection content
python inspect_memories.py --inspect bull_memory --limit 5

# Search memories
python inspect_memories.py --search trader_memory "NVDA analysis"

# Analyze patterns
python inspect_memories.py --analyze risk_manager_memory

# Export memories
python inspect_memories.py --export trader_memory --output trader_export.json

# Generate comprehensive report
python inspect_memories.py --report --output memory_report.json
```

## Memory Collections

The TradingAgents system typically creates these memory collections:

### Standard Collections
- **`bull_memory`** - Bull researcher's optimistic analyses and outcomes
- **`bear_memory`** - Bear researcher's pessimistic analyses and outcomes  
- **`trader_memory`** - Trader's final decisions and their results
- **`invest_judge_memory`** - Investment judge's consensus decisions
- **`risk_manager_memory`** - Risk manager's position sizing and risk assessments

### Memory Structure
Each memory contains:
- **Situation** - The market conditions and analysis that led to a decision
- **Recommendation** - The reflection and lessons learned from the outcome
- **Embedding** - Vector representation for semantic similarity search

## Analysis Capabilities

### 1. Collection Statistics
- Total number of memories
- Average document lengths
- Embedding dimensions
- Metadata structure

### 2. Content Inspection
- View actual stored memories
- See situation descriptions and recommendations
- Examine embedding previews

### 3. Semantic Search
- Find similar past trading scenarios
- Search by keywords or concepts
- Ranked by similarity scores

### 4. Pattern Analysis
- Most common words in situations and recommendations
- Length distributions
- Frequency analysis

### 5. Collection Comparison
- Compare memory counts across collections
- Analyze differences between components
- Overall system statistics

## Python API Usage

### Basic Memory Access
```python
from strands_agents.tools.memory import FinancialSituationMemory
from strands_agents.default_config import DEFAULT_CONFIG

# Create memory instance
memory = FinancialSituationMemory("trader_memory", DEFAULT_CONFIG)

# Search for similar situations
results = memory.get_memories("NVDA technical breakout", n_matches=5)

# Add new memories
situations_and_advice = [
    ("New trading situation", "Lessons learned from outcome")
]
memory.add_situations(situations_and_advice)
```

### Advanced Analysis
```python
from inspect_memories import MemoryInspector

# Create inspector
inspector = MemoryInspector()

# Discover all collections
collections = inspector.discover_collections()

# Get detailed statistics
stats = inspector.get_collection_stats("trader_memory")

# Search across collections
results = inspector.search_memories("bull_memory", "technical analysis", n_results=10)

# Analyze patterns
patterns = inspector.analyze_memory_patterns("risk_manager_memory")

# Generate comprehensive report
report_file = inspector.generate_report("analysis_report.json")
```

## Use Cases

### 1. Debugging Reflection Quality
```bash
# View recent reflections to check quality
python view_memories.py view trader_memory

# Search for specific scenarios
python view_memories.py search trader_memory "failed trade"
```

### 2. Monitoring Learning Progress
```bash
# Check how many memories each component has learned
python view_memories.py list

# Analyze patterns in successful trades
python view_memories.py search bull_memory "successful" 
```

### 3. Finding Similar Scenarios
```bash
# Find past situations similar to current market conditions
python view_memories.py search trader_memory "NVDA earnings beat"
```

### 4. Exporting for Analysis
```bash
# Export all memories for external analysis
python view_memories.py export trader_memory trader_data.json
python view_memories.py export bull_memory bull_data.json
```

### 5. System Health Monitoring
```bash
# Generate comprehensive system report
python inspect_memories.py --report system_health_report.json
```

## Data Export Formats

### JSON Export Structure
```json
{
  "collection_name": "trader_memory",
  "export_date": "2025-07-04T09:00:00",
  "total_memories": 25,
  "memories": [
    {
      "id": "0",
      "situation": "Market analysis and trading context...",
      "recommendation": "Lessons learned and insights...",
      "embedding": [0.1, -0.2, 0.3, ...]
    }
  ]
}
```

### Report Structure
```json
{
  "report_date": "2025-07-04T09:00:00",
  "total_collections": 5,
  "collections": ["bull_memory", "bear_memory", ...],
  "detailed_stats": {
    "trader_memory": {
      "total_memories": 25,
      "avg_document_length": 450,
      "embedding_dimensions": 1024
    }
  },
  "content_samples": {...},
  "pattern_analysis": {...},
  "comparison": {...}
}
```

## Troubleshooting

### Common Issues

#### No Collections Found
```bash
# Check if ChromaDB is accessible
python -c "import chromadb; print('ChromaDB accessible')"

# Run the system to create memories first
python main.py
```

#### Empty Collections
```bash
# Check if reflection system has been used
python view_memories.py list

# Run reflection demo to create sample data
python memory_inspection_demo.py
```

#### Search Returns No Results
```bash
# Check collection has data
python view_memories.py view trader_memory

# Try broader search terms
python view_memories.py search trader_memory "trade"
```

#### Export Fails
```bash
# Check write permissions
touch test_export.json && rm test_export.json

# Use absolute path
python view_memories.py export trader_memory /full/path/to/export.json
```

### Error Messages

#### "Collection not found"
- The specified collection doesn't exist
- Run the trading system first to create collections

#### "No memories stored"
- Collection exists but is empty
- Run some trading scenarios with reflection enabled

#### "Embedding generation failed"
- Check AWS credentials for Bedrock
- Verify model access permissions

## Best Practices

### 1. Regular Monitoring
- Check memory growth over time
- Monitor reflection quality
- Export backups regularly

### 2. Pattern Analysis
- Look for common successful patterns
- Identify recurring mistakes
- Analyze component-specific insights

### 3. Data Management
- Export important memories before system changes
- Clean up test data periodically
- Monitor storage usage

### 4. Search Optimization
- Use specific keywords for better results
- Try different search terms
- Combine multiple searches for comprehensive analysis

## Integration with TradingAgents

### Automatic Memory Creation
Memories are automatically created when:
- Reflection system runs after trading decisions
- Components learn from outcomes
- System processes trading results

### Memory Usage
Memories are automatically used when:
- Agents make new trading decisions
- Similar situations are encountered
- Reflection system provides context

### Configuration
Memory behavior is controlled by:
- `embedding_provider` setting
- `embedding_model` configuration
- ChromaDB settings

## Advanced Features

### Custom Analysis Scripts
Create custom analysis by extending the inspector:

```python
from inspect_memories import MemoryInspector

class CustomAnalyzer(MemoryInspector):
    def analyze_trading_performance(self, collection_name):
        # Custom analysis logic
        content = self.inspect_collection_content(collection_name, limit=100)
        # Analyze success/failure patterns
        # Return custom insights
        pass

analyzer = CustomAnalyzer()
insights = analyzer.analyze_trading_performance("trader_memory")
```

### Batch Operations
Process multiple collections:

```python
collections = ["bull_memory", "bear_memory", "trader_memory"]
for collection in collections:
    inspector.export_memories(collection, f"{collection}_backup.json")
```

### Automated Reporting
Set up regular reports:

```python
import schedule
import time

def generate_daily_report():
    inspector = MemoryInspector()
    inspector.generate_report(f"daily_report_{datetime.now().strftime('%Y%m%d')}.json")

schedule.every().day.at("09:00").do(generate_daily_report)
```

This comprehensive guide should help you effectively inspect, analyze, and manage the memories in your TradingAgents system!
