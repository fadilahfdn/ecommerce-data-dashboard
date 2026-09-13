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

# menyiapkan data untuk visualisasi
df_2018 = main_df[main_df['order_year'] == 2018]
top_3_categories = df_2018['product_category_name'].value_counts().head(3).index.tolist()
df_top_categories_2018 = df_2018[df_2018['product_category_name'].isin(top_3_categories)]

revenue_trend = df_top_categories_2018.groupby(by=['order_month_num', 'product_category_name']).agg({
    'price': 'sum'
}).reset_index()
revenue_trend.rename(columns={'price': 'total_revenue'}, inplace=True)

state_orders = df_top_categories_2018.groupby(by='customer_state').agg({
    'order_id': 'nunique'
}).reset_index()
state_orders = state_orders.sort_values(by='order_id', ascending=False)

# membangun antarmuka dashboard
st.title("E-Commerce Public Dataset Dashboard")
st.markdown("Dashboard ini menyajikan hasil analisis data e-commerce, berfokus pada tren pendapatan dan distribusi geografis pelanggan di tahun 2018.")

# membagi layout mrnjadi 2 kolom
col1, col2 = st.columns(2)

with col1:
  st.subheader("Tren Pendapatan Bulanan (3 Kategori Terlaris)")
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
  ax1.legend(title='Kategori Produk')
  st.pyplot(fig1)

with col2:
  st.subheader("10 Negara bagian dengan Pesanan Terbanyak")
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