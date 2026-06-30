from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenue sur le site de l'UFR STA"

if __name__ == '__main__':
    app.run(debug=True)

