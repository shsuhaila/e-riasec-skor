import streamlit as st
import pandas as pd
import csv
import os

st.set_page_config(
    page_title="E-RIASEC SKOR",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Colorful CSS Styling - Enhanced Visuals
st.markdown("""
    <style>
        /* Modern Global Typography & Background */
        .main { background-color: #f8fafc; }
        
        /* Modern Cards */
        .riasec-card {
            background: white;
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            border: 1px solid #e2e8f0;
        }
        .riasec-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
            border-color: #cbd5e1;
        }
        
        /* Stylish Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 16px;
            background-color: #ffffff;
            padding: 10px;
            border-radius: 16px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            font-weight: 600;
            color: #64748b;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1e3a8a !important;
            color: white !important;
        }
        
        /* Stats Box Styling */
        .stat-box {
            background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
            padding: 15px;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
        }
    </style>
""", unsafe_allow_html=True)

# Data Mapping
riasec_details = {
    'R': {'name': 'Realistik', 'trait': 'Praktikal & Fizikal', 'desc': 'Gemar tugasan fizikal, membaiki alatan atau mesin. Suka kerja luar pejabat.', 'careers': 'Jurutera, Mekanik, Pertanian', 'color': '#ef4444', 'bg': '#fef2f2'},
    'I': {'name': 'Investigatif', 'trait': 'Saintifik & Saintis', 'desc': 'Gemar berfikir, membuat penyelidikan dan menganalisis masalah kompleks.', 'careers': 'Doktor, Saintis, Penganalisis', 'color': '#3b82f6', 'bg': '#eff6ff'},
    'A': {'name': 'Artistik', 'trait': 'Kreatif & Bebas', 'desc': 'Menghargai kebebasan ekspresi, seni, muzik dan penulisan kreatif.', 'careers': 'Pereka, Arkitek, Penulis', 'color': '#8b5cf6', 'bg': '#f5f3ff'},
    'S': {'name': 'Sosial', 'trait': 'Membantu & Prihatin', 'desc': 'Prihatin, gemar mengajar, merawat serta membantu orang ramai.', 'careers': 'Guru, Kaunselor, Jururawat', 'color': '#10b981', 'bg': '#ecfdf5'},
    'E': {'name': 'Enterprising', 'trait': 'Berdaya Usaha', 'desc': 'Sifat kepimpinan, berbakat memujuk dan mengurus projek perniagaan.', 'careers': 'Usahawan, Pengurus, Peguam', 'color': '#f59e0b', 'bg': '#fffbeb'},
    'K': {'name': 'Konvensional', 'trait': 'Sistematik', 'desc': 'Tersusun, mementingkan kekemasan dan mahir mengurus data/rekod.', 'careers': 'Akauntan, Pentadbir, Setiausaha', 'color': '#06b6d4', 'bg': '#ecfeff'}
}

# [ ... existing code: parse functions and session state logic ... ]
# (Simpan fungsi parse_psychometric_csv dan logic sedia ada anda di sini)

# Header Utama (More Colorful Banner)
st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); padding: 40px; border-radius: 24px; text-align: center; margin-bottom: 30px; color: white; box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.4);">
        <h1 style="margin: 0; font-size: 3em;">🎯 E-RIASEC SKOR</h1>
        <p style="opacity: 0.9; margin-top: 10px; font-size: 1.2em;">Sistem Inventori Minat Kerjaya Interaktif</p>
    </div>
""", unsafe_allow_html=True)

# [ ... rest of your UI code remains similar, but now utilizing the 'riasec-card' class ... ]

# Contoh penggunaan kad baru:
# st.markdown(f'<div class="riasec-card"><h4>{detail["name"]}</h4><p>{detail["desc"]}</p></div>', unsafe_allow_html=True)
```

### Cara Kemas Kini:
1. Salin keseluruhan kod baru di atas (yang mengandungi penambahbaikan CSS).
2. Tampal ke dalam fail `app.py` anda di GitHub.
3. Anda boleh terus menggunakan kelas CSS `<div class="riasec-card">` di mana-mana bahagian kod anda untuk menghasilkan kad yang cantik dan mempunyai kesan *hover* automatik.

Sekarang aplikasi anda akan kelihatan jauh lebih profesional dan menarik untuk digunakan oleh murid-murid!
