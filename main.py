import streamlit as st
from cryptography.fernet import Fernet
import os

# ===============================
# Key Management
# ===============================

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    return open("secret.key", "rb").read()

# ===============================
# Encryption / Decryption Logic
# ===============================

def encrypt_message(message: str) -> bytes:
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())

def decrypt_message(token: bytes) -> str:
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(token).decode()

# ===============================
# Streamlit UI
# ===============================

st.set_page_config(page_title="Secure Data Encryption App", layout="centered", page_icon="🔐")
st.markdown(
    "<h1 style='text-align: center; color: #4A4A4A;'>🔐 Secure Data Encryption</h1>",
    unsafe_allow_html=True
)
st.markdown("##### A simple app to encrypt and decrypt sensitive information using Fernet encryption.")

# Key check
if not os.path.exists("secret.key"):
    generate_key()

# Tabs for better UX
tab1, tab2 = st.tabs(["🔏 Encrypt", "🔓 Decrypt"])

# ===============================
# 🔏 Encryption Tab
# ===============================

with tab1:
    st.markdown("### Encrypt a Message")
    with st.container():
        message = st.text_area("📝 Enter your message below:", height=150, placeholder="Type your secret message here...")

        col1, col2 = st.columns([1, 4])
        with col2:
            if st.button("🔐 Encrypt Message"):
                if message.strip() == "":
                    st.warning("Please enter a message before encryption.")
                else:
                    encrypted = encrypt_message(message)
                    st.success("✅ Encrypted successfully!")
                    st.code(encrypted.decode(), language="text")

# ===============================
# 🔓 Decryption Tab
# ===============================

with tab2:
    st.markdown("### Decrypt a Message")
    with st.container():
        encrypted_input = st.text_area("🧩 Paste the encrypted message below:", height=150, placeholder="Paste your encrypted message here...")

        col1, col2 = st.columns([1, 4])
        with col2:
            if st.button("🔓 Decrypt Message"):
                if encrypted_input.strip() == "":
                    st.warning("Please paste an encrypted message.")
                else:
                    try:
                        decrypted = decrypt_message(encrypted_input.encode())
                        st.success("🔑 Decrypted successfully!")
                        st.code(decrypted, language="text")
                    except Exception as e:
                        st.error("❌ Decryption failed! Please make sure the input is correct and the key matches.")

# ===============================
# Footer
# ===============================

st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ using Streamlit & Fernet</p>", unsafe_allow_html=True)
