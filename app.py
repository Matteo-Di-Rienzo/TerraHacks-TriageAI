from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    submitted = False
    data = {}
    if request.method == 'POST':
        data['name'] = request.form.get('name')
        data['color'] = request.form.get('color')
        submitted = True
    return render_template('index.html', submitted=submitted, data=data)

if __name__ == '__main__':
    app.run(debug=True)