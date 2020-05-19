from xml.etree import ElementTree


def getdata():
    filename = 'my_blast.xml'
    dom = ElementTree.parse(filename)
    hits = dom.findall('BlastOutput_iterations/Iteration/Iteration_hits/Hit')
    print(hits)
    for c in hits:
        Hit_id = c.find('Hit_id').text
        familie = c.find('Hit_def').text
        acessiecode = c.find('Hit_accession').text
        hit = c.find('Hit_num').text
        score = c.find('Hit_hsps/Hsp/Hsp_bit-score').text
        tscore = c.find('Hit_hsps/Hsp/Hsp_score').text
        evalue = c.find('Hit_hsps/Hsp/Hsp_evalue').text
        percidentity = c.find('Hit_hsps/Hsp/Hsp_identity').text
        queryseq = c.find('Hit_hsps/Hsp/Hsp_qseq').text
        print(hit, Hit_id, familie, acessiecode, score, tscore, evalue, percidentity, queryseq)

    return #datadic


def pushdata(datadic):
    print("Connecting to database.....")
    # conn = mysql.connector.connect(
    #                 host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
    #                      "azure.com",
    #                 user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
    #                 db="iaoqi", password="638942")
    conn = mysql.connector.connect(
        host="sql2.freemysqlhosting.net",
        user="sql234812",
        db="sql234812", password="iM4*eV6%")
    print("Connected")
    for i in datadic:
        if i[] != "":
            cursor = conn.cursor()
            cursor.execute(f"insert into lineage (name, parent_id) "
                           f"values (i[]);")
            conn.commit()
            print("lineage fill for ",i[]," completed")
        if i[] != "":
            cursorchecko = conn.cursor()
            cursor.execute(f"select naam_organisme from organisme where naam_organisme = i[]")
            if cursorchecko == "":
                linidcursor = conn.cursor()
                cursor.execute(f"select id from lineage where name = i[]")
                cursor = conn.cursor()
                cursor.execute(f"insert into organisme (naam_organisme lineage_id, eiwit_id) "
                               f"values (i[]}, linidcursor, i[]);")
                conn.commit()
                print("Organisme fill for ",i[]," completed")
        if i[] != "":
            cursorchecks = conn.cursor()
            cursor.execute(f"select header from sequentie where header = i[]")
            if cursorchecks == "":
                cursor = conn.cursor()
                cursor.execute(f"insert into sequentie (header, sequence, "
                               f"asci_score, 'read') values (i[], i[], i[], i[]);")
                conn.commit()
                print("Gegevens fill for ",i[]," completed")
                cursorchecks += ""
        if i[] != "":
            seqidcursor = conn.cursor()
            cursor.execute(f"select id from sequentie where header = i[]")
            orgidcursor = conn.cursor()
            cursor.execute(f"select id from organisme where naam_organisme = i[]")

            cursor = conn.cursor()
            cursor.execute(f"insert into eiwit (description, accessiecode, "
                           f"percent_identity, e_value, max_score, total_score,"
                           f"query_cover sequentie_id, Organisme_id) "
                           f"values (i[], i[], i[], i[], i[], i[],"
                           f"i[], seqidcursor, orgidcursor);")
            conn.commit()
            print("Eiwit  fill for ",i[]," completed")
    print("Database filled!\nClosing connection....")
    cursor.close()
    conn.close()
    print("Connection closed task compleded.")
    return

def main():
    #datadic =
    getdata()
    #pushdata(datadic)
main()
# Lijst aanmaken met alle values die worden opgehaald vanuit het xml bestand
# Data uit deze lijst overbrengen naar de database
# Lijst met data pet 5 de if for loop doen