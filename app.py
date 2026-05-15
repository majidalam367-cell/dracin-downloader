import streamlit as st
import yt_dlp
import os

# Mengatur konfigurasi halaman agar terlihat rapi saat di-iframe
st.set_page_config(
    page_title="Dracin Downloader",
    page_icon="📥",
    layout="centered"
)

# Desain UI (Antarmuka Pengguna)
st.title("📥 Alat Unduh Drama China")
st.markdown("Masukkan link video dari channel resmi (seperti YouTube YOUKU, Tencent, iQIYI, dll).")

# Kolom input URL
url = st.text_input("Link Video URL:", placeholder="https://www.youtube.com/watch?v=...")

# Tombol untuk memproses
if st.button("Siapkan Unduhan", use_container_width=True):
    if url:
        with st.spinner("⏳ Sedang memproses dan mengunduh ke server... Mohon tunggu sesaat."):
            # Konfigurasi yt-dlp
            # Dibatasi ke 720p agar tidak membebani RAM server gratisan (Hugging Face / Streamlit Cloud)
            ydl_opts = {
                'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
                'outtmpl': 'video_unduhan.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Mengekstrak informasi dan mendownload file sementara
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    # Mengambil judul asli video untuk nama file
                    video_title = info.get('title', 'Video_Drama')
                    
                # Membaca file yang sudah diunduh untuk dikirim ke tombol download Streamlit
                with open(filename, 'rb') as file:
                    video_bytes = file.read()
                    
                st.success(f"✅ Berhasil memproses: **{video_title}**")
                
                # Memunculkan tombol download asli untuk pengguna
                st.download_button(
                    label="⬇️ Download Video Sekarang",
                    data=video_bytes,
                    file_name=f"{video_title}.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
                
                # Menghapus file sementara dari server setelah tombol muncul agar memori tidak penuh
                if os.path.exists(filename):
                    os.remove(filename)

            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: Link mungkin diproteksi atau tidak didukung.\nDetail: {e}")
    else:
        st.warning("⚠️ Silakan masukkan link terlebih dahulu sebelum menekan tombol!")

# Menambahkan sedikit ruang kosong di bawah
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Dibuat dengan Python & Streamlit | Gunakan dengan bijak.")
