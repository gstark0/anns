from flask import Flask, render_template
from model import _model, data, get_data
import json

app = Flask(__name__)
app.register_blueprint(_model)

@app.route('/')
def main():
    get_data()
    return render_template('index.html', data=json.dumps(data))

if __name__ == "__main__":
    app.run()