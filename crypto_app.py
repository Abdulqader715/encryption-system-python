import streamlit as st
from cryptography.fernet import Fernet
from audio_recorder_streamlit import audio_recorder

# 1. إعدادات الصفحة
st.set_page_config(page_title="نظام تشفير", page_icon="🔐")

# 2. التنسيقات لجعل السهم بارزاً جداً وحذف الزوائد
st.markdown("""
    <style>
    /* جعل سهم القائمة الجانبية بارزاً جداً وكبيراً */
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        background-color: #0d47a1 !important; /* لون أزرق غامق بارز */
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        top: 15px !important;
        left: 15px !important;
        box-shadow: 0 0 15px rgba(13, 71, 161, 0.6) !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        border: 2px solid white !important;
    }
    
    /* تكبير أيقونة السهم داخل الزر */
    [data-testid="stSidebarCollapsedControl"] svg {
        width: 35px !important;
        height: 35px !important;
    }

    /* إخفاء الزوائد وشعار سترمليت */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob { display: none !important; }
    div[data-testid="stStatusWidget"] { visibility: hidden; }

    /* خلفية التطبيق */
    .stApp { background-color: #f8f9fa; }
    
    /* تنسيق العنوان الرئيسي */
    h1 { color: #0d47a1 !important; text-align: center; font-size: 28px !important; margin-top: 30px; font-weight: bold; }
    
    /* التذييل الثابت باسم عبد القادر */
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
        border-top: 3px solid #0d47a1;
        z-index: 999999;
        font-size: 16px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
    
    /* تنسيق الأزرار */
    .stButton>button {
        background: linear-gradient(45deg, #1e88e5, #0d47a1);
        color: white; border-radius: 12px; font-weight: bold; width: 100%; height: 3.2em;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية
with st.sidebar:
    st.markdown("## ⚙️ الإعدادات")
    user_key = st.text_input("مفتاح الأمان الخاص بك:", type="password")
    st.markdown("---")
    if st.button("توليد مفتاح جديد"):
        new_k = Fernet.generate_key().decode()
        st.success("انسخ المفتاح واحفظه:")
        st.code(new_k)

# 4. محتوى التطبيق
st.title("🛡️ نظام تشفير")

if user_key:
    try:
        cipher = Fernet(user_key.encode())
        tab1, tab2 = st.tabs(["📝 النصوص", "🎙️ الصوت"])

        with tab1:
            msg = st.text_area("أدخل الرسالة:", height=120)
            if st.button("تشفير النص"):
                if msg:
                    st.code(cipher.encrypt(msg.encode()).decode())
            
            st.markdown("---")
            enc_input = st.text_area("ضع الكود لفك التشفير:", height=120)
            if st.button("إظهار النص الأصلي"):
                try:
                    st.success(f"الرسالة: {cipher.decrypt(enc_input.encode()).decode()}")
                except:
                    st.error("خطأ: المفتاح أو الكود غير صحيح")

        with tab2:
            st.write("سجل صوتك هنا:")
            audio = audio_recorder(text="", icon_size="3x", neutral_color="#0d47a1")
            if audio:
                st.audio(audio)
                if st.button("تشفير وحفظ الصوت"):
                    st.download_button("تحميل الملف المشفر", cipher.encrypt(audio), file_name="secret_voice.bin")
    except:
        st.error("المفتاح غير صالح")
else:
    st.info("💡 اضغط على الزر الدائري الأزرق البارز (أعلى اليسار) للبدء.")

# التوقيع الثابت
st.markdown("""
    <div class="abdulqader-footer">
        Developed by: Abdulqader 🚀 | 2026
    </div>
    """, unsafe_allow_html=True)
