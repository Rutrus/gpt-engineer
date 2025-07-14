"""
Tests for Ollama integration with GPT Engineer.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from gpt_engineer.core.ai import AI


class TestOllamaIntegration:
    """Tests to verify Ollama integration."""

    def setup_method(self):
        """Initial setup for each test."""
        # Clear environment variables
        self.original_env = os.environ.copy()
        os.environ.pop("OPENAI_API_BASE", None)
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("MODEL_NAME", None)
        os.environ.pop("IS_OLLAMA", None)

    def teardown_method(self):
        """Cleanup after each test."""
        # Restore original environment variables
        os.environ.clear()
        os.environ.update(self.original_env)

    @patch("gpt_engineer.core.ai.ChatOpenAI")
    def test_ollama_detection_with_is_ollama_true(self, mock_chat_openai):
        """Test that Ollama is detected correctly with IS_OLLAMA=true."""
        # Configure environment variables for Ollama
        os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
        os.environ["OPENAI_API_KEY"] = "ollama"
        os.environ["IS_OLLAMA"] = "true"

        # Create AI instance
        ai = AI(model_name="qwen2.5-coder")

        # Verify that ChatOpenAI was called with correct parameters
        mock_chat_openai.assert_called_once()
        call_args = mock_chat_openai.call_args

        # Verify that Ollama parameters were passed
        assert call_args[1]["openai_api_base"] == "http://localhost:11434/v1"
        assert call_args[1]["openai_api_key"] == "ollama"
        assert call_args[1]["model"] == "qwen2.5-coder"

    @patch("gpt_engineer.core.ai.ChatOpenAI")
    def test_ollama_detection_with_is_ollama_false(self, mock_chat_openai):
        """Test that Ollama is not detected when IS_OLLAMA=false."""
        # Configure environment variables but set IS_OLLAMA to false
        os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
        os.environ["OPENAI_API_KEY"] = "ollama"
        os.environ["IS_OLLAMA"] = "false"

        # Create AI instance
        ai = AI(model_name="qwen2.5-coder")

        # Verify that ChatOpenAI was called without Ollama parameters
        mock_chat_openai.assert_called_once()
        call_args = mock_chat_openai.call_args

        # Verify that Ollama parameters were NOT passed
        assert "openai_api_base" not in call_args[1]
        assert "openai_api_key" not in call_args[1]
        assert call_args[1]["model"] == "qwen2.5-coder"

    @patch("gpt_engineer.core.ai.ChatOpenAI")
    def test_ollama_detection_without_is_ollama(self, mock_chat_openai):
        """Test that Ollama is not detected when IS_OLLAMA is not set."""
        # Configure environment variables but don't set IS_OLLAMA
        os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
        os.environ["OPENAI_API_KEY"] = "ollama"
        # IS_OLLAMA not set

        # Create AI instance
        ai = AI(model_name="qwen2.5-coder")

        # Verify that ChatOpenAI was called without Ollama parameters
        mock_chat_openai.assert_called_once()
        call_args = mock_chat_openai.call_args

        # Verify that Ollama parameters were NOT passed
        assert "openai_api_base" not in call_args[1]
        assert "openai_api_key" not in call_args[1]
        assert call_args[1]["model"] == "qwen2.5-coder"

    @patch("gpt_engineer.core.ai.ChatOpenAI")
    def test_ollama_with_different_case_values(self, mock_chat_openai):
        """Test that Ollama detection works with different case values."""
        test_cases = ["TRUE", "True", "true", "1", "YES", "Yes", "yes"]

        for test_value in test_cases:
            # Clear previous environment
            os.environ.pop("IS_OLLAMA", None)

            # Configure environment variables
            os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
            os.environ["OPENAI_API_KEY"] = "ollama"
            os.environ["IS_OLLAMA"] = test_value

            # Create AI instance
            ai = AI(model_name="qwen2.5-coder")

            # Verify that ChatOpenAI was called with Ollama parameters
            mock_chat_openai.assert_called()
            call_args = mock_chat_openai.call_args

            # Verify that Ollama parameters were passed
            assert call_args[1]["openai_api_base"] == "http://localhost:11434/v1"
            assert call_args[1]["openai_api_key"] == "ollama"

            # Reset mock for next iteration
            mock_chat_openai.reset_mock()

    @patch("gpt_engineer.core.ai.ChatOpenAI")
    def test_ollama_without_api_base(self, mock_chat_openai):
        """Test that Ollama is not used when OPENAI_API_BASE is not set."""
        # Set IS_OLLAMA but not OPENAI_API_BASE
        os.environ["IS_OLLAMA"] = "true"
        os.environ["OPENAI_API_KEY"] = "ollama"
        # OPENAI_API_BASE not set

        # Create AI instance
        ai = AI(model_name="qwen2.5-coder")

        # Verify that ChatOpenAI was called without Ollama parameters
        mock_chat_openai.assert_called_once()
        call_args = mock_chat_openai.call_args

        # Verify that Ollama parameters were NOT passed
        assert "openai_api_base" not in call_args[1]
        assert "openai_api_key" not in call_args[1]
        assert call_args[1]["model"] == "qwen2.5-coder"


if __name__ == "__main__":
    pytest.main([__file__])