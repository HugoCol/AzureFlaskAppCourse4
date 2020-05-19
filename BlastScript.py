# Import voor NCBI blast en lezen van XML bestand uit blast.
# NCBIWWW - Blast
# NCBIXML - XML bestand lezen
from Bio.Blast import NCBIWWW, NCBIXML

# Import voor de sleep tussen de NCBI runs
import time


def file_reader(txtbestand):
    """
    :Beschrijving: Leest het text bestand met alle gegevens in en zet dit in
    een lijst.
    :Parameters: bestand - Text bestand met alle data.
    :Return: gegevens - 2D lijst van text bestand
                        positie 0: forward header
                        positie 1: forward sequentie
                        positie 2: forward ascii code
                        positie 3: reverse header
                        positie 4: reverse sequentie
                        positie 5: reverse asccii code
                    Dus bv gegevens[10][0] geeft van 10de regel de fw header
    """
    dataset = open(txtbestand, "r")  # Opent de txt file met de dataset
    gegevens = []  # Maakt lege lijst aan

    # Leest het txt bestand in, replaced de enters en ï»¿. Split op tab.
    for regel in dataset:
        gegevens.append(regel.replace("\n", "").replace("ï»¿", "").split("\t"))

    # Verwijderd alle @ aan het begin van de fw/rv headers
    for i in range(len(gegevens)):
        gegevens[i][0] = gegevens[i][0].replace("@", "")
        gegevens[i][3] = gegevens[i][3].replace("@", "")

    return gegevens


def blast(gegevens):
    """
    :Beschrijving: Gebruikt de lijst gegevens uit de functie file_reader. De
                   sequenties worden hieruit gehaald en geblast met een sleep
                   van 5 seconden
    :Parameters: gegevens - 2D lijst met structuur [regel dataset][fw header]
                            [fw seq][fw ascii][rv header][rv seq][rv ascii]
    """

    # Leeg txt file dat positie van gegevenslijst opslaat in geval van crash.
    scriptpos = open("ScriptPositie.txt", "w+")

    # Haalt de sequentie uit de gegevens lijst en blast deze tegen de NCBI
    # database. Hierna worden de resultaten toegevoegd aan een XML bestand.
    for i in range(50,len(gegevens)):
        # Blast forward sequentie (positie [i][1] in gegevens lijst)
        fwseq = gegevens[i][1]
        print("Start Blast...")
        result_handle = NCBIWWW.qblast("blastx", "nr", fwseq)
        print("Blasten voltooid.")

        # Voegt BLAST resultaten toe aan XML bestand
        with open("my_blast.xml", "a") as out_handle:
            out_handle.write(result_handle.read())
        print("Gegevens in een XML bestand gezet")
        print("T/m", gegevens[i][0], "is gedaan.")

        # Schrijft in een txt file waar het script was gebleven voor als iets
        # crasht.
        scriptpos.write("T/m gegevens[" + str(i) + "][1] is klaar.\n")

        # Pauze van 5 seconden voor volgende blast.
        time.sleep(5)

        # ----------

        # Blast reverse sequentie (positie [i][4] in gegevens lijst)
        rvseq = gegevens[i][4]
        print("Start Blast...")
        result_handle = NCBIWWW.qblast("blastx", "nr", rvseq)
        print("Blasten voltooid.")

        # Voegt BLAST resultaten toe aan XML bestand
        with open("BlastResultaten.xml", "a") as out_handle:
            out_handle.write(result_handle.read())
        print("Gegevens in een XML bestand gezet.")
        print("T/m", gegevens[i][3], "is gedaan.")

        # Schrijft in een txt file waar het script was gebleven voor als iets
        # crasht.
        scriptpos.write("T/m gegevens[" + str(i) + "][4] is klaar.\n")

        # Pauze van 5 seconden voor volgende blast.
        time.sleep(5)


def main():
    # Naam van het txt bestand
    txtbestand = "data/dataset.txt"

    # Roept de functie file_reader aan.
    # Parameter txtbestand - naam van dataset txt file.
    # Return gegevens - 2D lijst
    gegevens = file_reader(txtbestand)

    # Roept de functie blast aan. Parameter gegevens - 2D lijst
    blast(gegevens)


main()