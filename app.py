from flask import Flask, render_template, request
from Websitescript import zoeken,databasecounter


app = Flask(__name__)



@app.route('/')
@app.route('/protein', methods=["POST", "GET"])
def database():
    if request.method == "POST":
        resultatenlijst = []

        buttonselect = request.form.get("selection","")

        print(buttonselect)

        zoekopdracht = request.form.get("zoek", "")
        print(zoekopdracht)

        sorton = request.form.get("filterop", "")
        HLLH = request.form.get("richting", "")

        resultatenlijst = zoeken(buttonselect, zoekopdracht, sorton, HLLH)


        rangeresultatentext = "Alleen de eerste 20 resultaten worden " \
                              "weergegeven. Dit kan worden aangepast " \
                              "onderaan de body in de range bij de for loop."


        return render_template("home.html",
                               resultaten=resultatenlijst,
                               resultatentext=
                               'Gevonden resultaten:',
                               resultatentextrange=rangeresultatentext)
    else:
        return render_template('home.html',
                               resultaten='',
                               resultatentext='',
                               resultatentextrange='')

@app.route('/populatie.html', methods=["POST", "GET"])
def populatie():
    tabledata = databasecounter()
    return render_template('populatie.html', tabledata=tabledata)


if __name__ == '__main__':
    app.run()
