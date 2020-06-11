# Ivar van den Akker
# 18-05-2020 tot 7-06-2020
# Script dat heel veel data uit 2 bestanden en 1 database haalt deze
# in een dictionary zet en met de dictionary de database vult

# Zorg ervoor dat dit script in de zelfde directory staat
# als alle xml bestanden
import mysql.connector
from xml.etree import ElementTree
import time
from Bio import Entrez
import os

teller1 = 0
teller2 = 0
teller3 = 0
teller4 = 0
keycounter = 1


# FW:17-25-91-100
# RV:17-25-34-94

def getdata(datafile, filename):
    """
    Deze functie opend een voor een alle xml bestanden en de
    datafile waar de orginele sequenties in zitten. Al deze
    data zet die bij elkaar in een dictionary om door te
    geven naar de functie pushdata
    :param datafile:
    :param filename:
    :return:
    """
    # Door bestand heen gaan
    dom = ElementTree.parse(filename)
    # Alle hits eruit zoeken
    hits = dom.findall('BlastOutput_iterations/Iteration/Iteration_hits/Hit')
    # Voor elke hit
    count = 1
    datadic = {}
    mestdatadic = {}
    file = open(datafile)
    fwcount = 1
    revcount = 2
    # Zet alle read data in een lijst fw en rev
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
            hit_id = c.find('Hit_id').text
            discript = c.find('Hit_def').text
            totaallengte = c.find('Hit_len').text
            querybegin = c.find('Hit_hsps/Hsp/Hsp_query-from').text
            queryeind = c.find('Hit_hsps/Hsp/Hsp_query-to').text
            querycovarage = (int(queryeind) - int(querybegin)) / int(
                totaallengte)
            print(discript)
            organis = discript.split('[')
            organism = organis[1].split(']')
            discription = organis[0]
            organisme = organism[0]
            acessiecode = c.find('Hit_accession').text
            print(acessiecode)
            hit = c.find('Hit_num').text
            score = c.find('Hit_hsps/Hsp/Hsp_bit-score').text
            tscore = c.find('Hit_hsps/Hsp/Hsp_score').text
            evalue = c.find('Hit_hsps/Hsp/Hsp_evalue').text
            percidentity = c.find('Hit_hsps/Hsp/Hsp_identity').text
            queryseq = c.find('Hit_hsps/Hsp/Hsp_qseq').text
            header = ""
            ascicode = ""
            # De volgende 6 lines haalen de lineage op
            time.sleep(0.4)
            Entrez.email = "thijschermens@gmail.com"
            seqio = Entrez.efetch(db="protein", id=acessiecode, retmode="xml")
            seqio_read = Entrez.read(seqio)
            seqio.close()
            lineage = seqio_read[0]["GBSeq_taxonomy"].split(";")
            # De volgende 16 lines zorgen ervoor dat de goede sequentie
            # bij de goede hit komt te staan
            if hit == str(1):
                global keycounter
                keycounter += 2
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
                        hbheader = nbheader.split('@')
                        header += hbheader[1]
                        ascicode += str(value[2])

            # Print alle data om te zien of het gewerkt heeft
            datalist = [hit_id, discription, organisme, acessiecode, score,
                        tscore, evalue, percidentity, queryseq, header,
                        ascicode, lineage, querycovarage]
            datadic[count] = datalist
            count += 1
    else:
        pass
    # print(datadic)
    print('Data Received')

    return datadic


def pushdata(datadic, numer):
    """ Deze functie neemt de dictionary datadic aan, hieruit haalt
    hij alle gegevens voor in de database en zet deze in de database
    elke keer word ook gekeken of het item al bestaat in de database.
    :param datadic:
    :return:
    """
    # Connectie met database maken
    print("Connecting to database.....")
    # Inlog gegevens voor Azure database (nette database)
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
             "azure.com",
        user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
        db="iaoqi", password="638942")
    # Inlog gegevens voor oefen database (Hier het script op testen)
    # conn = mysql.connector.connect(
    #     host="sql2.freemysqlhosting.net",
    #     user="sql234812",
    #     db="sql234812", password="iM4*eV6%")
    # print("Connected")
    # Roept de global variabele aan om bij te werken
    global teller1
    global teller2
    global teller3
    global teller4
    # Voor elke regel in de dictionary waar de data in staat
    for i in datadic:
        countlin = 0
        # Kijk of de plek gevult is met data
        if datadic[i][11] != "":
            for j in datadic[i][11]:
                print(j)
                lincheck = conn.cursor(buffered=True)
                string1 = f"select name from lineage where name = '{j}'"
                lincheck.execute(string1)
                conn.commit()
                test = lincheck.fetchall()
                lincheck.close()
                # Als test leeg is: (Dus er is niets gevonden in de dataase)
                if test == []:
                    # countlin 0 is (dus het is de erste lineage in de rij
                    if countlin == 0:
                        cursor = conn.cursor()
                        # Zet lineage in de database
                        string2 = f"insert into lineage (id, name) values " \
                                  f"('{teller1}', " \
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
                        string3 = f"select id from lineage where name " \
                                  f"= '{datadic[i][11][formercount]}'"
                        linid.execute(string3)
                        conn.commit()
                        liniageid = linid.fetchall()
                        replacer = str(liniageid[0])
                        replace1 = replacer.replace('(', "").replace\
                            (',', "").replace(')', "")
                        linid.close()
                        cursor = conn.cursor()
                        # Zet lineage in de database met parent key
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
                    # Print dat het item al bestaat
                    print("Item", j, "bestaat al")
                    countlin += 1
                    pass
            print("lineage fill for ", datadic[i][3], " completed\n\n\n\n\n")
            # Kijk of de plek gevult is met data
        if datadic[i][2] != "":
            # Kijken of de data die in de database gaat er al in staat
            cursorchecko = conn.cursor(buffered=True)
            string5 = f"select naam_organismenaam from organisme where " \
                      f"naam_organismenaam = '{datadic[i][2]}'"
            cursorchecko.execute(string5)
            conn.commit()
            organismecheck = cursorchecko.fetchall()
            cursorchecko.close()
            # Als de variabele leeg blijft data in de database zetten
            if organismecheck == []:
                # Het id van linage ophalen om deze in de
                # organisme tabel te zetten
                linidcursor = conn.cursor(buffered=True)
                string6 = f"select id from lineage where name " \
                          f"= '{datadic[i][11][-1]}'"
                linidcursor.execute(string6)
                conn.commit()
                # Het id prepareren zodat het alleen een cijfer is
                # ipv een lijst met cursor hits
                orglin = linidcursor.fetchall()
                linidcursor.close()
                replacer1 = str(orglin[0])
                replace2 = replacer1.replace('(', "").replace(',', "").replace(
                    ')', "")
                variabele1 = datadic[i][2]
                # Vul de tabel organisme
                cursor = conn.cursor()
                string7 = f"insert into organisme (id, naam_organismenaam, " \
                          f"lineage_id) values ('{teller2}', '{variabele1}'" \
                          f", '{replace2}')"
                cursor.execute(string7)
                conn.commit()
                cursor.close()
                # Print dat de data in de database staat
                print("Organisme fill for ", datadic[i][3],
                      " completed\n\n\n\n\n")
                teller2 += 1
                # Print als het organisme al in de database staat
            else:
                print(cursorchecko, "bestaat al")
                pass
        # Kijk of de plek gevult is met data
        if datadic[i][9] != "":
            # Kijken of de data die in de database gaat er al in staat
            cursorchecks = conn.cursor(buffered=True)
            string8 = f"select header from sequentie where header " \
                      f"= '{datadic[i][9]}'"
            cursorchecks.execute(string8)
            print(datadic[i][9])
            conn.commit()
            sequencecheck = cursorchecks.fetchall()
            cursorchecks.close()
            print(sequencecheck)
            # Als de variabele leeg blijft data in de database zetten
            if sequencecheck == []:
                cursor = conn.cursor()
                # Zet de sequentie in de database
                string9 = f"insert into sequentie (id, header, sequence, " \
                          f"asci_score, _read_) values ('{teller3}', " \
                          f"'{datadic[i][9]}', '{datadic[i][8]}', " \
                          f"'{datadic[i][10]}', '{numer}')"
                cursor.execute(string9)
                conn.commit()
                cursor.close()
                print("Sequentie fill for ", datadic[i][3],
                      " completed\n\n\n\n\n")
                teller3 += 1
                # Print item bestaat al als het in de database staat
            else:
                print(cursorchecks, "bestaat al")
                pass
        # Kijk of de plek gevult is met data
        if datadic[i][1] != "":
            # Kijk of het eiwit al in de database staat
            eiwitcheck = conn.cursor(buffered=True)
            string13 = f"select accessiecode from eiwit where accessiecode " \
                       f"= '{datadic[i][3]}'"
            eiwitcheck.execute(string13)
            print(datadic[i][9])
            conn.commit()
            eiwitchecksd = eiwitcheck.fetchall()
            print("-------\n\n", eiwitchecks, "\n\n--------")
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
                replace3 = replacer2.replace('(', "").replace(',', "").replace(
                    ')', "")
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
                replace4 = replacer3.replace('(', "").replace(',', "").replace(
                    ')', "")
                # De eiwit tabel vullen met data
                cursor = conn.cursor()
                string12 = f"insert into eiwit (id, description, " \
                           f"accessiecode, percent_identity, e_value, " \
                           f"max_score, total_score, query_cover, " \
                           f"sequentie_id, Organisme_id) values ('{teller4}'" \
                           f", '{datadic[i][1]}', '{datadic[i][3]}', " \
                           f"'{datadic[i][7]}', '{datadic[i][6]}', " \
                           f"'{datadic[i][4]}', '{datadic[i][5]}', " \
                           f"'{datadic[i][12]}', '{replace3}', '{replace4}')"
                cursor.execute(string12)
                conn.commit()
                cursor.close()
                teller4 += 1
                # Print al het vullen van de hit in de database
                # is gelukt
                print("Eiwit  fill for ", datadic[i][3], " completed")
            # Print als het eiwit al bestaat
            else:
                print("Eiwit ", datadic[i][3], "bestaat al")
    print("Database filled!\nClosing connection....")
    # Connectie met database sluiten
    conn.close()
    print("Connection closed task compleded.")
    return


def main():
    datafile = 'dataset.txt'
    # Voer functie uit voor alle fw reads (xml files)
    for i in range(1, 101):
        filename = "XMLForward" + str(i) + ".xml"
        datadic = getdata(datafile, filename)
        #pushdata(datadic, numer=1)
        print("Forward read ", str(i), " is verwerkt!\n", teller1, teller2,
              teller3, teller4)
    print("Forward reads verwerkt!\n\n", teller1, teller2, teller3, teller4,
          keycounter)
    # Voer functie uit voor alle reverse reads (xml files)
    for k in range(1, 101):
        # Zet de keycounter goed voor de reverse reads
        keycounter -= 199
        filename = "XMLReverse" + str(k) + ".xml"
        datadic = getdata(datafile, filename)
        #pushdata(datadic, numer=2)
        print("Forward read ", str(k), " is verwerkt!\n", teller1, teller2,
              teller3, teller4, keycounter)
    print("Reverse reads verwerkt!\n\n", teller1, teller2, teller3, teller4,
          keycounter)


main()
