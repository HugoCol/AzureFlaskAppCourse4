from flask import Flask,render_template,request
from dna_to_protein import translate
from fastafilereader import fastafile_reader

app = Flask(__name__)

@app.route('/')
@app.route('/protein',methods=["POST", "GET"])
def index():

    if request.method == "POST":
        seq = request.form.get("sequence", "")
        protein = translate(seq)
        return render_template('hello_world.html', title='Home',proteins=protein)
    else:
        return render_template('hello_world.html', title='Home',proteins='protein',fastafile='fastafile')

@app.route('/fastafile',methods=["POST", "GET"])
def fastafile():

    if request.method == "POST":
        fastafile = request.form.get("fastafile", "")
        print(fastafile)
        fasta_output = fastafile_reader(fastafile)
        return render_template('hello_world.html', title='Home',proteins='',fastafile=fasta_output)
    else:
        return render_template('hello_world.html', title='Home',proteins='',fastafile='fastafile')




if __name__ == '__main__':
    app.run()
