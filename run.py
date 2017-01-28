import os
from app import app
app.run(port=int(os.environ.get("PORT")), debug=True)
