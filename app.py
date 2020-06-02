from flask import Flask, render_template, request
from dna_to_protein import translate
import mysql.connector


app = Flask(__name__)


host = "hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com"
user = "iaoqi@hannl-hlo-bioinformatica-mysqlsrv"
password = "638942"
db = "iaoqi"

# dblist = []
#
# cursor = conn.cursor()
# cursor.execute(f"select * from ")
# for i in cursor:
#     dblist.append(i)


@app.route('/')
@app.route('/protein', methods=["POST", "GET"])
def database():
    if request.method == "POST":
        resultatenlijst = []
        zoekopdracht = request.form.get("zoek", "")

        conn = mysql.connector.connect(host=host,user=user,password=password,db=db)
        cursor = conn.cursor()
        query = "select * from eiwit where description like \"%" + zoekopdracht \
                + "%\""
        cursor.execute(query)

        for rij in cursor:
            resultatenlijst.append(rij)
        cursor.close()
        conn.close()

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
