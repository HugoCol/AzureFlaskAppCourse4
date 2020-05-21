from xml.etree import ElementTree


def getdata():
    # Bestand openen
    filename = 'my_blast.xml'
    # Door bestand heen gaan
    dom = ElementTree.parse(filename)
    # Alle hits eruit zoeken
    hits = dom.findall('BlastOutput_iterations/Iteration/Iteration_hits/Hit')
    print(hits)
    # Voor elke hit
    count = 1
    datadic = {}
    for c in hits:
        # Haal de data uit de hit en zet deze in een zelfbeschrijvende variabele
        Hit_id = c.find('Hit_id').text
        familie = c.find('Hit_def').text
        acessiecode = c.find('Hit_accession').text
        hit = c.find('Hit_num').text
        score = c.find('Hit_hsps/Hsp/Hsp_bit-score').text
        tscore = c.find('Hit_hsps/Hsp/Hsp_score').text
        evalue = c.find('Hit_hsps/Hsp/Hsp_evalue').text
        percidentity = c.find('Hit_hsps/Hsp/Hsp_identity').text
        queryseq = c.find('Hit_hsps/Hsp/Hsp_qseq').text
        # Print alle data om te zien of het gewerkt heeft
        datalist = [Hit_id, familie, acessiecode, score, tscore, evalue, percidentity, queryseq]
        datadic[count]=datalist
        count += 1
    print(datadic)

    return datadic


def pushdata(datadic):
    # Connectie met database maken
    print("Connecting to database.....")
    # Inlog gegevens voor Azure database (nette database)
    # conn = mysql.connector.connect(
    #                 host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
    #                      "azure.com",
    #                 user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
    #                 db="iaoqi", password="638942")
    # Inlog gegevens voor oefen database (Hier het script op testen)
    conn = mysql.connector.connect(
        host="sql2.freemysqlhosting.net",
        user="sql234812",
        db="sql234812", password="iM4*eV6%")
    print("Connected")
    # Voor elke regel in de dictionary waar de data in staat
    for i in datadic:
        # Kijk of de plek gevult is met data
        if i[] != "":
            # Vul de lineage tabel met data
            cursor = conn.cursor()
            cursor.execute(f"insert into lineage (name, parent_id) "
                           f"values (i[]);")
            conn.commit()
            print("lineage fill for ",i[]," completed")
        # Kijk of de plek gevult is met data
        if i[] != "":
            # Kijken of de data die in de database gaat er al in staat
            cursorchecko = conn.cursor()
            cursor.execute(f"select naam_organisme from organisme where naam_organisme = i[]")
            # Als de variabele leeg blijft data in de database zetten
            if cursorchecko == "":
                #Het id van linage ophalen om deze in de organisme tabel te zetten
                linidcursor = conn.cursor()
                cursor.execute(f"select id from lineage where name = i[]")
                cursor = conn.cursor()
                cursor.execute(f"insert into organisme (naam_organisme lineage_id, eiwit_id) "
                               f"values (i[]}, linidcursor, i[]);")
                conn.commit()
                print("Organisme fill for ",i[]," completed")
            cursorchecko += ""
        # Kijk of de plek gevult is met data
        if i[] != "":
            # Kijken of de data die in de database gaat er al in staat
            cursorchecks = conn.cursor()
            cursor.execute(f"select header from sequentie where header = i[]")
            # Als de variabele leeg blijft data in de database zetten
            if cursorchecks == "":
                cursor = conn.cursor()
                cursor.execute(f"insert into sequentie (header, sequence, "
                               f"asci_score, 'read') values (i[], i[], i[], i[]);")
                conn.commit()
                print("Gegevens fill for ",i[]," completed")
                cursorchecks += ""
        # Kijk of de plek gevult is met data
        if i[] != "":
            # Het id van sequentie ophalen om deze in de organisme tabel te zetten
            seqidcursor = conn.cursor()
            cursor.execute(f"select id from sequentie where header = i[]")
            # Het id van organisme ophalen om deze in de organisme tabel te zetten
            orgidcursor = conn.cursor()
            cursor.execute(f"select id from organisme where naam_organisme = i[]")
            # De eiwit tabel vullen met data
            cursor = conn.cursor()
            cursor.execute(f"insert into eiwit (description, accessiecode, "
                           f"percent_identity, e_value, max_score, total_score,"
                           f"query_cover sequentie_id, Organisme_id) "
                           f"values (i[], i[], i[], i[], i[], i[],"
                           f"i[], seqidcursor, orgidcursor);")
            conn.commit()
            print("Eiwit  fill for ",i[]," completed")
    print("Database filled!\nClosing connection....")
    # Connectie met database sluiten
    cursor.close()
    conn.close()
    print("Connection closed task compleded.")
    return

def main():
    datadic = getdata()
    #pushdata(datadic)
main()
# Lijst aanmaken met alle values die worden opgehaald vanuit het xml bestand
# Data uit deze lijst overbrengen naar de database
# Lijst met data pet 5 de if for loop doen