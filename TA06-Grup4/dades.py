import csv
try:

    def revisar_format_fitxer(nom_fitxer):
        with open(nom_fitxer, 'r') as fitxer:
            primera_linia = fitxer.readline().strip()

            # Determinar el delimitador
            if ',' in primera_linia:
                delimitador = ','
            elif '\t' in primera_linia:
                delimitador = '\t'
            elif ' ' in primera_linia:
                delimitador = ' '
            else:
                raise ValueError("No s'ha pogut determinar el delimitador de les dades.")

            # Llegir el fitxer amb el delimitador determinat
            fitxer.seek(0)
            lector = csv.reader(fitxer, delimiter=delimitador)

            # Revisar les capçaleres
            capçaleres = next(lector)
            if not capçaleres:
                raise ValueError("El fitxer no conté capçaleres.")

            # Revisar les dades
            for fila in lector:
                if len(fila) != len(capçaleres):
                    raise ValueError("Les dades no coincideixen amb les capçaleres.")

            print(f"El fitxer {nom_fitxer} té un format correcte amb delimitador '{delimitador}'.")


    # Exemple d'ús
    revisar_format_fitxer('exemple.csv')
except:
    print("Error en la lectura del fitxer")