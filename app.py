

```python
import streamlit as st
import pandas as pd
import csv
import io
import os

st.set_page_config(
    page_title="E-RIASEC SKOR",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gaya Premium CSS
st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        .stTabs [data-baseweb="tab-list"] {
            gap: 15px;
            background: rgba(241, 245, 249, 0.8);
            backdrop-filter: blur(8px);
            padding: 10px;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 700;
            color: #64748b;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #2563eb;
            background-color: rgba(219, 234, 254, 0.5);
            transform: translateY(-1px);
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
        }
        .riasec-card {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .riasec-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Data Maklumat RIASEC
riasec_details = {
    'R': {'name': 'Realistik', 'trait': 'Praktikal & Fizikal', 'desc': 'Gemar tugasan fizikal, menggunakan instrumen, membaiki alatan mekanikal atau mesin.', 'careers': ['Jurutera Mekanikal 🛠️', 'Mekanik Kenderaan 🚗', 'Ahli Pertanian Moden 🌱'], 'color': '#EF4444', 'bg_color': '#FEF2F2', 'border_color': '#FCA5A5'},
    'I': {'name': 'Investigatif', 'trait': 'Saintifik & Saintis', 'desc': 'Gemar tugasan berfikir, membuat penyelidikan, menganalisis masalah yang kompleks.', 'careers': ['Doktor Perubatan 🩺', 'Ahli Kimia/Farmasi 🧪', 'Penganalisis Data AI 📊'], 'color': '#3B82F6', 'bg_color': '#EFF6FF', 'border_color': '#93C5FD'},
    'A': {'name': 'Artistik', 'trait': 'Kreatif & Bebas', 'desc': 'Menghargai kebebasan berekspresi, kreatif, suka melukis, muzik, atau rekaan grafik.', 'careers': ['Pereka Grafik 🎨', 'Arkitek Bangunan 🏛️', 'Penulis Kreatif ✍️'], 'color': '#8B5CF6', 'bg_color': '#F5F3FF', 'border_color': '#C7D2FE'},
    'S': {'name': 'Sosial', 'trait': 'Membantu & Prihatin', 'desc': 'Prihatin kebajikan orang ramai, gemar mengajar, merawat, serta memberi kaunseling.', 'careers': ['Guru/Pensyarah 🎓', 'Kaunselor Ujian 🧠', 'Pengurus Sumber Manusia 👥'], 'color': '#10B981', 'bg_color': '#ECFDF5', 'border_color': '#6EE7B7'},
    'E': {'name': 'Enterprising', 'trait': 'Berdaya Usaha & Pemimpin', 'desc': 'Sifat kepimpinan kuat, berbakat memujuk, mengurus projek perniagaan, bercita-cita tinggi.', 'careers': ['Usahawan / CEO 💼', 'Pengurus Pemasaran 📈', 'Peguam ⚖️'], 'color': '#F59E0B', 'bg_color': '#FFFBEB', 'border_color': '#FCD34D'},
    'K': {'name': 'Konvensional', 'trait': 'Sistematik & Berstruktur', 'desc': 'Tersusun, mementingkan kekemasan, teratur dalam menguruskan data atau perakaunan.', 'careers': ['Akauntan 🧮', 'Pentadbir Data 📂', 'Pakar Logistik 📦'], 'color': '#06B6D4', 'bg_color': '#ECFEFF', 'border_color': '#67E8F9'}
}

class_badges = {
    "5 Sidiq": {"bg": "#E0F2FE", "txt": "#0369A1", "border": "#7DD3FC", "emoji": "🔵"},
    "5 Amanah": {"bg": "#D1FAE5", "txt": "#065F46", "border": "#6EE7B7", "emoji": "🟢"},
    "5 Tabligh": {"bg": "#FEF3C7", "txt": "#92400E", "border": "#FCD34D", "emoji": "🟡"}
}

# Pembaca Fail CSV Format SePKM Sebenar
def parse_psychometric_csv(file_path_or_buffer, class_name):
    students_list = []
    content = ""
    if isinstance(file_path_or_buffer, str):
        if not os.path.exists(file_path_or_buffer): return []
        with open(file_path_or_buffer, 'r', encoding='utf-8-sig', errors='ignore') as f:
            content = f.read()
    else:
        content = file_path_or_buffer.getvalue().decode('utf-8-sig', errors='ignore')

    lines = content.splitlines()
    start_parsing = False
    
    for line in lines:
        reader = csv.reader([line])
        row = next(reader, None)
        if not row: continue
        
        # Kesan permulaan data murid selepas nama kolum
        if len(row) > 1 and "Nama" in row[1] and "Jantina" in row:
            start_parsing = True
            continue
            
        if start_parsing and len(row) >= 10:
            try:
                # Memastikan baris tersebut mengandungi nombor bil yang sah (elak baca footer)
                if not row[0].strip().isdigit(): continue
                
                [cite_start]name = row[1].strip().upper() [cite: 1, 14]
                [cite_start]r_val = int(row[4].strip()) [cite: 1, 14]
                [cite_start]i_val = int(row[5].strip()) [cite: 1, 14]
                [cite_start]a_val = int(row[6].strip()) [cite: 1, 14]
                [cite_start]s_val = int(row[7].strip()) [cite: 1, 14]
                [cite_start]e_val = int(row[8].strip()) [cite: 1, 14]
                [cite_start]k_val = int(row[9].strip()) [cite: 1, 14]
                
                students_list.append({
                    "id": f"{class_name.lower().replace(' ', '_')}_{len(students_list)+1}",
                    "name": name,
                    "class": class_name,
                    "R": r_val, "I": i_val, "A": a_val, "S": s_val, "E": e_val, "K": k_val
                })
            except (ValueError, IndexError):
                continue
    return students_list

# Data Lalai Kelas 5 Sidiq
default_students = [
    { "id": "1", "name": "ANAS BIN HAIRUL AZHAR", "class": "5 Sidiq", "R": 15, "I": 19, "A": 16, "S": 15, "E": 22, "K": 14 },
    { "id": "2", "name": "ANIS FARHANA BINTI SAHIRUDDEN", "class": "5 Sidiq", "R": 14, "I": 25, "A": 12, "S": 23, "E": 19, "K": 24 },
    { "id": "3", "name": "ANIS NAJEYHAH BINTI SUHAIDI", "class": "5 Sidiq", "R": 18, "I": 20, "A": 18, "S": 21, "E": 16, "K": 13 },
    { "id": "4", "name": "AU'FA A'LIAH HAJAR BINTI AHMAD ZAKY", "class": "5 Sidiq", "R": 7, "I": 12, "A": 5, "S": 18, "E": 7, "K": 14 },
    { "id": "5", "name": "DANIAL FAIQ BIN JEFFRI", "class": "5 Sidiq", "R": 18, "I": 20, "A": 16, "S": 16, "E": 16, "K": 26 }
]

if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame(default_students)
    # Muat naik automatik dari GitHub sekiranya fail wujud
    for c_name, f_name in [("5 Amanah", "senarai-murid-psikometrik-AMANAH-INVENTORI-MINAT-KERJAYA-TINGKATAN-5-2026.csv"), 
                            ("5 Tabligh", "senarai-murid-psikometrik-TABLIGH-INVENTORI-MINAT-KERJAYA-TINGKATAN-5-2026.csv")]:
        if os.path.exists(f_name):
            loaded = parse_psychometric_csv(f_name, c_name)
            if loaded:
                st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame(loaded)], ignore_index=True)

def get_riasec_code(row):
    scores = {'R': row['R'], 'I': row['I'], 'A': row['A'], 'S': row['S'], 'E': row['E'], 'K': row['K']}
    return "".join([item[0] for item in sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:3]])

df = st.session_state.students_db.copy()
df['Kod'] = df.apply(get_riasec_code, axis=1)

# Header Utama Aplikasi
st.markdown("""
    <div style="background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 40%, #8b5cf6 100%); padding: 30px; border-radius: 24px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(59, 130, 246, 0.25);">
        <h1 style="color: white; margin: 0; font-family: system-ui, sans-serif; font-size: 2.5em; font-weight: 800;">🎯 EXPLORASI E-RIASEC SKOR</h1>
        <p style="color: #bfdbfe; margin-top: 8px; font-size: 1.1em; font-weight: 400;">Pusat Visualisasi Psikometrik & Padanan Kerjaya Pintar</p>
    </div>
""", unsafe_allow_html=True)

tab_carian, tab_statistik, tab_urus = st.tabs(["🔍 Carian & Eksplorasi Kerjaya", "📊 Dashboard Analisis Kelas", "🔒 Kawalan Pentadbir & CSV"])

# ==================== TAB 1: CARIAN INDIVIDU ====================
with tab_carian:
    st.markdown("<h3 style='color: #1e3a8a; margin-bottom:15px;'>Imbasan Profil Kerjaya Individu</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: 
        selected_class = st.selectbox("📁 Tapis Mengikut Kelas", ["5 Sidiq", "5 Amanah", "5 Tabligh"])
    class_df = df[df['class'] == selected_class].sort_values(by="name")
    with col2:
        selected_student_name = st.selectbox("👤 Pilih Nama Murid", class_df['name'].tolist() if not class_df.empty else ["-- Tiada Data Murid --"])
            
    if selected_student_name and selected_student_name != "-- Tiada Data Murid --":
        student_data = class_df[class_df['name'] == selected_student_name].iloc[0]
        code = student_data['Kod']
        badge = class_badges.get(selected_class, {"bg": "#E2E8F0", "txt": "#475569", "border": "#CBD5E1", "emoji": "📁"})
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 20px; color: white; margin-bottom: 25px;">
                <span style="background-color: {badge['bg']}; border: 1px solid {badge['border']}; color: {badge['txt']}; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; font-weight: bold;">
                    {badge['emoji']} {student_data['class']}
                </span>
                <h2 style="margin: 10px 0 5px 0; color: white;">{student_data['name']}</h2>
                <p style="color: #94a3b8; margin-bottom: 15px;">Tiga Kod Mata Holland Utama Anda:</p>
                <div style="display: inline-flex; gap: 10px;">
                    {"".join([f'<span style="background:{riasec_details[c]["color"]}; color:white; font-size:1.8em; font-weight:bold; padding: 5px 20px; border-radius:12px;">{c}</span>' for c in code])}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: #1e3a8a;'>💡 Huraian Tret Personaliti & Pilihan Kerjaya:</h4>", unsafe_allow_html=True)
        cols_cards = st.columns(3)
        for idx, char in enumerate(code):
            detail = riasec_details[char]
            with cols_cards[idx]:
                st.markdown(f"""
                    <div class="riasec-card" style="background-color: {detail['bg_color']}; border: 2px solid {detail['border_color']}; padding: 20px; border-radius: 16px; height:100%;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                            <span style="background-color: {detail['color']}; color: white; width: 35px; height: 35px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2em;">{char}</span>
                            <div>
                                <h4 style="margin: 0; color: #1e293b; font-weight: bold;">{detail['name']}</h4>
                                <small style="color: {detail['color']}; font-weight: bold;">{detail['trait']}</small>
                            </div>
                        </div>
                        <p style="font-size: 0.9em; color: #475569; line-height: 1.5;">{detail['desc']}</p>
                        <hr style="border: 0; border-top: 1px dashed {detail['border_color']}; margin: 10px 0;">
                        <span style="font-size: 0.75em; color: #64748b; font-weight: bold; display: block;">CADANGAN KERJAYA:</span>
                        {"".join([f'<span style="display:inline-block; background:white; border:1px solid #e2e8f0; padding:2px 8px; margin:2px; border-radius:15px; font-size:0.85em; color:#1e3a8a;">{job}</span>' for job in detail['careers']])}
                    </div>
                """, unsafe_allow_html=True)

# ==================== TAB 2: ANALISIS KELAS ====================
with tab_statistik:
    st.markdown("<h3 style='color: #1e3a8a;'>Analisis & Taburan Statistik Kelas</h3>", unsafe_allow_html=True)
    selected_analysis_class = st.selectbox("📂 Pilih Kelas Untuk Analisis Statistik", ["5 Sidiq", "5 Amanah", "5 Tabligh"], key="stats_class")
    analysis_df = df[df['class'] == selected_analysis_class]
    
    if analysis_df.empty:
        st.warning("⚠️ Tiada data tersedia untuk kelas ini. Sila masuk ke Tab Pentadbir untuk memuat naik fail CSV SePKM.")
    else:
        total_students = len(analysis_df)
        analysis_df['Dominan'] = analysis_df['Kod'].str[0]
        freq = analysis_df['Dominan'].value_counts().reindex(['R', 'I', 'A', 'S', 'E', 'K'], fill_value=0)
        top_trait = freq.idxmax()
        
        c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
        with c_kpi1: st.metric("Jumlah Murid Ujian", f"{total_students} Orang", "Aktif")
        with c_kpi2: st.metric("Tret Tertinggi Kelas", f"{riasec_details[top_trait]['name']} ({top_trait})", f"{freq[top_trait]} Murid")
        with c_kpi3: st.metric("Kadar Pengisian", "100%", "Selesai")
            
        st.write("---")
        col_chart, col_leaderboard = st.columns([3, 2])
        with col_chart:
            st.write("📊 **Carta Kekerapan Kecenderungan Utama Murid (Huruf Pertama)**")
            chart_data = pd.DataFrame({'Kategori': [f"{riasec_details[k]['name']} ({k})" for k in freq.index], 'Bilangan Murid': freq.values})
            st.bar_chart(data=chart_data, x='Kategori', y='Bilangan Murid', color='#2563eb')
            
        with col_leaderboard:
            st.write("🏆 **Kedudukan Kepentingan Tret Kelas**")
            for idx, (char, count) in enumerate(freq.sort_values(ascending=False).items()):
                pct = (count / total_students) * 100 if total_students > 0 else 0
                st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; background:white; padding:10px; margin-bottom:6px; border-radius:10px; border-left:5px solid {riasec_details[char]['color']}; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                        <span style="font-weight:bold;">{idx+1}. {riasec_details[char]['name']} ({char})</span>
                        <span style="color:{riasec_details[char]['color']}; font-weight:bold;">{count} Murid ({pct:.0f}%)</span>
                    </div>
                """, unsafe_allow_html=True)

# ==================== TAB 3: ADMIN & PASSWORD KAWALAN ====================
with tab_urus:
    st.markdown("<h3 style='color: #1e3a8a;'>Pintu Kawalan Pentadbir & Pengurusan Data</h3>", unsafe_allow_html=True)
    
    if 'logged_in' not in st.session_state: 
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        with st.form("login_form"):
            password_input = st.text_input("🔑 Masukkan Kata Laluan Pentadbir:", type="password")
            submitted_login = st.form_submit_button("Log Masuk")
            if submitted_login:
                if password_input == "cikgu123":
                    st.session_state.logged_in = True
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Kata laluan salah! Sila hubungi urus setia.")
    else:
        st.success("🔓 Akses Dibenarkan. Anda kini boleh menguruskan pangkalan data.")
        if st.button("🔴 Log Keluar Mod Admin"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        st.markdown("#### 📥 Muat Naik Fail CSV Sistem SePKM Sekolah")
        
        cu1, cu2 = st.columns(2)
        with cu1:
            st.markdown("<div style='background:#f0fdf4; padding:15px; border-radius:12px; border:1px solid #bbf7d0;'><strong>🟢 Fail Data 5 Amanah</strong></div>", unsafe_allow_html=True)
            f_amanah = st.file_uploader("Pilih fail CSV Kelas Amanah", type=['csv'], key="f_am")
            if f_amanah:
                res = parse_psychometric_csv(f_amanah, "5 Amanah")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "5 Amanah"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Data 5 Amanah Berjaya Dimuatkan! 🎉")
                    st.rerun()
                else:
                    st.error("Format data SePKM tidak ditemui atau fail kosong.")
                    
        with cu2:
            st.markdown("<div style='background:#fffbeb; padding:15px; border-radius:12px; border:1px solid #fcd34d;'><strong>🟡 Fail Data 5 Tabligh</strong></div>", unsafe_allow_html=True)
            f_tabligh = st.file_uploader("Pilih fail CSV Kelas Tabligh", type=['csv'], key="f_tb")
            if f_tabligh:
                res = parse_psychometric_csv(f_tabligh, "5 Tabligh")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "5 Tabligh"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Data 5 Tabligh Berjaya Dimuatkan! 🎉")
                    st.rerun()
                else:
                    st.error("Format data SePKM tidak ditemui atau fail kosong.")

        st.write("---")
        st.markdown("#### ➕ Daftar / Edit Murid Secara Manual")
        with st.form("manual_form"):
            m_name = st.text_input("Nama Penuh Murid:").upper()
            m_class = st.selectbox("Kelas Murid:", ["5 Sidiq", "5 Amanah", "5 Tabligh"])
            c_r, c_i, c_a, c_s, c_e, c_k = st.columns(6)
            with c_r: r_s = st.number_input("Skor R", 0, 30, 0)
            with c_i: i_s = st.number_input("Skor I", 0, 30, 0)
            with c_a: a_s = st.number_input("Skor A", 0, 30, 0)
            with c_s: s_s = st.number_input("Skor S", 0, 30, 0)
            with c_e: e_s = st.number_input("Skor E", 0, 30, 0)
            with c_k: k_s = st.number_input("Skor K", 0, 30, 0)
            
            submitted_manual = st.form_submit_button("💾 Simpan Rekod Murid")
            if submitted_manual and m_name:
                new_student = {
                    "id": f"manual_{len(st.session_state.students_db)+1}", "name": m_name, "class": m_class,
                    "R": r_s, "I": i_s, "A": a_s, "S": s_s, "E": e_s, "K": k_s
                }
                st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame([new_student])], ignore_index=True)
                st.success(f"Berjaya menambah data murid {m_name}!")
                st.rerun()

        st.write("---")
        st.markdown("#### 📑 Pangkalan Data Semasa Murid")
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Muat Turun Keseluruhan Data Analisis (CSV)",
            data=csv_buffer.getvalue(),
            file_name="analisis_keseluruhan_riasec_2026.csv",
            mime="text/csv"
        )
        st.dataframe(df[['name', 'class', 'R', 'I', 'A', 'S', 'E', 'K', 'Kod']], use_container_width=True, hide_index=True)
