from flask import Flask, render_template, request
from Websitescript import zoeken


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

        resultatenlijst = zoeken(buttonselect,zoekopdracht)


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


if __name__ == '__main__':
    app.run()
