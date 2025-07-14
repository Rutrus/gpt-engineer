#!/usr/bin/env python3
"""
Test script to verify Ollama integration with GPT Engineer.

This script verifies that:
1. Ollama is running
2. The specified model is available
3. GPT Engineer can connect to Ollama
4. Basic code generation works

Usage:
    python scripts/test_ollama.py [model]

Example:
    python scripts/test_ollama.py qwen2.5-coder:latest
"""

import os
import sys
import requests
from pathlib import Path


def check_ollama_server():
    """Check if the Ollama server is running."""
    try:
        response = requests.get("http://localhost:11434/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server is running")
            return True
        else:
            print(f"❌ Ollama server responded with code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Ollama server: {e}")
        print("   Make sure to run 'ollama serve' in another terminal")
        return False


def check_model_available(model_name):
    """Check if the specified model is available."""
    try:
        response = requests.get("http://localhost:11434/v1/models", timeout=5)
        if response.status_code == 200:
            data = response.json()

            # Debug: print the response structure
            print(f"🔍 API Response structure: {list(data.keys())}")

            # Handle different response formats
            models = []
            if "data" in data:
                models = data["data"]
            elif "models" in data:
                models = data["models"]
            else:
                # If response is directly a list
                models = data if isinstance(data, list) else []

            # Extract model names safely
            model_names = []
            for model in models:
                if isinstance(model, dict):
                    # Try different possible key names
                    name = model.get("name") or model.get("model") or model.get("id")
                    if name:
                        model_names.append(name)
                elif isinstance(model, str):
                    model_names.append(model)

            print(f"📋 Available models: {model_names}")

            if model_name in model_names:
                print(f"✅ Model '{model_name}' is available")
                return True
            else:
                print(f"❌ Model '{model_name}' is not available")
                print(f"   Available models: {', '.join(model_names)}")
                print(f"   To download: ollama pull {model_name}")
                return False
        else:
            print(f"❌ API responded with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        print(f"   Response content: {response.text if 'response' in locals() else 'No response'}")
        return False


def test_gpt_engineer_integration(model_name):
    """Test GPT Engineer integration."""
    try:
        # Configure environment variables
        os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
        os.environ["OPENAI_API_KEY"] = "ollama"
        os.environ["MODEL_NAME"] = model_name
        os.environ["IS_OLLAMA"] = "true"

        # Import after setting environment variables
        from gpt_engineer.core.ai import AI

        # Create AI instance
        ai = AI(model_name=model_name, temperature=0.1)

        # Test with a simple prompt
        prompt = "Write a Python function that adds two numbers"
        messages = ai.start(
            system="You are a helpful programming assistant.",
            user=prompt,
            step_name="test"
        )

        response = messages[-1].content
        print("✅ GPT Engineer successfully connected to Ollama")
        print(f"   Response: {response[:100]}...")
        return True

    except Exception as e:
        print(f"❌ Error in GPT Engineer integration: {e}")
        return False


def create_test_project():
    """Create a test project."""
    test_dir = Path("projects/test-ollama")
    test_dir.mkdir(parents=True, exist_ok=True)

    prompt_file = test_dir / "prompt"
    prompt_content = """Generate a simple Python function that:
1. Takes two numbers as parameters
2. Returns their sum
3. Includes basic documentation

Also generate a simple test to verify it works."""

    prompt_file.write_text(prompt_content)
    print(f"✅ Test project created in {test_dir}")
    return test_dir


def main():
    # Get model from arguments or use default
    model_name = sys.argv[1] if len(sys.argv) > 1 else "qwen2.5-coder"

    print(f"🧪 Testing Ollama integration using model: {model_name}")
    print("=" * 60)

    # Check server
    if not check_ollama_server():
        sys.exit(1)

    # Check model
    if not check_model_available(model_name):
        sys.exit(1)

    # Test integration
    if not test_gpt_engineer_integration(model_name):
        sys.exit(1)

    # Create test project
    test_dir = create_test_project()

    print("\n" + "=" * 60)
    print("🎉 All tests passed!")
    print(f"\nTo test GPT Engineer with Ollama:")
    print(f"1. cd {test_dir}")
    print(f"2. gpte . {model_name} --lite")
    print(f"\nOr from the root directory:")
    print(f"gpte projects/test-ollama {model_name} --lite")


if __name__ == "__main__":
    main()