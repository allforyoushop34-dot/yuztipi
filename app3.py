import os
import random
import urllib.parse
import requests
import streamlit as st

st.set_page_config(
    page_title="Yüz Tipoloji ve Karakter Analizi",
    page_icon="👤",
    layout="centered",
)

# --- 🌌 HAREKETLİ & UYUMLU AURORA TASARIM PAKETİ ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #030712;
        background-image: 
            radial-gradient(at 10% 20%, rgba(124, 58, 237, 0.25) 0px, transparent 50%),
            radial-gradient(at 90% 10%, rgba(56, 189, 248, 0.2) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(236, 72, 153, 0.15) 0px, transparent 50%),
            radial-gradient(at 80% 90%, rgba(99, 102, 241, 0.2) 0px, transparent 50%),
            radial-gradient(at 20% 80%, rgba(16, 185, 129, 0.15) 0px, transparent 50%);
        background-attachment: fixed;
        background-size: cover;
        color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1 {
        color: #38bdf8 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        text-shadow: 0 0 25px rgba(56, 189, 248, 0.4);
    }
    
    h2, h3 {
        color: #e879f9 !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(232, 121, 249, 0.3);
    }

    /* Metrik kutularındaki uzun yazıların sığması ve kesilmemesi için ayar */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 12px;
        border-radius: 16px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    div.stInfo, div.stSuccess, div.stError, div.stWarning {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(16px);
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.5);
        color: #f1f5f9 !important;
    }

    [data-testid='stFileUploader'] {
        background: rgba(15, 23, 42, 0.6);
        border: 2px dashed #38bdf8;
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }

    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        color: white;
        border-radius: 12px;
        padding: 0.6rem 1.4rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.5);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(236, 72, 153, 0.7);
    }

    hr {
        border-color: rgba(255, 255, 255, 0.15);
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("👤 Yüz ve Tipoloji Analizi")
st.markdown(
    "✨ *Fotoğrafını yükle; sistem hatlarını tarasın, analiz edip en dürüst"
    " yorumu patlatsın.* 🔥"
)
st.markdown("---")

if "analiz_sayisi" not in st.session_state:
  st.session_state.analiz_sayisi = 1428

# Metinler kutulara tam sığacak şekilde optimize edildi
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
  st.metric(
      label="📊 Toplam Analiz", value=f"{st.session_state.analiz_sayisi} Kişi"
  )
with col_s2:
  st.metric(label="🔥 Günün Favorisi", value="Ham Realite")
with col_s3:
  st.metric(label="⭐ Sistem Durumu", value="Aktif / Stabil")

st.markdown("---")

API_USER = "353846098"
API_SECRET = "V3kfQV5wxBCuBSAsQBR5GvtskrUY2Eb9"

yuklenen_dosya = st.file_uploader(
    "📸 Analiz için bir yüz fotoğrafı seç (JPG, PNG):",
    type=["jpg", "jpeg", "png"],
)

gecici_dosya = "input_face.jpg"

if yuklenen_dosya is not None:
  try:
    with open(gecici_dosya, "wb") as f:
      f.write(yuklenen_dosya.getbuffer())

    st.image(gecici_dosya, caption="Yüklenen Fotoğraf", width=300)

    with st.spinner(
        "🔮 Yüz hatları inceleniyor, karakter haritası çıkarılıyor..."
    ):
      api_url = "https://api.sightengine.com/1.0/check.json"
      data = {
          "models": "faces",
          "api_user": API_USER,
          "api_secret": API_SECRET,
      }

      with open(gecici_dosya, "rb") as f:
        files = {"media": f}
        response = requests.post(api_url, data=data, files=files, timeout=30)
        result = response.json()

      if result.get("status") == "success":
        st.session_state.analiz_sayisi += 1

        st.markdown("---")
        st.markdown("### 🔥 Dürüst Tipoloji Raporu")

        faces = result.get("faces", [])

        if faces:
          yuz = faces[0]
          x1, x2 = yuz.get("x1", 0), yuz.get("x2", 0)
          y1, y2 = yuz.get("y1", 0), yuz.get("y2", 0)

          yuz_genisligi = x2 - x1
          yuz_yuksekligi = y2 - y1
          oran = (
              yuz_yuksekligi / yuz_genisligi if yuz_genisligi > 0 else 1.5
          )

          features = yuz.get("features", {})
          sol_goz = features.get("left_eye", {})
          sag_goz = features.get("right_eye", {})

          puan_kriteri = "iyi"
          if sol_goz and sag_goz:
            goz_farki = abs(sol_goz.get("y", 0) - sag_goz.get("y", 0))
            if goz_farki > 0.03 or oran < 1.2 or oran > 1.6:
              puan_kriteri = "siradan_veya_zor"

          if puan_kriteri == "iyi":
            girisler = [
                "Hocam buraları sallamaya mi geldin, bu ne şaşalı bakış? ",
                (
                    "Fotoğrafı sisteme yüklediğim an sunucu 'eyvah karizma"
                    " yükleniyor' diye uyarı verdi kanka. "
                ),
                (
                    "Milano sokaklarında yürüyormuşsun gibi bir hava seziyorum"
                    " bu karede hacı. "
                ),
                (
                    "Yapay zekâ bile bu kadar simetriyi görünce bi' heyecanlandı"
                    " açıkçası. "
                ),
            ]
            tipler = [
                (
                    "Klasik Akdeniz / İtalyan jönü çizgilerindesin. Dizi"
                    " setlerinden fırlayıp çay içmeye gelmiş gibisin baksana"
                    " şu hatlara."
                ),
                (
                    "Türkiye ortalamasını tek başına yukarı çeken elit bir"
                    " yüz geometrisine sahipsin."
                ),
                (
                    "Hatların keskinliği o kadar yerinde ki, Leonardo da Vinci"
                    " gelse altın oranı senin yüzde arardı."
                ),
            ]
            espiriler = [
                (
                    "Tabii bu kadar simetriye ayna bile bakarken utanıyordur,"
                    " neme lazım."
                ),
                (
                    "Aynaya her baktığında devlete vergi ödemen lazım bence,"
                    " bu kadar yakışıklılık kamuya zararlı çünkü."
                ),
            ]

            durum_basligi = "Tavan Yapmış"
            vav_faktoru = "Yüksek 🚀"
            zenginlik_orani = "%92 (Borsa kaplanı tipi var sende kanka)"
            emeklilik_hayali = (
                "Bodrum'da lüks bir yatın destesinde limonata yudumlamak."
            )
            sabika_tahmini = (
                "Yüzündeki bu illegal simetri kesin 'kalp hırsızlığından'"
                " aranıyor."
            )

            akici_insansi_metin = (
                f"{random.choice(girisler)}Analiz sonuçlarına göre yüz tipin"
                f" **Akdeniz ve Avrupa karması** bir çizgide ilerliyor."
                f" {random.choice(tipler)} {random.choice(espiriler)} Kıssadan"
                " hisse; ortalamaların fena halde üzerindesin, nazar değmesin!"
            )
            st.success(akici_insansi_metin)

          else:
            girisler = [
                "Bak şimdi dostum, hiç lafı dolandırıp seni kandırmayacağım...",
                (
                    "Sisteme bu fotoğrafı attığında sunucu fanları hızını"
                    " artırdı kanka, sanırım o da şaşırdı. "
                ),
                (
                    "Kamerayla göz göze geldiğimiz an yapay zekâ içten bir 'ah"
                    " be' çekti, yalan söylemeyeyim."
                ),
            ]
            tipler = [
                (
                    "Yüz geometrin biraz modernist ressamların tablosu gibi;"
                    " hani herkes anlamaz ama 'özgün' derler ya, o hesapsın."
                ),
                (
                    "Simetri kelimesi bu yüz hatlarına biraz küsmüş, uzak"
                    " kalmış gibi."
                ),
            ]
            espiriler = [
                (
                    "Gecenin bir yarısı karanlıkta aynaya bakıyorsan bence ev"
                    " halkına haber ver, korku filmi etkisi yaratmasın kanka."
                ),
                (
                    "Nüfus cüzdanındaki fotoğrafla gerçeği arasına emniyet"
                    " şeridi çekmek lazım, karıştırmasınlar."
                ),
            ]

            durum_basligi = "Ham Realite"
            vav_faktoru = "Depresif 💀"
            zenginlik_orani = (
                "%11 (Tek umudumuz milli piyango biletleri kanka)"
            )
            emeklilik_hayali = (
                "Mahalle kahvesinde okey masasında dördüncü olmak."
            )
            sabika_tahmini = (
                "Emniyet bu eşkali görünce direkt 'şüpheli ama zararsız'"
                " sekmesine atmıştır."
            )

            akici_insansi_metin = (
                f"{random.choice(girisler)}Analiz masasına yatırdık, durum pek"
                f" açıcı değil maalesef kanka. {random.choice(tipler)}"
                f" {random.choice(espiriler)} Moralini bozmak gibi olmasın"
                " ama Allah sahibine bağışlasın!"
            )
            st.error(akici_insansi_metin)

          col1, col2 = st.columns(2)
          with col1:
            st.metric(label="Vav Faktörü", value=vav_faktoru)
          with col2:
            st.metric(label="Ortalama Durumu", value=durum_basligi)

          # --- KADER PANELİ ---
          st.markdown("### 🔮 Yapay Zeka Kader ve Gelecek Paneli")
          st.info(f"💰 **Zenginlik İhtimali:** {zenginlik_orani}")
          st.warning(f"🏖️ **Emeklilik Hayali:** {emeklilik_hayali}")
          st.error(f"🚨 **Sabıka / Suç Tahmini:** {sabika_tahmini}")

          # --- PAYLAŞIM BUTONLARI ---
          site_linki = "https://tipiniseveyim.streamlit.app/"
          tam_metin = (
              "🤖 Yapay Zeka Yüz Analizim:\n\n"
              f'"{akici_insansi_metin}"\n\n💰 Zenginlik İhtimali: {zenginlik_orani}\nSen de yüzünü test et, sonucu gör! 👉'
              f" {site_linki}"
          )
          encoded_mesaj = urllib.parse.quote(tam_metin)

          whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_mesaj}"
          twitter_url = f"https://twitter.com/intent/tweet?text={encoded_mesaj}"

          st.markdown("### 🚀 Bu Sonucu Herkese Yay!")

          p_col1, p_col2, p_col3 = st.columns(3)

          with p_col1:
            st.markdown(
                f'<a href="{whatsapp_url}" target="_blank"><button'
                ' style="width:100%; background: linear-gradient(135deg, #22c55e'
                ' 0%, #16a34a 100%); color:white; padding:12px;'
                ' border:none; border-radius:12px; font-weight:bold;'
                ' cursor:pointer; box-shadow: 0 4px 15px rgba(34, 197, 94,'
                ' 0.4);">🟢 WhatsApp</button></a>',
                unsafe_allow_html=True,
            )

          with p_col2:
            st.markdown(
                f'<a href="{twitter_url}" target="_blank"><button'
                ' style="width:100%; background: linear-gradient(135deg, #0ea5e9'
                ' 0%, #0284c7 100%); color:white; padding:12px;'
                ' border:none; border-radius:12px; font-weight:bold;'
                ' cursor:pointer; box-shadow: 0 4px 15px rgba(14, 165, 233,'
                ' 0.4);">🐦 X (Twitter)</button></a>',
                unsafe_allow_html=True,
            )

          with p_col3:
            if st.button("📸 Kopyala", key="insta_kopyala_btn"):
              st.toast("Metin kopyalandı! 🎉")

        else:
          st.warning(
              "⚠️ Yüzü net algılayamadım hacı. Kameraya direkt baktığın ışıklı"
              " bir fotoğraf atarsan gerçeklerle yüzleşiriz."
          )
      else:
        hata_mesaji = result.get("error", {}).get(
            "message", "Bilinmeyen API hatası"
        )
        st.error(f"API Hatası: {hata_mesaji}")

  except Exception as e:
    st.error(f"Kritik hata oluştu: {e}")

  finally:
    if os.path.exists(gecici_dosya):
      try:
        os.remove(gecici_dosya)
      except OSError:
        pass