#!/usr/bin/env python3
"""
Test Runner for TradingAgents Memory Tests

This script runs all memory-related tests in the tests directory.
"""

import sys
import os
from pathlib import Path
import subprocess
import time

# Add the parent directories to Python path
current_dir = Path(__file__).parent
strands_agents_dir = current_dir.parent
parent_dir = strands_agents_dir.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(strands_agents_dir))


def run_test_script(script_path: Path) -> bool:
    """Run a test script and return whether it passed."""
    try:
        print(f"\n{'='*60}")
        print(f"🧪 Running {script_path.name}")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Run the test script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent,
            capture_output=False,  # Show output in real-time
            text=True
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"\n✅ {script_path.name} PASSED (took {duration:.1f}s)")
            return True
        else:
            print(f"\n❌ {script_path.name} FAILED (took {duration:.1f}s)")
            return False
            
    except Exception as e:
        print(f"\n❌ Error running {script_path.name}: {e}")
        return False


def discover_test_scripts() -> list:
    """Discover all test scripts in the tests directory."""
    test_scripts = []
    tests_dir = Path(__file__).parent
    
    # Look for test scripts
    for script_path in tests_dir.glob("test_*.py"):
        if script_path.name != "run_all_tests.py":  # Don't include this runner
            test_scripts.append(script_path)
    
    # Also include quick test
    quick_test_path = tests_dir / "quick_memory_test.py"
    if quick_test_path.exists():
        test_scripts.append(quick_test_path)
    
    return sorted(test_scripts)


def main():
    """Run all memory tests."""
    print("🚀 TradingAgents Memory Test Suite Runner")
    print("=" * 60)
    
    # Discover test scripts
    test_scripts = discover_test_scripts()
    
    if not test_scripts:
        print("❌ No test scripts found in the tests directory")
        return False
    
    print(f"Found {len(test_scripts)} test scripts:")
    for script in test_scripts:
        print(f"  📄 {script.name}")
    
    # Run all tests
    passed_tests = 0
    total_tests = len(test_scripts)
    start_time = time.time()
    
    for script_path in test_scripts:
        if run_test_script(script_path):
            passed_tests += 1
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Final summary
    print(f"\n{'='*60}")
    print("🏁 FINAL TEST SUITE SUMMARY")
    print(f"{'='*60}")
    
    print(f"Total Test Scripts: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    print(f"Total Duration: {total_duration:.1f} seconds")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TEST SCRIPTS PASSED!")
        print("The TradingAgents memory system is working correctly.")
        print("\nVerified functionality:")
        print("✅ Memory creation and initialization")
        print("✅ Memory adding and storage")
        print("✅ Memory retrieval and search")
        print("✅ Error handling and recovery")
        print("✅ Data persistence")
        print("✅ Performance benchmarks")
        print("✅ Integration with reflection system")
        print("✅ Tool function compatibility")
        print("✅ Embedding generation and semantic search")
    elif passed_tests > 0:
        print(f"\n⚠️  {passed_tests} out of {total_tests} test scripts passed.")
        print("Some functionality is working, but there are issues to address.")
    else:
        print("\n❌ ALL TEST SCRIPTS FAILED!")
        print("The memory system needs significant attention.")
    
    print(f"\nFor detailed results, check the individual test outputs above.")
    
    return passed_tests == total_tests


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
