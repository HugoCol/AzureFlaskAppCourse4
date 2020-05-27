# Ivar van den Akker
# 18-05-2020 tot 27-05-2020
# Script dat heel veel data uit 2 bestanden en 1 database haalt deze
# in een dictionary zet en met de dictionary de database vult
import mysql.connector
from xml.etree import ElementTree
import time
from Bio import Entrez
import os

teller1 = 0
teller2 = 0
teller3 = 0
teller4 = 0

def getdata(datafile, filename):
    """
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
    keycounter = 0
    for line in file:
        mestdata = line.split('\t')
        mestdatadic[fwcount] = [mestdata[0], mestdata[1], mestdata[2]]
        mestdatadic[revcount] = [mestdata[3], mestdata[4], mestdata[5]]
        fwcount += 2
        revcount += 2
    for c in hits:
        if count <= 25:
            # Haal de data uit de hit en zet deze in een zelfbeschrijvende variabele
            Hit_id = c.find('Hit_id').text
            discript = c.find('Hit_def').text
            totaallengte = c.find('Hit_len').text
            querybegin = c.find('Hit_hsps/Hsp/Hsp_query-from').text
            queryeind = c.find('Hit_hsps/Hsp/Hsp_query-to').text
            querycovarage = (int(queryeind)-int(querybegin))/int(totaallengte)
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
            time.sleep(0.4)
            Entrez.email = "thijschermens@gmail.com"
            seqio = Entrez.efetch(db="protein", id=acessiecode, retmode="xml")
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
            datalist = [Hit_id, discription, organisme, acessiecode, score,
                        tscore, evalue, percidentity, queryseq, header,
                        ascicode, lineage, querycovarage]
            datadic[count] = datalist
            count += 1
    else:
        pass
    #print(datadic)
    print('Data Received')


    return datadic


def pushdata(datadic):
    """
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
    # Voor elke regel in de dictionary waar de data in staat
    global teller1
    global teller2
    global teller3
    global teller4
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
                print(lincheck)
                print(test)
                if test==[]:
                    if countlin == 0:
                        cursor = conn.cursor()
                        string2 = f"insert into lineage (id, name) values ('{teller1}', '{datadic[i][11][countlin]}')"
                        cursor.execute(string2)
                        conn.commit()
                        cursor.close()
                        countlin += 1
                        teller1 += 1
                    else:
                        formercount = countlin - 1
                        print(formercount)
                        # Vul de lineage tabel met data
                        linid = conn.cursor(buffered=True)
                        string3 = f"select id from lineage where name = '{datadic[i][11][formercount]}'"
                        linid.execute(string3)
                        conn.commit()
                        liniageid = linid.fetchall()
                        replacer = str(liniageid[0])
                        replace1 = replacer.replace('(',"").replace(',', "").replace(')', "")
                        print(replace1)
                        linid.close()
                        cursor = conn.cursor()
                        string4 = f"insert into lineage (id, name, parent_id) values ('{teller1}', '{datadic[i][11][countlin]}', '{replace1}')"
                        cursor.execute(string4)
                        conn.commit()
                        cursor.close()
                        countlin += 1
                        teller1 += 1

                else:
                    print("Item", j, "bestaat al")
                    countlin += 1
                    pass
            print("lineage fill for ", datadic[i][3], " completed\n\n\n\n\n")
            # Kijk of de plek gevult is met data
        if datadic[i][2] != "":
            # Kijken of de data die in de database gaat er al in staat
            cursorchecko = conn.cursor(buffered=True)
            string5 = f"select naam_organismenaam from organisme where naam_organismenaam = '{datadic[i][2]}'"
            cursorchecko.execute(string5)
            conn.commit()
            organismecheck = cursorchecko.fetchall()
            cursorchecko.close()
            # Als de variabele leeg blijft data in de database zetten
            if organismecheck == []:
                # Het id van linage ophalen om deze in de organisme tabel te zetten
                linidcursor = conn.cursor(buffered=True)
                string6 = f"select id from lineage where name = '{datadic[i][11][-1]}'"
                linidcursor.execute(string6)
                conn.commit()
                orglin = linidcursor.fetchall()
                linidcursor.close()
                replacer1 = str(orglin[0])
                replace2 = replacer1.replace('(', "").replace(',', "").replace(')', "")
                print(datadic[i][2])
                print(datadic[i][0])
                cursor = conn.cursor()
                string7 = f"insert into organisme (id, naam_organismenaam, lineage_id, eiwit_id) values ('{teller2}', '{datadic[i][2]}', '{replace2}', '{datadic[i][0]}')"
                cursor.execute(string7)
                conn.commit()
                cursor.close()
                print("Organisme fill for ", datadic[i][3], " completed")
                teller2 += 1
            else:
                print(cursorchecko, "bestaat al")
                pass
        # Kijk of de plek gevult is met data
        if datadic[i][9] != "":
            # Kijken of de data die in de database gaat er al in staat
            cursorchecks = conn.cursor(buffered=True)
            string8 = f"select header from sequentie where header = '{datadic[i][9]}'"
            cursorchecks.execute(string8)
            conn.commit()
            sequencecheck = cursorchecks.fetchall()
            cursorchecks.close()
            # Als de variabele leeg blijft data in de database zetten
            if sequencecheck == []:
                cursor = conn.cursor()
                string9 = f"insert into sequentie (id, header, sequence, asci_score, read) values ('{teller3}','{datadic[i][9]}', '{datadic[i][8]}', '{datadic[i][10]}', '1')"
                cursor.execute(string9)
                conn.commit()
                cursor.close()
                print("Gegevens fill for ", datadic[i][3], " completed")
                teller3 += 1
            else:
                print(cursorchecks, "bestaat al")
                pass
        # Kijk of de plek gevult is met data
        if datadic[i][1] != "":
            # Het id van sequentie ophalen om deze in de organisme tabel te zetten
            seqidcursor = conn.cursor(buffered=True)
            string10 = f"select id from sequentie where header = '{datadic[i][9]}'"
            seqidcursor.execute(string10)
            conn.commit()
            seqid = seqidcursor.fetchall()
            seqidcursor.close()
            replacer2 = str(seqid[0])
            replace3 = replacer2.replace('(', "").replace(',', "").replace(')', "")
            # Het id van organisme ophalen om deze in de organisme tabel te zetten
            orgidcursor = conn.cursor(buffered=True)
            string11 = f"select id from organisme where naam_organismenaam = '{datadic[i][2]}'"
            orgidcursor.execute(string11)
            conn.commit()
            orgid = orgidcursor.fetchall()
            orgidcursor.close()
            replacer3 = str(orgid[0])
            replace4 = replacer3.replace('(', "").replace(',', "").replace(')', "")
            # De eiwit tabel vullen met data
            cursor = conn.cursor()
            string12 = f"insert into eiwit (id, description, accessiecode, " \
                       f"percent_identity, e_value, max_score, total_score, " \
                       f"query_cover sequentie_id, Organisme_id) values " \
                       f"('{teller4}', '{datadic[i][1]}', '{datadic[i][3]}', '{datadic[i][7]}, " \
                       f"{datadic[i][6]}', '{datadic[i][4]}', '{datadic[i][5]}', '" \
                       f"{datadic[i][12]}', '{replace3}', '{replace4}')"
            cursor.execute(string12)
            conn.commit()
            cursor.close()
            teller4 += 1
            print("Eiwit  fill for ", datadic[i][3], " completed")
    print("Database filled!\nClosing connection....")
    # Connectie met database sluiten
    conn.close()
    print("Connection closed task compleded.")
    return


def main():
    datafile = 'data/dataset.txt'

    filename = 'data/XMLForward1.xml'
    datadic = getdata(datafile, filename)
    pushdata(datadic)


main()
# Lijst aanmaken met alle values die worden opgehaald vanuit het xml bestand
# Data uit deze lijst overbrengen naar de database
# Lijst met data pet 5 de if for loop doen