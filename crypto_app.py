import streamlit as st
from cryptography.fernet import Fernet
from audio_recorder_streamlit import audio_recorder

# 1. إعدادات الصفحة (الاسم يظهر في المتصفح)
st.set_page_config(page_title="نظام تشفير | Abdulqader", page_icon="🔐", layout="centered")

# 2. لمسات جمالية للـ Header والواجهة
st.markdown("""
    <style>
    /* تنسيق الشريط العلوي (Header) */
    header {
        visibility: visible !important;
        background-color: #0d47a1 !important;
    }
    
    /* تلوين أيقونات الشريط العلوي بالأبيض */
    header .st-emotion-cache-12w0qpk, header .st-emotion-cache-zq5wmm {
        color: white !important;
    }

    /* خلفية التطبيق */
    .stApp { background-color: #ffffff; }
    
    /* تصميم شعار علوي جذاب داخل الصفحة */
    .header-banner {
        background: linear-gradient(90deg, #0d47a1, #1e88e5);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* اسم عبد القادر في الأسفل */
    .abdulqader-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f3f4;
        color: #0d47a1;
        text-align: center;
        padding: 10px;
        font-weight: bold;
        border-top: 2px solid #0d47a1;
        z-index: 100;
    }

    /* تحسين الأزرار */
    .stButton>button {
        background: #0d47a1;
        color: white; border-radius: 8px; border: none; width: 100%; height: 3em;
    }
    
    /* إخفاء علامات المطورين فقط مع ترك الهيدر */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_container__1QSob { display: none !important; }
    </style>
    
    <div class="header-banner">
        <h2 style="margin:0;">🔐 نظام التشفير الاحترافي</h2>
        <p style="margin:0; opacity: 0.8;">أمانك هويتنا - عبد القادر 2026</p>
    </div>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية (ستظهر بشكل طبيعي في الهيدر)
with st.sidebar:
    st.markdown("## ⚙️ الإعدادات")
    user_key = st.text_input("مفتاح الأمان الخاص بك:", type="password")
    if st.button("توليد مفتاح جديد"):
        new_k = Fernet.generate_key().decode()
        st.code(new_k)

# 4. محتوى التطبيق
if user_key:
    try:
        cipher = Fernet(user_key.encode())
        tab1, tab2 = st.tabs(["📝 النصوص", "🎙️ الأصوات"])

        with tab1:
            st.markdown("### 🔒 التشفير")
            msg = st.text_area("أدخل النص هنا:", height=100)
            if st.button("تحويل إلى كود"):
                if msg: st.code(cipher.encrypt(msg.encode()).decode())
            
            st.markdown("---")
            st.markdown("### 🔓 فك التشفير")
            enc_input = st.text_area("ضع الكود هنا:", height=100)
            if st.button("استعادة النص"):
                try:
                    st.success(f"الرسالة: {cipher.decrypt(enc_input.encode()).decode()}")
                except:
                    st.error("خطأ في المفتاح أو الكود")

        with tab2:
            st.write("سجل صوتك للحماية:")
            audio = audio_recorder(text="", icon_size="3x", neutral_color="#0d47a1")
            if audio:
                st.audio(audio)
                if st.button("حفظ كملف مشفر"):
                    st.download_button("تحميل الملف", cipher.encrypt(audio), file_name="safe.bin")
    except:
        st.error("المفتاح غير صالح")
else:
    st.info("💡 افتح القائمة الجانبية من الأعلى (أيقونة السهم) للبدء.")

# التذييل الثابت
st.markdown('<div class="abdulqader-footer">Developed by: Abdulqader 🚀 | 2026</div>', unsafe_allow_html=True)
