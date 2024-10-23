import streamlit as st

# 设置 AppBuilder Token 的状态
if "APPBUILDER_TOKEN" not in st.session_state:
    st.session_state["APPBUILDER_TOKEN"] = ""

st.set_page_config(page_title="OpenAI Settings", layout="wide")

st.title("OpenAI 设置")

appbuilder_token = st.text_input("请输入您的 AppBuilder TOKEN", value=st.session_state["APPBUILDER_TOKEN"], max_chars=None, type='password')

saved = st.button("保存")

if saved:
    st.session_state["APPBUILDER_TOKEN"] = appbuilder_token
    st.success("Token 已成功保存!")
