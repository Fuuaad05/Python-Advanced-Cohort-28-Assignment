# Import the datetime class from the datetime module
from datetime import datetime, timedelta

# Define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f"Visitor '{name}' already signed in last! No back to back visits allowed."
        super().__init__(self.message)

# Define a custom exception for too-soon visitors
class TooSoonError(Exception):
    def __init__(self, last_name, last_time):
        self.message = (
            f"Last visitor '{last_name}' signed in at {last_time}. "
            "Please wait at least 5 minutes before the next visitor."
        )
        super().__init__(self.message)

# Define the main function that runs the program
def main():
    filename = "visitors.txt"
  
    # Ensure the file exists before we start using it
    try:
        with open(filename, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        print("file not found, creating a new file")
        with open(filename, "w", encoding="utf-8") as f:
            pass
    
    # Ask the user to type the visitor's name
    visitor = input("Enter visitor's name: ")
  
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_visitor, last_time = (None, None)

            if lines:
                # Split last record into name and timestamp
                parts = lines[-1].strip().split(" | ")
                if len(parts) == 2:
                    last_visitor, last_time_str = parts
                    last_time = datetime.fromisoformat(last_time_str)
      
        # Check for duplicate visitor
        if visitor == last_visitor:
            raise DuplicateVisitorError(visitor)
        
        # Check for cooldown (5 minutes)
        if last_time and (datetime.now() - last_time) < timedelta(minutes=5):
            raise TooSoonError(last_visitor, last_time)
    
        # Append new visitor
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now().isoformat()}\n")
        
        print("Visitor added successfully!")
  
    except (DuplicateVisitorError, TooSoonError) as e:
        print("Error:", e)

# Run the program
main()
