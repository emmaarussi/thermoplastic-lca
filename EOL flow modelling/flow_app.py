
import streamlit as st
import pandas as pd
from datetime import datetime

# Set up file paths
interview_file = "interviews.csv"
flow_file = "material_flows.csv"
collection_file = "collection_methods.csv"
categories_file = "stakeholder_categories.csv"

st.title("TPC Recycling: Stakeholder & Material Flow Tracker")

# Tabs for Interview and Material Flow
tab1, tab2 = st.tabs(["📋 Stakeholder Interviews", "🔁 Material Flows"])

with tab1:
    st.header("New Stakeholder Interview")
    with st.form("interview_form"):
        name = st.text_input("Name")
        category_df = pd.read_csv(categories_file)
        category_options = category_df["Category Name"].tolist()
        role = st.selectbox("Stakeholder Category", category_options)
        org = st.text_input("Organization")
        location = st.text_input("Location")
        material_types = st.text_input("Material Types (e.g., TPC panels, structural)")
        collection_df = pd.read_csv(collection_file)
        collection_options = collection_df["Collection Method"].tolist()
        collection_method = st.selectbox("Collection Method", collection_options)
        if collection_method != "Other":
            method_description = collection_df[collection_df["Collection Method"] == collection_method]["Description"].iloc[0]
            st.info(f"📝 {method_description}")
        volume = st.number_input("Estimated Volume (kg/month)", min_value=0)
        transportation = st.text_input("Transportation Mode")
        processing_tech = st.text_input("Processing Technology (if any)")
        st.subheader("End-of-Life Chain Assessment")
        current_eol = st.text_area("Current EoL Activities", help="What activities are you currently performing in the End-of-Life chain?")
        missing_eol = st.text_area("Missing/Planned EoL Activities", help="What activities are missing or planned, and why?")
        value_chain_exp = st.text_area("Value Chain Collaboration Experience", help="Have you set up value chains with smaller/other parties before?")
        
        st.write("Risk Factor Assessment (1-8, where 1 is lowest risk and 8 is highest risk)")
        col1, col2 = st.columns(2)
        with col1:
            risk_financial = st.slider("Financial Risk", 1, 8, 4)
            risk_technical = st.slider("Technical Risk", 1, 8, 4)
            risk_operational = st.slider("Operational Risk", 1, 8, 4)
        with col2:
            risk_regulatory = st.slider("Regulatory Risk", 1, 8, 4)
            risk_market = st.slider("Market Risk", 1, 8, 4)
            risk_environmental = st.slider("Environmental Risk", 1, 8, 4)

        st.write("Value Chain Responsibility Assessment")
        value_chain_type = st.radio("Value Chain Type", ["Open Loop", "Closed Loop", "Hybrid/Mixed", "Not Determined"])
        responsibility = st.radio("Primary Responsibility", ["Own Organization", "Partner Organization", "Shared", "Not Determined"])
        proximity = st.slider("Proximity to Responsible Party", 1, 5, 3, help="1: How feasible is it for you to directly communicate with the responsible partner? 1: Very far, 5: Very close")
        material_trace = st.radio("Material Traceability", ["Fully Traceable", "Partially Traceable", "Limited Traceability", "Not Traceable"])
        
        risks = st.text_area("Additional Risks / Concerns")
        interest = st.radio("Willing to collaborate?", ["Yes", "No", "Maybe"])
        submitted = st.form_submit_button("Save Interview")

        if submitted:
            new_entry = pd.DataFrame([{
                "timestamp": datetime.now(),
                "name": name, "role": role, "org": org, "location": location,
                "material_types": material_types, "collection_method": collection_method,
                "volume": volume, "transportation": transportation,
                "processing_tech": processing_tech, "current_eol": current_eol,
                "missing_eol": missing_eol, "value_chain_exp": value_chain_exp,
                "risk_financial": risk_financial, "risk_technical": risk_technical,
                "risk_operational": risk_operational, "risk_regulatory": risk_regulatory,
                "risk_market": risk_market, "risk_environmental": risk_environmental,
                "value_chain_type": value_chain_type, "responsibility": responsibility,
                "proximity": proximity, "material_trace": material_trace,
                "risks": risks, "interest": interest
            }])
            try:
                old_data = pd.read_csv(interview_file)
                updated = pd.concat([old_data, new_entry], ignore_index=True)
            except FileNotFoundError:
                updated = new_entry
            updated.to_csv(interview_file, index=False)
            st.success("Interview saved!")

    st.subheader("Saved Interviews")
    try:
        interview_data = pd.read_csv(interview_file)
        st.dataframe(interview_data)
    except FileNotFoundError:
        st.info("No interviews saved yet.")

with tab2:
    st.header("New Material Flow Entry")
    with st.form("flow_form"):
        source_org = st.text_input("Source Organization")
        source_type = st.text_input("Source Type (Airline, MRO, etc.)")
        material_type = st.text_input("Material Type")
        volume_flow = st.number_input("Volume (kg/month)", min_value=0)
        source_location = st.text_input("Source Location")
        collection = st.text_input("Collection Method")
        transport = st.text_input("Transport Mode")
        destination = st.text_input("Destination")
        processor = st.text_input("Processor")
        notes = st.text_area("Additional Notes")
        submitted_flow = st.form_submit_button("Save Flow")

        if submitted_flow:
            new_flow = pd.DataFrame([{
                "timestamp": datetime.now(),
                "source_org": source_org, "source_type": source_type,
                "material_type": material_type, "volume_kg_month": volume_flow,
                "source_location": source_location, "collection_method": collection,
                "transport_mode": transport, "destination": destination,
                "processor": processor, "notes": notes
            }])
            try:
                old_flows = pd.read_csv(flow_file)
                updated_flows = pd.concat([old_flows, new_flow], ignore_index=True)
            except FileNotFoundError:
                updated_flows = new_flow
            updated_flows.to_csv(flow_file, index=False)
            st.success("Material flow saved!")

    st.subheader("Mapped Material Flows")
    try:
        flow_data = pd.read_csv(flow_file)
        st.dataframe(flow_data)
    except FileNotFoundError:
        st.info("No material flows saved yet.")
