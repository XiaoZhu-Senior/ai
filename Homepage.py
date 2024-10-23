import streamlit as st
import appbuilder
import os
import time
from langchain.schema import AIMessage, HumanMessage

# 设置页面配置，必须在其他 Streamlit 命令之前调用
st.set_page_config(page_title="欢迎来到 ASL", layout="wide")

def app_builder_client():
    """创建 AppBuilder 客户端"""
    if "APPBUILDER_TOKEN" in st.session_state and st.session_state["APPBUILDER_TOKEN"]:
        os.environ["APPBUILDER_TOKEN"] = st.session_state["APPBUILDER_TOKEN"]
        app_id = "e968e4e0-c4be-45f8-9af4-3ba376df6646"  # 替换为你的 App ID
        return appbuilder.AppBuilderClient(app_id)
    return None

def get_response(conversation_id, prompt):
    """从 AppBuilder 获取回复并缓存结果"""
    client = app_builder_client()
    if client:
        return client.run(conversation_id, prompt)  # 确保这里传递 conversation_id
    else:
        return None

# 检查 TOKEN 是否已设置
if "APPBUILDER_TOKEN" in st.session_state and st.session_state["APPBUILDER_TOKEN"]:
    os.environ["APPBUILDER_TOKEN"] = st.session_state["APPBUILDER_TOKEN"]

    # 从 AppBuilder 获取应用 ID
    app_id = "e968e4e0-c4be-45f8-9af4-3ba376df6646"  # 替换为你的 App ID
    app_builder_client_instance = appbuilder.AppBuilderClient(app_id)

    if "conversation_id" not in st.session_state:
        st.session_state["conversation_id"] = app_builder_client_instance.create_conversation()

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # 聊天功能
    if app_builder_client_instance:
        with st.container():
            st.header("与 GPT 对话")

            for message in st.session_state["messages"]:
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.markdown(message.content)
                elif isinstance(message, AIMessage):
                    with st.chat_message("assistant"):
                        st.markdown(message.content)

            prompt = st.chat_input("请输入内容...")
            if prompt:
                st.session_state["messages"].append(HumanMessage(content=prompt))
                with st.chat_message("user"):
                    st.markdown(prompt)

                # 使用时间监测来调试响应时间
                start_time = time.time()
                resp = get_response(st.session_state["conversation_id"], prompt)  # 确保传递 conversation_id
                end_time = time.time()

                if resp:
                    ai_message = AIMessage(content=resp.content.answer)
                    st.session_state["messages"].append(ai_message)
                    with st.chat_message("assistant"):
                        st.markdown(ai_message.content)
                    st.write(f"请求处理时间: {end_time - start_time:.2f} 秒")
                else:
                    st.error("获取回复时出错，请检查 AppBuilder TOKEN 或网络连接。")
else:
    st.warning("请先在 'xzbot' 界面输入您的 AppBuilder TOKEN。")
