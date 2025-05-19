from flask import Flask, render_template, request
from main import generate_message

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        profession = request.form.get('profession', '').strip()
        interest = request.form.get('interest', '').strip()
        service = request.form.get('service', '').strip()
        language = request.form.get('language', '').strip()
        gp_name = request.form.get('gp_name', '').strip()

        message = generate_message(name, profession, interest, service, language, gp_name)

    return render_template("index.html", message=message)

if __name__ == '__main__':
    app.run(debug=True)
