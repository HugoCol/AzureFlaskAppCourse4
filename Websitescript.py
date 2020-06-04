# CHECKBOX: de checkbox bepaald welke tabel er word bevraagd.
# SERCHBAR: dit is het word waarop gezocht woord
import mysql.connector

def zoeken(filter, search, sorton, HLLH):
    msg = {}
    conn = mysql.connector.connect(
                    host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
                         "azure.com",
                    user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
                    db="iaoqi", password="638942")
    filtervariabele = 'description'
    sortonvariabele = 'eiwit.id'
    HLLHvariabele = 'ASC'
    if filter != "":
        filtervariabele = str(filter)
    else:
        pass
    if sorton != "":
        sortonvariabele = str(sorton)
    else:
        pass
    if HLLH != "":
        HLLHvariabele = str(HLLH)
    else:
        pass

    if search == "":
        cursor = conn.cursor()
        cursor.execute(f"select eiwit.id, description, accessiecode, "
                       f"percent_identity, e_value, max_score, total_score, "
                       f"query_cover, naam_organismenaam, linnaam, header, "
                       f"sequence, asci_score from eiwit join (select "
                       f"organisme.id as id, naam_organismenaam, lineage_id, "
                       f"lineage.name as linnaam from organisme join lineage "
                       f"on organisme.lineage_id=lineage.id) as orjoin on "
                       f"eiwit.Organisme_id=orjoin.id join sequentie s on "
                       f"eiwit.sequentie_id = s.id order by {sortonvariabele}"
                       f" {HLLHvariabele} limit 500;")
        for i in cursor:
            msg.update({i[0] :{"name":i[1],
                      "accessiecode":i[2],
                      "IDpercentage":i[3],
                      "Evalue":i[4],
                    'max_score':i[5],
                     'totale_score':i[6],
                       'query_cover':i[7],
                       'naam_organismenaam':i[8],
                       'linnaam':i[9],
                        'header':i[10],
                        'sequence':i[11],
                        'asci_score':i[12]
                               }})

        cursor.close()
        conn.close()
    else:
            cursor = conn.cursor()
            cursor.execute(f"select eiwit.id, description, accessiecode, "
                           f"percent_identity, e_value, max_score, total_score, "
                           f"query_cover, naam_organismenaam, linnaam, header, "
                           f"sequence, asci_score from eiwit join (select "
                           f"organisme.id as id, naam_organismenaam, lineage_id, "
                           f"lineage.name as linnaam from organisme join lineage on "
                           f"organisme.lineage_id=lineage.id) as orjoin on "
                           f"eiwit.Organisme_id=orjoin.id join sequentie s on "
                           f"eiwit.sequentie_id = s.id where instr("
                           f"{filtervariabele}, '{search}') order by "
                           f"{sortonvariabele} {HLLHvariabele} limit 500;")
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
    return msg


def databasecounter():

    orgcounter = {}
    conn = mysql.connector.connect(
                    host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
                         "azure.com",
                    user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
                    db="iaoqi", password="638942")
    cursor = conn.cursor()
    cursor.execute(f" select tussentabel.naam_organismenaam, COUNT(*) as Aantal "
                    f" from (select eiwit.id, naam_organismenaam from eiwit join organisme o "
                   f"on eiwit.Organisme_id = o.id) as tussentabel "
                    f"group by tussentabel.naam_organismenaam "
                   f"order by Aantal DESC limit 10; ")
    for i in cursor:
        orgcounter.update({i[0]: i[1]})
        print(i)
    return orgcounter