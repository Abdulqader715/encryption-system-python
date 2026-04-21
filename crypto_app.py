import streamlit as st
from cryptography.fernet import Fernet
from audio_recorder_streamlit import audio_recorder

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام تشفير", page_icon="🔐")

# 2. كود سحري لإخفاء كل الشعارات والزوائد
st.markdown("""
    <style>
    /* إخفاء شريط التقديم العلوي */
    div[data-testid="stStatusWidget"] { visibility: hidden; }
    
    /* إخفاء القائمة الرئيسية وشعار Streamlit في الأسفل */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* إخفاء علامة "Made with Streamlit" وأي شعارات عائمة */
    .viewerBadge_container__1QSob { display: none !important; }
    button[title="View source on GitHub"] { display: none !important; }
    
    /* خلفية التطبيق */
    .stApp { background-color: #f8f9fa; }
    
    /* تنسيق العنوان */
    h1 { color: #0d47a1 !important; text-align: center; font-size: 26px !important; margin-top: -50px; }
    
    /* تحسين الأزرار */
    .stButton>button {
        background: linear-gradient(45deg, #1e88e5, #1565c0);
        color: white; border: none; border-radius: 12px; height: 3em; font-weight: bold; width: 100%;
    }

    /* اسم عبد القادر في الأسفل بشكل نظيف جداً */
    .abdulqader-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        color: #0d47a1;
        text-align: center;
        padding: 15px;
        font-weight: bold;
        border-top: 2px solid #1e88e5;
        z-index: 999999;
        font-size: 16px;
    }
    
    /* إظهار سهم القائمة الجانبية الملون */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #1e88e5 !important;
        color: white !important;
        border-radius: 0 10px 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية
with st.sidebar:
    st.title("🔑 الإعدادات")
    user_key = st.text_input("أدخل مفتاح التشفير:", type="password")
    if st.button("توليد مفتاح جديد"):
        new_k = Fernet.generate_key().decode()
        st.code(new_k)
        st.caption("انسخ المفتاح واستخدمه بالأعلى")

# 4. واجهة التطبيق
st.title("🛡️ نظام تشفير")

if user_key:
    try:
        cipher = Fernet(user_key.encode())
        tab1, tab2 = st.tabs(["📝 النصوص", "🎤 الصوت"])

        with tab1:
            msg = st.text_area("اكتب الرسالة:", height=100)
            if st.button("تشفير"):
                if msg:
                    st.code(cipher.encrypt(msg.encode()).decode())
            
            st.markdown("---")
            enc_input = st.text_area("ضع الكود لفك تشفيره:", height=100)
            if st.button("إظهار النص"):
                try:
                    st.success(f"الرسالة: {cipher.decrypt(enc_input.encode()).decode()}")
                except:
                    st.error("خطأ في البيانات")

        with tab2:
            st.write("سجل صوتك هنا:")
            audio = audio_recorder(text="", icon_size="3x", neutral_color="#1e88e5")
            if audio:
                st.audio(audio)
                if st.button("تشفير الصوت"):
                    st.download_button("تحميل الملف المشفر", cipher.encrypt(audio), file_name="voice.bin")

    except:
        st.error("المفتاح غير صحيح")
else:
    st.info("الرجاء فتح القائمة الجانبية (السهم بالأعلى) ووضع المفتاح")

# التوقيع النهائي
st.markdown("""
    <div class="abdulqader-footer">
        Developed by: Abdulqader | 2026
    </div>
    """, unsafe_allow_html=True)
