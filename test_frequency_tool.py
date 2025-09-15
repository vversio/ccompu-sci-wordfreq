#!/usr/bin/env python3
"""
Test script for the frequency_tool.py
Creates a sample text file and tests the frequency analysis.
"""

import os
import tempfile
import subprocess
import json

def create_sample_text():
    """Create a sample text file for testing."""
    sample_text = """
    The quick brown fox jumps over the lazy dog. The fox is very quick and agile.
    The dog is lazy and slow. The fox runs fast through the forest.
    The dog sleeps under the tree. The fox and the dog are different animals.
    The quick fox jumps over the lazy dog again and again.
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_text)
        return f.name

def test_frequency_tool():
    """Test the frequency tool with a sample file."""
    print("Creating sample text file...")
    sample_file = create_sample_text()
    
    try:
        print(f"Testing frequency tool with file: {sample_file}")
        
        # Run the frequency tool
        result = subprocess.run(
            ["python", "frequency_tool.py", sample_file, "10"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Frequency tool executed successfully!")
            print("\n📊 Results:")
            print(result.stdout)
            
            # Parse and display results nicely
            try:
                data = json.loads(result.stdout)
                print("\n📋 Formatted Results:")
                for i, item in enumerate(data, 1):
                    print(f"{i:2d}. {item['word']:10s} - {item['count']:3d} times")
            except json.JSONDecodeError:
                print("⚠️  Could not parse JSON output")
        else:
            print("❌ Frequency tool failed!")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ Test timed out!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    finally:
        # Clean up
        if os.path.exists(sample_file):
            os.unlink(sample_file)
            print(f"\n🧹 Cleaned up test file: {sample_file}")

if __name__ == "__main__":
    print("🧪 Testing Word Frequency Tool")
    print("=" * 40)
    test_frequency_tool()
    print("\n✅ Test completed!")
