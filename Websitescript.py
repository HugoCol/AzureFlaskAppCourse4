import mysql.connector


def zoeken(filter, search, sorton, HLLH):
    """ deze functie haalt de data op uit de database en zet dit in een
    dictionary om deze te retouneren naar de plek waar de functie
    word aangeroeppen. Er kunnen meerdere filters worden toegepast op
    het ophalen van de data
    :param filter: string
    :param search: string
    :param sorton: string
    :param HLLH: string
    :return msg dictionary:
    """
    # Maak dictionary aan
    msg = {}
    # Connecteerd met de database
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
             "azure.com",
        user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
        db="iaoqi", password="638942")
    # Maak filtervariabele aan en geef ze standaart zoekfunctie
    # variabele weer
    filtervariabele = 'description'
    sortonvariabele = 'eiwit.id'
    HLLHvariabele = 'ASC'
    # Als er een filter word aangeklikt in de website dan
    # word de filtervariabele aangepast naar deze filter
    if filter != "":
        filtervariabele = str(filter)
    else:
        pass
    # Als er een sorteer filter word aangeklikt in de website dan
    # word de sorteervariabele aangepast naar deze filter
    if sorton != "":
        sortonvariabele = str(sorton)
    else:
        pass
    # Als er een richting van weergeven word aangeklikt in de website
    # dan word de HLLHvariabele aangepast naar deze richting
    if HLLH != "":
        HLLHvariabele = str(HLLH)
    else:
        pass
    # Als er niets gezocht word dan word de standaart zoek
    # optie uitgevoerd
    if search == "":
        cursor = conn.cursor()
        cursor.execute(f"select eiwit.id, description, accessiecode, "
                       f"percent_identity, e_value, max_score,"
                       f" total_score, "
                       f"query_cover, naam_organismenaam, linnaam,"
                       f" header, "
                       f"sequence, asci_score from eiwit"
                       f" join (select "
                       f"organisme.id as id, naam_organismenaam,"
                       f" lineage_id, "
                       f"lineage.name as linnaam from organisme"
                       f" join lineage "
                       f"on organisme.lineage_id=lineage.id) "
                       f"as orjoin on "
                       f"eiwit.Organisme_id=orjoin.id "
                       f"join sequentie s on "
                       f"eiwit.sequentie_id = s.id "
                       f"order by {sortonvariabele}"
                       f" {HLLHvariabele} limit 500;")
        # Voeg al de variabele toe aan een dictionary
        for i in cursor:
            msg.update({i[0]: {"name": i[1],
                               "accessiecode": i[2],
                               "IDpercentage": i[3],
                               "Evalue": i[4],
                               'max_score': i[5],
                               'totale_score': i[6],
                               'query_cover': i[7],
                               'naam_organismenaam': i[8],
                               'linnaam': i[9],
                               'header': i[10],
                               'sequence': i[11],
                               'asci_score': i[12]
                               }})

        cursor.close()
        conn.close()
    # Als er wel iets word gezocht zoek met alle filtervariabele
    else:
        cursor = conn.cursor()
        cursor.execute(f"select eiwit.id, description, accessiecode, "
                       f"percent_identity, e_value, max_score, "
                       f"total_score, query_cover, naam_organismenaam, "
                       f"linnaam, header, sequence, asci_score from "
                       f"eiwit join (select organisme.id as id, "
                       f"naam_organismenaam, lineage_id, lineage.name "
                       f"as linnaam from organisme join lineage on "
                       f"organisme.lineage_id=lineage.id) as orjoin on "
                       f"eiwit.Organisme_id=orjoin.id join sequentie s "
                       f"on eiwit.sequentie_id = s.id where "
                       f"instr({filtervariabele}, '{search}') order "
                       f"by {sortonvariabele} {HLLHvariabele} "
                       f"limit 500;")
        # Voeg al de variabele toe aan een dictionary
        for i in cursor:
            msg.update({i[0]: {"name": i[1],
                               "accessiecode": i[2],
                               "IDpercentage": i[3],
                               "Evalue": i[4],
                               'max_score': i[5],
                               'totale_score': i[6],
                               'query_cover': i[7],
                               'naam_organismenaam': i[8],
                               'linnaam': i[9],
                               'header': i[10],
                               'sequence': i[11],
                               'asci_score': i[12]
                               }})
        # Sluit de connectie
        cursor.close()
        conn.close()
    return msg


def databasecounter():
    """
    Deze functie haalt de tien meestvoorkomende organismen op uit de
    database
    :return orgcounter: dictionary
    """
    # Maak connectie met de database
    orgcounter = {}
    conn = mysql.connector.connect(
        host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
             "azure.com",
        user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
        db="iaoqi", password="638942")
    # Haal de top 10 organisme op met een query
    cursor = conn.cursor()
    cursor.execute(
        f" select tussentabel.naam_organismenaam, COUNT(*) as "
        f"Aantal from (select eiwit.id, naam_organismenaam from "
        f"eiwit join organisme o on eiwit.Organisme_id = o.id) as "
        f"tussentabel group by tussentabel.naam_organismenaam "
        f"order by Aantal DESC limit 10; ")
    # Zet de opgehaalde informatie in een dictionary
    for i in cursor:
        orgcounter.update({i[0]: i[1]})

    return orgcounter
