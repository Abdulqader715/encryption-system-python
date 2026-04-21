Import streamlit as st
from cryptography.fernet import Fernet

# 1. إعدادات الصفحة والتصميم (CSS)
st.set_page_config(page_title="SafeBox Pro", page_icon="🔐", layout="wide")

# إضافة لمسات جمالية بالألوان
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    .css-10trblm {
        color: #1f3044;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (Sidebar) بتنسيق أنيق
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2589/2589174.png", width=100)
    st.title("لوحة التحكم")
    st.markdown("---")
    
    st.subheader("🔑 إدارة المفاتيح")
    if st.button("توليد مفتاح أمان جديد"):
        new_key = Fernet.generate_key().decode()
        st.info("انسخ هذا المفتاح واحفظه جيداً:")
        st.code(new_key, language="text")
    
    st.markdown("---")
    user_key = st.text_input("أدخل مفتاح التشفير الخاص بك:", type="password", help="المفتاح ضروري لتشفير وفك تشفير الرسائل")

# 3. محتوى الصفحة الرئيسي
st.title("🔐 نظام SafeBox للتشفير العالمي")
st.write("نظام احترافي لتأمين الرسائل باستخدام خوارزميات AES المتطورة.")

if user_key:
    try:
        # التأكد من صحة تنسيق المفتاح
        cipher = Fernet(user_key.encode())
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 تشفير الرسائل")
            st.caption("سيتم تحويل النص إلى كود غير قابل للقراءة")
            msg = st.text_area("اكتب رسالتك هنا (عربي/إنجليزي/رموز):", height=150)
            if st.button("بدء التشفير"):
                if msg:
                    token = cipher.encrypt(msg.encode('utf-8'))
                    st.success("✅ تمت عملية التشفير")
                    st.code(token.decode(), language="text")
                else:
                    st.warning("⚠️ فضلاً، اكتب النص المراد تشفيره")

        with col2:
            st.markdown("### 📥 فك التشفير")
            st.caption("استرجع النص الأصلي باستخدام المفتاح الصحيح")
            encrypted_input = st.text_area("أدخل الكود المشفر هنا:", height=150)
            if st.button("بدء فك التشفير"):
                if encrypted_input:
                    try:
                        decrypted_msg = cipher.decrypt(encrypted_input.encode()).decode('utf-8')
                        st.balloons()
                        st.success("✅ تم استرجاع النص الأصلي:")
                        st.markdown(f"**{decrypted_msg}**")
                    except:
                        st.error("❌ فشل فك التشفير! المفتاح غير مطابق لهذا النص.")
                else:
                    st.warning("⚠️ فضلاً، أدخل الكود المشفر")
                    
    except Exception as e:
        st.sidebar.error("❌ المفتاح غير صالح. تأكد من استخدام مفتاح تم توليده بواسطة النظام.")
else:
    st.warning("👈 الرجاء إدخال مفتاح التشفير في القائمة الجانبية للبدء.")
    st.image("https://cdn.pixabay.com/photo/2019/10/21/04/13/castle-4564998_1280.png", width=400)

# تذييل الصفحة
st.markdown("---")
st.caption("تطوير: Abdulqader | نظام تشفير آمن 100%")
