import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema seaborn
sns.set(style='dark')

# ---- LOAD DATA ----
@st.cache_data
def load_data():
    sellers_df = pd.read_csv('./Data/sellers_dataset.csv')
    geolocation_df = pd.read_csv('./Data/geolocation_dataset.csv')
    products_df = pd.read_csv('./Data/products_dataset.csv')
    orders_df = pd.read_csv('./Data/orders_dataset.csv')
    order_payments_df = pd.read_csv('./Data/order_payments_dataset.csv')
    customers_df = pd.read_csv('./Data/customers_dataset.csv')
    order_items_df = pd.read_csv('./Data/order_items_dataset.csv')

    # Konversi ke datetime
    orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])
    
    return orders_df, order_payments_df, customers_df, order_items_df, products_df, geolocation_df

# Load data
orders_df, order_payments_df, customers_df, order_items_df, products_df, geolocation_df = load_data()

# ---- WELCOME MESSAGE ----
st.title('E-commerce Analysis Dashboard 📊')
st.write("Selamat datang di Dashboard E-commerce! Di sini, Anda dapat mengeksplorasi berbagai aspek dari data e-commerce, mulai dari tren penjualan hingga distribusi pelanggan. Nikmati analisis yang interaktif dan temukan wawasan menarik! 🚀")

# ---- SIDEBAR ----
st.sidebar.title('E-commerce Dashboard')
st.sidebar.image("Images.jpg", use_column_width=True)

# Profil Developer
st.sidebar.markdown("### Developer")
st.sidebar.write("**Nama:** Moch Nazham Ismul Azham")
st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/moch-nazham-ismul-azham-3b7513343/)")
st.sidebar.markdown("[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/JangAY)")

# ---- FILTER ----
st.sidebar.header("Filter Data")

# Filter Tanggal
min_date = orders_df['order_purchase_timestamp'].min().date()
max_date = orders_df['order_purchase_timestamp'].max().date()

start_date, end_date = st.sidebar.date_input(
    'Pilih Rentang Tanggal',
    [min_date, max_date]
)

# Konversi ke datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter Berdasarkan Kategori Produk
product_categories = ['All'] + sorted(products_df['product_category_name'].dropna().unique().tolist())
selected_category = st.sidebar.selectbox('Pilih Produk', product_categories)

# Filter Berdasarkan Metode Pembayaran
payment_methods = ['All'] + sorted(order_payments_df['payment_type'].dropna().unique().tolist())
selected_payment = st.sidebar.selectbox('Pilih Metode Pembayaran', payment_methods)

# Filter Berdasarkan Lokasi Geografis
geo_locations = ['All'] + sorted(geolocation_df['geolocation_state'].dropna().unique().tolist())
selected_location = st.sidebar.selectbox('Pilih Lokasi Geografis', geo_locations)

# ---- FILTER DATA ----
orders_filtered = orders_df[
    (orders_df['order_purchase_timestamp'] >= start_date) & 
    (orders_df['order_purchase_timestamp'] <= end_date)
].copy()  # Hindari SettingWithCopyWarning

if selected_category != 'All':
    order_items_filtered = order_items_df.merge(products_df, on='product_id')
    order_items_filtered = order_items_filtered[order_items_filtered['product_category_name'] == selected_category]
else:
    order_items_filtered = order_items_df.copy()

if selected_payment != 'All':
    order_payments_filtered = order_payments_df[order_payments_df['payment_type'] == selected_payment]
else:
    order_payments_filtered = order_payments_df.copy()

if selected_location != 'All':
    geolocation_filtered = geolocation_df[geolocation_df['geolocation_state'] == selected_location]
else:
    geolocation_filtered = geolocation_df.copy()


# ---- VISUALISASI ----
st.title('E-commerce Analysis Dashboard 📊')

# ---- TOP SELLING PRODUCTS ----
st.header('1. Produk yang Paling Banyak Dibeli')
def visual_product():
    top_products = order_items_filtered['product_id'].value_counts().head(10).reset_index()
    top_products.columns = ['product_id', 'total_sold']
    top_products = top_products.merge(products_df, on='product_id', how='left')

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y=top_products['product_category_name'], x=top_products['total_sold'], palette='viridis')
    plt.xlabel("Jumlah Pembelian")
    plt.ylabel("Kategori Produk")
    plt.title("Top 10 Produk Paling Banyak Dibeli")
    st.pyplot(fig)
    
    st.write("🔍 **Insight:** Produk dengan jumlah pembelian terbanyak menunjukkan kategori atau brand yang paling diminati pelanggan. Hal ini dapat menjadi acuan strategi pemasaran dan pengelolaan stok.")

visual_product()


# ---- CUSTOMER GEOGRAPHIC DISTRIBUTION ----
st.header('2. Distribusi Pelanggan Berdasarkan Lokasi Geografis')
def visual_geolocation():
    geo_counts = geolocation_df['geolocation_state'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=geo_counts.index, y=geo_counts.values, palette="coolwarm")
    plt.title("Order Distribution by Geolocation")
    plt.xlabel("State")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.write("🌍 **Insight:** Distribusi geografis menunjukkan daerah dengan jumlah pesanan terbanyak, yang dapat membantu dalam pengambilan keputusan terkait pengiriman dan strategi pemasaran lokal.")

visual_geolocation()

# ---- PAYMENT METHOD DISTRIBUTION ----
st.header('3. Metode Pembayaran yang Sering Digunakan')
def visual_payment_type():
    payment_counts = order_payments_filtered['payment_type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%', colors=sns.color_palette("Set2"))
    plt.title("Distribusi Metode Pembayaran")
    st.pyplot(fig)

    st.write("💳 **Insight:** Metode pembayaran yang paling sering digunakan mencerminkan preferensi pelanggan, sehingga dapat membantu dalam meningkatkan pengalaman transaksi.")

visual_payment_type()

# ---- SEASONAL ORDER TRENDS ----
st.header('4. Pola Musiman dalam Jumlah Pesanan')
def visual_monthly_orders():
    orders_filtered['order_month'] = orders_filtered['order_purchase_timestamp'].dt.to_period("M")
    monthly_orders = orders_filtered['order_month'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(12, 5))
    monthly_orders.plot(kind='line', marker='o', color='green')
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Pesanan")
    plt.title("Tren Musiman dalam Jumlah Pesanan")
    plt.grid()
    st.pyplot(fig)
    
    st.write("📆 **Insight:** Pola musiman ini membantu mengidentifikasi bulan-bulan dengan permintaan tinggi, yang dapat digunakan untuk merencanakan stok dan strategi promosi.")


visual_monthly_orders()

def visual_weekly_orders():
    orders_filtered['order_week'] = orders_filtered['order_purchase_timestamp'].dt.to_period("W")
    weekly_orders = orders_filtered['order_week'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(15, 6))
    weekly_orders.plot(kind='line', marker='o', color='blue')
    plt.xlabel("Mingguan")
    plt.ylabel("Jumlah Pesanan")
    plt.xticks(rotation=45)
    plt.title("Tren Mingguan dalam Jumlah Pesanan")
    plt.grid()
    st.pyplot(fig)

visual_weekly_orders()


# ---- FOOTER ----
st.sidebar.markdown("---")
st.sidebar.write("Developed by \nMoch Nazham Ismul Azham")
