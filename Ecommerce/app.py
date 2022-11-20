from venv import create
from website import create_app


#Running flask server
if __name__ == "__main__":
    app = create_app()
    app.run(debug = True) #re-runds flask web server everytime we make a change to avoind starting and stopping it