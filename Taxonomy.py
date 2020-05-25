# Thijs Ermens
# 25-05-2020 tot ...
# Script dat accessiecodes uit een xml bestand haalt en hiermee vervolgens
# de lineage geeft

from xml.etree import ElementTree
from Bio import Entrez
import xmltodict


def accessiecode_vinden():
    """
    Functie die accessiecode uit een xml bestand haalt en vertaalt naar een
    lijst
    :return: list - accessiecodes
    """
    # Bestand openen
    filename = 'data/XMLForward1.xml'
    dom = ElementTree.parse(filename)
    hits = dom.findall('BlastOutput_iterations/Iteration/Iteration_hits/Hit')

    # Het vinden van de accessiecodes en deze toevoegen aan een lijst
    accessiecode = []
    for c in hits:
        accessiecode.append(c.find('Hit_accession').text)
    return accessiecode

def lineage_toevoegen(accessiecodes):



if __name__ == '__main__':
    accessiecodes = accessiecode_vinden()
    lineage_toevoegen(accessiecodes)



