# Om de applicatie te runnen moet dit script gestart worden.
# Op deze pagina komen alle andere scripts samen tot een webapplicatie

# ophalen van alle modules
from flask import Flask, render_template, request
from Websitescript import zoeken, databasecounter
from Bio.Blast import NCBIWWW, NCBIXML
from xml.etree import ElementTree
import time
from Bio import Entrez
import mysql.connector

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
    # SELECT id FROM eiwit ORDER BY id DESC LIMIT 1;
    # SELECT id FROM sequentie ORDER BY id DESC LIMIT 1;
    # SELECT id FROM organisme ORDER BY id DESC LIMIT 1;
    # SELECT id FROM lineage ORDER BY id DESC LIMIT 1;
    conn = mysql.connector.connect(
             host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
                  "azure.com",
             user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
             db="iaoqi", password="638942")
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

            # Door bestand heen gaan
            dom = ElementTree.parse(XMLFile)
            # Alle hits eruit zoeken
            hits = dom.findall(
                'BlastOutput_iterations/Iteration/Iteration_hits/Hit')
            # Voor elke hit
            datadic = {}
            for c in hits:
                cursor = conn.cursor()
                string2 = f"SELECT id FROM eiwit ORDER BY id DESC LIMIT 1"
                cursor.execute(string2)
                conn.commit()
                eiwitid = cursor.fetchall()
                replacer = str(eiwitid[0])
                coreid = replacer.replace('(', "").replace \
                    (',', "").replace(')', "")
                cursor.close()
                if count <= 50:
                    # Haal de data uit de hit en zet deze in een zelf
                    # beschrijvende variabele
                    discript = c.find('Hit_def').text
                    totaallengte = c.find('Hit_len').text
                    querybegin = c.find(
                        'Hit_hsps/Hsp/Hsp_query-from').text
                    queryeind = c.find('Hit_hsps/Hsp/Hsp_query-to').text
                    querycoverage = (int(queryeind) - int(
                        querybegin)) / int(
                        totaallengte)
                    organis = discript.split('[')
                    organisme = organis[-1].strip(']')
                    acessiecode = c.find('Hit_accession').text
                    print(acessiecode)
                    score = c.find('Hit_hsps/Hsp/Hsp_bit-score').text
                    tscore = c.find('Hit_hsps/Hsp/Hsp_score').text
                    evalue = c.find('Hit_hsps/Hsp/Hsp_evalue').text
                    percidentity = \
                        c.find('Hit_hsps/Hsp/Hsp_identity').text
                    queryseq = c.find('Hit_hsps/Hsp/Hsp_qseq').text
                    header = "Website Blast"
                    ascicode = "Null"
                    time.sleep(0.4)
                    Entrez.email = "thijschermens@gmail.com"
                    seqio = Entrez.efetch(db="protein", id=acessiecode,
                                          retmode="xml")
                    seqio_read = Entrez.read(seqio)
                    seqio.close()
                    lineage = seqio_read[0]["GBSeq_taxonomy"].split(";")
                    eiwitid = coreid + 1
                    # Print alle data om te zien of het gewerkt heeft
                    datalist = [description, organisme,
                                acessiecode, score, tscore, evalue,
                                percidentity, queryseq, header,
                                ascicode, lineage, querycoverage]
                    datadic[eiwitid] = datalist
                    for i in datadic:
                        countlin = 0
                        for j in datadic[i][10]:
                            lincheck = conn.cursor(buffered=True)
                            string1 = f"select name from lineage where name = '{j}'"
                            lincheck.execute(string1)
                            conn.commit()
                            test = lincheck.fetchall()
                            lincheck.close()

                            lineageid = f"SELECT id FROM lineage ORDER BY id DESC LIMIT 1"
                            cursor.execute(lineageid)
                            conn.commit()
                            lineagelastid = cursor.fetchall()
                            replacer1 = str(lineagelastid[0])
                            replace2 = replacer1.replace('(', "").replace \
                                (',', "").replace(')', "")
                            cursor.close()
                            teller1 = replace2 + 1
                            if test == []:
                                if countlin != 0:
                                    string2 = f"insert into lineage (id, name) values " \
                                              f"('{teller1}', " \
                                              f"'{datadic[i][10][countlin]}')"
                                    cursor.execute(string2)
                                    conn.commit()
                                    cursor.close()
                                else:
                                    formercount = countlin - 1
                                    string3 = f"select parent_id from lineage where name " \
                                              f"= '{datadic[i][10][formercount]}'"
                                    linid.execute(string3)
                                    conn.commit()
                                    pliniageid = linid.fetchall()
                                    replacer = str(pliniageid[0])
                                    replace1 = replacer.replace('(', "").replace\
                                        (',', "").replace(')', "")
                                    linid.close()
                                    string4 = f"insert into lineage (id, name, " \
                                              f"parent_id) values ('{teller1}', " \
                                              f"'{datadic[i][10][countlin]}', " \
                                              f"'{replace1}')"
                                    cursor.execute(string4)
                                    conn.commit()
                                    cursor.close()
                                    countlin += 1
                            else:
                                pass
                        cursor = conn.cursor()
                        linidcursor = conn.cursor(buffered=True)
                        string6 = f"select id from lineage where name " \
                                  f"= '{datadic[i][10][-1]}'"
                        linidcursor.execute(string6)
                        conn.commit()
                        # Het id prepareren zodat het alleen een cijfer is
                        # ipv een lijst met cursor hits
                        orglin = linidcursor.fetchall()
                        linidcursor.close()
                        replacer2 = str(orglin[0])
                        replace3 = replacer2.replace('(', "").replace(',',
                                                                      "").replace(
                            ')', "")


                        cursor = conn.cursor()
                        organismelastid = f"SELECT id FROM organisme ORDER BY id DESC LIMIT 1"
                        cursor.execute(organismelastid)
                        conn.commit()
                        organismelastid = cursor.fetchall()
                        replacer3 = str(organismelastid[0])
                        replace4 = replacer3.replace('(', "").replace \
                            (',', "").replace(')', "")
                        cursor.close()

                        teller2 = int(replace4) + 1

                        cursor = conn.cursor()
                        string7 = f"insert into organisme (id, naam_organismenaam, " \
                                  f"lineage_id) values ('{teller2}', '{datadic[i][1]}'" \
                                  f", '{replace3}')"
                        cursor.execute(string7)
                        conn.commit()
                        cursor.close()

                        cursor = conn.cursor()
                        sequentielastid = f"SELECT id FROM sequentie ORDER BY id DESC LIMIT 1"
                        cursor.execute(sequentielastid)
                        conn.commit()
                        sequentielastid = cursor.fetchall()
                        replacer4 = str(sequentielastid[0])
                        replace5 = replacer4.replace('(', "").replace \
                            (',', "").replace(')', "")
                        cursor.close()

                        teller3 = int(replace5) + 1

                        numer = 3
                        cursor = conn.cursor()
                        # Zet de sequentie in de database
                        string9 = f"insert into sequentie (id, header, sequence, " \
                                  f"asci_score, _read_) values ('{teller3}', " \
                                  f"'{datadic[i][8]}', '{datadic[i][7]}', " \
                                  f"'{datadic[i][9]}', '{numer}')"
                        cursor.execute(string9)
                        conn.commit()
                        cursor.close()

                        seqidcursor = conn.cursor(buffered=True)
                        string10 = f"select id from sequentie where header " \
                                   f"= '{datadic[i][8]}'"
                        seqidcursor.execute(string10)
                        conn.commit()
                        seqid = seqidcursor.fetchall()
                        seqidcursor.close()
                        replacer6 = str(seqid[0])
                        replace7 = replacer6.replace('(', "").replace(',',
                                                                      "").replace(
                            ')', "")
                        # Het id van organisme ophalen om deze in de
                        # eiwit tabel te zetten
                        orgidcursor = conn.cursor(buffered=True)
                        string11 = f"select id from organisme where " \
                                   f"naam_organismenaam = '{datadic[i][1]}'"
                        orgidcursor.execute(string11)
                        conn.commit()
                        orgid = orgidcursor.fetchall()
                        orgidcursor.close()
                        replacer7 = str(orgid[0])
                        replace8 = replacer7.replace('(', "").replace(',',
                                                                      "").replace(
                            ')', "")
                        # De eiwit tabel vullen met data
                        cursor = conn.cursor()
                        string12 = f"insert into eiwit (id, description, " \
                                   f"accessiecode, percent_identity, e_value, " \
                                   f"max_score, total_score, query_cover, " \
                                   f"sequentie_id, Organisme_id) values ('{i}'" \
                                   f", '{datadic[i][0]}', '{datadic[i][2]}', " \
                                   f"'{datadic[i][6]}', '{datadic[i][5]}', " \
                                   f"'{datadic[i][3]}', '{datadic[i][4]}', " \
                                   f"'{datadic[i][11]}', '{replace7}', '{replace8}')"
                        cursor.execute(string12)
                        conn.commit()
                        cursor.close()

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
