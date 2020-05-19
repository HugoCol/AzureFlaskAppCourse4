def getdata():

    return datadic


def pushdata(datadic):
    print("Connecting to database.....")
    conn = mysql.connector.connect(
                    host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
                         "azure.com",
                    user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
                    db="iaoqi", password="638942")
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
    datadic = getdata()
    pushdata(datadic)
main()
# Lijst met data pet 5 de if for loop doen
# in de for loop op volgorde van tabbellen gaan vullen
# Bij de tabbellen die dubbele data kunnen bevatten eerst een if statement
# zetten die kijkt of deze data al in de tabel staat (bijvoorbeeld bij tabel soorten)
# Bij het vullen van de eiwit tabel moet er gekeken worden voor elke i welke
# FK er nodig zijn in de tabel voorstel: die ophalen met een select statement
# uit alle andere tabellen waar dan vb: de soortnaam in i gelijk is aan de soortnaam in de tabel