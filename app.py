import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "user_data.json"

def load_data():
    """Load existing data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_entry(name, email, message):
    """Add new entry to data"""
    data = load_data()
    entry = {
        "id": len(data) + 1,
        "name": name,
        "email": email,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    data.append(entry)
    save_data(data)
    return entry

def main():
    st.title("Simple Form Data App")
    st.write("Submit your information below:")
    
    # Form
    with st.form("user_form"):
        name = st.text_input("Name", max_chars=100)
        email = st.text_input("Email", max_chars=100)
        message = st.text_area("Message", max_chars=500)
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            if name and email and message:
                entry = add_entry(name, email, message)
                st.success(f"Thank you {name}! Your entry has been saved.")
                st.json(entry)
            else:
                st.error("Please fill in all fields.")
    
    # Display existing data
    st.subheader("Submitted Entries")
    data = load_data()
    if data:
        st.json(data)
    else:
        st.info("No entries yet.")

if __name__ == "__main__":
    main()