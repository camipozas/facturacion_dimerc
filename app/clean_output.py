import os
import shutil


def limpiar_output(output_dir):
    """
    Si el directorio de salida existe, elimínelo y vuelva a crearlo

    :param output_dir: El directorio donde se guardarán los archivos de salida
    """
    # Si existe la carpeta la eliminamos
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    # Si existe un archivo con el mismo nombre que la carpeta
    # lo eliminamos
    if os.path.isfile(output_dir):
        os.remove(output_dir)
    # Creamos la carpeta para que este limpia
    os.mkdir(output_dir)
    print('Carpeta limpia')
