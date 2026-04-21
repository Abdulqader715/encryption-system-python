import streamlit as st
from cryptography.fernet import Fernet
from audio_recorder_streamlit import audio_recorder

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام تشفير", page_icon="🔐")

# 2. التنسيقات وإظهار زر القائمة الجانبية بشكل "عائم"
st.markdown("""
    <style>
    /* جعل زر القائمة الجانبية ظاهراً وعائماً بلون أزرق */
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        background-color: #0d47a1 !important;
        color: white !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        top: 20px !important;
        left: 20px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* إخفاء شعارات Streamlit والتاج الأحمر */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob { display: none !important; }
    
    /* خلفية التطبيق */
    .stApp { background-color: #f8f9fa; }
    
    /* تنسيق العنوان */
    h1 { color: #0d47a1 !important; text-align: center; font-size: 26px !important; margin-top: 20px; }
    
    /* اسم عبد القادر في الأسفل بشكل ثابت واحترافي */
    .abdulqader-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        color: #0d47a1;
        text-align: center;
        padding: 12px;
        font-weight: bold;
        border-top: 2px solid #0d47a1;
        z-index: 9999;
        font-size: 15px;
    }
    
    /* تحسين شكل الأزرار */
    .stButton>button {
        background: linear-gradient(45deg, #1e88e5, #0d47a1);
        color: white; border-radius: 12px; font-weight: bold; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية
with st.sidebar:
    st.markdown("### 🔑 إعدادات الأمان")
    user_key = st.text_input("ضع مفتاحك هنا:", type="password")
    st.markdown("---")
    if st.button("توليد مفتاح جديد"):
        new_k = Fernet.generate_key().decode()
        st.code(new_k)
        st.caption("احفظ هذا الكود لاستخدامه دائماً")

# 4. محتوى التطبيق
st.title("🛡️ نظام تشفير")

if user_key:
    try:
        cipher = Fernet(user_key.encode())
        tab1, tab2 = st.tabs(["📝 نصوص", "🎙️ صوت"])

        with tab1:
            msg = st.text_area("النص المراد حمايته:", height=100)
            if st.button("تشفير النص"):
                if msg:
                    st.code(cipher.encrypt(msg.encode()).decode())
            
            st.markdown("---")
            enc_input = st.text_area("الكود المراد فكه:", height=100)
            if st.button("فك التشفير"):
                try:
                    st.success(f"الرسالة الأصلية: {cipher.decrypt(enc_input.encode()).decode()}")
                except:
                    st.error("المفتاح أو الكود خطأ")

        with tab2:
            st.write("سجل صوتك:")
            audio = audio_recorder(text="", icon_size="3x", neutral_color="#0d47a1")
            if audio:
                st.audio(audio)
                if st.button("حماية الصوت"):
                    st.download_button("تحميل الملف المشفر", cipher.encrypt(audio), file_name="secret.bin")
    except:
        st.error("مفتاح الأمان غير صالح")
else:
    # رسالة تنبيه واضحة
    st.info("👋 أهلاً بك! اضغط على الدائرة الزرقاء في أعلى اليسار لوضع مفتاح الأمان.")

# التوقيع
st.markdown("""
    <div class="abdulqader-footer">
        Developed by: Abdulqader 🚀 | 2026
    </div>
    """, unsafe_allow_html=True)
