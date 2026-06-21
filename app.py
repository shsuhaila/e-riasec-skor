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

# Premium Color & Interactivity Injector
st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        
        /* Glassmorphic Tabs */
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
        
        /* Ultra Smooth Hover Cards */
        .riasec-card {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .riasec-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Comprehensive RIASEC Database for Interactive Engine
riasec_details = {
    'R': {'name': 'Realistik', 'trait': 'Praktikal & Fizikal', 'desc': 'Gemar tugasan fizikal, menggunakan instrumen, membaiki alatan mekanikal atau mesin. Suka kerja praktikal di luar pejabat.', 'careers': ['Jurutera Mekanikal 🛠️', 'Mekanik Kenderaan 🚗', 'Ahli Pertanian Moden 🌱', 'Juruteknik Penerbangan ✈️', 'Arkitek Landskap 🏡'], 'color': '#EF4444', 'bg_color': '#FEF2F2', 'border_color': '#FCA5A5'},
    'I': {'name': 'Investigatif', 'trait': 'Saintifik & Saintis', 'desc': 'Gemar tugasan berfikir, membuat penyelidikan, menganalisis masalah yang kompleks, meminati sains dan perubatan.', 'careers': ['Doktor Perubatan 🩺', 'Ahli Kimia/Farmasi 🧪', 'Penganalisis Data AI 📊', 'Penyelidik Saintifik 🔬', 'Pakar Forensik 🕵️'], 'color': '#3B82F6', 'bg_color': '#EFF6FF', 'border_color': '#93C5FD'},
    'A': {'name': 'Artistik', 'trait': 'Kreatif & Bebas', 'desc': 'Menghargai kebebasan berekspresi, kreatif, suka melukis, muzik, penulisan kreatif, drama, atau rekaan grafik.', 'careers': ['Pereka Grafik/UIUX 🎨', 'Arkitek Bangunan 🏛️', 'Penulis Kreatif/Novel ✍️', 'Pengarah Filem/Pemuzik 🎬', 'Pereka Fesyen 👗'], 'color': '#8B5CF6', 'bg_color': '#F5F3FF', 'border_color': '#C7D2FE'},
    'S': {'name': 'Sosial', 'trait': 'Membantu & Prihatin', 'desc': 'Prihatin kebajikan orang ramai, gemar mengajar, merawat, memberi kaunseling serta selesa berinteraksi dalam kumpulan.', 'careers': ['Guru/Pensyarah 🎓', 'Kaunselor / Pakar Psikologi 🧠', 'Pengurus Sumber Manusia 👥', 'Jururawat/Pegawai Perubatan 🏥', 'Pekerja Kebajikan Komuniti 🤝'], 'color': '#10B981', 'bg_color': '#ECFDF5', 'border_color': '#6EE7B7'},
    'E': {'name': 'Enterprising', 'trait': 'Berdaya Usaha & Pemimpin', 'desc': 'Sifat kepimpinan kuat, berbakat memujuk, mengurus projek perniagaan, bercita-cita tinggi, mahir berucap di khalayak.', 'careers': ['Usahawan / CEO Syarikat 💼', 'Pengurus Pemasaran/Jualan 📈', 'Peguam / Pengamal Undang-undang ⚖️', 'Perunding Pelaburan 💰', 'Ahli Politik / Pemimpin Organisasi 🏛️'], 'color': '#F59E0B', 'bg_color': '#FFFBEB', 'border_color': '#FCD34D'},
    'K': {'name': 'Konvensional', 'trait': 'Sistematik & Berstruktur', 'desc': 'Tersusun, mementingkan kekemasan, teratur dalam menguruskan data, rekod, tugasan perkeranian atau perakaunan.', 'careers': ['Akauntan / Auditor 🧮', 'Pentadbir Data & Fail 📂', 'Setiausaha Korporat 👔', 'Penganalisis Kewangan Bank 🏦', 'Pakar Logistik 📦'], 'color': '#06B6D4', 'bg_color': '#ECFEFF', 'border_color': '#67E8F9'}
}

class_badges = {
    "5 Sidiq": {"bg": "#E0F2FE", "txt": "#0369A1", "border": "#7DD3FC", "emoji": "🔵"},
    "5 Amanah": {"bg": "#D1FAE5", "txt": "#065F46", "border": "#6EE7B7", "emoji": "🟢"},
    "5 Tabligh": {"bg": "#FEF3C7", "txt": "#92400E", "border": "#FCD34D", "emoji": "🟡"}
}

def parse_psychometric_csv(file_path_or_buffer, class_name):
    students_list = []
    content = ""
    if isinstance(file_path_or_buffer, str):
        if not os.path.exists(file_path_or_buffer): return []
        try:
            with open(file_path_or_buffer, 'r', encoding='utf-8-sig', errors='ignore') as f: content = f.read()
        except Exception: return []
    else:
        try: content = file_path_or_buffer.getvalue().decode('utf-8-sig', errors='ignore')
        except Exception: return []

    lines = content.splitlines()
    for line in lines:
        reader = csv.reader([line])
        row = next(reader, None)
        if not row or len(row) < 5: continue
        scores = {}
        for item in row:
            item_strip = item.strip()
            if '|' in item_strip:
                parts = item_strip.split('|')
                if len(parts) == 2 and parts[0].strip().upper() in ['R', 'I', 'A', 'S', 'E', 'K']:
                    try: scores[parts[0].strip().upper()] = int(parts[1].strip())
                    except ValueError: pass
        if len(scores) >= 6:
            name = row[1].strip().upper() if len(row) > 1 and not row[1].strip().isdigit() and len(row[1].strip()) > 3 else None
            if not name:
                for val in row:
                    val_clean = val.strip().upper()
                    if val_clean and len(val_clean) > 3 and not any(c.isdigit() for c in val_clean) and '|' not in val_clean:
                        name = val_clean
                        break
            if name:
                students_list.append({"id": f"{class_name.lower().replace(' ', '_')}_{len(students_list)+1}", "name": name, "class": class_name, "R": scores.get('R', 0), "I": scores.get('I', 0), "A": scores.get('A', 0), "S": scores.get('S', 0), "E": scores.get('E', 0), "K": scores.get('K', 0)})
    return students_list

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
    { "id": "10", "name": "MUHAMMAD ATIFF ZAYYAN BIN MOHAMAD FIRDAUS", "class": "5 Sidiq", "R": 21, "I": 21, "A": 18, "S": 22, "E": 18, "K": 12 }
]

if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame(default_students)
    for c_name, f_name in [("5 Amanah", "senarai-murid-psikometrik-AMANAH-INVENTORI-MINAT-KERJAYA-TINGKATAN-5-2026.csv"), ("5 Tabligh", "senarai-murid-psikometrik-TABLIGH-INVENTORI-MINAT-KERJAYA-TINGKATAN-5-2026.csv")]:
        loaded = parse_psychometric_csv(f_name, c_name)
        if loaded: st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame(loaded)], ignore_index=True)

def get_riasec_code(row):
    scores = {'R': row['R'], 'I': row['I'], 'A': row['A'], 'S': row['S'], 'E': row['E'], 'K': row['K']}
    return "".join([item[0] for item in sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:3]])

df = st.session_state.students_db.copy()
df['Kod'] = df.apply(get_riasec_code, axis=1)

# Gorgeous Colorful Main Header
st.markdown("""
    <div style="background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 40%, #8b5cf6 100%); padding: 35px; border-radius: 24px; text-align: center; margin-bottom: 30px; box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.3);">
        <h1 style="color: white; margin: 0; font-family: system-ui, sans-serif; font-size: 3em; font-weight: 800; letter-spacing: -1px;">🎯 EXPLORASI E-RIASEC SKOR</h1>
        <p style="color: #bfdbfe; margin-top: 12px; font-size: 1.25em; font-weight: 400;">Pusat Visualisasi Psikometrik & Padanan Kerjaya Interaktif Pintar</p>
    </div>
""", unsafe_allow_html=True)

tab_carian, tab_statistik, tab_urus = st.tabs(["🔍 Carian & Eksplorasi Kerjaya", "📊 Dashboard Analisis Kelas", "🔒 Kawalan Pentadbir & CSV"])

# ==================== TAB 1: CARIAN & INTERACTIVE MATCHING ====================
with tab_carian:
    st.markdown("<h3 style='color: #1e3a8a; margin-bottom:15px;'>Imbasan Profil Kerjaya Individu</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: selected_class = st.selectbox("📁 Tapis Mengikut Kelas", ["5 Sidiq", "5 Amanah", "5 Tabligh"])
    class_df = df[df['class'] == selected_class].sort_values(by="name")
    with col2:
        selected_student_name = st.selectbox("👤 Pilih Nama Murid", class_df['name'].tolist() if not class_df.empty else ["-- Tiada Murid --"])
            
    if selected_student_name and selected_student_name != "-- Tiada Murid --":
        student_data = class_df[class_df['name'] == selected_student_name].iloc[0]
        code = student_data['Kod']
        badge = class_badges.get(selected_class, {"bg": "#E2E8F0", "txt": "#475569", "border": "#CBD5E1", "emoji": "📁"})
        
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 30px; border-radius: 24px; color: white; margin-bottom: 30px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.15);">
                <span style="background-color: {badge['bg']}; border: 1px solid {badge['border']}; color: {badge['txt']}; padding: 6px 16px; border-radius: 30px; font-size: 0.85em; font-weight: bold;">
                    {badge['emoji']} {student_data['class']}
                </span>
                <h2 style="margin: 15px 0 5px 0; color: white; font-size: 2.2em;">{student_data['name']}</h2>
                <p style="color: #94a3b8; margin-bottom: 20px;">Tiga Kod Mata Holland Utama Anda:</p>
                <div style="display: inline-flex; gap: 10px;">
                    {"".join([f'<span style="background:{riasec_details[c]["color"]}; color:white; font-size:2em; font-weight:bold; padding: 10px 25px; border-radius:15px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">{c}</span>' for c in code])}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h4 style='color: #1e3a8a;'>💡 Huraian Personaliti & Bidang Kerjaya Sesuai:</h4>", unsafe_allow_html=True)
        cols_cards = st.columns(3)
        for idx, char in enumerate(code):
            detail = riasec_details[char]
            with cols_cards[idx]:
                st.markdown(f"""
                    <div class="riasec-card" style="background-color: {detail['bg_color']}; border: 2px solid {detail['border_color']}; padding: 25px; border-radius: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03); height:100%;">
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
                            <span style="background-color: {detail['color']}; color: white; width: 45px; height: 45px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.5em;">{char}</span>
                            <div>
                                <h4 style="margin: 0; color: #1e293b; font-size: 1.25em; font-weight: bold;">{detail['name']}</h4>
                                <small style="color: {detail['color']}; font-weight: bold; text-transform: uppercase; font-size: 0.75em;">{detail['trait']}</small>
                            </div>
                        </div>
                        <p style="font-size: 0.9em; color: #475569; line-height: 1.6; margin-bottom: 15px;">{detail['desc']}</p>
                        <hr style="border: 0; border-top: 1px dashed {detail['border_color']}; margin: 15px 0;">
                        <span style="font-size: 0.75em; color: #64748b; font-weight: bold; display: block; margin-bottom: 6px;">PILIHAN KERJAYA:</span>
                        {"".join([f'<span style="display:inline-block; background:white; border:1px solid #e2e8f0; padding:4px 10px; margin:3px; border-radius:20px; font-size:0.85em; color:#1e3a8a; font-weight:500;">{job}</span>' for job in detail['careers']])}
                    </div>
                """, unsafe_allow_html=True)
        
        # Dynamic Interactive Matcher Sandbox
        st.write("---")
        with st.expander("🔮 MAKMAL INTERAKTIF: Bina Kombinasi Kerjaya Pilihan Anda Sendiri!"):
            st.write("Cuba klik dan tukar susunan abjad di bawah untuk melihat cadangan kerjaya tersuai secara langsung:")
            sandbox_chars = st.multiselect("Pilih 3 Tret Minat Anda:", ['R', 'I', 'A', 'S', 'E', 'K'], default=list(code)[:3], max_selections=3)
            if len(sandbox_chars) == 3:
                st.info(f"✨ **Kombinasi Terpilih:** {' -> '.join([riasec_details[x]['name'] for x in sandbox_chars])}")
                s_cols = st.columns(3)
                for i, c in enumerate(sandbox_chars):
                    with s_cols[i]:
                        st.markdown(f"**Dominan ke-{i+1}: {riasec_details[c]['name']}**")
                        for j in riasec_details[c]['careers'][:3]: st.write(f"- {j}")

# ==================== TAB 2: ANALISIS STATISTIK DINAMIK ====================
with tab_statistik:
    st.markdown("<h3 style='color: #1e3a8a;'>Analisis & Taburan Statistik Kelas</h3>", unsafe_allow_html=True)
    selected_analysis_class = st.selectbox("📂 Pilih Kelas Untuk Analisis Statistik", ["5 Sidiq", "5 Amanah", "5 Tabligh"], key="stats_class")
    analysis_df = df[df['class'] == selected_analysis_class]
    
    if analysis_df.empty:
        st.warning("⚠️ Tiada data tersedia untuk kelas ini. Sila muat naik CSV di bahagian pentadbir.")
    else:
        # Dynamic Live Analytics Cards (KPI Metrics)
        total_students = len(analysis_df)
        analysis_df['Dominan'] = analysis_df['Kod'].str[0]
        freq = analysis_df['Dominan'].value_counts().reindex(['R', 'I', 'A', 'S', 'E', 'K'], fill_value=0)
        top_trait = freq.idxmax()
        
        c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
        with c_kpi1:
            st.metric("Jumlah Murid Aktif", f"{total_students} Orang", "Sistem Automatik")
        with c_kpi2:
            st.metric("Tret Tertinggi Kelas", f"{riasec_details[top_trait]['name']} ({top_trait})", f"{freq[top_trait]} Murid Dominan")
        with c_kpi3:
            st.metric("Kadar Penyertaan Ujian", "100%", "Lengkap")
            
        st.write("---")
        col_chart, col_leaderboard = st.columns([3, 2])
        with col_chart:
            st.write("📊 **Carta Kekerapan Kecenderungan Utama Murid (Huruf Pertama)**")
            chart_data = pd.DataFrame({'Kategori': [f"{riasec_details[k]['name']} ({k})" for k in freq.index], 'Bilangan Murid': freq.values})
            st.bar_chart(data=chart_data, x='Kategori', y='Bilangan Murid', color='#2563eb')
            
        with col_leaderboard:
            st.write("🏆 **Kedudukan Kepentingan Tret Kelas**")
            for idx, (char, count) in enumerate(freq.sort_values(ascending=False).items()):
                pct = (count / total_students) * 100
                st.markdown(f"""
                    <div style="display:flex; justify-content:space-between; background:white; padding:10px 15px; margin-bottom:8px; border-radius:12px; border-left:5px solid {riasec_details[char]['color']}; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                        <span style="font-weight:bold;">{idx+1}. {riasec_details[char]['name']} ({char})</span>
                        <span style="color:{riasec_details[char]['color']}; font-weight:bold;">{count} Murid ({pct:.0f}%)</span>
                    </div>
                """, unsafe_allow_html=True)

# ==================== TAB 3: ADMIN, CSV & PASSWORD LOCK ====================
with tab_urus:
    st.markdown("<h3 style='color: #1e3a8a;'>Pintu Kawalan Pentadbir & Pengurusan Data</h3>", unsafe_allow_html=True)
    
    if 'logged_in' not in st.session_state: st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        with st.form("login_form"):
            password_input = st.text_input("🔑 Masukkan Kata Laluan Pentadbir:", type="password")
            if st.form_submit_button("Log Masuk"):
                if password_input == "ellan711":
                    st.session_state.logged_in = True
                    st.balloons()  # Confetti effect!
                    st.rerun()
                else:
                    st.error("Kata laluan salah! Sila cuba lagi.")
    else:
        st.success("🔓 Anda berada dalam mod pentadbir. Anda boleh menambah atau memuat naik fail data.")
        if st.button("🔴 Log Keluar Mod Admin"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        # CSV Upload Section
        cu1, cu2 = st.columns(2)
        with cu1:
            st.markdown("<div style='background:#f0fdf4; padding:20px; border-radius:15px; border:1px solid #bbf7d0;'><strong>🟢 Muat Naik 5 Amanah</strong></div>", unsafe_allow_html=True)
            f_amanah = st.file_uploader("Fail CSV 5 Amanah", type=['csv'], key="f_am")
            if f_amanah:
                res = parse_psychometric_csv(f_amanah, "5 Amanah")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "5 Amanah"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Berjaya Mengemas kini Data 5 Amanah! 🪅")
                    st.rerun()
        with cu2:
            st.markdown("<div style='background:#fffbeb; padding:20px; border-radius:15px; border:1px solid #fef3c7;'><strong>🟡 Muat Naik 5 Tabligh</strong></div>", unsafe_allow_html=True)
            f_tabligh = st.file_uploader("Fail CSV 5 Tabligh", type=['csv'], key="f_tb")
            if f_tabligh:
                res = parse_psychometric_csv(f_tabligh, "5 Tabligh")
                if res:
                    st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "5 Tabligh"], pd.DataFrame(res)], ignore_index=True)
                    st.toast("Berjaya Mengemas kini Data 5 Tabligh! 🪅")
                    st.rerun()

        st.write("---")
        # Interactive Live Data Table Viewer & Exporter
        st.markdown("#### 📑 Pangkalan Data Semasa Murid")
        
        # CSV Download Button (Interactive Export Engine)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Eksport & Muat Turun Semua Data (CSV)",
            data=csv_buffer.getvalue(),
            file_name="analisis_keseluruhan_riasec_2026.csv",
            mime="text/csv"
        )
        
        st.dataframe(df[['name', 'class', 'R', 'I', 'A', 'S', 'E', 'K', 'Kod']], use_container_width=True, hide_index=True)
