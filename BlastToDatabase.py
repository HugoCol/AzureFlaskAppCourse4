# Ivar van den Akker
# 18-05-2020 tot 27-05-2020
# Script dat heel veel data uit 2 bestanden en 1 database haalt deze
# in een dictionary zet en met de dictionary de database vult
import mysql.connector
from xml.etree import ElementTree
import time
from Bio import Entrez
import os


def getdata(datafile):
    """
    :return:
    """
    # Bestand openen
    filename = 'data/XMLForward1.xml'
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
            datalist = [Hit_id, discription, organisme, acessiecode, score, tscore, evalue,
                        percidentity, queryseq, header, ascicode, lineage]
            datadic[count] = datalist
            count += 1
    else:
        pass
    #print(datadic)
    print('Data Recieved')


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
    for i in datadic:
        countlin = 0
        # Kijk of de plek gevult is met data
        if datadic[i][11] != "":
            for j in datadic[i][11]:
                print(j)
                lincheck = conn.cursor()
                lincheck.execute(f"select name from lineage where name = j")
                conn.commit()
                cursor.close()
                if lincheck == "":
                    if countlin == 0:
                        cursor = conn.cursor()
                        cursor.execute(f"insert into lineage (name, parent_id) "
                                       f"values (datadic[i][11][countlin]);")
                        conn.commit()
                        cursor.close()
                else:
                    formercount = countlin - 1
                    # Vul de lineage tabel met data
                    linid = conn.cursor()
                    linid.execute(f"select id from lineage where name = datadic[i][11][formercount]")
                    conn.commit()
                    cursor.close()
                    cursor = conn.cursor()
                    cursor.execute(f"insert into lineage (name, parent_id) "
                                   f"values (datadic[i][11][countlin], linid);")
                    conn.commit()
                    cursor.close()
                    countlin += 1
            else:
                print("Item", j,"Bestaat al")
                pass
            print("lineage fill for ", datadic[i][3], " completed")
            # Kijk of de plek gevult is met data
        if datadic[i][2] != "":
            # Kijken of de data die in de database gaat er al in staat
            cursorchecko = conn.cursor()
            cursor.execute(
                f"select naam_organisme from organisme where naam_organisme = datadic[i][]")
            conn.commit()
            cursor.close()
            # Als de variabele leeg blijft data in de database zetten
            if cursorchecko == "":
                # Het id van linage ophalen om deze in de organisme tabel te zetten
                linidcursor = conn.cursor()
                cursor.execute(
                    f"select id from lineage where name = datadic[i][11][-1]")
                conn.commit()
                cursor.close()


                cursor = conn.cursor()
                cursor.execute(
                    f"insert into organisme (naam_organisme lineage_id, eiwit_id) "
                    f"values (datadic[i][2], linidcursor, datadic[i][0]);")
                conn.commit()
                cursor.close()
                print("Organisme fill for ", datadic[i][3], " completed")
            else:
                print(cursorchecko, "bestaat al")
                pass
            cursorchecko += ""
        # Kijk of de plek gevult is met data
        if datadic[i][9] != "":
            # Kijken of de data die in de database gaat er al in staat
            cursorchecks = conn.cursor()
            cursor.execute(f"select header from sequentie where header = datadic[i][9]")
            conn.commit()
            cursor.close()
            # Als de variabele leeg blijft data in de database zetten
            if cursorchecks == "":
                cursor = conn.cursor()
                cursor.execute(f"insert into sequentie (header, sequence, "
                               f"asci_score, read) values (datadic[i][9], datadic[i][8], datadic[i][10], 1);")
                conn.commit()
                cursor.close()
                print("Gegevens fill for ", datadic[i][3], " completed")
            else:
                print(cursorchecks, "bestaat al")
                pass
            cursorchecks += ""
        # Kijk of de plek gevult is met data
        if datadic[i][1] != "":
            # Het id van sequentie ophalen om deze in de organisme tabel te zetten
            seqidcursor = conn.cursor()
            cursor.execute(
                f"select id from sequentie where header = datadic[i][9]")
            conn.commit()
            cursor.close()
            # Het id van organisme ophalen om deze in de organisme tabel te zetten
            orgidcursor = conn.cursor()
            cursor.execute(
                f"select id from organisme where naam_organisme = datadic[i][2]")
            conn.commit()
            cursor.close()
            # De eiwit tabel vullen met data
            cursor = conn.cursor()
            cursor.execute(f"insert into eiwit (description, accessiecode, "
                           f"percent_identity, e_value, max_score, total_score,"
                           f"query_cover sequentie_id, Organisme_id) "
                           f"values (datadic[i][1], datadic[i][3], datadic[i][7], datadic[i][6], datadic[i][4], datadic[i][5],"
                           f"datadic[i][], seqidcursor, orgidcursor);")
            conn.commit()
            cursor.close()
            print("Eiwit  fill for ", datadic[i][3], " completed")
    print("Database filled!\nClosing connection....")
    # Connectie met database sluiten
    conn.close()
    print("Connection closed task compleded.")
    return


def main():
    datafile = 'data/dataset.txt'
    datadic = getdata(datafile)
    pushdata(datadic)


main()
# Lijst aanmaken met alle values die worden opgehaald vanuit het xml bestand
# Data uit deze lijst overbrengen naar de database
# Lijst met data pet 5 de if for loop doen
