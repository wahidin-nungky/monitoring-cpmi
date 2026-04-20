import streamlit as st
import pandas as pd
from datetime import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Monitoring CPMI Online", layout="wide")

# --- SISTEM LOGIN SEDERHANA ---
def check_password():
    def password_guessed():
        if st.session_state["password"] == "admin123": # Ganti password di sini
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Masukkan Password Akses Staf", type="password", on_change=password_guessed, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password Salah, Coba Lagi", type="password", on_change=password_guessed, key="password")
        st.error("😕 Akses ditolak")
        return False
    else:
        return True

if check_password():
    # --- DATABASE (Simulasi Google Sheets dengan CSV) ---
    # Catatan: Untuk online permanen, kita akan hubungkan ke Google Sheets API
    DB_FILE = "data_cpmi_online.csv"
    
    try:
        df = pd.read_csv(DB_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            'Nama CPMI', 'Tanggal Daftar', 'PT Penempatan', 'Agency', 
            'ID SISKO', 'Paspor', 'Ujian Kompetensi', 'Status Terbang'
        ])

    st.title("🚀 Dashboard Monitoring CPMI Online")
    st.markdown("Sistem pemantauan alur proses CPMI secara real-time.")

    # --- BAGIAN INPUT DATA (Hanya untuk Staf) ---
    with st.expander("➕ Tambah Data CPMI Baru"):
        with st.form("input_form"):
            col1, col2 = st.columns(2)
            with col1:
                nama = st.text_input("Nama Lengkap CPMI")
                tgl = st.date_input("Tanggal Pendaftaran")
                pt = st.text_input("Nama PT Penempatan")
            with col2:
                agency = st.text_input("Nama Agency Luar Negeri")
                tujuan = st.text_input("Negara Tujuan")
            
            if st.form_submit_button("Daftarkan CPMI"):
                new_row = {
                    'Nama CPMI': nama, 'Tanggal Daftar': tgl, 'PT Penempatan': pt, 
                    'Agency': agency, 'ID SISKO': 'Belum', 'Paspor': 'Belum', 
                    'Ujian Kompetensi': 'Belum', 'Status Terbang': 'Proses'
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success(f"Data {nama} Berhasil Disimpan!")
                st.rerun()

    # --- TAMPILAN MONITORING ---
    st.write("### 📊 Data Progres CPMI")
    
    # Filter Pencarian
    search = st.text_input("Cari Nama CPMI atau PT:")
    if search:
        display_df = df[df['Nama CPMI'].str.contains(search, case=False) | df['PT Penempatan'].str.contains(search, case=False)]
    else:
        display_df = df

    # Tabel Interaktif (Bisa diedit langsung untuk update status)
    st.info("💡 Klik pada sel tabel untuk mengubah status, lalu klik tombol simpan di bawah.")
    edited_df = st.data_editor(display_df, num_rows="dynamic", use_container_width=True)

    if st.button("💾 Simpan Perubahan Status"):
        if search:
            # Update data asli berdasarkan perubahan di hasil pencarian
            df.update(edited_df)
        else:
            df = edited_df
        df.to_csv(DB_FILE, index=False)
        st.success("Database berhasil diperbarui secara online!")