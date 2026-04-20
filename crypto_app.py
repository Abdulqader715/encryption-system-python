import streamlit as st
from cryptography.fernet import Fernet

# إعداد واجهة البرنامج
st.set_page_config(page_title="SafeBox", page_icon="🔐")
st.title("🔐 نظام التشفير الشخصي")

# توليد أو استرجاع المفتاح
if 'key' not in st.session_state:
    st.session_state.key = Fernet.generate_key()

cipher = Fernet(st.session_state.key)

# واجهة التشفير
st.subheader("تشفير رسالة جديدة")
msg = st.text_input("اكتب رسالتك السرية هنا:")

if st.button("تشفير الآن"):
    if msg:
        token = cipher.encrypt(msg.encode())
        st.success("تم التشفير بنجاح!")
        st.code(token.decode())
        st.info(f"مفتاح فك التشفير: {st.session_state.key.decode()}")
    else:
        st.warning("الرجاء كتابة نص أولاً")

st.divider()

# واجهة فك التشفير
st.subheader("فك التشفير")
encrypted_input = st.text_area("أدخل النص المشفر هنا:")
if st.button("فك التشفير"):
    try:
        decrypted_msg = cipher.decrypt(encrypted_input.encode())
        st.balloons()
        st.success(f"الرسالة الأصلية هي: {decrypted_msg.decode()}")
    except:
        st.error("خطأ: تأكد من صحة النص المشفر أو المفتاح")