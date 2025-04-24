import streamlit as st
import pandas as pd
import base64
from pathlib import Path
from src.rag_pipeline import simplify_with_prompt, simplify_section
from src.visualizer import (
    extract_steps_from_abstract,
    generate_flowchart,
    generate_flowchart_from_section,
    determine_visualization_strategy
)
from src.pdf_extractor import extract_sections_from_pdf

st.set_page_config(page_title="InsightMuse", layout="wide")
st.title("🧠 InsightMuse — Research Paper Explainer + Visualizer")

st.sidebar.title("📁 Upload Input")
input_mode = st.sidebar.radio("Choose input type:", ["📄 Upload PDF", "📊 Upload CSV"])

# --- PDF Mode ---
if input_mode == "📄 Upload PDF":
    uploaded_pdf = st.sidebar.file_uploader("Upload Research Paper (PDF)", type=["pdf"])

    if uploaded_pdf:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_pdf.read())

        st.success("✅ PDF uploaded. Extracting sections...")
        sections = extract_sections_from_pdf("temp.pdf")

        if sections:
            selected_title = st.selectbox("📚 Choose a section to simplify", list(sections.keys()))
            selected_text = sections[selected_title]

            if st.button("✨ Simplify & Visualize This Section"):
                st.subheader("📄 Original Section: " + selected_title)
                st.markdown(selected_text)

                with st.spinner("Simplifying..."):
                    simplified = simplify_section(selected_title, selected_text)
                    st.subheader("✅ Simplified Explanation")
                    st.markdown(simplified)

                strategy = determine_visualization_strategy(selected_title, selected_text)

                if strategy == "flowchart":
                    with st.spinner("Generating flowchart..."):
                        flowchart_path = generate_flowchart_from_section(selected_title, selected_text)
                        st.subheader("📊 Visual Flowchart")
                        image_bytes = Path(flowchart_path).read_bytes()
                        b64 = base64.b64encode(image_bytes).decode()
                        st.markdown(f'<img src="data:image/png;base64,{b64}" width="100%">', unsafe_allow_html=True)

                elif strategy == "chart":
                    st.info("📈 This section is better represented with statistical charts or graphs. (Coming Soon!)")

                elif strategy == "summary":
                    st.info("📝 No diagram needed — the simplified text already communicates the key points.")

                else:
                    st.info("🤷 This section may not need a visual representation.")
        else:
            st.warning("⚠️ No recognizable sections found in the PDF.")

# --- CSV Mode ---
elif input_mode == "📊 Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload a CSV with an 'abstract' column", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "abstract" not in df.columns:
            st.error("CSV must contain an 'abstract' column.")
        else:
            row = st.selectbox("Choose an abstract to simplify", df["abstract"].tolist())

            if st.button("✨ Simplify & Visualize This Abstract"):
                st.subheader("📄 Original Abstract")
                st.markdown(row)

                with st.spinner("Simplifying..."):
                    summary = simplify_with_prompt(row)
                    st.subheader("✅ Simplified Explanation")
                    st.markdown(summary)

                with st.spinner("Generating chart..."):
                    chart_path = generate_chart_from_section(selected_title, selected_text)
                    st.subheader("📈 Statistical Chart")
                    image_bytes = Path(chart_path).read_bytes()
                    b64 = base64.b64encode(image_bytes).decode()
                    st.markdown(f'<img src="data:image/png;base64,{b64}" width="100%">', unsafe_allow_html=True)
