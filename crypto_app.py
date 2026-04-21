import streamlit as st
from cryptography.fernet import Fernet
from audio_recorder_streamlit import audio_recorder

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام تشفير", page_icon="🔐")

# 2. تنسيقات CSS متقدمة
st.markdown("""
    <style>
    /* خلفية التطبيق */
    .stApp { background-color: #f8f9fa; }
    
    /* تنسيق العنوان الرئيسي */
    h1 { color: #0d47a1 !important; font-weight: 800 !important; text-align: center; margin-bottom: 30px; }
    
    /* تنسيق التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff; border-radius: 10px 10px 0 0; padding: 10px 20px; font-weight: bold;
    }
    
    /* تصميم الأزرار */
    .stButton>button {
        background: linear-gradient(45deg, #1e88e5, #1565c0);
        color: white; border: none; border-radius: 12px; height: 3.2em;
        font-size: 16px; font-weight: bold; transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 12px rgba(0,0,0,0.15); color: white; }
    
    /* التذييل (اسمك في أسفل الصفحة) */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: white; color: #555; text-align: center;
        padding: 10px; font-family: 'Courier New', Courier, monospace;
        font-weight: bold; border-top: 1px solid #ddd; font-size: 14px;
    }
    
    /* إخفاء شعارات Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🔑 الإعدادات</h2>", unsafe_allow_html=True)
    user_key = st.text_input("مفتاح التشفير الخاص بك:", type="password", help="أدخل المفتاح المكون من 32 حرفاً")
    st.markdown("---")
    if st.button("توليد مفتاح أمان جديد"):
        new_k = Fernet.generate_key().decode()
        st.success("انسخ هذا المفتاح واحفظه:")
        st.code(new_k, language="text")

# 4. محتوى التطبيق
st.title("🛡️ نظام تشفير")

if user_key:
    try:
        cipher = Fernet(user_key.encode())
        tab1, tab2 = st.tabs(["📄 النصوص", "🎙️ الصوت"])

        with tab1:
            st.markdown("### 🔒 حماية النص")
            msg = st.text_area("أدخل النص المراد تشفيره:", height=100)
            if st.button("بدء التشفير"):
                if msg:
                    token = cipher.encrypt(msg.encode('utf-8'))
                    st.info("الرمز المشفر الناتج:")
                    st.code(token.decode())

            st.markdown("---")
            st.markdown("### 🔓 استعادة النص")
            enc_input = st.text_area("أدخل الرمز المشفر هنا:", height=100)
            if st.button("إظهار الرسالة الأصلية"):
                try:
                    decrypted = cipher.decrypt(enc_input.encode()).decode('utf-8')
                    st.success("الرسالة المستعادة:")
                    st.write(f"**{decrypted}**")
                except:
                    st.error("خطأ: الكود غير متوافق مع المفتاح")

        with tab2:
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.write("سجل صوتك ليتم تحويله إلى ملف مشفر:")
            audio_bytes = audio_recorder(text="", icon_size="3x", neutral_color="#1e88e5")
            st.markdown("</div>", unsafe_allow_html=True)

            if audio_bytes:
                st.audio(audio_bytes)
                if st.button("تشفير هذا الملف الصوتي"):
                    enc_audio = cipher.encrypt(audio_bytes)
                    st.success("تم التشفير!")
                    st.download_button("تحميل الصوت المشفر", enc_audio, file_name="secret.bin")

    except:
        st.error("مفتاح التشفير الذي وضعته غير صالح.")
else:
    st.warning("⚠️ يرجى إدخال مفتاح التشفير من القائمة الجانبية للبدء.")

# إضافة اسمك في الأسفل
st.markdown("""
    <div class="footer">
        Developed by: Abdulqader 🚀 | 2026
    </div>
    """, unsafe_allow_html=True)
