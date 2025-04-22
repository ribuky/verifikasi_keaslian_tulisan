from app import create_app, db
from flask_migrate import Migrate
import logging

logging.basicConfig(level=logging.DEBUG)
app = create_app()

app.static_folder = "../static"
app.static_url_path = "/static"

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)

print(f"Static folder is set to: {app.static_folder}")
print(f"Static URL path is set to: {app.static_url_path}")