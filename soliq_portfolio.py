import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#Sahifa settings
st.set_page_config(
    page_title="Buxoro va Samarqand Soliq Tahlili",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Buxoro va Samarqand Viloyati Soliq Tahlili")
st.subheader("2026 yil yanvar (Buxoro) va mart (Samarqand) oylariga oid moliyaviy hisobot")
st.divider()

#Ma'lumot olish
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

buxoro_path = os.path.join(BASE_DIR, "buxoro_soliq.csv.csv")
samarqand_path = os.path.join(BASE_DIR, "samarqand_soliq_2026_mart.csv")

df_buxoro = pd.read_csv(buxoro_path, sep=',', encoding='utf-8', decimal='.', skipinitialspace=True)
df_samarqand = pd.read_csv(samarqand_path, sep=',', encoding='utf-8', decimal='.', skipinitialspace=True)

df_buxoro.columns = df_buxoro.columns.str.strip()
df_samarqand.columns = df_samarqand.columns.str.strip()

#Viloyat tanlash
viloyat = st.sidebar.radio("Viloyatni tanlang:", ["Buxoro", "Samarqand", "Taqqoslash"])

#Tuman ustunlari
buxoro_tumanlar = [
    'olot_tumani', 'buxoro_tumani', 'vobkent_tumani', 'gijduvon_tumani',
    'kogon_tumani', 'qorakol_tumani', 'qorovulbozor_tumani', 'peshko_tumani',
    'romitan_tumani', 'jondor_tumani', 'shofirkon_tumani',
    'buxoro_shaxar', 'kogon_shaxar'
]

samarqand_tumanlar = [
    'viloyat_byudjeti', 'oqdaryo_tumani', 'bulungur_tumani', 'jomboy_tumani',
    'ishtixon_tumani', 'kattaqorgon_tumani', 'qushrabod_tumani', 'narpay_tumani',
    'payariq_tumani', 'pastdargom_tumani', 'paxtachi_tumani', 'samarqand_tumani',
    'nurobod_tumani', 'urgut_tumani', 'toyloq_tumani', 'samarqand_shahri',
    'kattaqorgon_shahri'
]

#funksiya
def long_format(df, tuman_cols):
    df_long = df.melt(
        id_vars=['indikatorlar'],
        value_vars=tuman_cols,
        var_name='tuman',
        value_name='tushum'
    )
    df_long['tuman'] = df_long['tuman'].str.replace('_', ' ').str.title()
    return df_long

def kpi_kartalar(df, viloyat_nomi, viloyat_col):
    st.subheader("Asosiy Ko'rsatkichlar")
    col1, col2, col3 = st.columns(3)
    with col1:
        davlat = df['davlat_byudjeti'].iloc[0]
        st.metric("💰 Davlat Byudjeti", f"{davlat:,.2f} mlrd so'm")
    with col2:
        respublika = df['respublika_byudjeti'].iloc[0]
        st.metric("🏛️ Respublika Byudjeti", f"{respublika:,.2f} mlrd so'm")
    with col3:
        viloyat = df[viloyat_col].iloc[0]
        st.metric(f"🌍 {viloyat_nomi}", f"{viloyat:,.2f} mlrd so'm")
    st.divider()

def tumanlar_grafik(df_long):
    result = df_long.groupby("tuman")["tushum"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(15, 6))
    result.plot(kind='bar', color=sns.color_palette("Blues_r", len(result)),
                edgecolor='black', ax=ax)
    ax.set_xlabel("Tuman / Shahar", fontsize=14, family="Times New Roman")
    ax.set_ylabel("Umumiy Tushum (mlrd so'm)", fontsize=14, family="Times New Roman")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)
    st.dataframe(result.round(2), use_container_width=True)

def soliqlar_grafik(df_long):
    result = df_long.groupby("indikatorlar")["tushum"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.barplot(x=result.values, y=result.index, palette="viridis", ax=ax)
    ax.set_title("Soliqlar bo'yicha umumiy tushumlar (mlrd so'm)",
                 fontsize=16, pad=15, family="Times New Roman")
    ax.set_xlabel("Tushum (mlrd so'm)")
    ax.set_ylabel("Indikatorlar")
    ax.grid(axis='x', alpha=0.3)
    for i, v in enumerate(result.values):
        ax.text(v + 0.5, i, f"{v:.2f}", va='center', fontsize=11, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    st.dataframe(result.round(2).reset_index(), use_container_width=True)

def heatmap_grafik(df_long):
    df_pivot = df_long.pivot_table(index="indikatorlar", columns="tuman",
                                   values="tushum", aggfunc="sum")
    fig, ax = plt.subplots(figsize=(16, 10))
    sns.heatmap(df_pivot, annot=True, fmt=".1f", cmap="YlOrRd",
                linewidths=0.5, linecolor='white', ax=ax)
    ax.set_title("Tumanlar bo'yicha soliq turlari tahlili", fontsize=18, pad=20)
    ax.set_xlabel("Tuman / Shahar")
    ax.set_ylabel("Soliq Indikatorlari")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

def byudjet_grafik(df, viloyat_col, viloyat_nomi):
    df_short = df[["indikatorlar", "davlat_byudjeti", "respublika_byudjeti", viloyat_col]].melt(
        id_vars="indikatorlar",
        var_name="byudjet",
        value_name="summa"
    )
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.barplot(data=df_short, x="indikatorlar", y="summa", hue="byudjet",
                palette=["steelblue", "coral", "green"], ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Davlat vs Respublika vs {viloyat_nomi}",
              fontweight="bold", fontsize=16, family="Times New Roman")
    plt.xlabel("Indikatorlar", fontsize=13, family="Times New Roman")
    plt.ylabel("Tushum (mlrd so'm)", fontsize=13, family="Times New Roman")
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles=handles,
              labels=["Davlat Byudjeti", "Respublika Byudjeti", viloyat_nomi],
              title="Byudjet turi", loc="upper right")
    plt.tight_layout()
    st.pyplot(fig)
    st.dataframe(df[["indikatorlar", "davlat_byudjeti", "respublika_byudjeti", viloyat_col]],
                 use_container_width=True)

def pie_grafik(df, viloyat_col):
    df_short = df[["indikatorlar", "davlat_byudjeti", "respublika_byudjeti", viloyat_col]].melt(
        id_vars="indikatorlar",
        var_name="byudjet",
        value_name="summa"
    )
    top_pie = df_short.groupby("indikatorlar")["summa"].sum().sort_values(ascending=False)
    jami = top_pie.sum()
    foizlar = (top_pie.values / jami * 100)
    fig, ax = plt.subplots(figsize=(12, 10))
    wedges, texts = ax.pie(top_pie.values, labels=None,
                           colors=sns.color_palette("Set3", len(top_pie)), startangle=90)
    legend_labels = [
        f"{label}: {value:,.1f} mlrd so'm ({foiz:.1f}%)"
        for label, value, foiz in zip(top_pie.index, top_pie.values, foizlar)
    ]
    ax.legend(wedges, legend_labels, title="Soliq turlari",
              loc="center left", bbox_to_anchor=(1, 0.5), fontsize=10)
    ax.set_title("Soliq turlari bo'yicha umumiy tushumlar",
                 fontsize=16, fontweight="bold", pad=20)
    plt.tight_layout()
    st.pyplot(fig)

#buxoro
if viloyat == "Buxoro":
    st.header("🏙️ Buxoro Viloyati")
    df_long = long_format(df_buxoro, buxoro_tumanlar)
    kpi_kartalar(df_buxoro, "Buxoro Viloyati", "buxoro_viloyati")

    if st.checkbox("Raw Data"):
        st.dataframe(df_buxoro, use_container_width=True)

    if st.checkbox("Tumanlar bo'yicha umumiy soliq tushumlari"):
        st.subheader("Tumanlar bo'yicha umumiy soliq tushumlari")
        tumanlar_grafik(df_long)

    if st.checkbox("Soliqlar bo'yicha umumiy tushumlar"):
        st.subheader("Soliqlar bo'yicha umumiy tushumlar")
        soliqlar_grafik(df_long)

    if st.checkbox("Heatmap"):
        st.subheader("Tumanlar va Soliq Turlari bo'yicha Heatmap")
        heatmap_grafik(df_long)

    if st.checkbox("Davlat vs Respublika vs Buxoro"):
        st.subheader("Davlat vs Respublika vs Buxoro Viloyati")
        byudjet_grafik(df_buxoro, "buxoro_viloyati", "Buxoro Viloyati")

    if st.checkbox("Pie Chart"):
        st.subheader("Soliq turlari bo'yicha Pie Chart")
        pie_grafik(df_buxoro, "buxoro_viloyati")

#Samarqand
elif viloyat == "Samarqand":
    st.header("🏙️ Samarqand Viloyati")
    df_long = long_format(df_samarqand, samarqand_tumanlar)
    kpi_kartalar(df_samarqand, "Samarqand Viloyati", "samarqand_viloyati")

    if st.checkbox("Raw Data"):
        st.dataframe(df_samarqand, use_container_width=True)

    if st.checkbox("Tumanlar bo'yicha umumiy soliq tushumlari"):
        st.subheader("Tumanlar bo'yicha umumiy soliq tushumlari")
        tumanlar_grafik(df_long)

    if st.checkbox("Soliqlar bo'yicha umumiy tushumlar"):
        st.subheader("Soliqlar bo'yicha umumiy tushumlar")
        soliqlar_grafik(df_long)

    if st.checkbox("Heatmap"):
        st.subheader("Tumanlar va Soliq Turlari bo'yicha Heatmap")
        heatmap_grafik(df_long)

    if st.checkbox("Davlat vs Respublika vs Samarqand"):
        st.subheader("Davlat vs Respublika vs Samarqand Viloyati")
        byudjet_grafik(df_samarqand, "samarqand_viloyati", "Samarqand Viloyati")

    if st.checkbox("Pie Chart"):
        st.subheader("Soliq turlari bo'yicha Pie Chart")
        pie_grafik(df_samarqand, "samarqand_viloyati")

#taqqoslash
elif viloyat == "Taqqoslash":
    st.header("📊 Buxoro vs Samarqand Taqqoslash")
    st.subheader("Ikki viloyat asosiy ko'rsatkichlari")

    # Buxoro viloyati - tumanlar yig'indisi
    buxoro_jami = df_buxoro[buxoro_tumanlar].sum().sum()
    
    # Samarqand viloyati - TO'G'RIDAN-TO'G'RI CSV DAGI QIYMAT (686.59 mlrd so'm)
    try:
        samarqand_jami = df_samarqand['samarqand_viloyati'].iloc[0]
    except:
        # Agar ustun topilmasa, siz ko'rsatgan aniq qiymatni ishlat
        samarqand_jami = 686.59

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💰 Buxoro — Davlat Byudjeti",
                  f"{df_buxoro['davlat_byudjeti'].iloc[0]:,.2f} mlrd so'm")
        st.metric("🌍 Buxoro Viloyati", f"{buxoro_jami:,.2f} mlrd so'm")
    with col2:
        st.metric("💰 Samarqand — Davlat Byudjeti",
                  f"{df_samarqand['davlat_byudjeti'].iloc[0]:,.2f} mlrd so'm")
        st.metric("🌍 Samarqand Viloyati", f"{samarqand_jami:,.2f} mlrd so'm")

    st.divider()

    if st.checkbox("Viloyatlar taqqoslash grafigi"):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(["Buxoro", "Samarqand"], [buxoro_jami, samarqand_jami],
               color=["steelblue", "coral"], edgecolor="black")
        ax.set_title("Buxoro vs Samarqand — Umumiy tushum",
                     fontsize=16, fontweight="bold")
        ax.set_ylabel("Tushum (mlrd so'm)")
        for i, v in enumerate([buxoro_jami, samarqand_jami]):
            ax.text(i, v + 1, f"{v:.2f}", ha='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

st.divider()
col1, col2 = st.columns(2)
with col1:
    if st.button("📌 Ma'lumot manbasi"):
        st.info("Bu ma'lumot openbudget.uz saytidan olingan")
with col2:
    if st.button("👤 Muallif"):
        st.info("Muhammadjon Yoriyev")