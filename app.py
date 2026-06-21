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
    "5 Tabligh": {"bg": "#FEF3C7", "txt": "#92400E", "border": "#FCD34D", "emoji": "🟡"},
    "1 Amanah": {"bg": "#F3E8FF", "txt": "#6B21A8", "border": "#D8B4FE", "emoji": "🟣"},
    "1 Fatonah": {"bg": "#FFE4E6", "txt": "#9F1239", "border": "#FECDD3", "emoji": "🔴"},
    "1 Tabligh": {"bg": "#FEF3C7", "txt": "#92400E", "border": "#FCD34D", "emoji": "🟡"},
    "1 Sidiq": {"bg": "#E0F2FE", "txt": "#0369A1", "border": "#7DD3FC", "emoji": "🔵"}
}

# Pembaca Fail CSV Format SePKM Dinamik
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
        if not row or len(row) < 5: continue
        
        # Cari permulaan jadual
        row_clean = [col.strip().upper() for col in row]
        if "NAMA" in row_clean and "BIL" in row_clean:
            start_parsing = True
            continue
            
        if start_parsing and len(row) >= 10:
            try:
                # Elakkan baris jumlah atau footer kosong
                if not row[0].strip().isdigit(): continue
                
                name = row[1].strip().upper()
                r_val = int(row[4].strip())
                i_val = int(row[5].strip())
                a_val = int(row[6].strip())
                s_val = int(row[7].strip())
                e_val = int(row[8].strip())
                k_val = int(row[9].strip())
                
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
    { "id": "5", "name": "DANIAL FAIQ BIN JEFFRI", "class": "5 Sidiq", "R": 18, "I": 20, "A": 16, "S": 16, "E": 16, "K": 26 },
    { "id": "6", "name": "KHAISAR AQMAR BIN MOHD KHAIRUL", "class": "5 Sidiq", "R": 15, "I": 22, "A": 12, "S": 20, "E": 20, "K": 18 },
    { "id": "7", "name": "MUHAMMAD AL-KAUTHAR BIN HAMZAH", "class": "5 Sidiq", "R": 18, "I": 21, "A": 14, "S": 22, "E": 19, "K": 18 },
    { "id": "8", "name": "MUHAMMAD ALI ALIMI BIN AZMAN", "class": "5 Sidiq", "R": 18, "I": 18, "A": 10, "S": 17, "E": 15, "K": 14 },
    { "id": "9", "name": "MUHAMMAD AMEERUL UMAIR BIN KAMARUNSAMAN", "class": "5 Sidiq", "R": 15, "I": 20, "A": 8, "S": 23, "E": 21, "K": 17 },
    { "id": "10", "name": "MUHAMMAD ATIFF ZAYYAN BIN MOHAMAD FIRDAUS", "class": "5 Sidiq", "R": 21, "I": 21, "A": 18, "S": 22, "E": 18, "K": 12 },
    { "id": "11", "name": "MUHAMMAD DANIAL FIRDAUS BIN NORHISHAM", "class": "5 Sidiq", "R": 9, "I": 10, "A": 8, "S": 20, "E": 13, "K": 12 },
    { "id": "12", "name": "MUHAMMAD IZZ DANIEL BIN MOHD AFIZI", "class": "5 Sidiq", "R": 21, "I": 22, "A": 15, "S": 25, "E": 20, "K": 27 },
    { "id": "13", "name": "MUHAMMAD ZHARIEF IRFAN BIN ZAMRI", "class": "5 Sidiq", "R": 11, "I": 13, "A": 1, "S": 13, "E": 12, "K": 17 },
    { "id": "14", "name": "NUR AFIFAH SYAURAH BINTI NORNIKMAT", "class": "5 Sidiq", "R": 27, "I": 25, "A": 10, "S": 28, "E": 25, "K": 23 },
    { "id": "15", "name": "NUR DAHIYAH ADANI BINTI AZLLAN", "class": "5 Sidiq", "R": 20, "I": 23, "A": 11, "S": 26, "E": 15, "K": 20 },
    { "id": "16", "name": "NUR DAMIA QISTINA BINTI MOHAMAD HAFIZ", "class": "5 Sidiq", "R": 9, "I": 17, "A": 12, "S": 18, "E": 9, "K": 14 },
    { "id": "17", "name": "NUR SAKINAH JANNAH BINTI MOHD NOOR", "class": "5 Sidiq", "R": 17, "I": 25, "A": 12, "S": 14, "E": 9, "K": 20 },
    { "id": "18", "name": "NUR YUMNEE BINTI MOHD FAIZAL", "class": "5 Sidiq", "R": 19, "I": 25, "A": 12, "S": 22, "E": 11, "K": 16 },
    { "id": "19", "name": "NUR ZAHRA ALYA BINTI AZHARUDDIN", "class": "5 Sidiq", "R": 12, "I": 22, "A": 8, "S": 12, "E": 4, "K": 13 },
    { "id": "20", "name": "NURUL IMAN KAMILA BINTI MOHD ARIFFIN", "class": "5 Sidiq", "R": 21, "I": 26, "A": 29, "S": 29, "E": 26, "K": 18 },
    { "id": "21", "name": "SITI NUR AMANINA BINTI MARZUKE", "class": "5 Sidiq", "R": 15, "I": 19, "A": 24, "S": 26, "E": 27, "K": 16 },
    { "id": "22", "name": "SITI NUR NAZIHA BINTI MUSA", "class": "5 Sidiq", "R": 21, "I": 23, "A": 25, "S": 18, "E": 22, "K": 17 }
]

if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame(default_students)
    
    # Fail Pemetaan (Meneroka semua fail CSV dalam folder kerja secara dinamik)
    csv_mappings = [
        ("5 Amanah", "senarai-murid-psikometrik-AMANAH-INVENTORI-MINAT-KERJAYA-TINGKATAN-5-2026.csv"),
        ("5 Tabligh", "senarai-murid-psikometrik-TABLIGH-INVENTORI-MINAT-KERJAYA-TINGKATAN-5-2026.csv"),
        ("1 Amanah", "senarai-murid-psikometrik-AMANAH-INVENTORI-MINAT-KERJAYA-TINGKATAN-1-2026.csv"),
        ("1 Fatonah", "senarai-murid-psikometrik-FATONAH-INVENTORI-MINAT-KERJAYA-TINGKATAN-1-2026.csv"),
        ("1 Tabligh", "senarai-murid-psikometrik-TABLIGH-INVENTORI-MINAT-KERJAYA-TINGKATAN-1-2026.csv"),
        ("1 Sidiq", "senarai-murid-psikometrik-SIDIQ-INVENTORI-MINAT-KERJAYA-TINGKATAN-1-2026.csv")
    ]
    
    for c_name, f_name in csv_mappings:
        if os.path.exists(f_name):
            loaded = parse_psychometric_csv(f_name, c_name)
            if loaded:
                # Padam rekod lama yang sepadan dengan kelas ini sebelum timpa data baharu
                st.session_state.students_db = st.session_state.students_db[st.session_state.students_db['class'] != c_name]
                st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame(loaded)], ignore_index=True)

def get_riasec_code(row):
    scores = {'R': row['R'], 'I': row['I'], 'A': row['A'], 'S': row['S'], 'E': row['E'], 'K': row['K']}
    return "".join([item[0] for item in sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:3]])

df = st.session_state.students_db.copy()
df['Kod'] = df.apply(get_riasec_code, axis=1)

# Header Utama
st.markdown("""
    <div style="background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 40%, #8b5cf6 100%); padding: 30px; border-radius: 24px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(59, 130, 246, 0.25);">
        <h1 style="color: white; margin: 0; font-family: system-ui, sans-serif; font-size: 2.5em; font-weight: 800;">🎯 EXPLORASI E-RIASEC SKOR</h1>
        <p style="color: #bfdbfe; margin-top: 8px; font-size: 1.1em; font-weight: 400;">Pusat Visualisasi Psikometrik & Padanan Kerjaya Pintar Sekolah</p>
    </div>
""", unsafe_allow_html=True)

tab_carian, tab_statistik, tab_urus = st.tabs(["🔍 Carian & Eksplorasi Kerjaya", "📊 Dashboard Analisis Kelas", "🔒 Kawalan Pentadbir & CSV"])

# ==================== TAB 1: CARIAN INDIVIDU ====================
with tab_carian:
    st.markdown("<h3 style='color: #1e3a8a; margin-bottom:15px;'>Imbasan Profil Kerjaya Individu</h3>", unsafe_allow_html=True)
    
    col_t, col_k, col_m = st.columns(3)
    with col_t:
        selected_form = st.selectbox("🎓 Pilih Tingkatan", ["Tingkatan 5", "Tingkatan 1"])
        
    with col_k:
        if selected_form == "Tingkatan 5":
            available_classes = ["5 Sidiq", "5 Amanah", "5 Tabligh"]
        else:
            available_classes = ["1 Amanah", "1 Fatonah", "1 Tabligh", "1 Sidiq"]
        selected_class = st.selectbox("📁 Pilih Kelas", available_classes)
        
    class_df = df[df['class'] == selected_class].sort_values(by="name")
    
    with col_m:
        selected_student_name = st.selectbox("👤 Pilih Nama Murid", class_df['name'].tolist() if not class_df.empty else ["-- Tiada Data Murid --"])
            
    if selected_student_name and selected_student_name != "-- Tiada Data Murid --":
        student_data = class_df[class_df['name'] == selected_student_name].iloc[0]
        code = student_data['Kod']
        badge = class_badges.get(selected_class, {"bg": "#E2E8F0", "txt": "#475569", "border": "#CBD5E1", "emoji": "📁"})
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 25px; border-radius: 20px; color: white; margin-bottom: 25px;">
                <span style="background-color: {badge['bg']}; border: 1px solid {badge['border']}; color: {badge['txt']}; padding: 4px 12px; border-radius: 20px; font-size: 0.85em; font-weight: bold;">
                    {badge['emoji']} {student_data['class']} ({selected_form})
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
    
    col_st1, col_st2 = st.columns(2)
    with col_st1:
        sel_form_stats = st.selectbox("🎓 Pilih Tingkatan Analisis", ["Tingkatan 5", "Tingkatan 1"], key="t_stats")
    with col_st2:
        if sel_form_stats == "Tingkatan 5":
            available_classes_stats = ["5 Sidiq", "5 Amanah", "5 Tabligh"]
        else:
            available_classes_stats = ["1 Amanah", "1 Fatonah", "1 Tabligh", "1 Sidiq"]
        selected_analysis_class = st.selectbox("📂 Pilih Kelas Analisis", available_classes_stats, key="stats_class")
        
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
                if password_input == "ellan711":
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
        st.markdown("#### 📥 Muat Naik Fail CSV Sistem SePKM Sekolah (Tingkatan 1 & 5)")
        
        up1, up2 = st.columns(2)
        with up1:
            st.markdown("<div style='background:#f3e8ff; padding:15px; border-radius:12px; border:1px solid #d8b4fe;'><strong>🟣 Fail Data 1 Amanah</strong></div>", unsafe_allow_html=True)
            f_am1 = st.file_uploader("Pilih fail CSV Kelas 1 Amanah", type=['csv'], key="f_am1")
            if f_am1:
                res = parse_psychometric_csv(f_am1, "1 Amanah")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "1 Amanah"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Data 1 Amanah Berjaya Dimuatkan! 🎉")
                    st.rerun()
                else: st.error("Format data SePKM tidak ditemui atau fail kosong.")
                
            st.markdown("<div style='background:#ffe4e6; padding:15px; border-radius:12px; border:1px solid #fecdd3; margin-top:15px;'><strong>🔴 Fail Data 1 Fatonah</strong></div>", unsafe_allow_html=True)
            f_fat1 = st.file_uploader("Pilih fail CSV Kelas 1 Fatonah", type=['csv'], key="f_fat1")
            if f_fat1:
                res = parse_psychometric_csv(f_fat1, "1 Fatonah")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "1 Fatonah"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Data 1 Fatonah Berjaya Dimuatkan! 🎉")
                    st.rerun()
                else: st.error("Format data SePKM tidak ditemui atau fail kosong.")

            st.markdown("<div style='background:#fffbeb; padding:15px; border-radius:12px; border:1px solid #fcd34d; margin-top:15px;'><strong>🟡 Fail Data 1 Tabligh</strong></div>", unsafe_allow_html=True)
            f_tb1 = st.file_uploader("Pilih fail CSV Kelas 1 Tabligh", type=['csv'], key="f_tb1")
            if f_tb1:
                res = parse_psychometric_csv(f_tb1, "1 Tabligh")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "1 Tabligh"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Data 1 Tabligh Berjaya Dimuatkan! 🎉")
                    st.rerun()
                else: st.error("Format data SePKM tidak ditemui atau fail kosong.")

            st.markdown("<div style='background:#e0f2fe; padding:15px; border-radius:12px; border:1px solid #7dd3fc; margin-top:15px;'><strong>🔵 Fail Data 1 Sidiq</strong></div>", unsafe_allow_html=True)
            f_sid1 = st.file_uploader("Pilih fail CSV Kelas 1 Sidiq", type=['csv'], key="f_sid1")
            if f_sid1:
                res = parse_psychometric_csv(f_sid1, "1 Sidiq")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "1 Sidiq"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Data 1 Sidiq Berjaya Dimuatkan! 🎉")
                    st.rerun()
                else: st.error("Format data SePKM tidak ditemui atau fail kosong.")

        with up2:
            st.markdown("<div style='background:#f0fdf4; padding:15px; border-radius:12px; border:1px solid #bbf7d0;'><strong>🟢 Fail Data 5 Amanah</strong></div>", unsafe_allow_html=True)
            f_am5 = st.file_uploader("Pilih fail CSV Kelas 5 Amanah", type=['csv'], key="f_am5")
            if f_am5:
                res = parse_psychometric_csv(f_am5, "5 Amanah")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "5 Amanah"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Data 5 Amanah Berjaya Dimuatkan! 🎉")
                    st.rerun()
                else: st.error("Format data SePKM tidak ditemui atau fail kosong.")
                
            st.markdown("<div style='background:#fffbeb; padding:15px; border-radius:12px; border:1px solid #fcd34d; margin-top:15px;'><strong>🟡 Fail Data 5 Tabligh</strong></div>", unsafe_allow_html=True)
            f_tb5 = st.file_uploader("Pilih fail CSV Kelas 5 Tabligh", type=['csv'], key="f_tb5")
            if f_tb5:
                res = parse_psychometric_csv(f_tb5, "5 Tabligh")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "5 Tabligh"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Data 5 Tabligh Berjaya Dimuatkan! 🎉")
                    st.rerun()
                else: st.error("Format data SePKM tidak ditemui atau fail kosong.")

        st.write("---")
        st.markdown("#### ➕ Daftar / Edit Murid Secara Manual")
        with st.form("manual_form"):
            m_name = st.text_input("Nama Penuh Murid:").upper()
            m_class = st.selectbox("Kelas Murid:", ["5 Sidiq", "5 Amanah", "5 Tabligh", "1 Amanah", "1 Fatonah", "1 Tabligh", "1 Sidiq"])
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
