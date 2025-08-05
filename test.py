import pytest
import json
import os
import tempfile
from app import load_data, save_data, add_entry

class TestApp:
    def setup_method(self):
        """Setup for each test method"""
        self.test_file = "test_data.json"
        # Clean up any existing test file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def teardown_method(self):
        """Cleanup after each test method"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_load_data_empty_file(self):
        """Test loading data when file doesn't exist"""
        # Temporarily change DATA_FILE
        import app
        original_file = app.DATA_FILE
        app.DATA_FILE = self.test_file
        
        data = load_data()
        assert data == []
        
        # Restore original
        app.DATA_FILE = original_file
    
    def test_save_and_load_data(self):
        """Test saving and loading data"""
        import app
        original_file = app.DATA_FILE
        app.DATA_FILE = self.test_file
        
        test_data = [{"id": 1, "name": "Test", "email": "test@test.com"}]
        save_data(test_data)
        
        loaded_data = load_data()
        assert loaded_data == test_data
        
        # Restore original
        app.DATA_FILE = original_file
    
    def test_add_entry(self):
        """Test adding a new entry"""
        import app
        original_file = app.DATA_FILE
        app.DATA_FILE = self.test_file
        
        entry = add_entry("John Doe", "john@example.com", "Hello world")
        
        assert entry["name"] == "John Doe"
        assert entry["email"] == "john@example.com"
        assert entry["message"] == "Hello world"
        assert entry["id"] == 1
        assert "timestamp" in entry
        
        # Verify it was saved
        data = load_data()
        assert len(data) == 1
        assert data[0]["name"] == "John Doe"
        
        # Restore original
        app.DATA_FILE = original_file
    
    def test_multiple_entries(self):
        """Test adding multiple entries"""
        import app
        original_file = app.DATA_FILE
        app.DATA_FILE = self.test_file
        
        add_entry("User 1", "user1@test.com", "Message 1")
        add_entry("User 2", "user2@test.com", "Message 2")
        
        data = load_data()
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[1]["id"] == 2
        
        # Restore original
        app.DATA_FILE = original_file

def test_data_persistence():
    """Test that data persists between function calls"""
    test_file = "persistence_test.json"
    
    try:
        import app
        original_file = app.DATA_FILE
        app.DATA_FILE = test_file
        
        # Add first entry
        add_entry("Test User", "test@example.com", "Test message")
        
        # Load data in a separate call
        data = load_data()
        assert len(data) == 1
        assert data[0]["name"] == "Test User"
        
        # Restore original
        app.DATA_FILE = original_file
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)