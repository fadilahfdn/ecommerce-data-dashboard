import pandas as pd
import plotly.express as px
import streamlit as st

# konfiggurasi halaman streamlit
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# memuat data menggunakan cache
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    return df
  
main_df = load_data()

# fitur sidebar
st.sidebar.header("Filter Data")

# dropdown untuk memilih tahun
year_list = main_df['order_year'].dropna().unique().astype(int).tolist()
year_list.sort()
selected_year = st.sidebar.selectbox("Pilih Tahun Transaksi:", year_list, index=len(year_list)-1)

# slider untuk memilih jumlah top kategori
top_n = st.sidebar.slider("Pilih Jumlah Kategori Terlaris:", min_value=1, max_value=5, value=3)

# filter rentang bulan transaksi
min_month = int(main_df['order_month_num'].min())
max_month = int(main_df['order_month_num'].max())
selected_months = st.sidebar.slider("Pilih Rentang Bulan:", min_value=min_month, max_value=max_month, value=(min_month, max_month))

# memfilter data utama berdasarkan tahun dan rentang yang dipilih
filtered_df = main_df[
   (main_df['order_year'] == selected_year) &
   (main_df['order_month_num'] >= selected_months[0]) &
   (main_df['order_month_num'] <= selected_months[1])
]

# mengambil kategori teratas
top_categories = filtered_df['product_category_name'].value_counts().head(top_n).index.tolist()
final_df = filtered_df[filtered_df['product_category_name'].isin(top_categories)]

revenue_trend = final_df.groupby(by=['order_month_num', 'product_category_name']).agg({
    'price': 'sum'
}).reset_index()
revenue_trend.rename(columns={'price': 'total_revenue'}, inplace=True)

state_orders = final_df.groupby(by='customer_state').agg({
    'order_id': 'nunique'
}).reset_index()
state_orders = state_orders.sort_values(by='order_id', ascending=False)

# membangun antarmuka dashboard
st.title("E-Commerce Public Dataset Dashboard")
st.markdown(f"Menampilkan tren pendapatan dan distribusi untuk **Top {top_n} Kategori Produk** pada tahun **{selected_year}** (Bulan {selected_months[0]} - {selected_months[1]}).")

# membagi layout mrnjadi 2 kolom
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tren Pendapatan Bulanan")
    # Plotly Line Chart
    fig1 = px.line(
        revenue_trend, 
        x='order_month_num', 
        y='total_revenue', 
        color='product_category_name',
        markers=True,
        labels={
            'order_month_num': 'Bulan', 
            'total_revenue': 'Total Pendapatan (BRL)', 
            'product_category_name': 'Kategori Produk'
        }
    )
    # memastikan sumbu X menampilkan angka bulan bulat
    fig1.update_xaxes(dtick=1) 
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Negara Bagian dengan Pesanan Terbanyak")
    # Plotly Bar Chart
    fig2 = px.bar(
        state_orders.head(10), 
        x='order_id', 
        y='customer_state', 
        color='customer_state',
        orientation='h',
        labels={
            'order_id': 'Total Pesanan', 
            'customer_state': 'Negara Bagian'
        }
    )
    fig2.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)
  
st.caption("Proyek Analisis Data Asah Dicoding 2026")