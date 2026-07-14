"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import os

    import pandas as pd

    os.makedirs("files/output", exist_ok=True)

    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)

    # Columnas de texto: minusculas, unificar separadores (-, _) por espacio,
    # colapsar espacios repetidos y quitar espacios sobrantes.
    text_columns = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for col in text_columns:
        df[col] = (
         
            df[col]
            .astype(str)
            .str.lower()
            .str.replace("-", " ", regex=False)
            .str.replace("_", " ", regex=False)
            .str.replace(r"\s+", " ", regex=True)
        )

    # monto_del_credito: quitar simbolo de moneda, comas, espacios y ".00"
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.replace(r"[\$,\s]", "", regex=True)
        .str.replace(r"\.00$", "", regex=True)
        .astype(float)
        .astype("Int64")
    )

    # fecha_de_beneficio: hay dos formatos mezclados (dd/mm/yyyy y yyyy/mm/dd)
    fecha_dmy = pd.to_datetime(
        df["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    )
    fecha_ymd = pd.to_datetime(
        df["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce"
    )
    df["fecha_de_beneficio"] = fecha_dmy.combine_first(fecha_ymd)

    # Eliminar registros con datos faltantes y registros duplicados
    df = df.dropna()
    df = df.drop_duplicates()

    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)