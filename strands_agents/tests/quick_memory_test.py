#!/usr/bin/env python3
"""
Quick Memory Adding Test

A simple script to quickly test that memory adding functionality works correctly.
Perfect for rapid verification during development.
"""

import sys
import os
from pathlib import Path
import time

# Add the parent directories to Python path
current_dir = Path(__file__).parent
strands_agents_dir = current_dir.parent
parent_dir = strands_agents_dir.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(strands_agents_dir))

from strands_agents.tools.memory import FinancialSituationMemory
from strands_agents.default_config import DEFAULT_CONFIG


def quick_memory_test():
    """Quick test of memory adding functionality."""
    print("🚀 Quick Memory Adding Test")
    print("=" * 40)
    
    try:
        # Create memory instance
        print("1. Creating memory instance...")
        memory = FinancialSituationMemory("quick_test_memory", DEFAULT_CONFIG)
        print("✅ Memory instance created")
        
        # Test data
        test_memories = [
            (
                "NVDA shows strong bullish breakout above $450 resistance with 2x volume",
                "BUY decision resulted in +15% return. Technical analysis was accurate."
            ),
            (
                "AAPL earnings beat but guidance mixed, showing consolidation pattern",
                "HOLD decision appropriate. Stock moved sideways as expected."
            ),
            (
                "TSLA bearish divergence with negative sentiment and production concerns",
                "SELL decision avoided -12% loss. Sentiment analysis proved predictive."
            )
        ]
        
        # Add memories
        print(f"\n2. Adding {len(test_memories)} memories...")
        start_time = time.time()
        memory.add_situations(test_memories)
        add_time = time.time() - start_time
        print(f"✅ Added memories in {add_time:.2f} seconds")
        
        # Test retrieval
        print("\n3. Testing memory retrieval...")
        test_queries = [
            "NVDA technical analysis",
            "earnings results",
            "sentiment analysis"
        ]
        
        for query in test_queries:
            start_time = time.time()
            results = memory.get_memories(query, n_matches=2)
            search_time = time.time() - start_time
            
            if results:
                top_similarity = results[0].get('similarity_score', 0)
                print(f"✅ '{query}': Found {len(results)} results in {search_time:.3f}s (top similarity: {top_similarity:.3f})")
            else:
                print(f"❌ '{query}': No results found")
        
        # Test specific search
        print("\n4. Testing specific scenario search...")
        nvda_results = memory.get_memories("NVDA bullish breakout", n_matches=1)
        if nvda_results:
            result = nvda_results[0]
            print("✅ Found NVDA scenario:")
            print(f"   Similarity: {result.get('similarity_score', 0):.3f}")
            print(f"   Situation: {result.get('matched_situation', '')[:100]}...")
            print(f"   Recommendation: {result.get('recommendation', '')[:100]}...")
        else:
            print("❌ Could not find NVDA scenario")
        
        print("\n🎉 Quick test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_memory_persistence():
    """Test that memories persist across instances."""
    print("\n🔄 Testing Memory Persistence")
    print("=" * 40)
    
    try:
        collection_name = "persistence_test_memory"
        
        # First instance - add data
        print("1. Creating first instance and adding data...")
        memory1 = FinancialSituationMemory(collection_name, DEFAULT_CONFIG)
        test_data = [("Persistence test situation", "This should persist")]
        memory1.add_situations(test_data)
        print("✅ Data added with first instance")
        
        # Delete first instance
        del memory1
        
        # Second instance - check data exists
        print("2. Creating second instance and checking data...")
        memory2 = FinancialSituationMemory(collection_name, DEFAULT_CONFIG)
        results = memory2.get_memories("Persistence test", n_matches=1)
        
        if results:
            print("✅ Data persisted across instances")
            return True
        else:
            print("❌ Data did not persist")
            return False
            
    except Exception as e:
        print(f"❌ Persistence test failed: {e}")
        return False


def test_error_handling():
    """Test error handling with invalid data."""
    print("\n🛡️ Testing Error Handling")
    print("=" * 40)
    
    try:
        memory = FinancialSituationMemory("error_test_memory", DEFAULT_CONFIG)
        
        # Test empty data
        print("1. Testing empty data...")
        memory.add_situations([])
        print("✅ Handled empty list")
        
        # Test invalid data
        print("2. Testing invalid data...")
        invalid_data = [
            ("", "Valid recommendation"),  # Empty situation
            ("Valid situation", ""),       # Empty recommendation
            (None, "Valid recommendation"), # None situation
        ]
        
        memory.add_situations(invalid_data)
        print("✅ Handled invalid data gracefully")
        
        # Test that valid data still works
        print("3. Testing valid data after errors...")
        valid_data = [("Valid situation", "Valid recommendation")]
        memory.add_situations(valid_data)
        
        results = memory.get_memories("Valid", n_matches=1)
        if results:
            print("✅ System still functional after error handling")
            return True
        else:
            print("❌ System not functional after errors")
            return False
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


def benchmark_performance():
    """Quick performance benchmark."""
    print("\n⚡ Performance Benchmark")
    print("=" * 40)
    
    try:
        memory = FinancialSituationMemory("benchmark_memory", DEFAULT_CONFIG)
        
        # Generate test data
        print("1. Generating test data...")
        test_data = []
        for i in range(20):
            situation = f"Benchmark test situation {i}: Market shows {'bullish' if i % 2 == 0 else 'bearish'} signals"
            recommendation = f"Benchmark recommendation {i}: {'BUY' if i % 2 == 0 else 'SELL'} decision with {5 + i}% result"
            test_data.append((situation, recommendation))
        
        # Benchmark adding
        print("2. Benchmarking memory adding...")
        start_time = time.time()
        memory.add_situations(test_data)
        add_time = time.time() - start_time
        print(f"✅ Added {len(test_data)} memories in {add_time:.3f} seconds")
        print(f"   Rate: {len(test_data)/add_time:.1f} memories/second")
        
        # Benchmark searching
        print("3. Benchmarking memory search...")
        search_times = []
        for i in range(5):
            start_time = time.time()
            results = memory.get_memories(f"benchmark test {i}", n_matches=3)
            search_time = time.time() - start_time
            search_times.append(search_time)
        
        avg_search_time = sum(search_times) / len(search_times)
        print(f"✅ Average search time: {avg_search_time:.3f} seconds")
        print(f"   Search rate: {1/avg_search_time:.1f} searches/second")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance benchmark failed: {e}")
        return False


def main():
    """Run all quick tests."""
    print("🧪 TradingAgents Quick Memory Tests")
    print("=" * 50)
    
    tests = [
        ("Basic Memory Test", quick_memory_test),
        ("Persistence Test", test_memory_persistence),
        ("Error Handling Test", test_error_handling),
        ("Performance Benchmark", benchmark_performance),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 QUICK TEST SUMMARY")
    print("=" * 50)
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All quick tests passed! Memory system is working correctly.")
        print("\nVerified capabilities:")
        print("✅ Memory creation and storage")
        print("✅ Memory retrieval and search")
        print("✅ Data persistence")
        print("✅ Error handling")
        print("✅ Performance benchmarks")
    elif passed > 0:
        print(f"\n⚠️  {passed} out of {total} tests passed. Some issues detected.")
    else:
        print("\n❌ All tests failed. Memory system needs attention.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
