import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide"
)

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("dayfinal.csv")
df['dteday'] = pd.to_datetime(df['dteday'])

# =====================
# SIDEBAR
# =====================
st.sidebar.title("🚲 Bike Sharing Dashboard")
year = st.sidebar.selectbox("Pilih Tahun", [2011, 2012])

df = df[df['yr'] == (year - 2011)]

# =====================
# HEADER
# =====================
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Analisis pola penyewaan sepeda berdasarkan cuaca, musim, dan waktu (2011–2012)")
st.markdown("---")

# =====================
# KPI SECTION
# =====================
col1, col2, col3 = st.columns(3)

col1.metric("Total Penyewaan", f"{df['cnt'].sum():,.0f}")
col2.metric("Rata-rata Harian", f"{df['cnt'].mean():,.0f}")
col3.metric("Max Harian", f"{df['cnt'].max():,.0f}")

st.markdown("---")

# =====================
# STYLE
# =====================
sns.set_theme(style="whitegrid")

# =====================
# 1. CUACA
# =====================
st.subheader("🌦 Pengaruh Cuaca terhadap Penyewaan")

weather_avg = df.groupby('weathersit')['cnt'].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=weather_avg.index, y=weather_avg.values, ax=ax)

ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

st.info("Cuaca cerah menghasilkan jumlah penyewaan tertinggi dibanding kondisi cuaca lainnya.")

# =====================
# 2. WORKING DAY
# =====================
st.subheader("🏢 Working Day vs Weekend")

workingday_avg = df.groupby('workingday')['cnt'].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(6,4))
sns.barplot(x=workingday_avg.index, y=workingday_avg.values, ax=ax)

ax.set_xlabel("Jenis Hari")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

st.info("Penyewaan lebih tinggi pada hari kerja karena digunakan sebagai transportasi harian.")

# =====================
# 3. TREND BULANAN
# =====================
st.subheader("📈 Tren Bulanan Penyewaan")

monthly = df.groupby(df['dteday'].dt.month)['cnt'].mean()

fig, ax = plt.subplots(figsize=(9,4))
sns.lineplot(x=monthly.index, y=monthly.values, marker="o", ax=ax)

ax.set_xticks(range(1,13))
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan")
plt.ylim(0) 
st.pyplot(fig)

st.info("Terdapat pola musiman: meningkat di pertengahan tahun (summer–fall).")
# =====================
# 4. Season
# =====================
season_avg = df.groupby('season')['cnt'].mean().sort_values(ascending=False)

fig, ax = plt.subplots()

sns.barplot(x=season_avg.index, y=season_avg.values, ax=ax)

ax.set_title('Rata-rata Penyewaan Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Penyewaan')

st.pyplot(fig)

# =====================
# 5. CLUSTERING MANUAL
# =====================
st.subheader("📦 Clustering Tingkat Permintaan")

low = df['cnt'].quantile(0.33)
high = df['cnt'].quantile(0.66)

def cluster(x):
    if x <= low:
        return "Low"
    elif x <= high:
        return "Medium"
    else:
        return "High"

df['cluster'] = df['cnt'].apply(cluster)

fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(x=df['cluster'], order=['Low','Medium','High'], ax=ax)

ax.set_xlabel("Kategori Demand")
ax.set_ylabel("Jumlah Hari")

st.pyplot(fig)

st.info("Distribusi demand relatif seimbang dengan sedikit dominasi high demand.")

# =====================
# INSIGHT FINAL
# =====================
st.markdown("---")
st.subheader("💡 Key Insights")

st.success("""
- Cuaca cerah menghasilkan demand tertinggi, menunjukkan bahwa layanan sangat bergantung pada kondisi cuaca yang nyaman untuk bersepeda.
- Demand yang lebih tinggi pada working day mengindikasikan bahwa bike sharing lebih banyak digunakan sebagai transportasi harian dibanding aktivitas rekreasi.
- Musim panas dan gugur menjadi periode puncak penyewaan, sehingga perlu peningkatan kapasitas operasional pada periode tersebut.
- Distribusi demand yang relatif seimbang menunjukkan bahwa layanan memiliki permintaan yang stabil sepanjang tahun.
""")

# =====================
# FOOTER
# =====================
st.markdown("---")
st.caption("Bike Sharing Analysis Dashboard | Built with Streamlit")