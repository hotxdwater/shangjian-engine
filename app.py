
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="熵减引擎 - 智能财务工具箱", layout="wide")

# 顶部Logo + 标题
st.markdown("""
    <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
        <img src="https://raw.githubusercontent.com/yourusername/logo-repo/main/final_logo.png" width="80">
        <div>
            <h1 style="margin: 0; font-size: 2.5em;">熵减引擎</h1>
            <p style="margin: 0; font-size: 1.1em; color: gray;">SHANGJIAN YINQING · 智能财务工具原型平台</p>
        </div>
    </div>
    <hr style="margin-top: 0px;">
""", unsafe_allow_html=True)

# 样式注入
st.markdown("""
    <style>
        .stButton>button, .stDownloadButton>button {
            background-color: #0056b3;
            color: white;
            border-radius: 6px;
            padding: 0.5em 1.2em;
            font-weight: 500;
            border: none;
        }
        .stButton>button:hover, .stDownloadButton>button:hover {
            background-color: #004494;
        }
        .custom-footer {
            font-size: 0.9em;
            color: #888;
            text-align: center;
            margin-top: 60px;
            padding-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="custom-footer">
    © 2025 京能集团 × 熵减引擎 Demo | Designed with 💡 and 🧠
</div>
""", unsafe_allow_html=True)

st.sidebar.title("📂 模块导航")
page = st.sidebar.radio("请选择功能模块：", [
    "上传与预览数据", "字段清洗与结构校验", "字段筛选提取", "BPC报表自动填报"
])

data_file = st.sidebar.file_uploader("📤 上传源数据文件（如13z0）", type=["xlsx"])
source_data = {}
if data_file:
    source_data = pd.read_excel(data_file, sheet_name=None)
    st.sidebar.success("✅ 文件已上传：{}".format(data_file.name))

card_style = "background-color:#f9f9f9;padding:30px 25px;border-radius:10px;border:1px solid #eee;margin-bottom:30px"

if page == "上传与预览数据":
    st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
    st.subheader("📁 数据上传与预览")
    if source_data:
        sheet = st.selectbox("请选择工作表：", list(source_data.keys()))
        df = source_data[sheet]
        st.dataframe(df.head())
    else:
        st.info("请上传Excel文件进行预览。")
    st.markdown("</div>", unsafe_allow_html=True)

def eliminate_symbols(x):
    return ''.join(e for e in str(x) if e.isalnum() or '一' <= e <= '鿿')

def preprocess_dataframe(df):
    df = df.copy()
    if "科目/描述" in df.columns:
        df["科目_cleaned"] = df["科目/描述"].apply(eliminate_symbols)
    return df

if page == "字段清洗与结构校验":
    st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
    st.subheader("🧹 字段清洗与结构校验")
    if source_data:
        sheet = st.selectbox("选择清洗的Sheet：", list(source_data.keys()), key="cleaning")
        df = source_data[sheet]
        df_cleaned = preprocess_dataframe(df)
        st.dataframe(df_cleaned.head())
    else:
        st.warning("请上传数据后再进行清洗。")
    st.markdown("</div>", unsafe_allow_html=True)

if page == "字段筛选提取":
    st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
    st.subheader("🔍 筛选指定字段数据")
    if source_data:
        sheet = st.selectbox("选择筛选的Sheet：", list(source_data.keys()), key="selecting")
        df = source_data[sheet]
        cols = st.multiselect("选择你想提取的列：", df.columns.tolist())
        if cols:
            st.dataframe(df[cols])
        else:
            st.info("请选择需要提取的列。")
    else:
        st.info("请先上传数据文件。")
    st.markdown("</div>", unsafe_allow_html=True)

storage = {
    "资产负债表": {"AC49": 143749551, "AD49": 110083799.2, "AO49": 0, "AP49": 0},
    "利润表": {"Z46": 19839493.44, "AD46": 57971792.97, "Z66": 34684648.3, "AD66": 94272738.5}
}

def fill_template(sheet_name, mapping_dict):
    template = pd.read_excel("BPC财务报表套表_完整空模板.xlsx", sheet_name=None)
    for sheet, df in template.items():
        if sheet == sheet_name:
            for cell, value in mapping_dict.items():
                col = ''.join(filter(str.isalpha, cell))
                row = int(''.join(filter(str.isdigit, cell))) - 1
                col_index = ord(col) - ord('A')
                try:
                    df.iat[row, col_index] = value
                except:
                    continue
            template[sheet] = df
    return template

def convert_to_excel(dict_data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet, df in dict_data.items():
            df.to_excel(writer, index=False, header=False, sheet_name=sheet)
        writer.save()
    output.seek(0)
    return output

if page == "BPC报表自动填报":
    st.markdown(f"<div style='{card_style}'>", unsafe_allow_html=True)
    st.subheader("🧾 一键生成自动填报BPC报表")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 下载资产负债表"):
            df_filled = fill_template("JNJTC1001-资产负债表", storage["资产负债表"])
            st.download_button("点击下载资产负债表", data=convert_to_excel(df_filled),
                               file_name="资产负债表_自动填报.xlsx")
    with col2:
        if st.button("📥 下载利润表"):
            df_filled = fill_template("JNJTC1002-利润表", storage["利润表"])
            st.download_button("点击下载利润表", data=convert_to_excel(df_filled),
                               file_name="利润表_自动填报.xlsx")
    st.markdown("</div>", unsafe_allow_html=True)
