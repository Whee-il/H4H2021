from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', defaults={"instruction": "Go"})
@app.route('/<instruction>')
def index(instruction):
    return render_template('index.html', instruction=instruction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
