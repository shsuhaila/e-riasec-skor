import streamlit as st
import pandas as pd
import csv
import io
import os

st.set_page_config(
    page_title="E-Profil Psikometrik Pintar (IMK & ITP)",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        
        /* Glassmorphic Navigation and Selection */
        .stTabs [data-baseweb="tab-list"] {
            gap: 15px;
            background: rgba(241, 245, 249, 0.9);
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
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
        }
        
        /* Premium Hover Cards */
        .riasec-card, .itp-card {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .riasec-card:hover, .itp-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
        }
    </style>
""", unsafe_allow_html=True)

riasec_details = {
    'R': {'name': 'Realistik', 'trait': 'Praktikal & Fizikal', 'desc': 'Gemar tugasan fizikal, menggunakan instrumen, membaiki alatan mekanikal atau mesin.', 'careers': ['Jurutera Mekanikal 🛠️', 'Mekanik Kenderaan 🚗', 'Ahli Pertanian Moden 🌱'], 'color': '#EF4444', 'bg_color': '#FEF2F2', 'border_color': '#FCA5A5'},
    'I': {'name': 'Investigatif', 'trait': 'Saintifik & Saintis', 'desc': 'Gemar tugasan berfikir, membuat penyelidikan, menganalisis masalah yang kompleks.', 'careers': ['Doktor Perubatan 🩺', 'Ahli Kimia/Farmasi 🧪', 'Penganalisis Data AI 📊'], 'color': '#3B82F6', 'bg_color': '#EFF6FF', 'border_color': '#93C5FD'},
    'A': {'name': 'Artistik', 'trait': 'Kreatif & Bebas', 'desc': 'Menghargai kebebasan berekspresi, kreatif, suka melukis, muzik, atau rekaan grafik.', 'careers': ['Pereka Grafik 🎨', 'Arkitek Bangunan 🏛️', 'Penulis Kreatif ✍️'], 'color': '#8B5CF6', 'bg_color': '#F5F3FF', 'border_color': '#C7D2FE'},
    'S': {'name': 'Sosial', 'trait': 'Membantu & Prihatin', 'desc': 'Prihatin kebajikan orang ramai, gemar mengajar, merawat, serta memberi kaunseling.', 'careers': ['Guru/Pensyarah 🎓', 'Kaunselor Ujian 🧠', 'Pengurus Sumber Manusia 👥'], 'color': '#10B981', 'bg_color': '#ECFDF5', 'border_color': '#6EE7B7'},
    'E': {'name': 'Enterprising', 'trait': 'Berdaya Usaha & Pemimpin', 'desc': 'Sifat kepimpinan kuat, berbakat memujuk, mengurus projek perniagaan, bercita-cita tinggi.', 'careers': ['Usahawan / CEO 💼', 'Pengurus Pemasaran 📈', 'Peguam ⚖️'], 'color': '#F59E0B', 'bg_color': '#FFFBEB', 'border_color': '#FCD34D'},
    'K': {'name': 'Konvensional', 'trait': 'Sistematik & Berstruktur', 'desc': 'Tersusun, mementingkan kekemasan, teratur dalam menguruskan data atau perakaunan.', 'careers': ['Akauntan 🧮', 'Pentadbir Data 📂', 'Pakar Logistik 📦'], 'color': '#06B6D4', 'bg_color': '#ECFEFF', 'border_color': '#67E8F9'}
}

itp_details = {
    'Autonomi': {
        'name': 'Autonomi', 'icon': '🔓', 'color': '#EF4444', 'bg_color': '#FEF2F2', 'border_color': '#FCA5A5',
        'Tinggi': 'Suka kebebasan sepenuhnya dalam tindakan, sangat berdikari & yakin membuat keputusan sendiri.',
        'Sederhana': 'Sederhana dari segi keakuran, kebebasan, berdikari, dan pengurusan aktiviti harian.',
        'Rendah': 'Lebih suka menerima arahan orang lain, akur kepada peraturan, dan mempunyai kebergantungan tinggi.'
    },
    'Kreatif': {
        'name': 'Kreatif', 'icon': '🎨', 'color': '#F59E0B', 'bg_color': '#FFFBEB', 'border_color': '#FCD34D',
        'Tinggi': 'Daya imaginasi yang tinggi, banyak idea kreatif, suka mencipta karya asli & benci kerja rutin.',
        'Sederhana': 'Mempunyai ciri-ciri berfikir kreatif pada tahap sederhana.',
        'Rendah': 'Lebih selesa menggunakan idea sedia ada berbanding mencipta atau menghasilkan benda baharu.'
    },
    'Agresif': {
        'name': 'Agresif', 'icon': '⚡', 'color': '#F43F5E', 'bg_color': '#FFF1F2', 'border_color': '#FECDD3',
        'Tinggi': 'Terlalu tegas, suka mengkritik orang lain secara terbuka demi mencapai matlamat peribadi.',
        'Sederhana': 'Sifat asertif (tegas diri). Menuntut hak secara adil sambil tetap menjaga emosi orang lain.',
        'Rendah': 'Seorang yang pasif, membiarkan orang lain memanipulasi diri dan memendam perasaan.'
    },
    'Ekstrovert': {
        'name': 'Ekstrovert', 'icon': '🗣️', 'color': '#0EA5E9', 'bg_color': '#F0F9FF', 'border_color': '#BAE6FD',
        'Tinggi': 'Peramah, suka bersosial (outgoing), suka bekerja berkumpulan & yakin berucap di hadapan khalayak.',
        'Sederhana': 'Sederhana dalam pergaulan sosial, gembira bercampur tetapi memerlukan ruang bersendiri.',
        'Rendah': 'Introvert, pemalu, lebih suka menyendiri, kurang selesa berada di majlis yang bising/ramai orang.'
    },
    'Pencapaian': {
        'name': 'Pencapaian', 'icon': '🏆', 'color': '#EAB308', 'bg_color': '#FEFCE8', 'border_color': '#FEF08A',
        'Tinggi': 'Sangat bermotivasi, berdaya saing tinggi, dan mementingkan kecemerlangan dalam semua tugas.',
        'Sederhana': 'Mempunyai tahap motivasi dan keinginan untuk berjaya di paras pertengahan.',
        'Rendah': 'Kurang bersemangat untuk bersaing, cepat berpuas hati dan tidak meletakkan matlamat tinggi.'
    },
    'Kepelbagaian': {
        'name': 'Kepelbagaian', 'icon': '🔄', 'color': '#6366F1', 'bg_color': '#EEF2FF', 'border_color': '#C7D2FE',
        'Tinggi': 'Suka perubahan drastik, mencuba perkara baharu secara berterusan & benci tugasan yang berulang.',
        'Sederhana': 'Fleksibiliti sederhana, memerlukan sedikit masa sebelum menyesuaikan diri dengan perubahan baru.',
        'Rendah': 'Sangat suka situasi stabil, tenang & selamat. Lebih selesa melakukan rutin harian yang sama.'
    },
    'Intelektual': {
        'name': 'Intelektual', 'icon': '📖', 'color': '#A855F7', 'bg_color': '#FAF5FF', 'border_color': '#E9D5FF',
        'Tinggi': 'Suka aktiviti mencabar minda, suka membaca buku ilmiah, akademik, serta rasa ingin tahu yang luas.',
        'Sederhana': 'Mempunyai tarikan sederhana terhadap topik-topik ilmiah yang kompleks.',
        'Rendah': 'Lebih berminat kepada aktiviti praktikal berbanding perbincangan teori sains atau falsafah.'
    },
    'Kepimpinan': {
        'name': 'Kepimpinan', 'icon': '👑', 'color': '#8B5CF6', 'bg_color': '#F5F3FF', 'border_color': '#DDD6FE',
        'Tinggi': 'Ciri ketua yang berkaliber, tegas, bijak membuat keputusan, dan pandai mempengaruhi orang lain.',
        'Sederhana': 'Boleh memimpin tetapi biasanya hanya selesa menguruskan kumpulan kecil.',
        'Rendah': 'Lebih selesa menjadi pengikut setia berbanding mengambil tanggungjawab sebagai ketua.'
    },
    'Struktur': {
        'name': 'Struktur', 'icon': '📐', 'color': '#14B8A6', 'bg_color': '#F0FDFA', 'border_color': '#99F6E4',
        'Tinggi': 'Mementingkan kekemasan, ketelitian, suka peraturan rigid, berdisiplin & jadual kerja tersusun.',
        'Sederhana': 'Anjal dalam cara bekerja tetapi masih mengekalkan kekemasan dalam urusan penting.',
        'Rendah': 'Suka aktiviti bebas tanpa peraturan rigid, gaya kerja lebih santai dan tidak berstruktur.'
    },
    'Resilien': {
        'name': 'Resilien', 'icon': '🪵', 'color': '#10B981', 'bg_color': '#ECFDF5', 'border_color': '#A7F3D0',
        'Tinggi': 'Ketahanan psikologi tinggi (mental & emosi kental), berjiwa waja & gigih menyelesaikan masalah.',
        'Sederhana': 'Mempunyai ketahanan psikologi sederhana, kadang-kadang memerlukan dorongan moral.',
        'Rendah': 'Mudah rasa tertekan, sensitif terhadap kritikan & mudah menyerah kalah sebelum berjuang.'
    },
    'Menolong': {
        'name': 'Menolong', 'icon': '🤝', 'color': '#84CC16', 'bg_color': '#F7FEE7', 'border_color': '#D9F99D',
        'Tinggi': 'Sifat empati yang tinggi, sangat prihatin, peka dengan kesusahan orang & suka menolong sukarela.',
        'Sederhana': 'Tahap penglibatan dalam aktiviti kebajikan masyarakat berada di paras sederhana.',
        'Rendah': 'Lebih mementingkan kebajikan diri sendiri berbanding memikirkan kebajikan orang lain.'
    },
    'Analitikal': {
        'name': 'Analitikal', 'icon': '🔎', 'color': '#06B6D4', 'bg_color': '#ECFEFF', 'border_color': '#AED9E0',
        'Tinggi': 'Peka kepada persekitaran, suka membuat pemerhatian tajam & menganalisis perkara berdasarkan fakta.',
        'Sederhana': 'Tahap kepekaan menganalisis situasi berada pada tahap normal.',
        'Rendah': 'Lebih suka bertindak mengikut emosi atau gerak hati berbanding mengkaji data secara logik.'
    },
    'Kritik Diri': {
        'name': 'Kritik Diri', 'icon': '😟', 'color': '#64748B', 'bg_color': '#F8FAFC', 'border_color': '#E2E8F0',
        'Tinggi': 'Sering merasa rendah diri, bimbang, cemas, dan berasa bersalah secara berlebihan (Perlu sokongan GBK).',
        'Sederhana': 'Tahap muhasabah diri yang stabil, boleh mengenal pasti kelemahan diri secara positif.',
        'Rendah': 'Sangat yakin dengan kualiti diri, jarang bimbang atau meragui keputusan yang telah dibuat.'
    },
    'Wawasan': {
        'name': 'Wawasan', 'icon': '🎯', 'color': '#D946EF', 'bg_color': '#FDF4FF', 'border_color': '#F5D0FE',
        'Tinggi': 'Berpandangan jauh, mempunyai visi kejayaan yang jelas, bercita-cita besar, dan optimis.',
        'Sederhana': 'Mempunyai perancangan umum masa hadapan tetapi belum terperinci sepenuhnya.',
        'Rendah': 'Menjalani kehidupan mengikut keadaan semasa tanpa memikirkan matlamat jangka panjang.'
    },
    'Ketelusan': {
        'name': 'Ketelusan', 'icon': '💎', 'color': '#71717A', 'bg_color': '#FAFAFA', 'border_color': '#E4E4E7',
        'Tinggi': 'Sangat jujur, ikhlas, dan tulen dalam memberikan jawapan tentang personaliti diri sendiri.',
        'Sederhana': 'Tahap keikhlasan yang boleh diterima dalam menggambarkan identiti diri.',
        'Rendah': 'Mempunyai kecenderungan untuk memanipulasi jawapan bagi menggambarkan imej diri yang sempurna.'
    }
}

class_badges = {
    "5 Sidiq": {"bg": "#E0F2FE", "txt": "#0369A1", "border": "#7DD3FC", "emoji": "🔵"},
    "5 Amanah": {"bg": "#D1FAE5", "txt": "#065F46", "border": "#6EE7B7", "emoji": "🟢"},
    "5 Tabligh": {"bg": "#FEF3C7", "txt": "#92400E", "border": "#FCD34D", "emoji": "🟡"},
    "1 Amanah": {"bg": "#F3E8FF", "txt": "#6B21A8", "border": "#D8B4FE", "emoji": "🟣"},
    "1 Fatonah": {"bg": "#FFE4E6", "txt": "#9F1239", "border": "#FECDD3", "emoji": "🔴"},
    "1 Tabligh": {"bg": "#FEF3C7", "txt": "#92400E", "border": "#FCD34D", "emoji": "🟡"},
    "1 Sidiq": {"bg": "#E0F2FE", "txt": "#0369A1", "border": "#7DD3FC", "emoji": "🔵"},
    "2 Fatonah": {"bg": "#ECFDF5", "txt": "#047857", "border": "#6EE7B7", "emoji": "🟢"}
}

def parse_itp_csv(file_path_or_buffer, class_name):
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
    
    traits_keys = ['Autonomi', 'Kreatif', 'Agresif', 'Ekstrovert', 'Pencapaian', 'Kepelbagaian', 'Intelektual', 'Kepimpinan', 'Struktur', 'Resilien', 'Menolong', 'Analitikal', 'Kritik Diri', 'Wawasan', 'Ketelusan']
    
    for line in lines:
        reader = csv.reader([line])
        row = next(reader, None)
        if not row or len(row) < 5: continue
        
        row_clean = [col.strip().upper() for col in row]
        if "NAMA" in row_clean and "BIL" in row_clean:
            start_parsing = True
            continue
            
        if start_parsing:
            try:
                if not row[0].strip().isdigit(): continue
                name = row[1].strip().upper()
                
                scores = {}
                for idx, trait in enumerate(traits_keys):
                    col_idx = 4 + idx
                    if col_idx < len(row):
                        val_str = row[col_idx].strip()
                        scores[trait] = int(val_str) if val_str.isdigit() else 0
                    else:
                        scores[trait] = 0
                        
                students_list.append({
                    "id": f"itp_{class_name.lower().replace(' ', '_')}_{len(students_list)+1}",
                    "name": name,
                    "class": class_name,
                    **scores
                })
            except (ValueError, IndexError):
                continue
    return students_list

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
        
        row_clean = [col.strip().upper() for col in row]
        if "NAMA" in row_clean and "BIL" in row_clean:
            start_parsing = True
            continue
            
        if start_parsing and len(row) >= 10:
            try:
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
                    "name": name, "class": class_name,
                    "R": r_val, "I": i_val, "A": a_val, "S": s_val, "E": e_val, "K": k_val
                })
            except (ValueError, IndexError):
                continue
    return students_list

default_students = [
    { "id": "1", "name": "ANAS BIN HAIRUL AZHAR", "class": "5 Sidiq", "R": 15, "I": 19, "A": 16, "S": 15, "E": 22, "K": 14 },
    { "id": "2", "name": "ANIS FARHANA BINTI SAHIRUDDEN", "class": "5 Sidiq", "R": 14, "I": 25, "A": 12, "S": 23, "E": 19, "K": 24 },
    { "id": "3", "name": "ANIS NAJEYHAH BINTI SUHAIDI", "class": "5 Sidiq", "R": 18, "I": 20, "A": 18, "S": 21, "E": 16, "K": 13 },
    { "id": "4", "name": "AU'FA A'LIAH HAJAR BINTI AHMAD ZAKY", "class": "5 Sidiq", "R": 7, "I": 12, "A": 5, "S": 18, "E": 7, "K": 14 },
    { "id": "5", "name": "DANIAL FAIQ BIN JEFFRI", "class": "5 Sidiq", "R": 18, "I": 20, "A": 16, "S": 16, "E": 16, "K": 26 }
]

default_itp_students = [
    {
        "id": "itp_1", "name": "AFIQAH BINTI KHAIRUDDIN", "class": "2 Fatonah",
        "Autonomi": 45, "Kreatif": 85, "Agresif": 50, "Ekstrovert": 75, "Pencapaian": 80,
        "Kepelbagaian": 70, "Intelektual": 65, "Kepimpinan": 80, "Struktur": 40, "Resilien": 75,
        "Menolong": 90, "Analitikal": 80, "Kritik Diri": 35, "Wawasan": 85, "Ketelusan": 95
    },
    {
        "id": "itp_2", "name": "DANISH IRFAN BIN ZULKIFLI", "class": "2 Fatonah",
        "Autonomi": 70, "Kreatif": 60, "Agresif": 40, "Ekstrovert": 85, "Pencapaian": 90,
        "Kepelbagaian": 75, "Intelektual": 80, "Kepimpinan": 85, "Struktur": 60, "Resilien": 80,
        "Menolong": 70, "Analitikal": 75, "Kritik Diri": 25, "Wawasan": 90, "Ketelusan": 80
    }
]

if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame(default_students)
    
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
                st.session_state.students_db = st.session_state.students_db[st.session_state.students_db['class'] != c_name]
                st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame(loaded)], ignore_index=True)

if 'itp_db' not in st.session_state:
    st.session_state.itp_db = pd.DataFrame(default_itp_students)
    
    itp_file = "senarai-murid-psikometrik-FATONAH-INVENTORI-TRET-PERSONALITI-TINGKATAN-2-2026.csv"
    if os.path.exists(itp_file):
        loaded_itp = parse_itp_csv(itp_file, "2 Fatonah")
        if loaded_itp:
            st.session_state.itp_db = st.session_state.itp_db[st.session_state.itp_db['class'] != "2 Fatonah"]
            st.session_state.itp_db = pd.concat([st.session_state.itp_db, pd.DataFrame(loaded_itp)], ignore_index=True)

def get_riasec_code(row):
    scores = {'R': row['R'], 'I': row['I'], 'A': row['A'], 'S': row['S'], 'E': row['E'], 'K': row['K']}
    return "".join([item[0] for item in sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:3]])

df_imk = st.session_state.students_db.copy()
df_imk['Kod'] = df_imk.apply(get_riasec_code, axis=1)
df_itp = st.session_state.itp_db.copy()

with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>📚 SELEKTOR</h2>", unsafe_allow_html=True)
    active_test = st.radio(
        "Pilih Jenis Pentaksiran:",
        ["🎯 Minat Kerjaya (IMK - RIASEC)", "🧠 Tret Personaliti (ITP)"],
        index=0
    )
    st.write("---")
    st.markdown("""
        <div style="background-color: #f1f5f9; padding: 15px; border-radius: 12px; border: 1px solid #cbd5e1; font-size: 0.85em; color: #475569;">
            <strong>ℹ️ INFO KAUNSELING:</strong><br>
            • <b>IMK (Ting 1 & 5)</b> membantu mengenal pasti minat bidang kerjaya murid.<br><br>
            • <b>ITP (Ting 2)</b> memetakan potensi personaliti unik murid dalam 15 konstruk.
        </div>
    """, unsafe_allow_html=True)

tab_carian, tab_statistik, tab_urus = st.tabs([
    "🔍 Carian Individu", 
    "📊 Dashboard Analisis Kelas", 
    "🔒 Urus Database & CSV"
])

if active_test == "🎯 Minat Kerjaya (IMK - RIASEC)":
    
    with tab_carian:
        st.markdown("<h3 style='color: #1e3a8a; margin-bottom:15px;'><i class='fa-solid fa-magnifying-glass'></i> Imbasan Profil Kerjaya Individu (IMK)</h3>", unsafe_allow_html=True)
        col_t, col_k, col_m = st.columns(3)
        with col_t:
            selected_form = st.selectbox("🎓 Pilih Tingkatan", ["Tingkatan 5", "Tingkatan 1"])
        with col_k:
            if selected_form == "Tingkatan 5":
                available_classes = ["5 Sidiq", "5 Amanah", "5 Tabligh"]
            else:
                available_classes = ["1 Amanah", "1 Fatonah", "1 Tabligh", "1 Sidiq"]
            selected_class = st.selectbox("📁 Pilih Kelas", available_classes)
            
        class_df = df_imk[df_imk['class'] == selected_class].sort_values(by="name")
        with col_m:
            selected_student_name = st.selectbox("👤 Pilih Nama Murid", class_df['name'].tolist() if not class_df.empty else ["-- Tiada Data Murid --"])
                
        if selected_student_name and selected_student_name != "-- Tiada Data Murid --":
            student_data = class_df[class_df['name'] == selected_student_name].iloc[0]
            code = student_data['Kod']
            badge = class_badges.get(selected_class, {"bg": "#E2E8F0", "txt": "#475569", "border": "#CBD5E1", "emoji": "📁"})
            
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 30px; border-radius: 24px; color: white; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);">
                    <span style="background-color: {badge['bg']}; border: 1px solid {badge['border']}; color: {badge['txt']}; padding: 6px 16px; border-radius: 30px; font-size: 0.85em; font-weight: bold;">
                        {badge['emoji']} {student_data['class']} ({selected_form})
                    </span>
                    <h2 style="margin: 15px 0 5px 0; color: white; font-weight: 800; font-size: 2.2em;">{student_data['name']}</h2>
                    <p style="color: #94a3b8; margin-bottom: 20px; font-size: 1.05em;">Tiga Kod Mata Holland Utama Anda:</p>
                    <div style="display: inline-flex; gap: 12px; flex-wrap: wrap;">
                        {"".join([f'<span style="background:{riasec_details[c]["color"]}; color:white; font-size:2em; font-weight:900; padding: 8px 25px; border-radius:16px; box-shadow: 0 8px 16px rgba(0,0,0,0.25); text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">{c}</span>' for c in code])}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<h4 style='color: #1e3a8a; font-weight: bold; margin-bottom:15px;'><i class='fa-solid fa-lightbulb text-warning'></i> Huraian Tret Personaliti & Pilihan Kerjaya:</h4>", unsafe_allow_html=True)
            cols_cards = st.columns(3)
            for idx, char in enumerate(code):
                detail = riasec_details[char]
                with cols_cards[idx]:
                    st.markdown(f"""
                        <div class="riasec-card" style="background-color: {detail['bg_color']}; border: 2px solid {detail['border_color']}; padding: 25px; border-radius: 20px; height:100%; box-shadow: 0 8px 16px -4px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
                                    <span style="background-color: {detail['color']}; color: white; width: 45px; height: 45px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 1.4em; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">{char}</span>
                                    <div>
                                        <h4 style="margin: 0; color: #1e293b; font-weight: 800; font-size: 1.15em;">{detail['name']}</h4>
                                        <small style="color: {detail['color']}; font-weight: 800; font-size: 0.8em; text-transform: uppercase;">{detail['trait']}</small>
                                    </div>
                                </div>
                                <p style="font-size: 0.95em; color: #475569; line-height: 1.6;">{detail['desc']}</p>
                            </div>
                            <div style="margin-top:15px;">
                                <hr style="border: 0; border-top: 1px dashed {detail['border_color']}; margin: 15px 0;">
                                <span style="font-size: 0.75em; color: #64748b; font-weight: bold; display: block; margin-bottom: 5px;">CADANGAN KERJAYA:</span>
                                {"".join([f'<span style="display:inline-block; background:white; border:1px solid #e2e8f0; padding:4px 10px; margin:3px; border-radius:15px; font-size:0.85em; color:#1e3a8a; font-weight:bold; box-shadow:0 1px 2px rgba(0,0,0,0.02);">{job}</span>' for job in detail['careers']])}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    with tab_statistik:
        st.markdown("<h3 style='color: #1e3a8a;'><i class='fa-solid fa-chart-line'></i> Dashboard Analisis Kelas (IMK)</h3>", unsafe_allow_html=True)
        col_st1, col_st2 = st.columns(2)
        with col_st1:
            sel_form_stats = st.selectbox("🎓 Pilih Tingkatan Analisis", ["Tingkatan 5", "Tingkatan 1"], key="t_stats")
        with col_st2:
            if sel_form_stats == "Tingkatan 5":
                available_classes_stats = ["5 Sidiq", "5 Amanah", "5 Tabligh"]
            else:
                available_classes_stats = ["1 Amanah", "1 Fatonah", "1 Tabligh", "1 Sidiq"]
            selected_analysis_class = st.selectbox("📂 Pilih Kelas Analisis", available_classes_stats, key="stats_class")
            
        analysis_df = df_imk[df_imk['class'] == selected_analysis_class]
        
        if analysis_df.empty:
            st.warning("⚠️ Tiada data tersedia untuk kelas ini. Sila muat naik fail CSV SePKM di Tab Pentadbir.")
        else:
            total_students = len(analysis_df)
            analysis_df['Dominan'] = analysis_df['Kod'].str[0]
            freq = analysis_df['Dominan'].value_counts().reindex(['R', 'I', 'A', 'S', 'E', 'K'], fill_value=0)
            top_trait = freq.idxmax()
            
            kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
            with kpi_col1:
                st.markdown(f"<div style='background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 20px; border-radius: 18px; text-align: center;'><h5>JUMLAH MURID</h5><h2>{total_students} Orang</h2></div>", unsafe_allow_html=True)
            with kpi_col2:
                st.markdown(f"<div style='background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); color: white; padding: 20px; border-radius: 18px; text-align: center;'><h5>TRET TERTINGGI</h5><h2>{riasec_details[top_trait]['name']}</h2></div>", unsafe_allow_html=True)
            with kpi_col3:
                st.markdown("<div style='background: linear-gradient(135deg, #059669 0%, #34d399 100%); color: white; padding: 20px; border-radius: 18px; text-align: center;'><h5>STATUS</h5><h2>Lengkap</h2></div>", unsafe_allow_html=True)
                
            st.write("---")
            col_chart, col_leaderboard = st.columns([3, 2])
            with col_chart:
                st.write("📊 **Carta Kekerapan Kecenderungan Utama Murid (Huruf Pertama)**")
                chart_data = pd.DataFrame({'Kategori': [f"{riasec_details[k]['name']} ({k})" for k in freq.index], 'Bilangan Murid': freq.values})
                st.bar_chart(data=chart_data, x='Kategori', y='Bilangan Murid', color='#3b82f6')
            with col_leaderboard:
                st.write("🏆 **Kedudukan Kepentingan Tret Kelas**")
                for idx, (char, count) in enumerate(freq.sort_values(ascending=False).items()):
                    pct = (count / total_students) * 100 if total_students > 0 else 0
                    st.markdown(f"""
                        <div style="display:flex; justify-content:space-between; background:white; padding:12px 15px; margin-bottom:8px; border-radius:12px; border-left:6px solid {riasec_details[char]['color']}; box-shadow:0 2px 4px rgba(0,0,0,0.03);">
                            <span style="font-weight:800; color:#1e293b;">{idx+1}. {riasec_details[char]['name']} ({char})</span>
                            <span style="color:{riasec_details[char]['color']}; font-weight:900;">{count} Murid ({pct:.0f}%)</span>
                        </div>
                    """, unsafe_allow_html=True)

    with tab_urus:
        st.markdown("<h3 style='color: #1e3a8a;'><i class='fa-solid fa-lock'></i> Pintu Kawalan Pentadbir (IMK)</h3>", unsafe_allow_html=True)
        if 'logged_in' not in st.session_state: st.session_state.logged_in = False
        
        if not st.session_state.logged_in:
            with st.form("login_form_imk"):
                password_input = st.text_input("🔑 Masukkan Kata Laluan Pentadbir:", type="password")
                if st.form_submit_button("Log Masuk"):
                    if password_input == "cikgu123":
                        st.session_state.logged_in = True
                        st.balloons()
                        st.rerun()
                    else: st.error("Kata laluan salah!")
        else:
            st.success("🔓 Mod Pentadbir Aktif.")
            if st.button("🔴 Log Keluar"):
                st.session_state.logged_in = False
                st.rerun()
            st.write("---")
            
            st.markdown("#### 📥 Muat Naik Fail CSV Sistem SePKM (Tingkatan 1 & 5)")
            up1, up2 = st.columns(2)
            with up1:
                f_am1 = st.file_uploader("Pilih fail CSV Kelas 1 Amanah", type=['csv'])
                if f_am1:
                    res = parse_psychometric_csv(f_am1, "1 Amanah")
                    if res:
                        st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "1 Amanah"], pd.DataFrame(res)], ignore_index=True)
                        st.toast("1 Amanah Dimuatkan!")
                        st.rerun()
            with up2:
                f_am5 = st.file_uploader("Pilih fail CSV Kelas 5 Amanah", type=['csv'])
                if f_am5:
                    res = parse_psychometric_csv(f_am5, "5 Amanah")
                    if res:
                        st.session_state.students_db = pd.concat([st.session_state.students_db[st.session_state.students_db['class'] != "5 Amanah"], pd.DataFrame(res)], ignore_index=True)
                        st.toast("5 Amanah Dimuatkan!")
                        st.rerun()
            st.write("---")
            st.markdown("#### ➕ Daftar Murid Secara Manual (IMK)")
            with st.form("manual_form_imk"):
                m_name = st.text_input("Nama Penuh Murid:").upper()
                m_class = st.selectbox("Kelas Murid:", ["5 Sidiq", "5 Amanah", "5 Tabligh", "1 Amanah", "1 Fatonah", "1 Tabligh", "1 Sidiq"])
                c_r, c_i, c_a, c_s, c_e, c_k = st.columns(6)
                with c_r: r_s = st.number_input("Skor R", 0, 30, 0)
                with c_i: i_s = st.number_input("Skor I", 0, 30, 0)
                with c_a: a_s = st.number_input("Skor A", 0, 30, 0)
                with c_s: s_s = st.number_input("Skor S", 0, 30, 0)
                with c_e: e_s = st.number_input("Skor E", 0, 30, 0)
                with c_k: k_s = st.number_input("Skor K", 0, 30, 0)
                if st.form_submit_button("💾 Simpan"):
                    new_student = {"id": f"manual_{len(st.session_state.students_db)+1}", "name": m_name, "class": m_class, "R": r_s, "I": i_s, "A": a_s, "S": s_s, "E": e_s, "K": k_s}
                    st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame([new_student])], ignore_index=True)
                    st.success("Berjaya!")
                    st.rerun()

            st.write("---")
            st.dataframe(df_imk[['name', 'class', 'R', 'I', 'A', 'S', 'E', 'K', 'Kod']], use_container_width=True, hide_index=True)

else:
    
    with tab_carian:
        st.markdown("<h3 style='color: #1e3a8a; margin-bottom:15px;'><i class='fa-solid fa-brain'></i> Imbasan Tret Personaliti Murid (ITP)</h3>", unsafe_allow_html=True)
        col_t_itp, col_k_itp, col_m_itp = st.columns(3)
        with col_t_itp:
            selected_form_itp = st.selectbox("🎓 Pilih Tingkatan", ["Tingkatan 2"])
        with col_k_itp:
            available_classes_itp = ["2 Fatonah"]
            selected_class_itp = st.selectbox("📁 Pilih Kelas", available_classes_itp)
            
        class_df_itp = df_itp[df_itp['class'] == selected_class_itp].sort_values(by="name")
        with col_m_itp:
            selected_student_itp = st.selectbox("👤 Pilih Nama Murid", class_df_itp['name'].tolist() if not class_df_itp.empty else ["-- Tiada Data Murid --"])
            
        if selected_student_itp and selected_student_itp != "-- Tiada Data Murid --":
            student_data_itp = class_df_itp[class_df_itp['name'] == selected_student_itp].iloc[0]
            badge = class_badges.get(selected_class_itp, {"bg": "#D1FAE5", "txt": "#065F46", "border": "#6EE7B7", "emoji": "🟢"})
            
            # Cari 3 Tret Tertinggi
            scores_map = {k: student_data_itp[k] for k in itp_details.keys()}
            sorted_tret = sorted(scores_map.items(), key=lambda x: -x[1])[:3]
            
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); padding: 30px; border-radius: 24px; color: white; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.25);">
                    <span style="background-color: {badge['bg']}; border: 1px solid {badge['border']}; color: {badge['txt']}; padding: 6px 16px; border-radius: 30px; font-size: 0.85em; font-weight: bold;">
                        {badge['emoji']} {student_data_itp['class']} ({selected_form_itp})
                    </span>
                    <h2 style="margin: 15px 0 5px 0; color: white; font-weight: 800; font-size: 2.2em;">{student_data_itp['name']}</h2>
                    <p style="color: #cbd5e1; margin-bottom: 20px; font-size: 1.05em;">3 Tret Personaliti Utama Teratas Anda:</p>
                    <div style="display: inline-flex; gap: 12px; flex-wrap: wrap;">
                        {"".join([f'<span style="background:linear-gradient(135deg, {itp_details[t[0]]["color"]} 0%, #111 100%); color:white; font-size:1.1em; font-weight:bold; padding: 10px 20px; border-radius:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">{itp_details[t[0]]["icon"]} {t[0]} ({t[1]}%)</span>' for t in sorted_tret])}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Pemetaan 15 Progress Bars untuk Tret Personaliti
            st.markdown("<h4 style='color: #1e3a8a; font-weight: bold; margin-bottom:15px;'><i class='fa-solid fa-list-check'></i> Profil Tret Personaliti Penuh (15 Konstruk):</h4>", unsafe_allow_html=True)
            
            col_bar1, col_bar2 = st.columns(2)
            for idx, key in enumerate(itp_details.keys()):
                score_val = int(student_data_itp[key])
                if score_val >= 70:
                    tahap = "Tinggi"
                    badge_col = "red" if key in ['Agresif', 'Kritik Diri'] else "green"
                    tahap_desc = itp_details[key]['Tinggi']
                elif score_val >= 40:
                    tahap = "Sederhana"
                    badge_col = "orange"
                    tahap_desc = itp_details[key]['Sederhana']
                else:
                    tahap = "Rendah"
                    badge_col = "blue"
                    tahap_desc = itp_details[key]['Rendah']
                
                target_col = col_bar1 if idx % 2 == 0 else col_bar2
                with target_col:
                    st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                <span style="font-weight: bold; color: #1e293b;">{itp_details[key]['icon']} {key}</span>
                                <span style="font-weight: bold; color: {itp_details[key]['color']};">{score_val}% (<span style="color: {badge_col}; font-weight: 800;">{tahap}</span>)</span>
                            </div>
                            <div style="background-color: #f1f5f9; height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 8px;">
                                <div style="background-color: {itp_details[key]['color']}; width: {score_val}%; height: 100%; border-radius: 4px;"></div>
                            </div>
                            <p style="font-size: 0.85em; color: #64748b; line-height: 1.4; margin: 0;">{tahap_desc}</p>
                        </div>
                    """, unsafe_allow_html=True)

    with tab_statistik:
        st.markdown("<h3 style='color: #1e3a8a;'><i class='fa-solid fa-chart-line'></i> Dashboard Analisis Kelas (ITP)</h3>", unsafe_allow_html=True)
        col_st1_itp, col_st2_itp = st.columns(2)
        with col_st1_itp:
            sel_form_stats_itp = st.selectbox("🎓 Pilih Tingkatan Analisis", ["Tingkatan 2"], key="t_stats_itp")
        with col_st2_itp:
            available_classes_stats_itp = ["2 Fatonah"]
            selected_analysis_class_itp = st.selectbox("📂 Pilih Kelas Analisis", available_classes_stats_itp, key="stats_class_itp")
            
        analysis_df_itp = df_itp[df_itp['class'] == selected_analysis_class_itp]
        
        if analysis_df_itp.empty:
            st.warning("⚠️ Tiada data tersedia untuk kelas ini. Sila muat naik fail CSV SePKM di Tab Pentadbir.")
        else:
            total_students_itp = len(analysis_df_itp)
            traits_itp = list(itp_details.keys())
            
            # Kira purata skor untuk setiap tret dalam kelas
            avg_scores = {trait: analysis_df_itp[trait].mean() for trait in traits_itp}
            sorted_avg = sorted(avg_scores.items(), key=lambda x: -x[1])
            top_class_trait = sorted_avg[0][0]
            
            kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
            with kpi_col1:
                st.markdown(f"<div style='background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); color: white; padding: 20px; border-radius: 18px; text-align: center;'><h5>JUMLAH MURID</h5><h2>{total_students_itp} Orang</h2></div>", unsafe_allow_html=True)
            with kpi_col2:
                st.markdown(f"<div style='background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); color: white; padding: 20px; border-radius: 18px; text-align: center;'><h5>TRET PURATA TERTINGGI</h5><h2>{top_class_trait} ({avg_scores[top_class_trait]:.1f}%)</h2></div>", unsafe_allow_html=True)
            with kpi_col3:
                st.markdown("<div style='background: linear-gradient(135deg, #059669 0%, #34d399 100%); color: white; padding: 20px; border-radius: 18px; text-align: center;'><h5>UJIAN</h5><h2>I.T.P.</h2></div>", unsafe_allow_html=True)
                
            st.write("---")
            col_chart_itp, col_leaderboard_itp = st.columns([3, 2])
            with col_chart_itp:
                st.write("📊 **Purata Skor Tret Personaliti Kelas (%)**")
                chart_data_itp = pd.DataFrame({'Tret': list(avg_scores.keys()), 'Purata Skor (%)': list(avg_scores.values())})
                st.bar_chart(data=chart_data_itp, x='Tret', y='Purata Skor (%)', color='#8b5cf6')
            with col_leaderboard_itp:
                st.write("🏆 **Kedudukan Kekuatan Tret Kelas**")
                for idx, (tret, score) in enumerate(sorted_avg):
                    st.markdown(f"""
                        <div style="display:flex; justify-content:space-between; background:white; padding:12px 15px; margin-bottom:8px; border-radius:12px; border-left:6px solid {itp_details[tret]['color']}; box-shadow:0 2px 4px rgba(0,0,0,0.03);">
                            <span style="font-weight:800; color:#1e293b;">{idx+1}. {itp_details[tret]['icon']} {tret}</span>
                            <span style="color:{itp_details[tret]['color']}; font-weight:900;">{score:.1f}%</span>
                        </div>
                    """, unsafe_allow_html=True)

    with tab_urus:
        st.markdown("<h3 style='color: #1e3a8a;'><i class='fa-solid fa-lock'></i> Pintu Kawalan Pentadbir (ITP)</h3>", unsafe_allow_html=True)
        if 'logged_in' not in st.session_state: st.session_state.logged_in = False
        
        if not st.session_state.logged_in:
            with st.form("login_form_itp"):
                password_input = st.text_input("🔑 Masukkan Kata Laluan Pentadbir:", type="password")
                if st.form_submit_button("Log Masuk"):
                    if password_input == "ellan711":
                        st.session_state.logged_in = True
                        st.balloons()
                        st.rerun()
                    else: st.error("Kata laluan salah!")
        else:
            st.success("🔓 Mod Pentadbir Aktif.")
            if st.button("🔴 Log Keluar"):
                st.session_state.logged_in = False
                st.rerun()
            st.write("---")
            
            st.markdown("#### 📥 Muat Naik Fail CSV Sistem SePKM (Tret Personaliti - Tingkatan 2)")
            f_itp_upload = st.file_uploader("Pilih fail CSV Kelas 2 Fatonah (ITP)", type=['csv'])
            if f_itp_upload:
                res_itp = parse_itp_csv(f_itp_upload, "2 Fatonah")
                if res_itp:
                    st.session_state.itp_db = pd.concat([st.session_state.itp_db[st.session_state.itp_db['class'] != "2 Fatonah"], pd.DataFrame(res_itp)], ignore_index=True)
                    st.toast("Data 2 Fatonah (ITP) Dimuatkan!")
                    st.rerun()
                else: st.error("Gagal membaca format CSV SePKM ITP.")
            
            st.write("---")
            st.markdown("#### ➕ Daftar Murid Secara Manual (ITP)")
            with st.form("manual_form_itp"):
                m_name = st.text_input("Nama Penuh Murid:").upper()
                m_class = st.selectbox("Kelas Murid:", ["2 Fatonah"])
                
                scores_manual = {}
                cols = st.columns(5)
                for idx, key in enumerate(itp_details.keys()):
                    with cols[idx % 5]:
                        scores_manual[key] = st.number_input(f"{itp_details[key]['icon']} {key} (0-100)", 0, 100, 50)
                
                if st.form_submit_button("💾 Simpan"):
                    new_student_itp = {"id": f"itp_manual_{len(st.session_state.itp_db)+1}", "name": m_name, "class": m_class}
                    new_student_itp.update(scores_manual)
                    st.session_state.itp_db = pd.concat([st.session_state.itp_db, pd.DataFrame([new_student_itp])], ignore_index=True)
                    st.success("Berjaya!")
                    st.rerun()

            st.write("---")
            st.dataframe(df_itp, use_container_width=True, hide_index=True)
