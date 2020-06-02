from flask import Flask, render_template, request
from dna_to_protein import translate


app = Flask(__name__)


@app.route('/')
@app.route('/protein', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        seq = request.form.get("sequence", "")
        protein = translate(seq)
        return render_template('home.html', title='Home',
                               proteins=protein)
    else:
        return render_template('home.html', title='Home',
                               proteins='protein', fastafile='fastafile')


if __name__ == '__main__':
    app.run()
