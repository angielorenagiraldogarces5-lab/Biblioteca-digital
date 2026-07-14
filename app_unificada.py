import streamlit as st
import sqlite3
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Mi Biblioteca Digital", layout="centered")
PASSWORD_ADMIN = "tu_clave"

# --- FUNCIONES DE BASE DE DATOS ---
def obtener_libros():
    if not os.path.exists('biblioteca.db'): return []
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM libros")
        libros = cursor.fetchall()
    except:
        libros = []
    conn.close()
    return libros

# --- BARRA LATERAL ---
menu = st.sidebar.radio("Navegación", ["📚 Biblioteca", "⚙️ Administración"])

if menu == "📚 Biblioteca":
    st.title("📚 Mi Biblioteca Digital")
    libros = obtener_libros()
    if not libros:
        st.info("Aún no hay libros disponibles.")
    else:
        for libro in libros:
            # Estructura: 0:id, 1:titulo, 2:autor, 3:sinopsis, 4:orden, 5:portada, 6:pdf
            titulo, autor, sinopsis, ruta_portada, ruta_pdf = libro[1], libro[2], libro[3], libro[5], libro[6]
            with st.container():
                col1, col2 = st.columns([1, 2])
                with col1:
                    if os.path.exists(ruta_portada): st.image(ruta_portada, use_container_width=True)
                with col2:
                    st.subheader(titulo)
                    st.write(f"**Autor:** {autor}")
                    st.write(sinopsis)
                    if os.path.exists(ruta_pdf):
                        with open(ruta_pdf, "rb") as f:
                            st.download_button("📥 Descargar", data=f, file_name=os.path.basename(ruta_pdf))
                st.divider()

else:
    # --- LÓGICA DE ADMINISTRACIÓN ---
    if 'admin_logged' not in st.session_state: st.session_state.admin_logged = False
    
    if not st.session_state.admin_logged:
        clave = st.text_input("Clave de acceso", type="password")
        if st.button("Acceder"):
            if clave == "Angie2006":
                st.session_state.admin_logged = True
                st.rerun()
            else: st.error("Clave incorrecta")
    else:
        st.title("⚙️ Panel Administrativo")
        with st.expander("➕ Subir nuevo libro"):
            with st.form("form_carga", clear_on_submit=True):
                titulo = st.text_input("Título")
                autor = st.text_input("Autor")
                sinopsis = st.text_area("Sinopsis")
                portada = st.file_uploader("Portada", type=['jpg', 'png', 'jpeg'])
                pdf = st.file_uploader("PDF", type=['pdf'])
                
                if st.form_submit_button("Subir libro"):
                    if titulo and portada and pdf:
                        os.makedirs("media/portadas", exist_ok=True)
                        os.makedirs("media/libros", exist_ok=True)
                        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                        ruta_p = f"media/portadas/{ts}_{portada.name}"
                        ruta_l = f"media/libros/{ts}_{pdf.name}"
                        with open(ruta_p, "wb") as f: f.write(portada.getbuffer())
                        with open(ruta_l, "wb") as f: f.write(pdf.getbuffer())
                        
                        conn = sqlite3.connect('biblioteca.db')
                        cursor = conn.cursor()
                        cursor.execute('''CREATE TABLE IF NOT EXISTS libros 
                                          (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, autor TEXT, 
                                           sinopsis TEXT, orden_en_saga INTEGER, ruta_portada TEXT, ruta_pdf TEXT, saga_id INTEGER)''')
                        cursor.execute("INSERT INTO libros (titulo, autor, sinopsis, ruta_portada, ruta_pdf) VALUES (?,?,?,?,?)", 
                                       (titulo, autor, sinopsis, ruta_p, ruta_l))
                        conn.commit()
                        conn.close()
                        st.success("¡Libro guardado!")
                    else: st.error("Completa todos los campos")

        st.subheader("🗑️ Eliminar libros existentes")
        libros_admin = obtener_libros()
        if not libros_admin:
            st.write("No hay libros disponibles para eliminar.")
        else:
            for libro in libros_admin:
                id_libro, titulo_l = libro[0], libro[1]
                col1, col2 = st.columns([4, 1])
                col1.write(f"**{titulo_l}**")
                if col2.button("Eliminar", key=f"del_{id_libro}"):
                    conn = sqlite3.connect('biblioteca.db')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
                    conn.commit()
                    conn.close()
                    st.rerun()