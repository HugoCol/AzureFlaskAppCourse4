# CHECKBOX: de checkbox bepaald welke tabel er word bevraagd.
# SERCHBAR: dit is het word waarop gezocht woord
import mysql.connector

def zoeken(filter, search):
    msg = {}
    conn = mysql.connector.connect(
                    host="hannl-hlo-bioinformatica-mysqlsrv.mysql.database."
                         "azure.com",
                    user="iaoqi@hannl-hlo-bioinformatica-mysqlsrv",
                    db="iaoqi", password="638942")
    if search = "":
        cursor = conn.cursor()
        cursor.execute(f"select eiwit.id, description, accessiecode, "
                       f"percent_identity, e_value, max_score, total_score, "
                       f"query_cover, naam_organismenaam, linnaam, header, "
                       f"sequence, asci_score from eiwit join (select "
                       f"organisme.id as id, naam_organismenaam, lineage_id, "
                       f"lineage.name as linnaam from organisme join lineage "
                       f"on organisme.lineage_id=lineage.id) as orjoin on "
                       f"eiwit.Organisme_id=orjoin.id join sequentie s on "
                       f"eiwit.sequentie_id = s.id order by eiwit.id ASC "
                       f"limit 500;")
        for i in cursor:
            msg[f"{i[0]}"] = values[f"{i[1]} {i[2]} {i[3]} {i[4]} {i[5]}" \
                                    f" {i[6]} {i[7]} {i[8]} {i[9]}" \
                                    f" {i[10]} {i[11]}"]
        cursor.close()
        conn.close()
    else:
        if filter = '':
            cursor = conn.cursor()
            cursor.execute(f"select eiwit.id, description, accessiecode, "
                           f"percent_identity, e_value, max_score, total_score, "
                           f"query_cover, naam_organismenaam, linnaam, header, "
                           f"sequence, asci_score from eiwit join (select "
                           f"organisme.id as id, naam_organismenaam, lineage_id, "
                           f"lineage.name as linnaam from organisme join lineage on "
                           f"organisme.lineage_id=lineage.id) as orjoin on "
                           f"eiwit.Organisme_id=orjoin.id join sequentie s on "
                           f"eiwit.sequentie_id = s.id where description ='"
                           f"{search}'order by eiwit.id ASC limit 500;")
            for i in cursor:
                msg[f"{i[0]}"] = values[f"{i[1]} {i[2]} {i[3]} {i[4]} {i[5]}" \
                                        f" {i[6]} {i[7]} {i[8]} {i[9]} " \
                                        f"{i[10]} {i[11]}"]
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
                           f"eiwit.sequentie_id = s.id where '{filter}'='"
                           f"{search}'order by eiwit.id ASC limit 500;")
            for i in cursor:
                msg[f"{i[0]}"] = values[f"{i[1]} {i[2]} {i[3]} {i[4]} {i[5]}" \
                                        f" {i[6]} {i[7]} {i[8]} {i[9]} " \
                                        f"{i[10]} {i[11]}"]
            cursor.close()
            conn.close()

    return msg