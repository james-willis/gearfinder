import os
from app import app
app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
