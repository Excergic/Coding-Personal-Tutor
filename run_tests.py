#!/usr/bin/env python3
"""
Test runner script - runs tests before executing main application
"""
import subprocess
import sys
import os


def run_tests():
    """Run all tests and return True if they pass"""
    print("🧪 Running tests before starting the application...")
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "test_main.py", 
            "-v",
            "--tb=short"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Tests failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Main function that runs tests then the application"""
    if run_tests():
        print("\n🚀 Starting main application...\n")
        # Import and run your main application
        import main
        main.main()
    else:
        print("\n🛑 Tests failed. Fix the issues before running the application.")
        sys.exit(1)


if __name__ == "__main__":
    main()
