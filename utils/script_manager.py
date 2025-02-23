import json
import base64
from cryptography.fernet import Fernet
from pathlib import Path

class ScriptManager:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        self.scripts_file = Path("../data/scripts.json")
        self.scripts_file.parent.mkdir(exist_ok=True)
        
        if not self.scripts_file.exists():
            self.save_scripts({})

    def encrypt_data(self, data):
        return self.cipher.encrypt(json.dumps(data).encode())

    def decrypt_data(self, encrypted_data):
        return json.loads(self.cipher.decrypt(encrypted_data).decode())

    def save_script(self, script_data):
        scripts = self.load_scripts()
        scripts[script_data['game_id']] = {
            'name': script_data['name'],
            'version': script_data['version'],
            'content': base64.b64encode(script_data['content'].encode()).decode(),
            'created_at': script_data['created_at'].isoformat()
        }
        self.save_scripts(scripts)

    def load_scripts(self):
        if not self.scripts_file.exists():
            return {}
        with open(self.scripts_file, 'rb') as f:
            encrypted_data = f.read()
            return self.decrypt_data(encrypted_data)

    def save_scripts(self, scripts):
        encrypted_data = self.encrypt_data(scripts)
        with open(self.scripts_file, 'wb') as f:
            f.write(encrypted_data)