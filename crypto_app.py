import streamlit as st
from cryptography.fernet import Fernet
from audio_recorder_streamlit import audio_recorder

# 1. إعدادات الصفحة وتصغير الخطوط
st.set_page_config(page_title="الأبجدية", page_icon="🔐")

st.markdown("""
    <style>
    /* تصغير العنوان الرئيسي */
    h1 { font-size: 28px !important; color: #2E7D32; text-align: center; }
    /* تحسين شكل الأزرار */
    .stButton>button { 
        width: 100%; border-radius: 8px; background-color: #4CAF50; color: white; border: none; height: 2.5em;
    }
    /* تنسيق الحقول */
    .stTextArea textarea { border-radius: 10px; }
    /* إخفاء القائمة الزائدة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (بسيطة جداً)
with st.sidebar:
    st.write("### 🔑 الإعدادات")
    user_key = st.text_input("ضع مفتاح الأمان هنا:", type="password")
    st.markdown("---")
    if st.button("توليد مفتاح جديد"):
        new_k = Fernet.generate_key().decode()
        st.code(new_k, language="text")
        st.caption("انسخ هذا المفتاح واحفظه لاستخدامه دائماً")

# 3. محتوى الصفحة
st.title("🛡️ نظام الأبجدية")

if user_key:
    try:
        cipher = Fernet(user_key.encode())
        tab1, tab2 = st.tabs(["📝 نصوص", "🎤 صوت"])

        with tab1:
            # قسم التشفير
            st.markdown("#### 🔒 تشفير نص جديد")
            msg = st.text_area("اكتب هنا ما تريد حمايته:", height=100)
            if st.button("تشفير الآن"):
                if msg:
                    token = cipher.encrypt(msg.encode('utf-8'))
                    st.success("تم التشفير بنجاح:")
                    st.code(token.decode(), language="text")

            st.markdown("---")
            
            # قسم فك التشفير
            st.markdown("#### 🔓 فك التشفير")
            enc_input = st.text_area("ضع الكود المشفر هنا:", height=100)
            if st.button("إظهار النص الأصلي"):
                try:
                    decrypted = cipher.decrypt(enc_input.encode()).decode('utf-8')
                    st.info(f"النص هو: {decrypted}")
                except:
                    st.error("الكود أو المفتاح غير صحيح")

        with tab2:
            st.write("اضغط للتحدث وتشفير صوتك:")
            audio_bytes = audio_recorder(text="", icon_size="3x", neutral_color="#4CAF50")
            if audio_bytes:
                st.audio(audio_bytes)
                if st.button("حفظ كملف مشفر"):
                    enc_audio = cipher.encrypt(audio_bytes)
                    st.download_button("تحميل الملف المشفر", enc_audio, file_name="voice.bin")

    except:
        st.error("مفتاح الأمان الذي أدخلته غير صحيح")
else:
    st.warning("الرجاء وضع مفتاح الأمان في القائمة الجانبية (على اليسار أو بالأعلى) للبدء")
