import os
import csv
import logging
from datetime import datetime

# Configure logging to append to the file
logging.basicConfig(filename='error_log.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

def revisar_format(fitxer):
    return fitxer.endswith('.dat')

def llegir_fitxer(fitxer):
    try:
        with open(fitxer, 'r') as f:
            dades = f.read(1024)
        return dades
    except Exception as e:
        logging.error(f"Error leyendo el archivo {fitxer}: {e}")
        return None

def hi_ha_comentaris(fitxer, delimitador):
    try:
        with open(fitxer, 'r') as f:
            dades = csv.reader(f, delimiter=delimitador)
            for linia in dades:
                if linia[0].startswith('#'):
                    return True
        return False
    except Exception as e:
        logging.error(f"Error revisando comentarios en el archivo {fitxer}: {e}")
        return False

def revisar_capcaleres(fitxer, delimitador, primera_capcalera=None, segona_capcalera=None):
    try:
        with open(fitxer, 'r') as f:
            dades = csv.reader(f, delimiter=delimitador)
            capcalera = []
            for linia in dades:
                capcalera.append(linia)
                if len(capcalera) == 2:
                    break

            if len(capcalera) < 2:
                logging.error(f"El archivo {fitxer} no tiene suficientes filas de cabecera.")
                return False, primera_capcalera, segona_capcalera

            if primera_capcalera is None:
                primera_capcalera = capcalera[0]
            if capcalera[0] != primera_capcalera:
                logging.error(f"La primera fila de cabecera en el archivo {fitxer} no es idéntica.")
                return False, primera_capcalera, segona_capcalera

            if segona_capcalera is None:
                segona_capcalera = [str] * len(capcalera[1])

            if len(capcalera[1]) != len(segona_capcalera):
                logging.error(f"La segunda fila de cabecera en el archivo {fitxer} no tiene el mismo formato.")
                return False, primera_capcalera, segona_capcalera

            for i in range(len(capcalera[1])):
                if not isinstance(capcalera[1][i], segona_capcalera[i]):
                    logging.error(f"Discrepancia en la segunda fila de cabecera en el archivo {fitxer}: "
                                  f"{capcalera[1][i]} (type {type(capcalera[1][i])}) != {segona_capcalera[i]}")
                    return False, primera_capcalera, segona_capcalera

                if capcalera[1][i] != capcalera[1][i].strip():
                    logging.error(f"Valor con espacios extra en la segunda fila de cabecera en el archivo {fitxer}: "
                                  f"{capcalera[1][i]}")
                    return False, primera_capcalera, segona_capcalera

            return True, primera_capcalera, segona_capcalera
    except Exception as e:
        logging.error(f"Error revisando cabeceras en el archivo {fitxer}: {e}")
        return False, primera_capcalera, segona_capcalera

def processar_fitxers(directori):
    if not os.path.exists(directori):
        logging.error(f"El directorio {directori} no existe. El programa ha finalizado.")
        return
    primera_capcalera = None
    segona_capcalera = None
    for arrel, subdirs, fitxers in os.walk(directori):
        for fitxer in fitxers:
            if not revisar_format(fitxer):
                logging.error(f"El archivo {fitxer} no tiene la extensión .dat")
                continue
            fitxer_complet = os.path.join(arrel, fitxer)
            dades = llegir_fitxer(fitxer_complet)
            if dades is None:
                continue
            delimitador = ',' if ',' in dades else '\t' if '\t' in dades else ' '
            hi_ha_comentaris(fitxer_complet, delimitador)
            capcalera_correcta, primera_capcalera, segona_capcalera = revisar_capcaleres(fitxer_complet, delimitador, primera_capcalera, segona_capcalera)

def main():
    directori = os.path.join(os.path.dirname(__file__), '../E01/precip.MIROC5.RCP60.2006-2100.SDSM_REJ')
    processar_fitxers(directori)

if __name__ == "__main__":
    main()