import streamlit as st
from ai_dental_intake import extract_patient_intake


def display_symptom(value):
    if value is True:
        return "Yes"
    elif value is False:
        return "No"
    else:
        return "Not provided"

st.title("Dental Intake Extractor")
st.write("Describe your own dental problem in your own words")
patient_description = st.text_area("Describe your symptoms")
button_clicked = st.button("Extract Intake")
if button_clicked:
    if patient_description:
        structured_intake = extract_patient_intake(patient_description)
        st.subheader("Structured Intake\n\n")
        st.write("Complaint")
        st.write(structured_intake.complaint)
        st.write("Duration")
        st.write(structured_intake.duration_days)
        st.write("Symptoms")
        if structured_intake.symptoms:
            st.write(f"Swelling: {display_symptom(structured_intake.symptoms.swelling)}")
            st.write(f"Bleeding: {display_symptom(structured_intake.symptoms.bleeding)}")
            st.write(f"Fever: {display_symptom(structured_intake.symptoms.fever)}")
        else:
            st.write("No symptom information provided")

    else:
        st.warning("Please describe your problem")