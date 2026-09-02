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

# --- Sosyal Medya Önizleme (Open Graph) Etiketleri ---
st.markdown(
    """
    <head>
        <meta property="og:title" content="Yüz Tipoloji ve Karakter Analizi">
        <meta property="og:description" content="Yüzünü tarat, yapay zekanın hakkındaki en dürüst ve eğlenceli yorumunu keşfet!">
        <meta property="og:image" content="https://tipiniseveyim.streamlit.app/preview.jpg">
        <meta property="og:url" content="https://tipiniseveyim.streamlit.app/">
        <meta name="twitter:card" content="summary_large_image">
    </head>
""",
    unsafe_allow_html=True,
)

st.title("👤 Yüz ve Tipoloji Analizi - Cesaretin Var Mı ?")
st.markdown(
    "Fotoğrafını yükle ; sistem hatlarını tarasın, analiz edip en dürüst"
    " yorumu patlatsın 🔥 "
)
st.markdown("---")

# --- SAYAÇ / İSTATİSTİK BAŞLANGICI ---
if "analiz_sayisi" not in st.session_state:
  st.session_state.analiz_sayisi = 1428

col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
  st.metric(
      label="📊 Toplam Analiz", value=f"{st.session_state.analiz_sayisi} Kişi"
  )
with col_s2:
  st.metric(label="🔥 Günün Favorisi", value="Ham Realite")
with col_s3:
  st.metric(label="⭐ Sistem Durumu", value="Stabil / Kritik")

st.markdown("---")
# ------------------------------------

API_USER = "353846098"
API_SECRET = "V3kfQV5wxBCuBSAsQBR5GvtskrUY2Eb9"

if API_USER == "BURAYA_SIGHTENGINE_USER_YAZIN":
  st.warning(
      "⚠️ Lütfen kod içerisindeki API_USER and API_SECRET alanlarına kendi"
      " Sightengine bilgilerinizi girin."
  )

yuklenen_dosya = st.file_uploader(
    "Bir yüz fotoğrafı seç (JPG, PNG):", type=["jpg", "jpeg", "png"]
)

if yuklenen_dosya is not None:
  gecici_dosya = "input_face.jpg"

  try:
    with open(gecici_dosya, "wb") as f:
      f.write(yuklenen_dosya.getbuffer())

    st.image(gecici_dosya, caption="Yüklenen Fotoğraf", use_container_width=True)

    with st.spinner(
        "Yüz hatları inceleniyor, karakter haritası çıkarılıyor..."
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
                    "Raporu çıkarırken kahvemden bir yudum aldım, ekranın"
                    " parıltısı gözümü aldı neredeyse. "
                ),
                (
                    "Milano sokaklarında yürüyormuşsun gibi bir hava seziyorum"
                    " bu karede hacı. "
                ),
                (
                    "Ekranı açtığım gibi ortamın havası değişti, hayırdır"
                    " müdür? "
                ),
                (
                    "Yapay zekâ bile bu kadar simetriyi görünce bi' heyecanlandı"
                    " açıkçası. "
                ),
                (
                    "Kanka bu karede tuhaf bir Hollywood jönü esintisi var, fark"
                    " etmedim sanma. "
                ),
                (
                    "Işık mı vurmuş yoksa doğuştan mı böyle parlıyorsun,"
                    " çözemedim valla. "
                ),
                (
                    "Sisteme bu fotoğrafı vermek, güneşe karşı namaz kılmak gibi"
                    " bişi oldu dostum. "
                ),
                (
                    "Ortamı fena yakmışsın, itiraf et bu kare için özel mi"
                    " uğraştın? "
                ),
                (
                    "Kamera lensi bile sana bakarken biraz utandı sanki, o"
                    " derece. "
                ),
                (
                    "Hacı sen buraların fazlasısın, bu yüz hatları uluslararası"
                    " ligde oynar. "
                ),
                (
                    "Analiz tuşuna basar basmaz sistem otomatik olarak ayağa"
                    " kalktı resmen. "
                ),
                ("Böyle simetri her babayiğide nasip olmaz, maşallahı var. "),
                (
                    "Ekranın öteki tarafındaki enerjiyi buraya kadar hissettik"
                    " valla kanka. "
                ),
            ]

            tipler = [
                (
                    "Klasik Akdeniz / İtalyan jönü çizgilerindesin. Dizi"
                    " setlerinden fırlayıp çay içmeye gelmiş gibisin baksana"
                    " şu hatlara."
                ),
                (
                    "Kuzeyli ve keskin konturlara sahip nadir tiplerdensin."
                    " Hatlardaki simetri neredeyse cetvelle çizilmiş gibi."
                ),
                (
                    "Türkiye ortalamasını tek başına yukarı çeken elit bir"
                    " yüz geometrisine sahipsin. Mahallede 'bu adamda iş var'"
                    " dedirten cinsten."
                ),
                (
                    "Fransız film festivallerinde ödül toplayacak o melankolik"
                    " ve karizmatik bakış açısı sende mevcut."
                ),
                (
                    "Hatların keskinliği o kadar yerinde ki, Leonardo da Vinci"
                    " gelse altın oranı senin yüzde arardı."
                ),
                (
                    "Sportif ve dinç bir çene yapısı var; direkt 'ben bu"
                    " hayatta her şeyi başarırmışım' havası veriyor."
                ),
                (
                    "Kusursuza yakın oranlar... İnsan bakınca kendine"
                    " güvensizlik geliyor, öyle net bir tip."
                ),
                (
                    "Hem mert hem de modern jön, tam bir jenerik dizi karakteri"
                    " yüz hatları diyebiliriz."
                ),
                (
                    "Göz hizası ve elmacık kemiği uyumu adeta bir mimari yapı"
                    " gibi kusursuz oturmuş."
                ),
                (
                    "Kariyer sahibi, güven veren ve ortama girince dikkatleri"
                    " üzerine çeken Alpha tipi."
                ),
                (
                    "İspanyol matadorlarını andıran o keskin ve delikanlı"
                    " yüz hatlarına sahipsin kanka."
                ),
                (
                    "Doğuştan filtreli gibi geziyorsun ortada, teknolojiye"
                    " ihtiyacın yok maşallah."
                ),
                (
                    "Yüz hatlarındaki o otoriter ama bir o kadar sempatik denge"
                    " tam kartvizitlik."
                ),
                (
                    "Hollywood'un aradığı o 'cool' ama samimi komşu çocuğu"
                    " profilini tam 12'den yakalamışsın."
                ),
                (
                    "Çizgiler o kadar net ve oturaklı ki, bakınca 'işte lider"
                    " kumaşı' dedirtiyor."
                ),
            ]

            espiriler = [
                (
                    "Tabii bu kadar simetriye ayna bile bakarken utanıyordur,"
                    " neme lazım."
                ),
                (
                    "Nüfus kağıdına fotoğraf koymasan da olur, sistem seni zaten"
                    " doğrudan 'VIP' statüsüne aldı."
                ),
                (
                    "Çevrendekiler 'bu tip bizde neden yok' diye iç çekiyordur,"
                    " şimdiden söylemiş olayım."
                ),
                (
                    "Aynaya her baktığında devlete vergi ödemen lazım bence,"
                    " bu kadar yakışıklılık kamuya zararlı çünkü."
                ),
                (
                    "Sokakta yürürken arkandan 'acaba dizi oyuncusu mu' diye"
                    " bakanların sayısı bence seksen milyonu geçer."
                ),
                (
                    "Fotoğrafını cihaza koyarken fanlar bile 'nefes alalım'"
                    " diye yavaşladı resmen."
                ),
                (
                    "Allah için özenmiş de yaratmış derler ya, tam olarak"
                    " o masalın başrolüsün."
                ),
                (
                    "Kanka bu yüz hatlarıyla milletin bahtını kapatıyorsun,"
                    " biraz insaf etseydin keşke."
                ),
                (
                    "Kızlar falan buraları okuyorsa şimdiden geçmiş olsun,"
                    " kalp atışları hızlanmıştır."
                ),
                (
                    "Kusursuzluk başa bela derler, umarım bu havalı"
                    " hallerinden başın dönmüyordur."
                ),
                (
                    "Sistemin şarjı bitti senin yüzünden, bu kadar elektrik"
                    " fazla geldi makineye."
                ),
                (
                    "Kanka ID kartını falan çıkartırken memurlar bile onay"
                    " verirken iki kez düşünüyordur."
                ),
                (
                    "Girdiğin ortamlarda 'arkadaş tek başına havayı"
                    " değiştiriyor' diyorlardır kesin."
                ),
                (
                    "Nazar boncuğunu cebinde taşı, bu simetriye göz"
                    " değmemesi imkansız çünkü."
                ),
                (
                    "Güzellik yarışmasına girsen hakemler jüriliği bırakıp"
                    " seni alkışlar valla."
                ),
            ]

            durum_basligi = "Tavan Yapmış 🚀"
            vav_faktoru = "Yüksek / Çarpıcı"
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
                f" {random.choice(tipler)} Elmacık kemikleri ve bakış açısı tam"
                f" 'ben buradayım' diyor. {random.choice(espiriler)} Kıssadan"
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
                (
                    "Tarzın var ama yüz hatların biraz... şey, 'sanatsal' bir"
                    " boyutta takılıyor hacı. "
                ),
                (
                    "Fotoğrafı yükledikten sonra ekranın rengi bi' sarardı,"
                    " kendine gelmesi zaman aldı. "
                ),
                (
                    "Kanka bu kareyi analiz etmek biraz cesaret isterdi,"
                    " başardık çok şükür. "
                ),
                (
                    "Yapay zekânın sigortaları attı, 'bu ne biçim geometri' diye"
                    " isyan ediyor ekran. "
                ),
                (
                    "Hiç kusura bakma müdür, doğruları konuşmak boynumuzun"
                    " borcu. "
                ),
                (
                    "Görseli açtığımda ekran kendi kendine 'bunu da mı"
                    " görecektim' der gibi sesler çıkardı. "
                ),
                (
                    "Kanka bilerek mi bu kadar dramatik bir açı buldun,"
                    " çözemedim ki. "
                ),
                (
                    "Sistemin yapay zekâsı raporu yazarken iki kere mola"
                    " vermek zorunda kaldı. "
                ),
                (
                    "Hacı senden ricam bir daha bu kadar iddialı açılarla"
                    " yaklaşma kameraya. "
                ),
                (
                    "Raporu hazırlarken klavyem bile zorlanarak tuşlara bastı"
                    " valla. "
                ),
                (
                    "Bodoslama gerçeğe dalıyoruz hazırlıklı ol kanka, sakın"
                    " darılmaca gücenme yok. "
                ),
                (
                    "Kameranın lensi bile bu yükü kaldırmak için ekstradan"
                    " zorlandı sanki. "
                ),
            ]

            tipler = [
                (
                    "Yüz geometrin biraz modernist ressamların tablosu gibi;"
                    " hani herkes anlamaz ama 'özgün' derler ya, o hesapsın."
                ),
                (
                    "Simetri kelimesi bu yüz hatlarına biraz küsmüş, uzak"
                    " kalmış gibi. Türkiye ortalamasındasındır ama böyle"
                    " mahallenin en yorgun abisi modunda."
                ),
                (
                    "Avrupai tip dedikleri bu olsa gerek ama sanki Avrupa'nın"
                    " refah seviyesi yüksek yerleri değil de batık"
                    " kasabaları gibi kanka."
                ),
                (
                    "Çizgiler o kadar asimetrik ki, modern sanat galerisine"
                    " koysan kapıda kuyruk olur."
                ),
                (
                    "Hacı sen buraların insanı değilmişsin gibi, sanki uzay"
                    " boşluğundan random düşmüş bir tipolojin var."
                ),
                (
                    "Doğal bir otantikliğin var; hani köylerdeki 70'ler"
                    " albüm kapaklarından fırlamış gibi."
                ),
                (
                    "Yüz hatların o kadar iddialı ki, her sabah aynaya"
                    " baktığında kendi kendine 'bugün de hayattayız' diyorsundur"
                    " kesin."
                ),
                (
                    "Geometrik olarak dağınık bir imparatorluk gibisin; her"
                    " parça ayrı bir telden çalıyor."
                ),
                (
                    "Klasik tipin dışındasın, tamamen 'ben kendi kurallarım"
                    " olan bir insanım' temalı bir yüz."
                ),
                (
                    "Böyle biraz 'acıların çocuğu' esintili, melankolik ama"
                    " trajikomik bir duruş seziyorum."
                ),
                (
                    "Türkiye ortalamasının tam sınırındasın ama böyle"
                    " uçurumun kenarında yürüyen türden bir sınır."
                ),
                (
                    "Yüz hatlarındaki o spontane karışım, yapay zekâyı bile"
                    " 'bunu nasıl kategorize edeceğim' diye düşündürtüyor."
                ),
                (
                    "Estetik kuralları bu yüzü görünce mutfaktan su içmeye"
                    " gitmiş resmen kanka."
                ),
                (
                    "Karakteristik desek yalan olur, 'kendine has bir"
                    " felaket' desek daha doğru olur."
                ),
                (
                    "Hacı hatlar biraz yorgun, biraz da 'ne arıyorum ben"
                    " dünyada' der gibi bakıyor."
                ),
            ]

            espiriler = [
                (
                    "Gecenin bir yarısı karanlıkta aynaya bakıyorsan bence ev"
                    " halkına haber ver, korku filmi etkisi yaratmasın kanka."
                ),
                (
                    "Sevgilin varsa kıymetini bil, çünkü bu tipolojiyle sana"
                    " katlanması dünyevi bir mucize sayılır."
                ),
                (
                    "Estetik masasına yatarsan doktor ellerini havaya kaldırıp"
                    " 'kral bunu kurtaramayız' diyerek kaçabilir."
                ),
                (
                    "Nüfus cüzdanındaki fotoğrafla gerçeği arasına emniyet"
                    " şeridi çekmek lazım, karıştırmasınlar."
                ),
                (
                    "Kanka korku filmi seçmelerine falan katılsan, direkt"
                    " başrolde oynarsın, hiç masraf yapmazlar."
                ),
                (
                    "Aynalar seninle her sabah görüşürken psikolojik destek"
                    " alıyordur yeminle."
                ),
                (
                    "Allah sahibine bağışlasın diyeceğim ama sahibine de"
                    " biraz sabır versin."
                ),
                (
                    "Kanka yüzünün hatları ekonomi gibi; sürekli bir"
                    " düşüşte, istikrarı yakalayamadık."
                ),
                (
                    "Bu tipolojiyle sokağa çıkmak cesaret ister, tebrik"
                    " ederim valla büyük özgüven."
                ),
                (
                    "Polis çevirmesinde 'indir camı' dediklerinde memur"
                    " korkudan gaza basıp gidebilir kanka."
                ),
                (
                    "Kameraya filtre falan koyduysan acil o uygulamayı sil,"
                    " çünkü filtresiz hali cidden riskliymiş."
                ),
                (
                    "Komedi filmi çekmek isteseler seni arasalar başka"
                    " oyuncuya gerek kalmaz."
                ),
                (
                    "Gözler başka yere, burun başka memlekete bakıyor sanki;"
                    " koalisyon hükümeti gibi yüz."
                ),
                (
                    "Kanka moralini bozmak gibi olmasın ama bu hatlarla"
                    " Tinder'da match alman ancak hataya bakar."
                ),
                (
                    "Yapay zekâ raporu bitirince 'ben bu yükü kaldıramam'"
                    " deyip az kalsın kendini formatlıyordu."
                ),
            ]

            durum_basligi = "Hüzünlü / Ham Realite 💀"
            vav_faktoru = "Depresif / Tartışmalı"
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
                f" açıcı değil maalesef kanka. {random.choice(tipler)} Yani"
                f" evet, istatistiki olarak yaşıyorsun ama bu biraz 'zoraki'"
                f" bir ortalama olmuş. {random.choice(espiriler)} Moralini"
                " bozmak gibi olmasın ama Allah sahibine bağışlasın!"
            )
            st.error(akici_insansi_metin)

          col1, col2 = st.columns(2)
          with col1:
            st.metric(label="Vav Faktörü", value=vav_faktoru)
          with col2:
            st.metric(label="Ortalama Durumu", value=durum_basligi)

          # --- GELECEK SİMÜLASYONU VE KADER PANELİ ---
          st.markdown("### 🔮 Yapay Zeka Kader ve Gelecek Paneli")

          st.info(f"💰 **Zengin Olma İhtimali:** {zenginlik_orani}")
          st.warning(f"🏖️ **Emeklilik Hayali:** {emeklilik_hayali}")
          st.error(f"🚨 **Sabıka / Suç Tahmini:** {sabika_tahmini}")

          # --- PAYLAŞIM BUTONLARI ---
          site_linki = "https://tipiniseveyim.streamlit.app/"

          tam_metin = (
              "🤖 Yapay Zeka Yüz Analizim:\n\n"
              f'"{akici_insansi_metin}"\n\n💰 Zenginlik İhtimalim: {zenginlik_orani}\nSen de yüzünü test et, sonucu gör! 👉'
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
                ' style="width:100%; background-color:#25D366; color:white;'
                ' padding:10px; border:none; border-radius:5px; font-weight:bold;'
                ' cursor:pointer;">🟢 WhatsApp</button></a>',
                unsafe_allow_html=True,
            )

          with p_col2:
            st.markdown(
                f'<a href="{twitter_url}" target="_blank"><button'
                ' style="width:100%; background-color:#1DA1F2; color:white;'
                ' padding:10px; border:none; border-radius:5px; font-weight:bold;'
                ' cursor:pointer;">🐦 X (Twitter)</button></a>',
                unsafe_allow_html=True,
            )

          with p_col3:
            if st.button("📸 Instagram / Kopyala", key="insta_kopyala_btn"):
              st.toast(
                  "Metin kopyalandı! Instagram Hikayene veya TikTok'a"
                  " yapıştırabilirsin. 🎉"
              )

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