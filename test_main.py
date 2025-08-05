import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the current directory to Python path to import main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main

# Add the current directory to Python path to import main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import main


class TestMainApp:
    
    def test_system_prompt_exists(self):
        """Test that system prompt is properly defined"""
        assert main.system_prompt is not None
        assert len(main.system_prompt) > 0
        assert "python programming" in main.system_prompt.lower()
    
    def test_model_constant(self):
        """Test that MODEL constant is properly set"""
        assert main.MODEL == "llama3.2:1b"
    
    @patch('builtins.input')
    def test_user_prompt(self, mock_input):
        """Test user_prompt function returns user input"""
        mock_input.return_value = "What is a generator in Python?"
        
        result = main.user_prompt()
        
        assert result == "What is a generator in Python?"
        mock_input.assert_called_once_with("Ask me anything about python programming language: ")
    
    @patch('builtins.input')
    def test_messages_structure(self, mock_input):
        """Test that messages function returns proper structure"""
        mock_input.return_value = "Test query"
        
        messages = main.messages()
        
        assert isinstance(messages, list)
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"
        assert messages[0]["content"] == main.system_prompt
        assert messages[1]["content"] == "Test query"
    
    @patch('builtins.input')
    @patch('main.ollama.chat')
    def test_get_response_success(self, mock_ollama, mock_input):
        """Test get_response returns proper response"""
        mock_input.return_value = "What is yield in Python?"
        mock_ollama.return_value = {
            'message': {
                'content': 'Yield is used to create generators in Python.'
            }
        }
        
        response = main.get_response()
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert response == 'Yield is used to create generators in Python.'
        mock_ollama.assert_called_once()
    
    @patch('builtins.input')
    @patch('main.ollama.chat')
    def test_get_response_with_model_parameter(self, mock_ollama, mock_input):
        """Test that get_response calls ollama with correct model"""
        mock_input.return_value = "Test query"
        mock_ollama.return_value = {
            'message': {'content': 'Test response'}
        }
        
        main.get_response()
        
        # Verify ollama.chat was called with correct parameters
        call_args = mock_ollama.call_args
        assert call_args[1]['model'] == "llama3.2:1b"
        assert 'messages' in call_args[1]
    
    @patch('builtins.input')
    @patch('main.ollama.chat')
    @patch('builtins.print')
    def test_main_function(self, mock_print, mock_ollama, mock_input):
        """Test main function executes without errors"""
        mock_input.return_value = "Test query"
        mock_ollama.return_value = {
            'message': {'content': 'Test response'}
        }
        
        # Should not raise any exceptions
        main.main()
        
        # Verify print was called with the response
        mock_print.assert_called_once_with('Test response')


# Integration test to ensure all imports work
def test_imports():
    """Test that all required modules can be imported"""
    try:
        import os
        import requests
        import ollama
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


# Test for environment validation
def test_model_availability():
    """Test that the model string is valid format"""
    model = main.MODEL
    assert ":" in model  # Should have format like "llama3.2:1b"
    parts = model.split(":")
    assert len(parts) == 2
    assert parts[0]  # Model name should not be empty
    assert parts[1]  # Version should not be empty
