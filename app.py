from flask import Flask, render_template, request
from Websitescript import zoeken, databasecounter
from Bio.Blast import NCBIWWW
from xml.etree import ElementTree
import time
from Bio import Entrez
import mysql.connector


app = Flask(__name__)


@app.route('/')
@app.route('/home.html', methods=["POST", "GET"])
def database():
    if request.method == "POST":
        buttonselect = request.form.get("selection", "")

        zoekopdracht = request.form.get("zoek", "")

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
            # Blast de protein sequentie tegen de blastx database.
            result_handle = NCBIWWW.qblast("blastx", "nr", sequentie,
                                           hitlist_size=25)

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
            for line in file:
                mestdata = line.split('\t')
                mestdatadic[fwcount] = [mestdata[0], mestdata[1], mestdata[2]]
                mestdatadic[revcount] = [mestdata[3], mestdata[4], mestdata[5]]
                fwcount += 2
                revcount += 2
            for c in hits:
                if count <= 25:
                    # Haal de data uit de hit en zet deze in een
                    # zelfbeschrijvende variabele
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

                    datalist = [Hit_id, description, organisme, acessiecode,
                                score, tscore, evalue, percidentity,
                                queryseq, header, ascicode, lineage,
                                querycoverage]
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

            conn = mysql.connector.connect(
                host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
                     "azure.com",
                user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
                db="iaoqi", password="638942")

            teller1cursor = conn.cursor() # lineage id
            teller1string = "select id from lineage order by id desc limit 1;"
            teller1cursor.execute(teller1string)
            teller1fetch = teller1cursor.fetchall()
            teller1string = str(teller1fetch[0]).replace("(", "").replace\
                (",", "").replace(")", "")
            teller1 = int(teller1string) + 1
            teller1cursor.close()

            teller2cursor = conn.cursor() # organisme id
            teller2string = "select id from organisme order by id desc " \
                            "limit 1;"
            teller2cursor.execute(teller2string)
            teller2fetch = teller2cursor.fetchall()
            teller2string = str(teller2fetch[0]).replace("(", "").\
                replace(",", "").replace(")", "")
            teller2 = int(teller2string) + 1
            teller2cursor.close()

            teller3cursor = conn.cursor() # sequentie id
            teller3string = "select id from sequentie order by id desc " \
                            "limit 1;"
            teller3cursor.execute(teller3string)
            teller3fetch = teller3cursor.fetchall()
            teller3string = str(teller3fetch[0]).replace("(", "").\
                replace(",", "").replace(")", "")
            teller3 = int(teller3string) + 1
            teller3cursor.close()

            teller4cursor = conn.cursor() # eiwit id
            teller4string = "select id from eiwit order by id desc limit 1;"
            teller4cursor.execute(teller4string)
            teller4fetch = teller4cursor.fetchall()
            teller4string = str(teller4fetch[0]).replace("(", "").\
                replace(",", "").replace(")", "")
            teller4 = int(teller4string) + 1
            teller4cursor.close()

            read = 3

            for i in datadic:
                countlin = 0
                # Kijk of de plek gevult is met data
                if datadic[i][11] != "":
                    for j in datadic[i][11]:
                        lincheck = conn.cursor(buffered=True)
                        string1 = f"select name from lineage where name = " \
                                  f"'{j}'"
                        lincheck.execute(string1)
                        conn.commit()
                        test = lincheck.fetchall()
                        lincheck.close()
                        # Als test leeg is: (Dus er is niets gevonden in
                        # de database)
                        if test == []:
                            # countlin 0 is (dus het is de eerste
                            # lineage in de rij
                            if countlin == 0:
                                cursor = conn.cursor()
                                # Zet lineage in de database
                                string2 = f"insert into lineage (id, name) " \
                                          f"values ('{teller1}', " \
                                          f"'{datadic[i][11][countlin]}')"
                                cursor.execute(string2)
                                conn.commit()
                                cursor.close()
                                countlin += 1
                                teller1 += 1
                                # Als het niet de eerste lineage is
                            else:
                                formercount = countlin - 1
                                # Vul de lineage tabel met data
                                linid = conn.cursor(buffered=True)
                                # Haal het parent id op
                                string3 = f"select id from lineage where " \
                                          f"name = " \
                                          f"'{datadic[i][11][formercount]}'"
                                linid.execute(string3)
                                conn.commit()
                                liniageid = linid.fetchall()
                                replacer = str(liniageid[0])
                                replace1 = replacer.replace('(', "").\
                                    replace(',', "").replace(')', "")
                                linid.close()
                                cursor = conn.cursor()
                                # Zet lineage in de database met parent
                                # key
                                string4 = f"insert into lineage (id, name, " \
                                          f"parent_id) values ('{teller1}', " \
                                          f"'{datadic[i][11][countlin]}', " \
                                          f"'{replace1}')"
                                cursor.execute(string4)
                                conn.commit()
                                cursor.close()
                                countlin += 1
                                teller1 += 1
                        # Als test wel gevult is
                        else:
                            countlin += 1
                            pass
                    # Kijk of de plek gevult is met data
                if datadic[i][2] != "":
                    # Kijken of de data die in de database gaat er al in
                    # staat
                    cursorchecko = conn.cursor(buffered=True)
                    string5 = f"select naam_organismenaam from organisme " \
                              f"where naam_organismenaam = '{datadic[i][2]}'"
                    cursorchecko.execute(string5)
                    conn.commit()
                    organismecheck = cursorchecko.fetchall()
                    cursorchecko.close()
                    # Als de variabele leeg blijft data in de database
                    # zetten
                    if organismecheck == []:
                        # Het id van linage ophalen om deze in de
                        # organisme tabel te zetten
                        linidcursor = conn.cursor(buffered=True)
                        string6 = f"select id from lineage where name " \
                                  f"= '{datadic[i][11][-1]}'"
                        linidcursor.execute(string6)
                        conn.commit()
                        # Het id prepareren zodat het alleen een cijfer
                        # is ipv een lijst met cursor hits
                        orglin = linidcursor.fetchall()
                        linidcursor.close()
                        replacer1 = str(orglin[0])
                        replace2 = replacer1.replace('(', "").replace\
                            (',', "").replace(')', "")
                        variabele1 = datadic[i][2]
                        # Vul de tabel organisme
                        cursor = conn.cursor()
                        string7 = f"insert into organisme (id, " \
                                  f"naam_organismenaam, lineage_id) values " \
                                  f"('{teller2}', '{variabele1}', " \
                                  f"'{replace2}')"
                        cursor.execute(string7)
                        conn.commit()
                        cursor.close()
                        teller2 += 1
                    else:
                        pass
                # Kijk of de plek gevult is met data
                if datadic[i][9] != "":
                    # Kijken of de data die in de database gaat er al in
                    # staat
                    cursorchecks = conn.cursor(buffered=True)
                    string8 = f"select sequence from sequentie where " \
                              f"sequence = '{datadic[i][8]}'"
                    cursorchecks.execute(string8)
                    conn.commit()
                    sequencecheck = cursorchecks.fetchall()
                    cursorchecks.close()
                    # Als de variabele leeg blijft data in de database
                    # zetten
                    if sequencecheck == []:
                        cursor = conn.cursor()
                        # Zet de sequentie in de database
                        string9 = f"insert into sequentie (id, header, " \
                                  f"sequence, asci_score, _read_) values " \
                                  f"('{teller3}', '{datadic[i][9]}', " \
                                  f"'{datadic[i][8]}', '{datadic[i][10]}', " \
                                  f"'{read}')"
                        cursor.execute(string9)
                        conn.commit()
                        cursor.close()
                        teller3 += 1
                    else:
                        pass
                # Kijk of de plek gevult is met data
                if datadic[i][1] != "":
                    # Kijk of het eiwit al in de database staat
                    eiwitcheck = conn.cursor(buffered=True)
                    string13 = f"select accessiecode from eiwit where " \
                               f"accessiecode = '{datadic[i][3]}'"
                    eiwitcheck.execute(string13)
                    conn.commit()
                    eiwitchecks = eiwitcheck.fetchall()
                    eiwitcheck.close()
                    # Als het eiwit niet in de database staat
                    if eiwitchecks == []:
                        # Het id van sequentie ophalen om deze in
                        # de organisme tabel te zetten
                        seqidcursor = conn.cursor(buffered=True)
                        string10 = f"select id from sequentie where header " \
                                   f"= '{datadic[i][9]}'"
                        seqidcursor.execute(string10)
                        conn.commit()
                        seqid = seqidcursor.fetchall()
                        seqidcursor.close()
                        replacer2 = str(seqid[0])
                        replace3 = replacer2.replace('(', "").\
                            replace(',', "").replace(')', "")
                        # Het id van organisme ophalen om deze in de
                        # eiwit tabel te zetten
                        orgidcursor = conn.cursor(buffered=True)
                        string11 = f"select id from organisme where " \
                                   f"naam_organismenaam = '{datadic[i][2]}'"
                        orgidcursor.execute(string11)
                        conn.commit()
                        orgid = orgidcursor.fetchall()
                        orgidcursor.close()
                        replacer3 = str(orgid[0])
                        replace4 = replacer3.replace('(', "").\
                            replace(',', "").replace(')', "")
                        # De eiwit tabel vullen met data
                        cursor = conn.cursor()
                        string12 = f"insert into eiwit (id, description, " \
                                   f"accessiecode, percent_identity, " \
                                   f"e_value, max_score, total_score, " \
                                   f"query_cover, sequentie_id, " \
                                   f"Organisme_id) values ('{teller4}', " \
                                   f"'{datadic[i][1]}', '{datadic[i][3]}', " \
                                   f"'{datadic[i][7]}', '{datadic[i][6]}', " \
                                   f"'{datadic[i][4]}', '{datadic[i][5]}', " \
                                   f"'{datadic[i][12]}', '{replace3}', " \
                                   f"'{replace4}')"
                        cursor.execute(string12)
                        conn.commit()
                        cursor.close()
                        teller4 += 1
                    else:
                        pass
            conn.close()

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


if __name__ == '__main__':
    app.run()
