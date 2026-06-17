import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-RIASEC SKOR",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

riasec_details = {
    'R': {
        'name': 'Realistik',
        'trait': 'Praktikal & Fizikal',
        'desc': 'Gemar tugasan fizikal, menggunakan instrumen, membaiki alatan mekanikal atau mesin. Lebih gemar kerja praktikal di luar pejabat.',
        'careers': 'Jurutera, Mekanik, Ahli Pertanian, Juruteknik',
        'color': 'red'
    },
    'I': {
        'name': 'Investigatif',
        'trait': 'Saintifik & Saintis',
        'desc': 'Gemar tugasan berfikir, membuat penyelidikan, menganalisis masalah yang kompleks, gemar membaca topik teknikal serta bidang perubatan.',
        'careers': 'Doktor, Ahli Kimia, Penganalisis Data, Penyelidik',
        'color': 'blue'
    },
    'A': {
        'name': 'Artistik',
        'trait': 'Kreatif & Bebas',
        'desc': 'Menghargai kebebasan berekspresi, kreatif, artistik, suka melukis, muzik, penulisan kreatif atau rekaan grafik.',
        'careers': 'Pereka Grafik, Arkitek, Penulis, Pemuzik, Pelakon',
        'color': 'purple'
    },
    'S': {
        'name': 'Sosial',
        'trait': 'Membantu & Prihatin',
        'desc': 'Prihatin kebajikan orang ramai, gemar mengajar, merawat pesakit, memberi kaunseling serta selesa berinteraksi dalam kumpulan.',
        'careers': 'Guru, Kaunselor, Pegawai HR, Jururawat, Pekerja Sosial',
        'color': 'green'
    },
    'E': {
        'name': 'Enterprising',
        'trait': 'Berdaya Usaha & Pemimpin',
        'desc': 'Sifat kepimpinan kuat, berbakat memujuk, mengurus projek perniagaan, bercita-cita tinggi, mahir berucap di hadapan umum.',
        'careers': 'Usahawan, Pengarah Syarikat, Pengurus Jualan, Peguam',
        'color': 'orange'
    },
    'K': {
        'name': 'Konvensional',
        'trait': 'Sistematik & Berstruktur',
        'desc': 'Tersusun, mementingkan kekemasan, teratur dalam menguruskan data, rekod, tugasan perkeranian atau perakaunan.',
        'careers': 'Akauntan, Pentadbir Fail, Setiausaha, Penganalisis Kewangan',
        'color': 'green'
    }
}

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

def get_riasec_code(row):
    scores = {'R': row['R'], 'I': row['I'], 'A': row['A'], 'S': row['S'], 'E': row['E'], 'K': row['K']}
    sorted_scores = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return "".join([item[0] for item in sorted_scores[:3]])

df = st.session_state.students_db.copy()
df['Kod'] = df.apply(get_riasec_code, axis=1)

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🎓 E-RIASEC SKOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1em; color: #4B5563;'>Sistem Carian & Analisis Kod Kerjaya Murid (5 Sidiq, 5 Amanah, 5 Tabligh)</p>", unsafe_allow_html=True)
st.write("---")

tab_carian, tab_statistik, tab_urus = st.tabs([
    "🔍 Carian Individu", 
    "📊 Statistik Kelas", 
    "⚙️ Urus Database"
])

with tab_carian:
    st.subheader("Carian Profil Kerjaya Murid")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_class = st.selectbox("Pilih Kelas", ["5 Sidiq", "5 Amanah", "5 Tabligh"], key="search_class")
    
    class_df = df[df['class'] == selected_class].sort_values(by="name")
    
    with col2:
        if not class_df.empty:
            selected_student_name = st.selectbox("Nama Murid", class_df['name'].tolist(), key="search_student")
        else:
            st.selectbox("Nama Murid", ["-- Tiada Murid Berdaftar --"], disabled=True)
            selected_student_name = None
            
    if selected_student_name and selected_student_name != "-- Tiada Murid Berdaftar --":
        student_data = class_df[class_df['name'] == selected_student_name].iloc[0]
        code = student_data['Kod']
        
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1e293b, #0f172a); padding: 25px; border-radius: 15px; color: white; margin-bottom: 25px;">
                <span style="background-color: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); padding: 4px 12px; border-radius: 20px; font-size: 0.8em; font-weight: bold; color: #93c5fd;">
                    📍 {student_data['class']}
                </span>
                <h2 style="margin: 10px 0 5px 0; color: white;">{student_data['name']}</h2>
                <p style="color: #cbd5e1; margin: 0; font-size: 0.9em;">Keputusan Profil Ujian Minat Kerjaya RIASEC</p>
                <div style="margin-top: 15px; background: rgba(255, 255, 255, 0.1); display: inline-block; padding: 10px 25px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.2);">
                    <span style="font-size: 0.8em; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; display: block;">KOD TIGA HURUF UTAMA</span>
                    <strong style="font-size: 2.2em; color: #fde047; font-family: sans-serif;">{code}</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.write("### 🔍 Huraian Personaliti Kod Kerjaya:")
        cols_cards = st.columns(3)
        for idx, char in enumerate(code):
            detail = riasec_details[char]
            with cols_cards[idx]:
                st.markdown(
                    f"""
                    <div style="background-color: white; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); height: 100%;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                            <span style="background-color: #3b82f6; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.1em;">
                                {char}
                            </span>
                            <div>
                                <h4 style="margin: 0; color: #1e293b;">{detail['name']}</h4>
                                <small style="color: #64748b; font-weight: bold; text-transform: uppercase; font-size: 0.75em;">{detail['trait']}</small>
                            </div>
                        </div>
                        <p style="font-size: 0.85em; color: #475569; line-height: 1.5; margin-bottom: 15px;">{detail['desc']}</p>
                        <div style="background-color: #f8fafc; padding: 10px; border-radius: 8px; border: 1px dashed #cbd5e1;">
                            <span style="font-size: 0.75em; color: #94a3b8; font-weight: bold; display: block; margin-bottom: 2px;">CADANGAN KERJAYA:</span>
                            <span style="font-size: 0.85em; color: #2563eb; font-weight: bold;">{detail['careers']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        st.write("---")
        st.write("### 📈 Markah Penuh Mengikut Tret")
        
        col_pb1, col_pb2 = st.columns(2)
        traits = [('R', 'Realistik'), ('I', 'Investigatif'), ('A', 'Artistik'), ('S', 'Sosial'), ('E', 'Enterprising'), ('K', 'Konvensional')]
        
        for index, (char, name) in enumerate(traits):
            score = int(student_data[char])
            percentage = score / 30.0
            
            target_col = col_pb1 if index < 3 else col_pb2
            with target_col:
                st.write(f"**{char} - {name}** ({score}/30)")
                st.progress(percentage)
                
    else:
        st.info("💡 Sila pilih kelas terlebih dahulu, kemudian klik pada nama murid untuk memulakan analisis.")

with tab_statistik:
    st.subheader("Taburan Kecenderungan Kelas")
    selected_analysis_class = st.selectbox("Pilih Kelas Untuk Analisis", ["5 Sidiq", "5 Amanah", "5 Tabligh"], key="analysis_class")
    
    analysis_df = df[df['class'] == selected_analysis_class]
    
    if analysis_df.empty:
        st.warning(f"⚠️ Tiada data tersedia untuk kelas {selected_analysis_class}. Sila isi maklumat murid di tab 'Urus Database'.")
    else:
        analysis_df['Dominan'] = analysis_df['Kod'].str[0]
        freq = analysis_df['Dominan'].value_counts()
        
        for char in ['R', 'I', 'A', 'S', 'E', 'K']:
            if char not in freq:
                freq[char] = 0
        
        freq = freq.reindex(['R', 'I', 'A', 'S', 'E', 'K'])
        col_chart, col_details = st.columns([3, 2])
        
        with col_chart:
            st.write("**Carta Taburan Kod Dominan Utama (Huruf Pertama)**")
            chart_data = pd.DataFrame({
                'Kecenderungan': ['Realistik (R)', 'Investigatif (I)', 'Artistik (A)', 'Sosial (S)', 'Enterprising (E)', 'Konvensional (K)'],
                'Jumlah Murid': freq.values
            })
            st.bar_chart(data=chart_data, x='Kecenderungan', y='Jumlah Murid', color='#1E3A8A')
            
        with col_details:
            st.write("**Leaderboard Kategori Kelas**")
            sorted_freq = freq.sort_values(ascending=False)
            
            for rank, (char, count) in enumerate(sorted_freq.items()):
                pct = (count / len(analysis_df)) * 100
                medal = "🏆" if rank == 0 else "🥈" if rank == 1 else "🥉" if rank == 2 else "•"
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; background-color: #f8fafc; padding: 10px; margin-bottom: 8px; border-radius: 8px; border-left: 4px solid #1e3a8a;">
                        <span style="font-weight: bold;">{medal} {char} - {riasec_details[char]['name']}</span>
                        <span><b>{count} Murid</b> ({pct:.0f}%)</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            dominant_char = sorted_freq
