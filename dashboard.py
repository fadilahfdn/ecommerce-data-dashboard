import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# memfilter data utama berdasarkan tahun yang dipilih
filtered_df = main_df[main_df['order_year'] == selected_year]

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
st.markdown(f"Menampilkan tren pendapatan dan distribusi untuk **Top {top_n} Kategori Produk** pada tahun **{selected_year}**.")

# membagi layout mrnjadi 2 kolom
col1, col2 = st.columns(2)

with col1:
  st.subheader("Tren Pendapatan Bulanan")
  fig1, ax1 = plt.subplots(figsize=(10, 6))
  sns.lineplot(
      data=revenue_trend,
      x='order_month_num',
      y='total_revenue',
      hue='product_category_name',
      marker='o',
      ax=ax1
  )
  ax1.set_xlabel("Bulan")
  ax1.set_ylabel("Total Pendapatan")
  ax1.set_xticks(sorted(revenue_trend['order_month_num'].unique()))
  ax1.legend(title='Kategori Produk', bbox_to_anchor=(1.05, 1), loc='upper left')
  plt.tight_layout()
  st.pyplot(fig1)

with col2:
  st.subheader("Negara bagian dengan Pesanan Terbanyak")
  fig2, ax2 = plt.subplots(figsize=(10, 6))
  sns.barplot(
      data=state_orders.head(10),
      x='order_id',
      y='customer_state', 
      hue='customer_state', 
      palette='viridis', 
      legend=False, 
      ax=ax2
  )
  ax2.set_xlabel("Total Pesanan")
  ax2.set_ylabel("Negara Bagian")
  st.pyplot(fig2)
  
st.caption("Proyek Analisis Data Asah Dicoding 2026")