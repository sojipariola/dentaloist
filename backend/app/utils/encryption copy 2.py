import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

ENV_FILE_PATH = ".env"

def get_fernet_key():
    key = os.getenv("ENCRYPTION_KEY")
    
    if key:
        try:
            Fernet(key.encode())  # Validate key
            return key
        except ValueError:
            print("⚠️ Invalid Fernet key in .env. Generating a new one...")
    
    # Generate new key
    new_key = Fernet.generate_key().decode()
    print(f"🔑 Generated new Fernet key: {new_key}")

    # Persist it to .env
    with open(ENV_FILE_PATH, "r") as f:
        lines = f.readlines()
    
    with open(ENV_FILE_PATH, "w") as f:
        found = False
        for line in lines:
            if line.startswith("ENCRYPTION_KEY="):
                f.write(f"ENCRYPTION_KEY={new_key}\n")
                found = True
            else:
                f.write(line)
        if not found:
            f.write(f"ENCRYPTION_KEY={new_key}\n")
    
    # Set in environment for this session
    os.environ["ENCRYPTION_KEY"] = new_key
    return new_key


# Usage
encryption_key = get_fernet_key()
fernet = Fernet(encryption_key.encode())
