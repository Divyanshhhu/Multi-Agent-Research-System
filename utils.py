from fpdf import FPDF

def create_pdf(state, topic):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    text = f"""

Topic

{topic}

-------------------

REPORT

{state['report']}

-------------------

FACT CHECK

{state['fact_check']}

-------------------

CRITIC FEEDBACK

{state['feedback']}
"""

    text = text.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 10, text)

    filename = "research_report.pdf"

    pdf.output(filename)

    return filename