import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set konfigurasi halaman
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# Set style seaborn
sns.set(style='dark')

# --- Helper Functions (Optimized with Caching) ---

@st.cache_data
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return daily_orders_df

@st.cache_data
def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name_english").product_id.count().sort_values(ascending=False).reset_index()
    return sum_order_items_df

@st.cache_data
def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_unique_id", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    recent_date = df["order_purchase_timestamp"].max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df

# --- Load Cleaned Data ---
all_df = pd.read_csv("dashboard/main_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# --- Sidebar Filter ---
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.title("🛍️ E-Commerce Filter")
    
    # Filter Rentang Waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    st.divider()

    # Filter Kategori Produk
    all_categories = sorted(all_df['product_category_name_english'].unique())
    selected_categories = st.multiselect(
        "Pilih Kategori Produk",
        options=all_categories,
        default=[] 
    )

    st.divider()

    # Informasi Penulis
    with st.expander("ℹ️ Tentang Pengembang"):
        st.write("**Nama:** Carlos Qnova Bha'a Gani")
        st.write("**Email:** carlosqnova88@gmail.com")

# --- Filtering Logic ---
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

if selected_categories:
    main_df = main_df[main_df['product_category_name_english'].isin(selected_categories)]

# --- Dashboard Utama ---
st.header('E-Commerce Public Dashboard ✨')

if main_df.empty:
    st.warning("⚠️ Tidak ada data untuk rentang waktu dan kategori yang dipilih.")
else:
    daily_orders_df = create_daily_orders_df(main_df)
    sum_order_items_df = create_sum_order_items_df(main_df)
    rfm_df = create_rfm_df(main_df)

    # Ringkasan Metrik Utama
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Orders", value=daily_orders_df.order_count.sum())
    with col2:
        total_rev = format_currency(daily_orders_df.revenue.sum(), "BRL", locale='pt_BR')
        st.metric("Total Revenue", value=total_rev)
    with col3:
        avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR')
        st.metric("Avg. Transaction", value=avg_monetary)

    st.divider()

    tab1, tab2, tab3 = st.tabs(["Daily Analysis", "Product Performance", "RFM Analysis"])

    with tab1:
        st.subheader('Daily Orders Trend')
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.plot(
            daily_orders_df["order_purchase_timestamp"],
            daily_orders_df["order_count"],
            marker='o', linewidth=2, color="#72BCD4"
        )
        ax.tick_params(axis='y', labelsize=15)
        ax.tick_params(axis='x', labelsize=12, rotation=45)
        st.pyplot(fig)

    with tab2:
        st.subheader("Best & Worst Performing Products")
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))
        colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

        # Best Products (Ditambah hue dan legend=False agar tidak error log)
        sns.barplot(x="product_id", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors, hue="product_category_name_english", legend=False, ax=ax[0])
        ax[0].set_title("Best Performing Product", loc="center", fontsize=18)
        ax[0].set_xlabel(None)

        # Worst Products
        sns.barplot(x="product_id", y="product_category_name_english", data=sum_order_items_df.sort_values(by="product_id", ascending=True).head(5), palette=colors, hue="product_category_name_english", legend=False, ax=ax[1])
        ax[1].set_title("Worst Performing Product", loc="center", fontsize=18)
        ax[1].invert_xaxis()
        ax[1].yaxis.tick_right()
        ax[1].set_xlabel(None)
        
        st.pyplot(fig)

    with tab3:
        st.subheader("Best Customers based on RFM")
        fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 10))
        colors = ["#72BCD4"] * 5

        # Recency
        sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, hue="customer_id", legend=False, ax=ax[0])
        ax[0].set_title("By Recency (days)", fontsize=20)
        ax[0].tick_params(axis='x', rotation=45)

        # Frequency
        sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, hue="customer_id", legend=False, ax=ax[1])
        ax[1].set_title("By Frequency", fontsize=20)
        ax[1].tick_params(axis='x', rotation=45)

        # Monetary
        sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, hue="customer_id", legend=False, ax=ax[2])
        ax[2].set_title("By Monetary", fontsize=20)
        ax[2].tick_params(axis='x', rotation=45)

        st.pyplot(fig)

st.caption('Copyright (c) 2026 - Analisis Data E-Commerce')