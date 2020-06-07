# Om de applicatie te runnen moet dit script gestart worden.
# Op deze pagina komen alle andere scripts samen tot een webapplicatie

# ophalen van alle modules
from flask import Flask, render_template, request
from Websitescript import zoeken, databasecounter
from Bio.Blast import NCBIWWW, NCBIXML
from xml.etree import ElementTree
import time
from Bio import Entrez

# app aanroepen
app = Flask(__name__)


# home page
@app.route('/')
@app.route('/home.html', methods=["POST", "GET"])
def database():
    """
    Hier wordt de homepage gerenderd. verschillende inputs door de
    gebuiker worden opgehaald als variabelen; input tekst,
    waar in te zoeken en sorteren. Data uit de database wordt
    teruggegeven
    :return:
    input: gebruikersinput van de website
    output: data vanuit de database in tabellen en regels.
    """

    if request.method == "POST":
        resultatenlijst = []

        buttonselect = request.form.get("selection", "")

        zoekopdracht = request.form.get("zoek", "")

        sorton = request.form.get("filterop", "")
        HLLH = request.form.get("richting", "")

        resultatenlijst = zoeken(buttonselect, zoekopdracht, sorton,
                                 HLLH)

        rangeresultatentext = "Alleen de eerste 20 resultaten worden " \
                              "weergegeven. Dit kan worden aangepast " \
                              "onderaan de body in de range " \
                              "bij de for loop."
        # render the template
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


# resultaten pagina
@app.route('/populatie.html', methods=["POST", "GET"])
def populatie():
    """
    pagina met onderzoeksresultaten, de opgehaalde data is de tien
    meest voorkomende organismen in de database
    :return:
    resultatenpagina met tien meest voorkomende organismen
    """
    # haalt query op met top tien meest voorkomende organismen
    tabledata = databasecounter()
    # render de template met de table data
    return render_template('populatie.html', tabledata=tabledata)


# informatie over de applicatie en het project/
@app.route('/info.html')
def info():
    """
    :return:
    render de info.html template met informatie over de applicatie
    """
    return render_template('info.html')


# over ons pagina
@app.route('/over_ons.html')
def over_ons():
    """
    :return:
    render de over_ons.html template met informatie over de
    onderzoeksgroep
    """
    return render_template('over_ons.html')


# blast pagina
@app.route('/blast.html', methods=["POST", "GET"])
def blast():
    """
    deze functie rendert de blast.html template
    op de pagina kan de gebruiker een sequentie invoeren, deze wordt
    geblast en toegevoegd aan de bestaande database
    als de sequentie meer dan DNA-code is wordt het process gestopt

    input: DNA-sequentie
    output: Blast resultaat en toevoeging in de database
    """
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

            # Blast de protein sequentie tegen de blastx database.
            result_handle = NCBIWWW.qblast("blastx", "nr", sequentie,
                                           hitlist_size=1)

            # Schrijft de output van BLAST weg in XML bestand.
            with open("XMLBlastWebsite.xml", "w") as out_handle:
                out_handle.write(result_handle.read())

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
                mestdatadic[fwcount] = [mestdata[0], mestdata[1],
                                        mestdata[2]]
                mestdatadic[revcount] = [mestdata[3], mestdata[4],
                                         mestdata[5]]
                fwcount += 2
                revcount += 2
            for c in hits:
                if count <= 50:
                    # Haal de data uit de hit en zet deze in een zelf
                    # beschrijvende variabele
                    Hit_id = c.find('Hit_id').text
                    discript = c.find('Hit_def').text
                    totaallengte = c.find('Hit_len').text
                    querybegin = c.find(
                        'Hit_hsps/Hsp/Hsp_query-from').text
                    queryeind = c.find('Hit_hsps/Hsp/Hsp_query-to').text
                    querycoverage = (int(queryeind) - int(
                        querybegin)) / int(
                        totaallengte)
                    organis = discript.split('[')
                    organism = organis[1].split(']')
                    description = organis[0]
                    organisme = organism[0]
                    acessiecode = c.find('Hit_accession').text
                    print(acessiecode)
                    hit = c.find('Hit_num').text
                    score = c.find('Hit_hsps/Hsp/Hsp_bit-score').text
                    tscore = c.find('Hit_hsps/Hsp/Hsp_score').text
                    evalue = c.find('Hit_hsps/Hsp/Hsp_evalue').text
                    percidentity = \
                        c.find('Hit_hsps/Hsp/Hsp_identity').text
                    queryseq = c.find('Hit_hsps/Hsp/Hsp_qseq').text
                    header = ""
                    ascicode = ""
                    time.sleep(0.4)
                    Entrez.email = "thijschermens@gmail.com"
                    seqio = Entrez.efetch(db="protein", id=acessiecode,
                                          retmode="xml")
                    seqio_read = Entrez.read(seqio)
                    seqio.close()
                    lineage = seqio_read[0]["GBSeq_taxonomy"].split(";")
                    if hit == str(1):
                        keycounter += 1
                        for (key, value) in mestdatadic.items():
                            if key == keycounter:
                                nbheader = str(value[0])
                                hbheader = nbheader.split('@')
                                header += hbheader[1]
                                ascicode += str(value[2])

                    else:
                        for (key, value) in mestdatadic.items():
                            if key == keycounter:
                                nbheader = str(value[0])
                                hbheader += nbheader.split('@')
                                header += hbheader[1]
                                ascicode += str(value[2])

                    # Print alle data om te zien of het gewerkt heeft
                    datalist = [Hit_id, description, organisme,
                                acessiecode, score, tscore, evalue,
                                percidentity, queryseq, header,
                                ascicode, lineage, querycoverage]
                    datadic[count] = datalist
                    count += 1
            else:
                pass
            datalijst = []
            # [1]=name [3]=accessiecode [7]=percentidentity [6]=e-value
            # [4]=max-score [5]=totale_score [-1]=query-cov [2]=org_naam
            # [11][-1]=linnaam [9]=header [8]=sequence [10]=ascii
            for i in datadic:
                datalijst.append(datadic[i])

            # Als er geen hits zijn gevonden met blasten:
            if datalijst == []:
                geenresultaten = "Er zijn geen resultaten gevonden"

            # Return webpagina met de gegevens als iets is ingevuld in
            # de textbox.
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


# roep de app aan
if __name__ == '__main__':
    app.run()
