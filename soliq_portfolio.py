import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ====================== SAHIFA SOZLAMALARI ======================
st.set_page_config(
    page_title="Buxoro Soliq Tahlili",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Buxoro Viloyati Soliq Tahlili")
st.subheader("2026 yil yanvar oyiga oid moliyaviy hisobot")
st.divider()

# ====================== MA'LUMOTNI O'QISH ======================
file_path = r'D:\Data_analitika_portfolio\buxoro_soliq.csv.csv'

df = pd.read_csv(file_path, 
                 sep=',', 
                 encoding='utf-8', 
                 decimal='.', 
                 skipinitialspace=True)

df.columns = df.columns.str.strip()

# ====================== LONG FORMAT ======================
tuman_columns = [
    'olot_tumani', 'buxoro_tumani', 'vobkent_tumani', 'gijduvon_tumani',
    'kogon_tumani', 'qorakol_tumani', 'qorovulbozor_tumani', 'peshko_tumani',
    'romitan_tumani', 'jondor_tumani', 'shofirkon_tumani',
    'buxoro_shaxar', 'kogon_shaxar'
]

df_long = df.melt(
    id_vars=['indikatorlar'],
    value_vars=tuman_columns,
    var_name='tuman',
    value_name='tushum'
)

df_long['tuman'] = df_long['tuman'].str.replace('_', ' ').str.title()


# ====================== KPI KARTALAR ======================
st.subheader("Asosiy Ko'rsatkichlar")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💰 Davlat Byudjeti", "27,269.86 mlrd so'm")
with col2:
    st.metric("🏛️ Respublika Byudjeti", "21,846.63 mlrd so'm")
with col3:
    st.metric("🌍 Buxoro Viloyati", "363.97 mlrd so'm")

st.divider()

if st.checkbox("Data"):
   st.subheader("📋 Raw Data ")
   st.dataframe(df, use_container_width=True)
   st.divider()

# ====================== CHECKBOXLAR ======================
show_tuman = st.checkbox("Tumanlar bo'yicha umumiy soliq tushumlari")
show_soliq = st.checkbox("Soliqlar bo'yicha umumiy tushumlari")
show_heatmap = st.checkbox("Tumanlar va Soliq Turlari bo'yicha Heatmap")
show_byudjet = st.checkbox("Davlat vs Respublika vs Buxoro Viloyati")
show_pie = st.checkbox(" Soliq turlari bo'yicha Pie Chart")

# ====================== 1. TUMANLAR GRAFIKI ======================
if show_tuman:
    st.subheader("Tumanlar bo'yicha umumiy soliq tushumlari")
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

# ====================== 2. SOLIQLAR GRAFIKI ======================
if show_soliq:
    st.subheader("Soliqlar bo'yicha umumiy tushumlar")
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

# ====================== 3. HEATMAP ======================
if show_heatmap:
    st.subheader("Tumanlar va Soliq Turlari bo'yicha Heatmap")
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

# ====================== 4. DAVLAT vs RESPUBLIKA vs BUXORO ======================
if show_byudjet:
    st.subheader("📊 Davlat Byudjeti vs Respublika Byudjeti vs Buxoro Viloyati")
    
    # Ma'lumotni long formatga o'tkazish
    df_short = df[["indikatorlar", "davlat_byudjeti", "respublika_byudjeti", "buxoro_viloyati"]].melt(
        id_vars="indikatorlar", 
        var_name="byudjet", 
        value_name="summa"
    )
    
    # Grafik yaratish
    fig, ax = plt.subplots(figsize=(14, 7))
    
    sns.barplot(
        data=df_short,
        x="indikatorlar",
        y="summa",
        hue="byudjet",
        palette=["steelblue", "coral", "green"],
        ax=ax
    )
    
    plt.xticks(rotation=45, ha="right")
    plt.title("Davlat vs Respublika vs Buxoro viloyati", 
              fontweight="bold", fontsize=16, family="Times New Roman")
    plt.xlabel("Indikatorlar", fontsize=13, family="Times New Roman")
    plt.ylabel("Tushum (mlrd so'm)", fontsize=13, family="Times New Roman")
    
    # Legendni to'g'rilash
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(
        handles=handles,
        labels=["Davlat Byudjeti", "Respublika Byudjeti", "Buxoro viloyati"],
        title="Byudjet turi",
        loc="upper right"
    )
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Jadvalni chiqarish (to'g'ri yozilishi)
    st.subheader("Davlat, Respublika va Buxoro Viloyati bo'yicha batafsil ma'lumot")
    st.dataframe(
        df[["indikatorlar", "davlat_byudjeti", "respublika_byudjeti", "buxoro_viloyati"]],
        use_container_width=True
    )

# ====================== 5. PIE CHART (Checkbox bilan) ======================
if show_pie:
    st.subheader("Soliq turlari bo'yicha umumiy tushumlar (Pie Chart)")
    
    df_short = df[["indikatorlar", "davlat_byudjeti", "respublika_byudjeti", "buxoro_viloyati"]].melt(
        id_vars="indikatorlar", 
        var_name="byudjet", 
        value_name="summa"
    )
    
    top_pie = df_short.groupby("indikatorlar")["summa"].sum().sort_values(ascending=False)
    
    jami = top_pie.sum()
    foizlar = (top_pie.values / jami * 100)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    wedges, texts = ax.pie(
        top_pie.values,
        labels=None,
        colors=sns.color_palette("Set3", len(top_pie)),
        startangle=90
    )
    
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

if st.button("Ma'lumot o'rnida"):
    st.text("Bu ma'lumot openbudget.uz saytidan olingan")
    
if st.button("By"):
    st.text("Muhammadjon Yoriyev")

