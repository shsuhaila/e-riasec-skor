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

# Custom Colorful CSS Styling
st.markdown("""
    <style>
        /* Global Background styling */
        .main {
            background-color: #f8fafc;
        }
        
        /* Custom styled tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: #f1f5f9;
            padding: 8px 12px;
            border-radius: 12px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            color: #475569;
            background-color: transparent;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #1e3a8a;
            background-color: #e2e8f0;
        }
        .stTabs [aria-selected="true"] {
            background-color: #ffffff !important;
            color: #1e3a8a !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        /* Hover effects for custom HTML cards */
        .riasec-card {
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .riasec-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05) !important;
        }
    </style>
""", unsafe_allow_html=True)

riasec_details = {
    'R': {
        'name': 'Realistik',
        'trait': 'Praktikal & Fizikal',
        'desc': 'Gemar tugasan fizikal, menggunakan instrumen, membaiki alatan mekanikal atau mesin. Lebih gemar kerja praktikal di luar pejabat.',
        'careers': 'Jurutera, Mekanik, Ahli Pertanian, Juruteknik',
        'color': '#EF4444',      # Red
        'bg_color': '#FEF2F2',   # Soft Red
        'border_color': '#FCA5A5'
    },
    'I': {
        'name': 'Investigatif',
        'trait': 'Saintifik & Saintis',
        'desc': 'Gemar tugasan berfikir, membuat penyelidikan, menganalisis masalah yang kompleks, gemar membaca topik teknikal serta bidang perubatan.',
        'careers': 'Doktor, Ahli Kimia, Penganalisis Data, Penyelidik',
        'color': '#3B82F6',      # Blue
        'bg_color': '#EFF6FF',   # Soft Blue
        'border_color': '#93C5FD'
    },
    'A': {
        'name': 'Artistik',
        'trait': 'Kreatif & Bebas',
        'desc': 'Menghargai kebebasan berekspresi, kreatif, artistik, suka melukis, muzik, penulisan kreatif atau rekaan grafik.',
        'careers': 'Pereka Grafik, Arkitek, Penulis, Pemuzik, Pelakon',
        'color': '#8B5CF6',      # Purple
        'bg_color': '#F5F3FF',   # Soft Purple
        'border_color': '#C7D2FE'
    },
    'S': {
        'name': 'Sosial',
        'trait': 'Membantu & Prihatin',
        'desc': 'Prihatin kebajikan orang ramai, gemar mengajar, merawat pesakit, memberi kaunseling serta selesa berinteraksi dalam kumpulan.',
        'careers': 'Guru, Kaunselor, Pegawai HR, Jururawat, Pekerja Sosial',
        'color': '#10B981',      # Emerald Green
        'bg_color': '#ECFDF5',   # Soft Green
        'border_color': '#6EE7B7'
    },
    'E': {
        'name': 'Enterprising',
        'trait': 'Berdaya Usaha & Pemimpin',
        'desc': 'Sifat kepimpinan kuat, berbakat memujuk, mengurus projek perniagaan, bercita-cita tinggi, mahir berucap di hadapan umum.',
        'careers': 'Usahawan, Pengarah Syarikat, Pengurus Jualan, Peguam',
        'color': '#F59E0B',      # Amber Orange
        'bg_color': '#FFFBEB',   # Soft Amber
        'border_color': '#FCD34D'
    },
    'K': {
        'name': 'Konvensional',
        'trait': 'Sistematik & Berstruktur',
        'desc': 'Tersusun, mementingkan kekemasan, teratur dalam menguruskan data, rekod, tugasan perkeranian atau perakaunan.',
        'careers': 'Akauntan, Pentadbir Fail, Setiausaha, Penganalisis Kewangan',
        'color': '#06B6D4',      # Cyan
        'bg_color': '#ECFEFF',   # Soft Cyan
        'border_color': '#67E8F9'
    }
}

# Helper to map class to nice color badges
class_badges = {
    "5 Sidiq": {"bg": "#E0F2FE", "txt": "#0369A1", "border": "#7DD3FC", "emoji": "🔵"},
    "5 Amanah": {"bg": "#D1FAE5", "txt": "#065F46", "border": "#6EE7B7", "emoji": "🟢"},
    "5 Tabligh": {"bg": "#FEF3C7", "txt": "#92400E", "border": "#FCD34D", "emoji": "🟡"}
}

def parse_psychometric_csv(file_path_or_buffer, class_name):
    students_list = []
    content = ""
    
    # 1. Membaca kandungan fail dengan sokongan pengekodan pelbagai format
    if isinstance(file_path_or_buffer, str):
        if not os.path.exists(file_path_or_buffer):
            return []
        try:
            with open(file_path_or_buffer, 'r', encoding='utf-8-sig', errors='ignore') as f:
                content = f.read()
        except Exception:
            return []
    else:
        # Cuba membaca menggunakan UTF-8-SIG, jika ralat cuba UTF-16, dan CP1252
        try:
            content = file_path_or_buffer.getvalue().decode('utf-8-sig', errors='ignore')
        except Exception:
            try:
                content = file_path_or_buffer.getvalue().decode('utf-16', errors='ignore')
            except Exception:
                try:
                    content = file_path_or_buffer.getvalue().decode('cp1252', errors='ignore')
                except Exception:
                    return []

    lines = content.splitlines()
    if not lines:
        return []

    best_delimiter = ','
    header_idx = -1
    cols_found = []
    
    # 2. Imbas 50 baris pertama untuk mencari baris Kepala Jadual (Header) yang sebenar
    for sep in [',', ';', '\t']:
        for i, line in enumerate(lines[:50]):
            try:
                parts = [p.strip().upper() for p in next(csv.reader([line], delimiter=sep))]
                
                # Semak jika baris ini mempunyai ruangan Nama
                has_name = any('NAMA' in p or 'NAME' in p or 'MURID' in p or 'PELAJAR' in p for p in parts)
                
                # Semak jika ada ruangan skor RIASEK
                riasec_cols = ['R', 'I', 'A', 'S', 'E', 'K']
                riasec_full_cols = ['REALISTIK', 'INVESTIGATIF', 'ARTISTIK', 'SOSIAL', 'ENTERPRISING', 'KONVENSIONAL', 'REALISTIC', 'INVESTIGATIVE', 'ARTISTIC', 'SOCIAL', 'CONVENTIONAL']
                
                has_riasec = sum(1 for r in riasec_cols if r in parts) >= 4 or sum(1 for rf in riasec_full_cols if any(rf in p for p in parts)) >= 4
                
                if has_name and has_riasec:
                    header_idx = i
                    best_delimiter = sep
                    cols_found = parts
                    break
            except Exception:
                continue
        if header_idx != -1:
            break
            
    # Jika gagal mencari baris kepala jadual berformat, cuba cari baris yang hanya mengandungi perkataan 'NAMA'
    if header_idx == -1:
        for sep in [',', ';', '\t']:
            for i, line in enumerate(lines[:50]):
                try:
                    parts = [p.strip().upper() for p in next(csv.reader([line], delimiter=sep))]
                    if any('NAMA' in p or 'NAME' in p for p in parts) and len(parts) >= 7:
                        header_idx = i
                        best_delimiter = sep
                        cols_found = parts
                        break
                except Exception:
                    continue
            if header_idx != -1:
                break

    # 3. Jika gagal mengesan kepala jadual, gunakan kaedah Sandaran Kasar (Kesan Nama + 6 Angka)
    if header_idx == -1:
        return parse_raw_unformatted_csv(lines, class_name)

    # 4. Memadankan kedudukan ruangan nama dan markah RIASEK
    name_idx = -1
    r_idx, i_idx, a_idx, s_idx, e_idx, k_idx = -1, -1, -1, -1, -1, -1
    
    for idx, col in enumerate(cols_found):
        col_clean = col.strip().upper()
        if 'NAMA' in col_clean or 'NAME' in col_clean or 'MURID' in col_clean or 'PELAJAR' in col_clean:
            name_idx = idx
        elif col_clean == 'R' or 'REALISTIK' in col_clean or 'REALISTIC' in col_clean or 'SKOR R' in col_clean:
            r_idx = idx
        elif col_clean == 'I' or 'INVESTIGATIF' in col_clean or 'INVESTIGATIVE' in col_clean or 'SKOR I' in col_clean:
            i_idx = idx
        elif col_clean == 'A' or 'ARTISTIK' in col_clean or 'ARTISTIC' in col_clean or 'SKOR A' in col_clean:
            a_idx = idx
        elif col_clean == 'S' or 'SOSIAL' in col_clean or 'SOCIAL' in col_clean or 'SKOR S' in col_clean:
            s_idx = idx
        elif col_clean == 'E' or 'ENTERPRISING' in col_clean or 'ENTERPRISE' in col_clean or 'SKOR E' in col_clean:
            e_idx = idx
        elif col_clean == 'K' or 'KONVENSIONAL' in col_clean or 'CONVENTIONAL' in col_clean or 'SKOR K' in col_clean:
            k_idx = idx

    # Jika nama masih tiada, andaikan ruangan pertama
    if name_idx == -1:
        name_idx = 0

    # 5. Membaca baris data bermula selepas baris kepala jadual
    for line in lines[header_idx + 1:]:
        if not line.strip():
            continue
        try:
            reader = csv.reader([line], delimiter=best_delimiter)
            row = next(reader, None)
            if not row or len(row) <= max(name_idx, r_idx, i_idx, a_idx, s_idx, e_idx, k_idx):
                continue
                
            student_name = row[name_idx].strip().upper()
            # Abaikan jika baris tersebut bukan nama murid sebenar
            if not student_name or student_name.isdigit() or len(student_name) < 3 or 'NAMA' in student_name or 'JUMLAH' in student_name or 'PURATA' in student_name:
                continue
                
            def get_score(idx_val):
                if idx_val != -1 and idx_val < len(row):
                    val = row[idx_val].strip()
                    try:
                        return int(float(val))
                    except ValueError:
                        return 0
                return 0
                
            scores = {
                "R": get_score(r_idx),
                "I": get_score(i_idx),
                "A": get_score(a_idx),
                "S": get_score(s_idx),
                "E": get_score(e_idx),
                "K": get_score(k_idx)
            }
            
            # Hanya simpan jika murid mempunyai sekurang-kurangnya satu markah
            if sum(scores.values()) > 0:
                students_list.append({
                    "id": f"{class_name.lower().replace(' ', '_')}_{len(students_list)+1}",
                    "name": student_name,
                    "class": class_name,
                    "R": scores["R"],
                    "I": scores["I"],
                    "A": scores["A"],
                    "S": scores["S"],
                    "E": scores["E"],
                    "K": scores["K"]
                })
        except Exception:
            continue
            
    # Jika masih gagal mendapatkan senarai, cuba guna sandaran warisan (legacy fallback)
    if not students_list:
        return parse_psychometric_csv_legacy(lines, class_name)
        
    return students_list

def parse_raw_unformatted_csv(lines, class_name):
    """Membaca CSV yang tiada kepala jadual langsung dengan mengesan 1 teks panjang (nama) dan 6 angka (skor)."""
    students_list = []
    best_sep = ','
    for line in lines[:20]:
        if ';' in line and line.count(';') > line.count(','):
            best_sep = ';'
            break
            
    for line in lines:
        if not line.strip():
            continue
        try:
            row = [item.strip() for item in next(csv.reader([line], delimiter=best_sep))]
            if len(row) < 7:
                continue
                
            nums = []
            cand_name = ""
            for item in row:
                if item.isdigit():
                    nums.append(int(item))
                elif len(item) > 3 and not any(c.isdigit() for c in item) and 'NAMA' not in item.upper() and 'KELAS' not in item.upper():
                    cand_name = item.upper()
                    
            if cand_name and len(nums) >= 6:
                students_list.append({
                    "id": f"{class_name.lower().replace(' ', '_')}_{len(students_list)+1}",
                    "name": cand_name,
                    "class": class_name,
                    "R": nums[0], "I": nums[1], "A": nums[2], "S": nums[3], "E": nums[4], "K": nums[5]
                })
        except Exception:
            continue
    return students_list

def parse_psychometric_csv_legacy(lines, class_name):
    """Format sandaran lama yang mencari simbol | bagi data tersuai."""
    students_list = []
    for line in lines:
        try:
            row = next(csv.reader([line]))
            if not row or len(row) < 5:
                continue
                
            scores = {}
            name = None
            for item in row:
                item_strip = item.strip()
                if '|' in item_strip:
                    parts = item_strip.split('|')
                    if len(parts) == 2:
                        key = parts[0].strip().upper()
                        val_str = parts[1].strip()
                        if key in ['R', 'I', 'A', 'S', 'E', 'K']:
                            try:
                                scores[key] = int(val_str)
                            except ValueError:
                                pass
                                
            if len(scores) >= 6:
                cand_name = row[1].strip().upper() if len(row) > 1 else ""
                if cand_name and not cand_name.isdigit() and len(cand_name) > 3:
                    name = cand_name
                else:
                    for val in row:
                        val_clean = val.strip().upper()
                        if val_clean and len(val_clean) > 3 and not any(char.isdigit() for char in val_clean) and '|' not in val_clean:
                            name = val_clean
                            break
                if name:
                    students_list.append({
                        "id": f"{class_name.lower().replace(' ', '_')}_{len(students_list)+1}_{name[:5]}",
                        "name": name,
                        "class": class_name,
                        "R": scores.get('R', 0),
                        "I": scores.get('I', 0),
                        "A": scores.get('A', 0),
                        "S": scores.get('S', 0),
                        "E": scores.get('E', 0),
                        "K": scores.get('K', 0)
                    })
        except Exception:
            pass
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
    initial_df = pd.DataFrame(default_students)
    st.session_state.students_db = initial_df
    
    # Auto-load Amanah jika fail berada dalam folder kerja
    amanah_file_name = "senarai-murid-psikometrik-AMANAH-INVENTORI-MINAT-KERJAYA-TINGKATAN-5-2026.csv"
    amanah_data = parse_psychometric_csv(amanah_file_name, "5 Amanah")
    if amanah_data:
        st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame(amanah_data)], ignore_index=True)
        
    # Auto-load Tabligh jika fail berada dalam folder kerja
    tabligh_file_name = "senarai-murid-psikometrik-TABLIGH-INVENTORI-MINAT-KERJAYA-TINGKATAN-5-2026.csv"
    tabligh_data = parse_psychometric_csv(tabligh_file_name, "5 Tabligh")
    if tabligh_data:
        st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame(tabligh_data)], ignore_index=True)

def get_riasec_code(row):
    scores = {'R': row['R'], 'I': row['I'], 'A': row['A'], 'S': row['S'], 'E': row['E'], 'K': row['K']}
    sorted_scores = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return "".join([item[0] for item in sorted_scores[:3]])

df = st.session_state.students_db.copy()
df['Kod'] = df.apply(get_riasec_code, axis=1)

# Header Utama (More Colorful Banner)
st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #06b6d4 100%); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3);">
        <h1 style="color: white; margin: 0; font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 2.8em; letter-spacing: 1px;">🎯 E-RIASEC SKOR</h1>
        <p style="color: #e0f2fe; margin-top: 10px; font-size: 1.2em; font-weight: 300;">Sistem Pengurusan & Analisis Interaktif Ujian Psikometrik Minat Kerjaya</p>
    </div>
""", unsafe_allow_html=True)

tab_carian, tab_statistik, tab_urus = st.tabs([
    "🔍 Carian Individu", 
    "📊 Statistik & Taburan Kelas", 
    "⚙️ Urus Database & Muat Naik CSV"
])

# ==================== TAB 1: CARIAN INDIVIDU ====================
with tab_carian:
    st.markdown("<h3 style='color: #1e3a8a;'>Carian Profil Kerjaya Murid</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        selected_class = st.selectbox("📁 Pilih Kelas", ["5 Sidiq", "5 Amanah", "5 Tabligh"], key="search_class")
    
    class_df = df[df['class'] == selected_class].sort_values(by="name")
    
    with col2:
        if not class_df.empty:
            selected_student_name = st.selectbox("👤 Pilih Nama Murid", class_df['name'].tolist(), key="search_student")
        else:
            st.selectbox("👤 Pilih Nama Murid", ["-- Tiada Murid Berdaftar --"], disabled=True)
            selected_student_name = None
            
    if selected_student_name and selected_student_name != "-- Tiada Murid Berdaftar --":
        student_data = class_df[class_df['name'] == selected_student_name].iloc[0]
        code = student_data['Kod']
        badge_style = class_badges.get(selected_class, {"bg": "#E2E8F0", "txt": "#475569", "border": "#CBD5E1", "emoji": "📁"})
        
        # Colorful Profil Banner
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 30px; border-radius: 18px; color: white; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span style="background-color: {badge_style['bg']}; border: 1px solid {badge_style['border']}; color: {badge_style['txt']}; padding: 6px 16px; border-radius: 30px; font-size: 0.85em; font-weight: bold;">
                            {badge_style['emoji']} {student_data['class']}
                        </span>
                        <h2 style="margin: 15px 0 5px 0; color: white; font-size: 2.2em; font-family: sans-serif;">{student_data['name']}</h2>
                        <p style="color: #94a3b8; margin: 0; font-size: 1.0em;">Laporan Inventori Minat Kerjaya (Tiga Mata Holland)</p>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.08); padding: 15px 30px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.15); text-align: center; min-width: 180px;">
                        <span style="font-size: 0.75em; text-transform: uppercase; letter-spacing: 1.5px; color: #cbd5e1; display: block; margin-bottom: 5px;">KOD KERJAYA</span>
                        <strong style="font-size: 2.6em; color: #fde047; font-family: sans-serif; letter-spacing: 2px;">{code}</strong>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<h4 style='color: #1e3a8a;'>🎨 Huraian Personaliti Kod Tiga Huruf Utama:</h4>", unsafe_allow_html=True)
        cols_cards = st.columns(3)
        for idx, char in enumerate(code):
            detail = riasec_details[char]
            with cols_cards[idx]:
                st.markdown(
                    f"""
                    <div class="riasec-card" style="background-color: {detail['bg_color']}; border: 2px solid {detail['border_color']}; padding: 25px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 15px;">
                                <span style="background-color: {detail['color']}; color: white; width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.4em; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                                    {char}
                                </span>
                                <div>
                                    <h4 style="margin: 0; color: #1e293b; font-size: 1.25em; font-weight: bold;">{detail['name']}</h4>
                                    <small style="color: {detail['color']}; font-weight: bold; text-transform: uppercase; font-size: 0.8em; letter-spacing: 0.5px;">{detail['trait']}</small>
                                </div>
                            </div>
                            <p style="font-size: 0.9em; color: #475569; line-height: 1.6; margin-bottom: 20px;">{detail['desc']}</p>
                        </div>
                        <div style="background-color: white; padding: 12px; border-radius: 10px; border: 1px dashed {detail['border_color']};">
                            <span style="font-size: 0.75em; color: #64748b; font-weight: bold; display: block; margin-bottom: 4px;">CADANGAN KERJAYA:</span>
                            <span style="font-size: 0.9em; color: #1e3a8a; font-weight: bold;">{detail['careers']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        st.write("---")
        st.markdown("<h4 style='color: #1e3a8a;'>📈 Analisis Markah Penuh Mengikut Tret</h4>", unsafe_allow_html=True)
        
        col_pb1, col_pb2 = st.columns(2)
        traits = [('R', 'Realistik'), ('I', 'Investigatif'), ('A', 'Artistik'), ('S', 'Sosial'), ('E', 'Enterprising'), ('K', 'Konvensional')]
        
        for index, (char, name) in enumerate(traits):
            score = int(student_data[char])
            percentage = score / 30.0
            color = riasec_details[char]['color']
            
            target_col = col_pb1 if index < 3 else col_pb2
            with target_col:
                st.write(f"**{char} - {name}** ({score}/30)")
                # Color code progress bar utilizing standard streamlit, but wrapping with custom visual cue
                st.progress(percentage)
                
    else:
        st.info("💡 Sila pilih kelas terlebih dahulu, kemudian klik pada nama murid untuk melihat profil visual yang menarik!")

# ==================== TAB 2: STATISTIK KELAS ====================
with tab_statistik:
    st.markdown("<h3 style='color: #1e3a8a;'>Analisis Taburan Tret Dominan Kelas</h3>", unsafe_allow_html=True)
    selected_analysis_class = st.selectbox("📂 Pilih Kelas Untuk Analisis Statistik", ["5 Sidiq", "5 Amanah", "5 Tabligh"], key="analysis_class")
    
    analysis_df = df[df['class'] == selected_analysis_class]
    
    if analysis_df.empty:
        st.warning(f"⚠️ Tiada data tersedia untuk kelas {selected_analysis_class}. Sila muat naik fail CSV di tab sebelah dahulu!")
    else:
        analysis_df['Dominan'] = analysis_df['Kod'].str[0]
        freq = analysis_df['Dominan'].value_counts()
        
        for char in ['R', 'I', 'A', 'S', 'E', 'K']:
            if char not in freq:
                freq[char] = 0
        
        freq = freq.reindex(['R', 'I', 'A', 'S', 'E', 'K'])
        
        # Color Legend for RIASEC Chart
        st.markdown("""
            <div style="display: flex; gap: 15px; justify-content: center; margin-bottom: 20px; flex-wrap: wrap;">
                <span style="background-color: #EF4444; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; font-weight: bold;">R - Realistik</span>
                <span style="background-color: #3B82F6; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; font-weight: bold;">I - Investigatif</span>
                <span style="background-color: #8B5CF6; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; font-weight: bold;">A - Artistik</span>
                <span style="background-color: #10B981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; font-weight: bold;">S - Sosial</span>
                <span style="background-color: #F59E0B; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; font-weight: bold;">E - Enterprising</span>
                <span style="background-color: #06B6D4; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8em; font-weight: bold;">K - Konvensional</span>
            </div>
        """, unsafe_allow_html=True)
        
        col_chart, col_details = st.columns([3, 2])
        
        with col_chart:
            st.write("**Carta Taburan Kod Dominan Utama (Huruf Pertama)**")
            chart_data = pd.DataFrame({
                'Kecenderungan': ['Realistik (R)', 'Investigatif (I)', 'Artistik (A)', 'Sosial (S)', 'Enterprising (E)', 'Konvensional (K)'],
                'Jumlah Murid': freq.values
            })
            st.bar_chart(data=chart_data, x='Kecenderungan', y='Jumlah Murid', color='#1E3A8A')
            
        with col_details:
            st.write("**Kedudukan Kategori Kelas (Leaderboard)**")
            sorted_freq = freq.sort_values(ascending=False)
            
            for rank, (char, count) in enumerate(sorted_freq.items()):
                pct = (count / len(analysis_df)) * 100 if len(analysis_df) > 0 else 0
                medal = "🏆" if rank == 0 else "🥈" if rank == 1 else "🥉" if rank == 2 else "•"
                color = riasec_details[char]['color']
                bg_color = riasec_details[char]['bg_color']
                
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; background-color: {bg_color}; padding: 12px; margin-bottom: 8px; border-radius: 10px; border-left: 5px solid {color}; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                        <span style="font-weight: bold; color: #1e293b;">{medal} {char} - {riasec_details[char]['name']}</span>
                        <span style="background-color: white; border: 1px solid {color}; padding: 2px 10px; border-radius: 20px; font-size: 0.95em; font-weight: bold; color: {color};">
                            {count} Murid ({pct:.0f}%)
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            dominant_char = sorted_freq.index[0]
            sec_dominant_char = sorted_freq.index[1]
            st.success(f"💡 **Rumusan Profil Kelas:** Majoriti murid kelas {selected_analysis_class} mempunyai ciri **{riasec_details[dominant_char]['name']} ({dominant_char})** sebagai kecenderungan utama mereka, dan di tempat kedua adalah **{riasec_details[sec_dominant_char]['name']} ({sec_dominant_char})**!")

# ==================== TAB 3: URUS DATABASE ====================
with tab_urus:
    st.markdown("<h3 style='color: #1e3a8a;'>Urus Database & Muat Naik CSV</h3>", unsafe_allow_html=True)
    st.info("💡 **Muat Naik Mudah:** Anda boleh memuat naik fail CSV psikometrik yang dieksport terus daripada sistem SePKM sekolah anda tanpa sebarang perubahan format!")
    
    col_upload1, col_upload2 = st.columns(2)
    
    with col_upload1:
        st.markdown("<div style='background-color: #ECFDF5; border: 1px solid #A7F3D0; padding: 20px; border-radius: 12px;'>", unsafe_allow_html=True)
        st.markdown("#### 🟢 Muat Naik Kelas 5 Amanah")
        amanah_upload = st.file_uploader("Pilih fail CSV untuk 5 Amanah", type=['csv'], key="upload_amanah")
        if amanah_upload is not None:
            parsed_amanah = parse_psychometric_csv(amanah_upload, "5 Amanah")
            if parsed_amanah:
                st.session_state.students_db = st.session_state.students_db[st.session_state.students_db['class'] != "5 Amanah"]
                st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame(parsed_amanah)], ignore_index=True)
                st.success(f"✅ Berjaya memproses {len(parsed_amanah)} murid bagi 5 Amanah!")
                st.rerun()
            else:
                st.error("Ralat memproses fail! Pastikan fail anda mengandungi format data SePKM.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_upload2:
        st.markdown("<div style='background-color: #FEF3C7; border: 1px solid #FCD34D; padding: 20px; border-radius: 12px;'>", unsafe_allow_html=True)
        st.markdown("#### 🟡 Muat Naik Kelas 5 Tabligh")
        tabligh_upload = st.file_uploader("Pilih fail CSV untuk 5 Tabligh", type=['csv'], key="upload_tabligh")
        if tabligh_upload is not None:
            parsed_tabligh = parse_psychometric_csv(tabligh_upload, "5 Tabligh")
            if parsed_tabligh:
                st.session_state.students_db = st.session_state.students_db[st.session_state.students_db['class'] != "5 Tabligh"]
                st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame(parsed_tabligh)], ignore_index=True)
                st.success(f"✅ Berjaya memproses {len(parsed_tabligh)} murid bagi 5 Tabligh!")
                st.rerun()
            else:
                st.error("Ralat memproses fail! Pastikan fail anda mengandungi format data SePKM.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("---")
    
    col_form, col_list = st.columns([1, 2])
    
    with col_form:
        st.markdown("<h4 style='color: #1e3a8a;'>Daftar/Edit Murid (Manual)</h4>", unsafe_allow_html=True)
        with st.form("add_student_form", clear_on_submit=True):
            new_name = st.text_input("Nama Penuh Murid").upper().strip()
            new_class = st.selectbox("Kelas Murid", ["5 Sidiq", "5 Amanah", "5 Tabligh"])
            
            st.write("**Markah Setiap Tret (0 - 30)**")
            r_score = st.number_input("R - Realistik", min_value=0, max_value=30, value=0)
            i_score = st.number_input("I - Investigatif", min_value=0, max_value=30, value=0)
            a_score = st.number_input("A - Artistik", min_value=0, max_value=30, value=0)
            s_score = st.number_input("S - Sosial", min_value=0, max_value=30, value=0)
            e_score = st.number_input("E - Enterprising", min_value=0, max_value=30, value=0)
            k_score = st.number_input("K - Konvensional", min_value=0, max_value=30, value=0)
            
            submitted = st.form_submit_with_button("💾 Simpan Rekod Murid")
            
            if submitted:
                if not new_name:
                    st.error("Nama murid tidak boleh dibiarkan kosong!")
                else:
                    new_student = {
                        "id": f"manual_{len(st.session_state.students_db) + 1}_{new_name[:5]}",
                        "name": new_name,
                        "class": new_class,
                        "R": r_score,
                        "I": i_score,
                        "A": a_score,
                        "S": s_score,
                        "E": e_score,
                        "K": k_score
                    }
                    st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame([new_student])], ignore_index=True)
                    st.success(f"Murid '{new_name}' berjaya didaftarkan!")
                    st.rerun()

    with col_list:
        st.markdown("<h4 style='color: #1e3a8a;'>Senarai Database Semasa</h4>", unsafe_allow_html=True)
        filter_table_class = st.selectbox("Tapis Paparan Kelas", ["Semua", "5 Sidiq", "5 Amanah", "5 Tabligh"])
        
        if filter_table_class == "Semua":
            table_df = df
        else:
            table_df = df[df['class'] == filter_table_class]
            
        st.dataframe(
            table_df[['name', 'class', 'R', 'I', 'A', 'S', 'E', 'K', 'Kod']],
            column_config={
                "name": "Nama Murid",
                "class": "Kelas",
                "Kod": "Kod Tiga Huruf"
            },
            use_container_width=True,
            hide_index=True
        )
        
        if st.button("🚨 Padam Semua & Reset ke Asal"):
            st.session_state.students_db = pd.DataFrame(default_students)
            st.success("Database berjaya di-reset ke asal (Hanya data 5 Sidiq)!")
            st.rerun()
