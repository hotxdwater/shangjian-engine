import streamlit as st
import webbrowser
import threading

def open_browser():
    webbrowser.open_new("http://localhost:8501")

threading.Timer(1.0, open_browser).start()

st.set_page_config(page_title="熵减引擎")
st.title("欢迎使用智能财务工具箱")

st.markdown("这是一个基于 Streamlit 构建的高集成度财务辅助工具平台，当前为演示版本。")
st.markdown("- ✅ 模块化功能")
st.markdown("- 📊 智能数据处理")
st.markdown("- 📁 一键导出")
st.markdown("- 🧠 打通填报与分析")

st.success("系统启动成功，欢迎体验。")