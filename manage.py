import os
from app import create_app, db

env = os.getenv("FLASK_ENV") or "test"
print(f"Active environment: * {env} *")
app = create_app(env)

if __name__ == "__main__":
    app.run()
