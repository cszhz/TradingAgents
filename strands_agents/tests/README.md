# TradingAgents Memory Tests

This directory contains comprehensive tests for the TradingAgents memory system, including memory adding, retrieval, error handling, and integration testing.

## Test Files

### Core Test Files

#### `test_adding_memories.py`
Comprehensive test suite for memory adding functionality:
- ✅ Basic memory storage and retrieval
- ✅ Error handling for invalid data
- ✅ Large batch processing
- ✅ Concurrent access support
- ✅ Data persistence across instances
- ✅ Tool function integration
- ✅ Reflection system integration
- ✅ Embedding generation and semantic search
- ✅ Real-world trading scenario handling

#### `quick_memory_test.py`
Quick verification tests for rapid development:
- ✅ Basic memory operations
- ✅ Data persistence
- ✅ Error handling
- ✅ Performance benchmarks

### Utility Files

#### `run_all_tests.py`
Test runner that executes all test scripts and provides a comprehensive summary.

#### `MEMORY_INSPECTION_GUIDE.md`
Comprehensive guide for inspecting and analyzing stored memories.

## Running Tests

### Quick Test (Recommended for Development)
```bash
cd strands_agents/tests
python quick_memory_test.py
```

### Comprehensive Test Suite
```bash
cd strands_agents/tests
python test_adding_memories.py
```

### Run All Tests
```bash
cd strands_agents/tests
python run_all_tests.py
```

### Individual Test Components
```bash
# From the tests directory
python -c "from test_adding_memories import MemoryAddingTester; tester = MemoryAddingTester(); tester.test_basic_memory_adding()"
```

## Test Coverage

### Memory Operations
- **Creation**: Memory instance initialization
- **Adding**: Single and batch memory addition
- **Retrieval**: Semantic search and similarity matching
- **Persistence**: Data survival across instance recreation
- **Concurrency**: Multiple instances accessing same collections

### Error Handling
- **Invalid Data**: Empty strings, None values, malformed input
- **Collection Conflicts**: Duplicate collection creation
- **Embedding Failures**: Fallback mechanisms
- **Network Issues**: Timeout and retry handling

### Integration Testing
- **Tool Functions**: Memory tools used by agents
- **Reflection System**: Automatic memory creation from reflections
- **ChromaDB**: Database operations and persistence
- **Bedrock Embeddings**: Vector generation and search

### Performance Testing
- **Batch Processing**: Large memory sets (50+ items)
- **Search Performance**: Query response times
- **Memory Usage**: Resource consumption monitoring
- **Concurrent Access**: Multi-instance performance

## Expected Test Results

### Successful Test Run
```
🎉 ALL TESTS PASSED! Memory adding functionality is working perfectly.

Key capabilities verified:
✅ Basic memory storage and retrieval
✅ Error handling for invalid data
✅ Large batch processing
✅ Concurrent access support
✅ Data persistence across instances
✅ Tool function integration
✅ Reflection system integration
✅ Embedding generation and semantic search
✅ Real-world trading scenario handling
```

### Test Metrics
- **Success Rate**: Should be 100% for fully functional system
- **Performance**: Memory adding <1s for 50 items, search <0.1s
- **Error Recovery**: System continues functioning after errors
- **Data Integrity**: All stored memories retrievable

## Troubleshooting

### Common Issues

#### ChromaDB Connection Errors
```bash
# Check ChromaDB accessibility
python -c "import chromadb; print('ChromaDB accessible')"
```

#### Embedding Generation Failures
```bash
# Check AWS credentials for Bedrock
aws sts get-caller-identity

# Check model access
aws bedrock list-foundation-models --region us-west-2
```

#### Import Path Issues
```bash
# Verify Python path setup
python -c "import sys; print(sys.path)"
```

#### Memory Collection Conflicts
```bash
# Clean up test collections
python -c "
import chromadb
client = chromadb.Client()
for col in client.list_collections():
    if col.name.startswith('test_'):
        client.delete_collection(col.name)
        print(f'Cleaned {col.name}')
"
```

### Test Environment Setup

#### Required Dependencies
```bash
pip install chromadb boto3 openai
```

#### Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-west-2
```

#### Configuration
Ensure `strands_agents/default_config.py` has correct settings:
```python
DEFAULT_CONFIG = {
    "embedding_provider": "bedrock",
    "embedding_model": "amazon.titan-embed-text-v2:0",
    "aws_region": "us-west-2",
    # ... other settings
}
```

## Test Data

### Sample Trading Scenarios
The tests use realistic trading scenarios:
- **NVDA**: Technical breakout with AI narrative
- **TSLA**: Bearish divergence with sentiment analysis
- **AAPL**: Mixed signals requiring conservative approach
- **SPY**: Risk management during market uncertainty
- **AMZN**: AWS growth focus with diversified business model

### Memory Structure
Each test memory contains:
- **Situation**: Market conditions and analysis context
- **Recommendation**: Lessons learned and trading insights
- **Embedding**: Vector representation for similarity search

## Continuous Integration

### Automated Testing
```bash
# Add to CI/CD pipeline
cd strands_agents/tests
python run_all_tests.py
if [ $? -eq 0 ]; then
    echo "All memory tests passed"
else
    echo "Memory tests failed"
    exit 1
fi
```

### Performance Monitoring
```bash
# Monitor test performance over time
python quick_memory_test.py 2>&1 | grep "Rate:" | tee performance.log
```

### Test Coverage Reports
```bash
# Generate coverage report (if coverage.py installed)
coverage run test_adding_memories.py
coverage report -m
```

## Contributing

### Adding New Tests
1. Create test file following naming convention: `test_*.py`
2. Include comprehensive error handling
3. Add performance benchmarks where appropriate
4. Update this README with new test descriptions

### Test Guidelines
- **Isolation**: Each test should be independent
- **Cleanup**: Clean up test data after execution
- **Documentation**: Clear test descriptions and expected outcomes
- **Error Handling**: Graceful handling of test failures
- **Performance**: Include timing and resource usage metrics

## Support

For issues with the memory tests:
1. Check the troubleshooting section above
2. Verify environment setup and dependencies
3. Run individual test components to isolate issues
4. Check AWS credentials and Bedrock model access
5. Review ChromaDB installation and configuration

The memory test suite is designed to be comprehensive, reliable, and informative, providing confidence in the TradingAgents memory system functionality.
