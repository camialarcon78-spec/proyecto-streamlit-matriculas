import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Matrículas",
    layout="wide"
)



(st.markdown("""# 🎓 Panel de Matrículas en Educación Superior
### Análisis interactivo de la matrícula en instituciones de educación superior en Chile
"""))

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    color: white;
    font-size: 50px;
    font-weight: 800;
}

h2{
    color:#4FC3F7;
}

h3{
    color:white;
}

p{
    font-size:18px;
}

[data-testid="stSidebar"]{
    background-color:#1C1F2B;
}

div[data-testid="stMetric"]{
    background:#202636;
    border-radius:15px;
    padding:20px;
    border:1px solid #3A3F4B;
}

</style>
""", unsafe_allow_html=True)

st.header("🎯 Objetivo del proyecto")

st.write("""
Este dashboard fue desarrollado con el propósito de analizar la evolución de la matrícula
en la educación superior chilena entre los años 2007 y 2025.

A través de distintas visualizaciones interactivas es posible explorar cómo se distribuye
la matrícula según variables como género, región, modalidad, jornada y carrera,
facilitando la comprensión de tendencias relevantes y apoyando la toma de decisiones
basadas en datos.
""")

st.header("📊 ¿Qué encontrarás en este dashboard?")

col1, col2 = st.columns(2)

with col1:
    st.success("🧹 Limpieza de datos")
    st.success("📊 Indicadores principales")
    st.success("📈 Gráficos interactivos")

with col2:
    st.success("🌎 Análisis por región")
    st.success("🎓 Información de carreras")
    st.success("💡 Conclusiones e insights")

@st.cache_data
def cargar_datos():
    df = pd.read_csv(
        "Matricula_2007_2025_WEB_15_07_2025 (1).csv",
        sep=";",
        encoding="latin-1",
        low_memory=False
    )
    return df

pagina = st.sidebar.selectbox(
    "Selecciona una sección",
    [
        "🏠 Inicio",
        "🧹 Limpieza de datos",
        "📊 Visualizaciones",
        "💡 Conclusiones"
    ]
)

df = cargar_datos()



# Completar valores nulos
df["TOTAL MATRÍCULA MUJERES"] = df["TOTAL MATRÍCULA MUJERES"].fillna(0)
df["TOTAL MATRÍCULA HOMBRES"] = df["TOTAL MATRÍCULA HOMBRES"].fillna(0)
df["TOTAL MATRÍCULA NO BINARIOS O INDEFINIDOS"] = df["TOTAL MATRÍCULA NO BINARIOS O INDEFINIDOS"].fillna(0)
df["TOTAL MATRÍCULA PRIMER AÑO"] = df["TOTAL MATRÍCULA PRIMER AÑO"].fillna(0)

# Renombrar columnas
df.rename(columns={
    "AÑO": "año",
    "TOTAL MATRÍCULA": "total_matricula",
    "TOTAL MATRÍCULA MUJERES": "matricula_mujeres",
    "TOTAL MATRÍCULA HOMBRES": "matricula_hombres",
    "TOTAL MATRÍCULA NO BINARIOS O INDEFINIDOS": "no_binarios_o_indefinidos",
    "TOTAL MATRÍCULA PRIMER AÑO": "matricula_primer_año",
    "TOTAL MATRÍCULA MUJERES PRIMER AÑO": "mujeres_primer_año",
    "TOTAL MATRÍCULA HOMBRES PRIMER AÑO": "hombres_primer_año",
    "CLASIFICACIÓN INSTITUCIÓN NIVEL 1": "clasificacion_nivel_1",
    "REGIÓN": "region",
    "COMUNA": "comuna",
    "NOMBRE CARRERA": "nombre_carrera",
    "ÁREA DEL CONOCIMIENTO": "area_conocimiento",
    "MODALIDAD": "modalidad",
    "JORNADA": "jornada",
    "ACREDITACIÓN INSTITUCIONAL": "acreditacion_institucional"
}, inplace=True, errors="ignore")

# Limpiar espacios en texto
df["area_conocimiento"] = df["area_conocimiento"].str.strip()

# Convertir MAT_2025 → 2025
df["año"] = df["año"].str.replace("MAT_", "", regex=False)
df["año"] = df["año"].astype(int)

# Eliminar columnas que no utilizarás
columnas_eliminar = [
    "rango_edad_15_a_19",
    "rango_edad_20_a_24",
    "rango_edad_25_a_29",
    "rango_edad_30_a_34",
    "rango_edad_35_a_39",
    "no_binarios_o_indefinidos",
    "no_binarios_o_indefinidos_primer_año",
    "promedio_edad_no_binario"
]

df.drop(columns=columnas_eliminar, inplace=True, errors="ignore")

# Optimizar algunas columnas
for columna in ["region", "comuna", "acreditacion_institucional"]:
    if columna in df.columns:
        df[columna] = df[columna].astype("category")



st.sidebar.header("Filtros")

if "region" in df.columns:
    regiones = st.sidebar.multiselect(
        "Selecciona región",
        options=sorted(df["region"].dropna().unique()),
        default=sorted(df["region"].dropna().unique())
    )

    df_filtrado = df[df["region"].isin(regiones)]
else:
    df_filtrado = df

if pagina == "Inicio":
    st.header("Inicio")
    st.write("""
    Esta aplicación permite analizar la matrícula en educación superior,
    considerando variables como región, género, carrera e institución.
    """)


elif pagina == "Limpieza de datos":
    st.header("Limpieza y preparación de datos")

    st.write("""
    En esta sección se presenta el proceso de limpieza aplicado a la base de datos.
    El objetivo fue preparar la información para que pudiera ser utilizada correctamente
    en los gráficos y análisis del dashboard.
    """)

    st.subheader("1. Vista previa de la base original procesada")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("2. Tamaño de la base de datos")
    filas, columnas = df.shape

    col1, col2 = st.columns(2)
    col1.metric("Cantidad de filas", filas)
    col2.metric("Cantidad de columnas", columnas)

    st.subheader("3. Columnas disponibles después de la limpieza")
    st.write(df.columns.tolist())

    st.subheader("4. Valores nulos después de la limpieza")
    nulos = df.isnull().sum().reset_index()
    nulos.columns = ["Columna", "Cantidad de valores nulos"]

    st.dataframe(nulos, use_container_width=True)

    st.subheader("5. Tipos de datos")
    tipos_datos = df.dtypes.astype(str).reset_index()
    tipos_datos.columns = ["Columna", "Tipo de dato"]

    st.dataframe(tipos_datos, use_container_width=True)

    st.subheader("6. Acciones realizadas")
    st.markdown("""
    - Se completaron valores nulos en las columnas de matrícula.
    - Se renombraron columnas para facilitar su uso en Python.
    - Se transformó la columna `año`, pasando de valores como `MAT_2025` a `2025`.
    - Se eliminaron columnas que no eran necesarias para el análisis principal.
    - Se limpiaron espacios en blanco en variables de texto.
    - Se optimizaron algunas columnas categóricas como región, comuna y acreditación institucional.
    """)

    st.success("La base de datos quedó preparada para el análisis y la visualización.")

elif pagina == "Visualizaciones":
    st.header("Visualizaciones del dashboard")

    st.write("""
    En esta sección se presentan los principales gráficos interactivos del proyecto,
    considerando la matrícula total, género, región, jornada y modalidad.
    """)

    # KPIs principales
    st.subheader("Indicadores principales")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total matrícula",
        f"{df_filtrado['total_matricula'].sum():,.0f}"
    )

    col2.metric(
        "Matrícula mujeres",
        f"{df_filtrado['matricula_mujeres'].sum():,.0f}"
    )

    col3.metric(
        "Matrícula hombres",
        f"{df_filtrado['matricula_hombres'].sum():,.0f}"
    )

    # Gráfico 1: evolución de matrícula total
    st.subheader("1. Evolución de la matrícula total por año")

    matricula_anual = (
        df_filtrado.groupby("año")["total_matricula"]
        .sum()
        .reset_index()
        .sort_values("año")
    )

    fig1 = px.line(
        matricula_anual,
        x="año",
        y="total_matricula",
        markers=True,
        title="Evolución de la matrícula total"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: matrícula por género
    st.subheader("2. Matrícula por género")

    genero = df_filtrado[["matricula_mujeres", "matricula_hombres"]].sum().reset_index()
    genero.columns = ["genero", "matricula"]

    fig2 = px.bar(
        genero,
        x="genero",
        y="matricula",
        title="Distribución de matrícula por género",
        text_auto=True
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: matrícula por región
    st.subheader("3. Matrícula total por región")

    matricula_region = (
        df_filtrado.groupby("region")["total_matricula"]
        .sum()
        .reset_index()
        .sort_values("total_matricula", ascending=False)
    )

    fig3 = px.bar(
        matricula_region,
        x="total_matricula",
        y="region",
        orientation="h",
        title="Matrícula total por región",
        text_auto=True
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: matrícula por jornada
    st.subheader("4. Matrícula por jornada")

    if "jornada" in df_filtrado.columns:
        jornada = (
            df_filtrado.groupby("jornada")["total_matricula"]
            .sum()
            .reset_index()
            .sort_values("total_matricula", ascending=False)
        )

        fig4 = px.pie(
            jornada,
            names="jornada",
            values="total_matricula",
            title="Distribución de matrícula por jornada"
        )

        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("La columna jornada no está disponible en la base.")

    # Gráfico 5: matrícula por modalidad
    st.subheader("5. Matrícula por modalidad")

    if "modalidad" in df_filtrado.columns:
        modalidad = (
            df_filtrado.groupby("modalidad")["total_matricula"]
            .sum()
            .reset_index()
            .sort_values("total_matricula", ascending=False)
        )

        fig5 = px.bar(
            modalidad,
            x="modalidad",
            y="total_matricula",
            title="Matrícula por modalidad",
            text_auto=True
        )

        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.warning("La columna modalidad no está disponible en la base.")

    # Gráfico 6: top carreras
    st.subheader("6. Top 10 carreras con mayor matrícula")

    if "nombre_carrera" in df_filtrado.columns:
        top_carreras = (
            df_filtrado.groupby("nombre_carrera")["total_matricula"]
            .sum()
            .reset_index()
            .sort_values("total_matricula", ascending=False)
            .head(10)
        )

        fig6 = px.bar(
            top_carreras,
            x="total_matricula",
            y="nombre_carrera",
            orientation="h",
            title="Top 10 carreras con mayor matrícula",
            text_auto=True
        )

        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.warning("La columna nombre_carrera no está disponible en la base.")


elif pagina == "Conclusiones":

    st.subheader("Conclusiones")

    st.markdown("""
    A partir del análisis realizado, se observa que la matrícula en educación superior 
    presenta diferencias relevantes según género, región, carrera, jornada y modalidad. 
    Estas visualizaciones permiten comprender mejor cómo se distribuyen los estudiantes 
    y facilitan la identificación de tendencias importantes para la toma de decisiones.
    """)

    st.subheader("Principales hallazgos")

    st.markdown("""
    - La matrícula total permite visualizar la magnitud del sistema de educación superior.
    - La comparación por género ayuda a identificar brechas o diferencias de participación.
    - El análisis por región permite reconocer dónde se concentra la mayor cantidad de estudiantes.
    - Las variables de jornada y modalidad muestran cómo se organiza la oferta académica.
    """)

    st.subheader("Propuesta futura")

    st.markdown("""
    Como mejora futura, se podría incorporar un modelo predictivo que estime la evolución 
    de la matrícula en los próximos años. Además, el aplicativo podría ampliarse con nuevos 
    filtros, comparación entre instituciones y análisis de titulados para complementar el estudio.
    """)
