import mysql.connector


def getdata():

    return funcdic,
def pushdata():
    print("Connecting to database.....")
    conn = mysql.connector.connect(
                    host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
                         "azure.com",
                    user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
                    db="iaoqi", password="638942")
    print("Connected")
    for i in datadic:
        if i != "":
            cursor = conn.cursor()
            cursor.execute(f"insert into functies (functie_eiwit) "
                           f"values ();")
            conn.commit()
            print("Functietabel fill completed")
        if i != "":
            cursor = conn.cursor()
            cursor.execute(f"insert into sequences (seq_read1, seq_read2) "
                           f"values ();")
            conn.commit()
            print("Sequences table fill completed")
        if i != "":
            cursor = conn.cursor()
            cursor.execute(f"insert into soort (soortnaam) "
                           f"values ();")
            conn.commit()
            print("Soort table fill completed")
        if i != "":
            cursor = conn.cursor()
            cursor.execute(f"insert into geslacht (geslacht_naam) "
                           f"values ();")
            conn.commit()
            print("Geslacht table fill completed")
        if i != "":
            cursor = conn.cursor()
            cursor.execute(f"insert into familie (familie_naam) "
                           f"values ();")
            conn.commit()
            print("Familie table fill completed")
        if i != "":
            cursor = conn.cursor()
            cursor.execute(f"insert into gegevens (max_score, total_score, "
                           f"query_cover, percent_identity, e_value) "
                           f"values ();")
            conn.commit()
            print("Gegevens table fill completed")
        if i != "":
            cursor = conn.cursor()
            cursor.execute(f"insert into eiwit (eiwit_naam, familie_id, "
                           f"geslacht_id, soort_id, seq_id, functie_id, gegevens_id) "
                           f"values ();")
            conn.commit()
            print("Eiwit table fill completed")

    cursor.close()
    conn.close()
    return

if __name__ == '__main__':
    pushdata()


# Lijst met data pet 5 de if for loop doen
# in de for loop op volgorde van tabbellen gaan vullen
# Bij de tabbellen die dubbele data kunnen bevatten eerst een if statement
# zetten die kijkt of deze data al in de tabel staat (bijvoorbeeld bij tabel soorten)
# Bij het vullen van de eiwit tabel moet er gekeken worden voor elke i welke
# FK er nodig zijn in de tabel voorstel: die ophalen met een select statement
# uit alle andere tabellen waar dan vb: de soortnaam in i gelijk is aan de soortnaam in de tabel
