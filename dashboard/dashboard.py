import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
top_10_cities = pd.read_csv("dashboard/top_10_cities.csv")
bottom_5_cities = pd.read_csv("dashboard/bottom_5_cities.csv")
top_10_states = pd.read_csv("dashboard/top_10_states.csv")
bottom_5_states = pd.read_csv("dashboard/bottom_5_states.csv")
top_10_products = pd.read_csv("dashboard/top_10_products.csv")
bottom_10_products = pd.read_csv("dashboard/bottom_10_products.csv")
monthly_sales = pd.read_csv("dashboard/monthly_sales.csv")

# Menampilkan judul dashboard
st.title("Dashboard E-Commerce")

# Membuat sidebar agar user bisa menggunakan fitur filter
st.sidebar.header("Filter Data")

# Filter berdasarkan bulan 
st.sidebar.subheader("Filter berdasarkan Bulan")

# Memastikan menggunakan bulan-bulan yang tersedia dalam dataset
available_months = monthly_sales["order_purchase_timestamp"].unique()
selected_months = st.sidebar.multiselect(
    "Pilih Bulan",
    options=available_months,
    default=available_months 
)

# Filter monthly_sales berdasarkan bulan yang dipilih
filtered_monthly_sales = monthly_sales[monthly_sales["order_purchase_timestamp"].isin(selected_months)]

# Filter untuk kategori produk
st.sidebar.subheader("Filter berdasarkan Kategori Produk")
all_products = list(top_10_products['product_category_name'].unique()) + list(bottom_10_products['product_category_name'].unique())
all_products = sorted(list(set(all_products)))  # Menghilangkan duplikat dan mengurutkan

# Multiselect untuk kategori produk
selected_products = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    options=all_products,
    default=all_products[:5]  # Default: 5 produk pertama
)

# Filter data produk berdasarkan pilihan
filtered_top_products = top_10_products[top_10_products['product_category_name'].isin(selected_products)] if selected_products else top_10_products
filtered_bottom_products = bottom_10_products[bottom_10_products['product_category_name'].isin(selected_products)] if selected_products else bottom_10_products

# Filter untuk region (state)
st.sidebar.subheader("Filter berdasarkan Region (State)")
all_states = list(top_10_states['customer_state'].unique()) + list(bottom_5_states['customer_state'].unique())
all_states = sorted(list(set(all_states)))  # Menghilangkan duplikat dan mengurutkan

# Radio button untuk memilih semua state atau beberapa state tertentu
state_filter_option = st.sidebar.radio(
    "Pilihan Filter State",
    options=["Tampilkan Semua State", "Pilih State Tertentu"]
)

selected_states = all_states
if state_filter_option == "Pilih State Tertentu":
    selected_states = st.sidebar.multiselect(
        "Pilih State",
        options=all_states,
        default=all_states[:3]  # Default: 3 state pertama
    )

# Filter data state berdasarkan pilihan
filtered_top_states = top_10_states[top_10_states['customer_state'].isin(selected_states)] if selected_states else top_10_states
filtered_bottom_states = bottom_5_states[bottom_5_states['customer_state'].isin(selected_states)] if selected_states else bottom_5_states

# Visualisasi Tren Penjualan Bulanan dengan data yang telah Difilter
# Set tema seaborn
sns.set_theme(style="whitegrid")

# membuat subheader dengan informasi bulan yang dipilih
selected_months_text = ", ".join(selected_months) if len(selected_months) <= 5 else f"{len(selected_months)} bulan terpilih"
st.subheader(f"Tren Total Order dan Revenue per Bulan ({selected_months_text})")

# Jika data yang difilter kosong/tidak ada, akan menampilkan pesan dibawah
if filtered_monthly_sales.empty:
    st.warning("Tidak ada data untuk bulan yang dipilih. Silakan pilih bulan yang berbeda.")
else:
    # Ukuran figure
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot total orders sebagai bar chart
    order_bars = sns.barplot(
        x="order_purchase_timestamp", 
        y="total_orders",
        data=filtered_monthly_sales, 
        color="skyblue", 
        label="Total Orders", 
        ax=ax1
    )

    # membuat sumbu y kedua untuk revenue
    ax2 = ax1.twinx()
    
    # Plot revenue sebagai line chart 
    x = range(len(filtered_monthly_sales))
    ax2.plot(
        x, 
        filtered_monthly_sales["total_revenue"], 
        marker="o", 
        color="red", 
        linewidth=2, 
        label="Total Revenue"
    )

    # Label dan judul
    ax1.set_xlabel("Bulan", fontsize=12)
    ax1.set_ylabel("Jumlah Order", fontsize=12, color="blue")
    ax2.set_ylabel("Total Revenue (Rp)", fontsize=12, color="red")
    plt.title("Tren Total Order dan Revenue per Bulan", fontsize=14)

    # mengeset x-ticks menggunakan bulan dari dataset
    ax1.set_xticks(range(len(filtered_monthly_sales)))
    ax1.set_xticklabels(filtered_monthly_sales["order_purchase_timestamp"], rotation=45)

    # menambahkan legenda
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # menampilkan plot di streamlit
    st.pyplot(fig)

    # menampilkan data dalam tabel dengan data yang telah difilter
    st.subheader("Data Penjualan Bulanan")
    st.dataframe(filtered_monthly_sales)

# Metrics untuk menampilkan ringkasan data
st.subheader("Ringkasan Data")
col1, col2, col3 = st.columns(3)

# menghitung total order dan revenue untuk periode waktu yang dipilih
total_orders = filtered_monthly_sales['total_orders'].sum() if not filtered_monthly_sales.empty else 0
total_revenue = filtered_monthly_sales['total_revenue'].sum() if not filtered_monthly_sales.empty else 0
avg_revenue_per_order = total_revenue / total_orders if total_orders > 0 else 0

with col1:
    st.metric(label="Total Order", value=f"{total_orders:,}")
with col2:
    st.metric(label="Total Revenue", value=f"Rp {total_revenue:,.2f}")
with col3:
    st.metric(label="Rata-rata Revenue per Order", value=f"Rp {avg_revenue_per_order:,.2f}")

# Visualisasi Top 10 Kota dengan Pelanggan Terbanyak
st.subheader("Top 10 Kota dengan Pelanggan Terbanyak")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y=top_10_cities["customer_city"], x=top_10_cities["customer_count"], palette="Blues_r", ax=ax)
ax.set_xlabel("Jumlah Pelanggan")
ax.set_ylabel("Kota")
ax.set_title("Top 10 Kota dengan Pelanggan Terbanyak")
st.pyplot(fig)

# Visualisasi Bottom 5 Kota dengan Pelanggan Paling Sedikit
st.subheader("Bottom 5 Kota dengan Pelanggan Paling Sedikit")
fig, ax = plt.subplots(figsize=(10, 4))
sns.barplot(y=bottom_5_cities["customer_city"], x=bottom_5_cities["customer_count"], palette="Reds_r", ax=ax)
ax.set_xlabel("Jumlah Pelanggan")
ax.set_ylabel("Kota")
ax.set_title("Bottom 5 Kota dengan Pelanggan Paling Sedikit")
st.pyplot(fig)

# Visualisasi Top 10 Provinsi dengan Pelanggan Terbanyak (Data yang Difilter)
st.subheader(f"Top Provinsi dengan Pelanggan Terbanyak (Filter: {', '.join(selected_states) if len(selected_states) <= 5 else f'{len(selected_states)} state terpilih'})")
if filtered_top_states.empty:
    st.warning("Tidak ada data untuk state yang dipilih. Silakan pilih state yang berbeda.")
else:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=filtered_top_states["customer_state"], x=filtered_top_states["customer_count"], palette="Greens_r", ax=ax)
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Provinsi")
    ax.set_title("Top Provinsi dengan Pelanggan Terbanyak")
    st.pyplot(fig)

# Visualisasi Bottom 5 Provinsi dengan Pelanggan Paling Sedikit (Data yang Difilter)
st.subheader(f"Bottom Provinsi dengan Pelanggan Paling Sedikit (Filter: {', '.join(selected_states) if len(selected_states) <= 5 else f'{len(selected_states)} state terpilih'})")
if filtered_bottom_states.empty:
    st.warning("Tidak ada data untuk state yang dipilih. Silakan pilih state yang berbeda.")
else:
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(y=filtered_bottom_states["customer_state"], x=filtered_bottom_states["customer_count"], palette="Oranges_r", ax=ax)
    ax.set_xlabel("Jumlah Pelanggan")
    ax.set_ylabel("Provinsi")
    ax.set_title("Bottom Provinsi dengan Pelanggan Paling Sedikit")
    st.pyplot(fig)

# Menampilkan data dalam tabel
st.subheader("Data Pelanggan per Kota dan Provinsi")
st.write("Top 10 Kota:")
st.dataframe(top_10_cities)

st.write("Bottom 5 Kota:")
st.dataframe(bottom_5_cities)

st.write("Top 10 Provinsi (Data yang Difilter):")
st.dataframe(filtered_top_states)

st.write("Bottom 5 Provinsi (Data yang Difilter):")
st.dataframe(filtered_bottom_states)

# Visualisasi Top 10 Produk Terlaris (Data yang Difilter)
st.subheader(f"Top Produk Terlaris (Filter: {len(selected_products)} produk terpilih)")
if filtered_top_products.empty:
    st.warning("Tidak ada data untuk kategori produk yang dipilih. Silakan pilih kategori produk yang berbeda.")
else:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=filtered_top_products["product_category_name"], x=filtered_top_products["sales"], palette="Blues_r", ax=ax)
    ax.set_xlabel("Jumlah Terjual")
    ax.set_ylabel("Kategori Produk")
    ax.set_title("Top Produk Terlaris")
    st.pyplot(fig)

# Visualisasi Bottom 10 Produk Paling Sedikit Terjual (Data yang Difilter)
st.subheader(f"Bottom Produk Paling Sedikit Terjual (Filter: {len(selected_products)} produk terpilih)")
if filtered_bottom_products.empty:
    st.warning("Tidak ada data untuk kategori produk yang dipilih. Silakan pilih kategori produk yang berbeda.")
else:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=filtered_bottom_products["product_category_name"], x=filtered_bottom_products["sales"], palette="Reds_r", ax=ax)
    ax.set_xlabel("Jumlah Terjual")
    ax.set_ylabel("Kategori Produk")
    ax.set_title("Bottom Produk Paling Sedikit Terjual")
    st.pyplot(fig)

# Menampilkan data dalam tabel
st.subheader("Data Penjualan Produk")
st.write(f"Top Produk Terlaris (Filter: {len(selected_products)} produk terpilih):")
st.dataframe(filtered_top_products)

st.write(f"Bottom Produk Paling Sedikit Terjual (Filter: {len(selected_products)} produk terpilih):")
st.dataframe(filtered_bottom_products)

st.caption('Copyright (c) 2025. Zidan Muhammad Ikvan | Proyek Akhir Analisis Data')
