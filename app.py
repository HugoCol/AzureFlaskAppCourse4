from flask import Flask, render_template, request
from Websitescript import zoeken, databasecounter
from Bio.Blast import NCBIWWW, NCBIXML
from xml.etree import ElementTree
import time
from Bio import Entrez

app = Flask(__name__)


@app.route('/')
@app.route('/home.html', methods=["POST", "GET"])
def database():
    if request.method == "POST":
        resultatenlijst = []

        buttonselect = request.form.get("selection", "")

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


@app.route('/info.html')
def info():
    return render_template('info.html')


@app.route('/over_ons.html')
def over_ons():
    return render_template('over_ons.html')


@app.route('/blast.html', methods=["POST", "GET"])
def blast():
    if request.method == "POST":
        geenresultaten = ""
        # Gegevens uit textbox halen en dit in hoofdletters zetten.
        sequentie = request.form.get("sequentie", "").upper()

        # Txt voor sequentie weer te geven op website
        sequentietxt = "De volgende sequentie is ingevoerd: "

        # Telt het aantal A, T, C, G in de sequentie.
        a_count = sequentie.count("A")
        t_count = sequentie.count("T")
        c_count = sequentie.count("C")
        g_count = sequentie.count("G")

        # Berekend lengte van de sequentie.
        lengte_seq = len(sequentie)

        # Kijkt of de ingevoerde sequentie DNA is.
        if lengte_seq == a_count + t_count + c_count + g_count and \
                sequentie != "":
            ''' # Blast de protein sequentie tegen de blastx database.
            result_handle = NCBIWWW.qblast("blastx", "nr", sequentie,
                                           hitlist_size=25)

            # Schrijft de output van BLAST weg in XML bestand.
            with open("XMLBlastWebsite.xml", "w") as out_handle:
                out_handle.write(result_handle.read())
            '''

            XMLFile = "XMLBlastWebsite.xml"
            datafile = 'dataset.txt'

            # Door bestand heen gaan
            dom = ElementTree.parse(XMLFile)
            # Alle hits eruit zoeken
            hits = dom.findall(
                'BlastOutput_iterations/Iteration/Iteration_hits/Hit')
            # Voor elke hit
            count = 1
            datadic = {}
            mestdatadic = {}
            file = open(datafile)
            fwcount = 1
            revcount = 2
            keycounter = 0
            for line in file:
                mestdata = line.split('\t')
                mestdatadic[fwcount] = [mestdata[0], mestdata[1], mestdata[2]]
                mestdatadic[revcount] = [mestdata[3], mestdata[4], mestdata[5]]
                fwcount += 2
                revcount += 2
            for c in hits:
                if count <= 2:
                    # Haal de data uit de hit en zet deze in een zelfbeschrijvende variabele
                    Hit_id = c.find('Hit_id').text
                    discript = c.find('Hit_def').text
                    totaallengte = c.find('Hit_len').text
                    querybegin = c.find('Hit_hsps/Hsp/Hsp_query-from').text
                    queryeind = c.find('Hit_hsps/Hsp/Hsp_query-to').text
                    querycoverage = (int(queryeind) - int(querybegin)) / int(
                        totaallengte)
                    organis = discript.split('[')
                    organism = organis[1].split(']')
                    description = organis[0]
                    organisme = organism[0]
                    acessiecode = c.find('Hit_accession').text
                    print(acessiecode)
                    score = c.find('Hit_hsps/Hsp/Hsp_bit-score').text
                    tscore = c.find('Hit_hsps/Hsp/Hsp_score').text
                    evalue = c.find('Hit_hsps/Hsp/Hsp_evalue').text
                    percidentity = c.find('Hit_hsps/Hsp/Hsp_identity').text
                    queryseq = c.find('Hit_hsps/Hsp/Hsp_qseq').text
                    header = "Geen header bij de ingevoerde sequentie"
                    ascicode = "Geen ascii code bij de ingevoerde sequentie"
                    time.sleep(0.4)
                    Entrez.email = "thijschermens@gmail.com"
                    seqio = Entrez.efetch(db="protein", id=acessiecode,
                                          retmode="xml")
                    seqio_read = Entrez.read(seqio)
                    seqio.close()
                    lineage = seqio_read[0]["GBSeq_taxonomy"].split(";")

                    # Print alle data om te zien of het gewerkt heeft
                    datalist = [Hit_id, description, organisme, acessiecode,
                                score,
                                tscore, evalue, percidentity, queryseq, header,
                                ascicode, lineage, querycoverage]
                    datadic[count] = datalist
                    count += 1
            else:
                pass
            datalijst = []
            # [1]=name [2]=org_naam [3]=accessiecode [4]=max-score
            # [5]=totale_score [6]=e-value [7]=percentidentity
            # [8]=sequence [9]=header [10]=ascii [11][-1]=linnaam
            # [-1]=query-cov
            for i in datadic:
                datalijst.append(datadic[i])

            # Als er geen hits zijn gevonden met blasten:
            if datalijst == []:
                geenresultaten = "Er zijn geen resultaten gevonden"

            # Return webpagina met de gegevens als iets is ingevuld in de
            # textbox.
            return render_template("blast.html",
                                   sequentie=sequentie,
                                   sequentietxt=sequentietxt,
                                   datalijst=datalijst,
                                   geenres=geenresultaten)
        else:
            return render_template("blast.html",
                                   sequentietxt="Incorrecte sequentie "
                                                "ingevoerd.")
    else:
        # Return de lege webpagina zonder dat iets is ingevuld in de
        # textbox.
        return render_template("blast.html")


if __name__ == '__main__':
    app.run()
