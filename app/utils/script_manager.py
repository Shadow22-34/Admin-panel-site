import json
import os
from datetime import datetime

class ScriptManager:
    def __init__(self):
        self.scripts_file = os.path.join(os.getcwd(), "data", "scripts.json")
        self.ensure_data_dir()

    def ensure_data_dir(self):
        os.makedirs(os.path.dirname(self.scripts_file), exist_ok=True)
        if not os.path.exists(self.scripts_file):
            with open(self.scripts_file, "w") as f:
                json.dump({"scripts": {}, "last_updated": None}, f, indent=4)

    # ... rest of the code remains the same ...