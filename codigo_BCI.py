import pandas as pd
import warnings

from params import output_dir


def bci(dimerc_banco, descripcion_bci):
    """
    Toma dos marcos de datos, uno con las transacciones bancarias y el otro con la descripción de las
    transacciones, y los fusiona en un solo marco de datos y exporta como .xlsx

    :param dimerc_banco: Este es el marco de datos que contiene los datos del archivo DIMERC
    :param descripcion_bci: Este es el marco de datos que contiene la descripción de las transacciones
    """
    warnings.filterwarnings('ignore')
    pd.set_option('display.float_format', lambda x: '%.3f' % x)

    DF = dimerc_banco
    df_descripcion_bci = descripcion_bci
    df_descripcion_bci = df_descripcion_bci.dropna(subset=['Saldo'])

    if str(df_descripcion_bci['Saldo'].dtype) == 'object':
        df_descripcion_bci['Saldo'] = df_descripcion_bci['Saldo'].str.replace(
            '.', '')
        df_descripcion_bci['Saldo'] = df_descripcion_bci['Saldo'].str.replace(
            ',', '.')
        df_descripcion_bci['Saldo'] = df_descripcion_bci['Saldo'].astype(float)

    df_descripcion_bci['Saldo'] *= -1
    condicion1 = DF['Clase de documento'] == 'CT'
    condicion2 = DF['Cuenta de mayor'] == 1101021011
    df = DF[condicion1 & condicion2]
    lista = ['FECHA', 'SUCURSAL', 'N° DE']
    df_descripcion_bci = df_descripcion_bci.drop(lista, axis=1)
    tabla = df.merge(df_descripcion_bci, how='left',
                     left_on='Importe en moneda doc.', right_on='Saldo')

    importes_problematicos = tabla['Importe en moneda doc.'].value_counts() > 1
    importes_problematicos = pd.DataFrame(importes_problematicos)
    importes_problematicos = importes_problematicos[importes_problematicos['Importe en moneda doc.']]

    if importes_problematicos.shape[0] > 0:
        importes_problematicos = importes_problematicos.index
        condicion = df['Importe en moneda doc.'].isin(importes_problematicos)
        df = df.drop(df[condicion].index)
        condicion = df_descripcion_bci['Saldo'].isin(importes_problematicos)
        df_descripcion_bci = df_descripcion_bci.drop(
            df_descripcion_bci[condicion].index)
        tabla = df.merge(df_descripcion_bci, how='left',
                         left_on='Importe en moneda doc.', right_on='Saldo')

    inter = tabla.dropna(subset=['DESCRIPCION'])
    tabla.loc[inter.index, 'Texto'] = inter['DESCRIPCION']
    tabla = tabla.drop(['DESCRIPCION', 'Saldo'], axis=1)

    condicion3 = ~DF['Importe en moneda doc.'].isin(importes_problematicos)
    tabla.index = DF[condicion1 & condicion2 & condicion3].index
    DF.loc[condicion1 & condicion2 & condicion3] = tabla
    df_output = DF.to_excel(f"{output_dir}/2000 Bancos.xlsx", index=False)


'''def correr():
    limpiar_output(output_dir)
    dimerc = pd.read_excel(f'{input_dir}/2000 Bancos 1.XLSX')
    descripcion_bci = pd.read_excel(
        f'{input_dir}/Descripcion BCI.xlsx').drop(0)
    bci(dimerc, descripcion_bci)


hola = correr()'''
