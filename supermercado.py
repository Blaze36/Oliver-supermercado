import streamlit as st
import pandas as pd



def registrar_en_carrito(nombre, precio, cant, tipo):
    tasa = 0.18 if tipo == "Alcohol (18%)" else 0.15
    base = float(precio) * float(cant)
    impuesto_valor = base * tasa
    total_fila = base + impuesto_valor
    
    nueva_entrada = {
        "Producto": nombre,
        "Precio Unit.": precio,
        "Cant.": cant,
        "ISV": f"{int(tasa*100)}%",
        "SubTotal": total_fila
    }
    
    st.session_state.table_data = pd.concat(
        [st.session_state.table_data, pd.DataFrame([nueva_entrada])],
        ignore_index=True
    )

if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame(
        columns=["Producto", "Precio Unit.", "Cant.", "ISV", "SubTotal"]
    )

st.title("Supermercado Blaze")


with st.form("entrada_datos"):
    st.subheader("Registro de Artículo")
    col_a, col_b = st.columns(2)
    
    with col_a:
        nom = st.text_input("Nombre del artículo")
        pre = st.number_input("Precio base", min_value=0.0, format="%.2f")
    
    with col_b:
        can = st.number_input("Cantidad", min_value=1, step=1)
        alc = st.selectbox("¿Categoría especial?", ["Normal (15%)", "Alcohol (18%)"])
    
    enviar = st.form_submit_button("🛒 Añadir al Carrito")

if enviar:
    if nom:
        registrar_en_carrito(nom, pre, can, alc)
        st.success(f"{nom} añadido")
    else:
        st.warning("Escribe el nombre del producto")

st.subheader(" Detalle de la Compra")
st.dataframe(st.session_state.table_data, use_container_width=True)

if not st.session_state.table_data.empty:
    if st.button(" Calcular Total"):
        gran_total = st.session_state.table_data["SubTotal"].sum()
        
        st.divider()
        st.metric("TOTAL A PAGAR", f"L. {gran_total:.2f}")
        
        st.success("¡Gracias por su compra!")
        st.info("Vuelva pronto al mercado Blaze")