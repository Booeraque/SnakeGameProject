import json
import os
from pymongo import MongoClient

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the DB directory and file paths
DB_DIR = os.path.join(script_dir, 'db')
DB_FILE = os.path.join(DB_DIR, 'data.json')

# MongoDB connection
client = MongoClient('mongodb+srv://s26904:7WbLWoMF4cbwR4Ps@myfirstdb.7gpmlbm.mongodb.net/')  # MongoDB localhost connection
db = client['snake_game']
collection = db['game_sessions']


# Function to check if the database location and file exist
def check_database_existence():
    if os.path.exists(DB_DIR) and os.path.isfile(os.path.join(DB_DIR, DB_FILE)):
        # Check if file is not empty
        if os.path.getsize(os.path.join(DB_DIR, DB_FILE)) > 0:
            return True
    return False


# Function to read data from JSON file
def read_data_from_file(filename):
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist, returning empty list")
        return []
    with open(filename, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {filename}, returning empty list")
            return []


# Function to write data to JSON file
def write_data_to_file(data, filename):
    with open(filename, 'w') as file:
        try:
            json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error writing JSON to file {filename}: {e}")


# Function to store game result in JSON file
def store_game_result(name, score, map_size):
    # Load existing data from JSON file
    data = read_data_from_file(DB_FILE)
    # Append new game result to data
    data.append({'name': name, 'score': score, 'map_size': map_size})
    # Write updated data back to JSON file
    write_data_to_file(data, DB_FILE)
    print(f"Stored game result in JSON: {name}, {score}, {map_size}")


# Function to store game result in MongoDB
def store_game_result_to_mongodb(name, score, map_size):
    collection.insert_one({'name': name, 'score': score, 'map_size': map_size})


# Function to initialize the database
def initialize_database():
    if not check_database_existence():
        # Create database directory if it doesn't exist
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
        # Create empty data file
        with open(os.path.join(DB_DIR, DB_FILE), 'w') as file:
            json.dump([], file, indent=4)


# Initialize the database upon script execution
initialize_database()
