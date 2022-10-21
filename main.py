from ast import Return
import streamlit as st
import pandas as pd
import os
import io
import streamlit_authenticator as stauth



st.set_page_config(
    layout="wide",
    menu_items={
        "Get help": None,
        "Report a Bug": None,
        "About": None,
    },
)

st.title('AYI TOOLS')

title = st.text_input('INGRESE SU USUARIO', 'USUARIO')
if title != 'MATIAS@GMAIL.COM':
  st.write('ACCESO NOK', title)
else:




    filters = dict()

    data_bytes = io.BytesIO()

    #googleSheetId = os.environ["SHEET_ID"] 

    googleSheetId = '1b7m7t729bmOk6WUExyWgPlPMWIERKrx5TK1NBbdRU1s'

    worksheetName = "Hoja 2".replace(" ", "%20")

    SHEET_URL = (
        "https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}".format(
            googleSheetId, worksheetName
        )
    )

    data = pd.read_csv(SHEET_URL, header=0)

    data.columns = [x.replace(" ", "_") for x in data.columns]

    data.columns = [x.replace("__", "_") for x in data.columns]

    data.columns = [x.replace("[", "") for x in data.columns]

    data.columns = [x.replace("]", "") for x in data.columns]

    data.columns = [x.replace("¿", "") for x in data.columns]

    data.columns = [x.replace("?", "") for x in data.columns]

    data.columns = [x.replace("(", "") for x in data.columns]

    data.columns = [x.replace(")", "") for x in data.columns]

    data.columns = [x.replace(":", "") for x in data.columns]

    data.columns = [x.replace("-", "") for x in data.columns]

    data.columns = [x.replace("!", "") for x in data.columns]

    data.columns = [x.replace("¡", "") for x in data.columns]

    data.columns = [x[0:-1] if x.endswith("_") else x for x in data.columns]

    data.columns = [x.replace("/", "_o_") for x in data.columns]

    data.fillna("N/A", inplace=True)

    t1, t2 = st.tabs(
        [
            "Filtrar por correo/nombre",
            "Filtrar por conocimiento",
        ]
    )

    with t1:

        st.subheader("Ejemplos de búsqueda:")
        st.markdown(
            """
            - CARLOS MENDEZ
            - Carlos Mendez
            - Carlos mendez
            - carlos mendez
            - carlos.mendez
            - carlos.mendez@ayi.group
                    """
        )

        l_col, _ = st.columns([2, 4])

        with l_col:
            search = st.text_input("Buscar:")
            search_button = st.button("Buscar")

        if search or search_button:

            email = search.lower()

            if " " in email:
                email = email.replace(" ", ".")

            if not "@" in email:

                email = f"{email}@ayi.group"

            mask = data["Dirección_de_correo_electrónico"] == email

            user = data[mask]

            st.title("Resultado:")

            for i, x in enumerate(user.columns):
                if not i == 0:
                    if not user.iloc[0, i] == "N/A":
                        if x == "Dirección_de_correo_electrónico":
                            st.markdown("# {}".format(user[x].values.any()))
                            continue
                        st.markdown(
                            """### {}:
                                {}""".format(
                                x, user[x].values.any()
                            )
                        )

        else:
            display_data = data
            display_data.columns = [x for x in display_data.columns]
            st.dataframe(display_data)

    with t2:

        cols = (
            x
            for x in data.columns
            if not "correo" in x.lower()
            and not "conocimiento" in x.lower()
            and not "caso" in x.lower()
            and not ".1" in x.lower()
            and not "marca_temporal" in x.lower()
        )

        columns = st.multiselect("Columnas:", [x for x in cols], key="exc")

        query_mode = " | "

        exclusive = st.checkbox("Condiciones excluyentes")

        if exclusive:
            query_mode = " & "

        if columns:

            for x in data.columns:
                if x in columns:
                    label = x
                    filters[label] = st.selectbox(
                        label,
                        (
                            value
                            for value in data[x].unique()
                            if ".1" not in str(value) and not value == "N/A"
                        ),
                    )

            query = query_mode.join(
                [
                    "{}.str.contains('{}')".format(key, value)
                    for key, value in filters.items()
                ]
            )

            filtered_data = data.query(query)

            st.write(filtered_data)

            filtered_data.to_excel(data_bytes)

        else:
            display_data = data

            st.dataframe(display_data)

            data.to_excel(data_bytes)

        col1, _, _ = st.columns([1, 1, 3])

        with col1:

            file_name = st.text_input(
                "Nombre del archivo (enter para aplicar):", placeholder="Data"
            )

            if file_name == "":
                file_name = "Data"

            file_format = st.selectbox("Formato:", [".xlsx (Excel)", ".csv"])

            if " " in file_format:
                file_format = file_format.split(" ")[0]

            st.download_button(
                "Descargar {}".format(file_format),
                data_bytes.getvalue(),
                "{}{}".format(file_name, file_format),
                "text/excel",
            )
