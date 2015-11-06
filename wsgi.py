"""
Startup da aprlicação.
"""
from rest import create_app

app = create_app('config.default')

if __name__ == "__main__":
    app.run(debug=True)
