"""Streamlit Data Quality & Governance Dashboard."""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="AWS Data Quality & Governance", layout="wide")

st.title("🛡️ AWS Data Quality & Governance Platform")
st.caption("Developed by Jayant Verman | AWS Native Data Platform")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Pipeline Overview",
    "🎯 Data Quality Trends",
    "🔍 Macie PII Findings",
    "🔒 Lake Formation Policies",
    "🕸️ Marquez Lineage Graph",
])

with tab1:
    st.header("Pipeline Architecture & Status")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Data Quality Score", "98.4%", "+1.2%")
    col2.metric("Curated Records", "1,968", "rows")
    col3.metric("Quarantine Records", "32", "rows")
    col4.metric("PII Columns Masked", "4", "columns")

with tab2:
    st.header("Great Expectations Score History")
    df = pd.DataFrame({"Date": ["2023-11-01", "2023-11-15", "2023-12-01", "2023-12-15", "2024-01-01", "2024-01-15"], "Quality Score (%)": [94.0, 95.2, 97.1, 96.5, 98.0, 98.4]})
    st.line_chart(df.set_index("Date"))

with tab3:
    st.header("AWS Macie PII Findings Inventory")
    findings = pd.DataFrame([
        {"Column": "ssn", "Category": "National ID", "Severity": "HIGH", "Action": "Column Masked"},
        {"Column": "email", "Category": "Contact Info", "Severity": "MEDIUM", "Action": "Column Masked"},
        {"Column": "phone", "Category": "Contact Info", "Severity": "MEDIUM", "Action": "Column Masked"},
        {"Column": "address", "Category": "Personal Location", "Severity": "LOW", "Action": "Restricted Access"},
    ])
    st.dataframe(findings, use_container_width=True)

with tab4:
    st.header("Lake Formation Fine-Grained Access Control")
    st.subheader("Query Comparison Preview")
    role = st.radio("Select Querying Role:", ["Privileged Role (Full Access)", "Restricted Role (Masked PII)"])
    if "Privileged" in role:
        st.code("SELECT customer_id, first_name, email, ssn FROM customers LIMIT 1;\n\nResults:\nCUST-0000001 | John | john.doe@email.com | 123-45-6789", language="sql")
    else:
        st.code("SELECT customer_id, first_name, email, ssn FROM customers LIMIT 1;\n\nResults:\nCUST-0000001 | John | [MASKED] | [MASKED]", language="sql")

with tab5:
    st.header("OpenLineage & Marquez Data Lineage Graph")
    st.info("Lineage Graph Flow: S3 Raw Landing -> Glue Crawler -> Great Expectations Validation -> S3 Curated / Quarantine -> Lake Formation Governed Athena Table")
