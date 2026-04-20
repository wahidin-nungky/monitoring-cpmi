import streamlit as st
import pandas as pd
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CPMI Management System v3.0",
    page_icon="💎",
    layout="wide"
)

# --- CUSTOM CSS UNTUK UI ELEGAN ---
st.markdown("""
    <style>
    /* Mengubah font dan background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #f8f9fa;
    }

    /* Styling Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 600;
        color: #64748b;
    }

    /* Footer Style */
    .footer-text {
        position: fixed;
        bottom: 20px;
        left: 20px;
        font-size: 12px;
        color: #94a3b8;
        font-style: italic;
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE ---
DB_FILE = "data_cpmi_v2.csv"
try:
    df = pd.read_csv(DB_FILE)
    if 'Sponsor' not in df.columns:
        df['Sponsor'] = "-"
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        'Nama CPMI', 'Tanggal Daftar', 'PT Penempatan', 'Agency Luar Negeri', 
        'Negara Tujuan', 'ID SISKO', 'Paspor', 'Ujian Kompetensi', 
        'Psikotest', 'MCU Full', 'Kontrak Kerja', 'Visa Kerja', 'Status Terbang', 'Sponsor'
    ])

# --- SISTEM LOGIN ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("### 🔐 Secure Access")
        pwd = st.text_input("Password Staf", type="password")
        if st.button("Log In", use_container_width=True):
            if pwd == "admin123":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Password tidak sesuai.")
    st.stop()

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.markdown("## 💎 CPMI System")
    st.markdown("`Versi 3.0 Professional` ")
    st.divider()
    
    menu = st.radio("MAIN MENU", ["📊 Real-time Dashboard", "➕ Registrasi Baru"])
    
    st.divider()
    if st.button("🔓 Keluar"):
        st.session_state["password_correct"] = False
        st.rerun()
    
    # --- CREDIT DI SIDEBAR ---
    st.markdown("<br><br>" * 5, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Created by: Wahidin**")
    st.markdown("*powered by GEMINI*")

# --- MENU: TAMBAH DATA ---
if menu == "➕ Registrasi Baru":
    st.markdown("### ➕ Input Data CPMI")
    with st.container():
        with st.form("form_baru", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nama = st.text_input("Nama Lengkap")
                tgl = st.date_input("Tanggal Daftar", datetime.now())
                pt = st.text_input("PT Penempatan")
                sponsor = st.text_input("Sponsor / PL")
            with col2:
                agency = st.text_input("Agency Luar Negeri")
                negara = st.selectbox("Negara Tujuan", ["Taiwan", "Hong Kong", "Singapura", "Malaysia", "Polandia", "Jepang", "Korea Selatan"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("Daftarkan Sekarang", use_container_width=True):
                new_data = {
                    'Nama CPMI': nama, 'Tanggal Daftar': tgl, 'PT Penempatan': pt,
                    'Agency Luar Negeri': agency, 'Negara Tujuan': negara,
                    'ID SISKO': '⏳ Belum', 'Paspor': '⏳ Belum', 'Ujian Kompetensi': '⏳ Belum',
                    'Psikotest': '⏳ Belum', 'MCU Full': '⏳ Belum', 'Kontrak Kerja': '⏳ Belum',
                    'Visa Kerja': '⏳ Belum', 'Status Terbang': 'Proses', 'Sponsor': sponsor
                }
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.balloons()
                st.success(f"Berhasil: {nama} telah terdaftar.")

# --- MENU: DASHBOARD ---
elif menu == "📊 Real-time Dashboard":
    st.markdown("### 📊 Monitoring Progres")
    
    # Header Statistics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Terdaftar", len(df))
    m2.metric("Proses MCU", len(df[df['MCU Full'] == '⏳ Belum']))
    m3.metric("Kontrak Signed", len(df[df['Kontrak Kerja'] == '✅ Signed']))
    m4.metric("Siap Terbang", len(df[df['Status Terbang'] == 'Ready']))

    st.markdown("---")

    # Search bar & Filter
    search_col1, search_col2 = st.columns([2, 1])
    with search_col1:
        search = st.text_input("🔍 Filter Data", placeholder="Cari berdasarkan nama, PT, atau sponsor...")
    
    if search:
        display_df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    else:
        display_df = df

    # Data Editor Modern
    st.write("#### 📑 Progress Tracking")
    edited_df = st.data_editor(
        display_df,
        column_config={
            "ID SISKO": st.column_config.SelectboxColumn("SISKO", options=["⏳ Belum", "✅ Selesai"]),
            "Paspor": st.column_config.SelectboxColumn("Paspor", options=["⏳ Belum", "✅ Selesai"]),
            "Ujian Kompetensi": st.column_config.SelectboxColumn("Ujian", options=["⏳ Belum", "✅ Lulus"]),
            "Psikotest": st.column_config.SelectboxColumn("Psikotest", options=["⏳ Belum", "✅ Rekom", "❌ No Rekom"]),
            "MCU Full": st.column_config.SelectboxColumn("MCU", options=["⏳ Belum", "✅ Fit", "❌ Unfit"]),
            "Kontrak Kerja": st.column_config.SelectboxColumn("Kontrak", options=["⏳ Belum", "✅ Signed"]),
            "Visa Kerja": st.column_config.SelectboxColumn("Visa", options=["⏳ Belum", "✅ Terbit"]),
            "Status Terbang": st.column_config.SelectboxColumn("Status", options=["Proses", "Ready", "✈️ Terbang"]),
            "Sponsor": st.column_config.TextColumn("Sponsor", help="Nama Petugas Lapangan"),
        },
        use_container_width=True,
        num_rows="dynamic",
        disabled=["Tanggal Daftar"] # Tanggal daftar tidak bisa diedit sembarangan
    )

    # Simpan Button
    if st.button("💾 Sinkronisasi Data", use_container_width=True):
        df.update(edited_df)
        df.to_csv(DB_FILE, index=False)
        st.toast("Database updated successfully!", icon="🌐")
