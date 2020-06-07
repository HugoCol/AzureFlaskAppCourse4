# Thijs Ermens
# 25-05-2020 tot ...
# Script dat accessiecodes uit een xml bestand haalt en
# hiermee vervolgens de lineage geeft

from xml.etree import ElementTree
from Bio import Entrez
import xmltodict
import time


def accessiecode_vinden():
    """
    Functie die accessiecode uit een xml bestand haalt en vertaalt naar
    een lijst
    :return: list - accessiecodes
    """
    # Bestand openen
    filename = 'data/XMLForward1.xml'
    dom = ElementTree.parse(filename)
    hits = dom.findall(
        'BlastOutput_iterations/Iteration/Iteration_hits/Hit')

    # Het vinden van de accessiecodes en deze toevoegen aan een lijst
    accessiecode = []
    for c in hits:
        accessiecode.append(c.find('Hit_accession').text)
    return accessiecode


def lineage_toevoegen(accessiecodes):
    """
    Functie die een dictionary maakt van alle accessiecodes met de
    bijbehorende lineage
    :param accessiecodes: list - accessiecodes
    :return: dictionary - value = accessiecode, keys = lineage
    """
    for i in accessiecodes:
        time.sleep(0.4)
        Entrez.email = "thijschermens@gmail.com"
        seqio = Entrez.efetch(db="protein", id=i, retmode="xml")
        seqio_read = Entrez.read(seqio)
        seqio.close()
        lineage = seqio_read[0]["GBSeq_taxonomy"].split(";")
        print(lineage)


if __name__ == '__main__':
    accessiecodes = accessiecode_vinden()
    lineage_toevoegen(accessiecodes)
