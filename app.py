import streamlit as st

from biofrq.pipeline import FRQGradingPipeline
from biofrq.schemas import GradeRequest, RubricCriterion

st.set_page_config(page_title="BioGrade AI", page_icon="🧬", layout="wide")
st.title("🧬 BioGrade AI")
st.caption("BERT-powered Biology FRQ review assistant")

st.warning("Research prototype: recommendations require teacher review before any final grade is assigned.")

question = st.text_area(
    "FRQ prompt",
    "Explain how natural selection can change allele frequencies in a population.",
)
response = st.text_area(
    "Student response",
    "Individuals with advantageous heritable traits survive and reproduce more often, so those alleles become more common over generations.",
)

st.subheader("Rubric criteria")
c1 = st.text_input("Criterion 1", "Identifies differential survival or reproduction")
c2 = st.text_input("Criterion 2", "Explains that advantageous heritable alleles increase in frequency across generations")

if st.button("Analyze response", type="primary"):
    with st.spinner("Running BERT rubric analysis..."):
        pipeline = FRQGradingPipeline()
        request = GradeRequest(
            question=question,
            response=response,
            rubric=[
                RubricCriterion(id="c1", description=c1),
                RubricCriterion(id="c2", description=c2),
            ],
        )
        result = pipeline.grade(request)

    left, right = st.columns(2)
    left.metric("Recommended score", f"{result.recommended_score}/{result.max_score}")
    right.metric("Prompt relevance", f"{result.relevance:.2f}")

    for criterion in result.criteria:
        with st.expander(f"{criterion.criterion_id}: {'Point suggested' if criterion.awarded else 'No point suggested'}"):
            st.write(f"Confidence: **{criterion.confidence:.2f}**")
            st.write(f"Evidence: _{criterion.evidence or 'No evidence found'}_")

    st.info("Final scoring decision remains with the instructor.")
