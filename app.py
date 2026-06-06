import streamlit as st
from pipeline import run_research_pipeline
from utils import create_pdf

# ===========================================
# PAGE CONFIG
# ===========================================

st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🤖",
    layout="wide"
)

# ===========================================
# SESSION STATE
# ===========================================

if "history" not in st.session_state:
    st.session_state.history = []

# ===========================================
# SIDEBAR
# ===========================================

with st.sidebar:

    st.title("🤖 Multi-Agent Research")

    st.markdown("---")

    st.markdown("""
### Pipeline

🔎 Search Agent

📖 Reader Agent

✍️ Writer Chain

✅ Fact Checker

⭐ Critic

---

Built With

- LangChain
- LangGraph
- Tavily
- OpenRouter
- Streamlit
""")

    st.divider()

    st.subheader("📚 Previous Research")

    for item in reversed(st.session_state.history):

        with st.expander(item["topic"]):

            st.write(item["report"][:400] + "...")

# ===========================================
# HEADER
# ===========================================

st.title("🤖 Multi-Agent AI Research System")

st.markdown(
"""
Search → Read → Write → Fact Check → Critic
"""
)

st.divider()

# ===========================================
# INPUT
# ===========================================

topic = st.text_input(
    "Enter a research topic",
    placeholder="Future of Quantum Computing"
)

# ===========================================
# RUN BUTTON
# ===========================================

if st.button("🚀 Run Research", use_container_width=True):

    if topic.strip():

        progress = st.progress(0)
        status = st.empty()

        status.info("🔎 Searching...")
        progress.progress(20)

        state = run_research_pipeline(topic)

        progress.progress(100)

        status.success(
            f"Completed in {state['execution_time']} sec"
        )

        # save history
        st.session_state.history.append(
            {
                "topic": topic,
                "report": state["report"]
            }
        )

        # =======================================
        # METRICS
        # =======================================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Execution Time",
                f"{state['execution_time']} sec"
            )

        with col2:
            st.metric(
                "Agents Used",
                "5"
            )

        with col3:
            st.metric(
                "Pipeline Status",
                state["status"]
            )

        st.divider()

        # =======================================
        # EXPANDERS
        # =======================================

        with st.expander("🔎 Search Results"):
            st.markdown(state["search_results"])

        with st.expander("📖 Scraped Content"):
            st.markdown(state["scraped_content"])

        with st.expander("📝 Final Report", expanded=True):
            st.markdown(state["report"])

        with st.expander("✅ Fact Check"):
            st.markdown(state["fact_check"])

        with st.expander("⭐ Critic Feedback"):
            st.markdown(state["feedback"])

        # =======================================
        # DOWNLOADS
        # =======================================

        report_md = f"""
# Topic

{topic}

---

# Report

{state['report']}

---

# Fact Check

{state['fact_check']}

---

# Critic Feedback

{state['feedback']}
"""

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "📥 Download Markdown",
                report_md,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col2:

            pdf_file = create_pdf(state, topic)

            with open(pdf_file, "rb") as f:

                st.download_button(
                    "📄 Download PDF",
                    f,
                    file_name="research_report.pdf",
                    use_container_width=True
                )

    else:

        st.warning("Please enter a topic.")