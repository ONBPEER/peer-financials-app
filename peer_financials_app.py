import streamlit as st
import pandas as pd

# Title
st.title("Peer Financials Lookup Tool")

# User Input
company_input = st.text_input("Enter a public company name to find peers:")

# Dummy peer data for demo purposes
# In a real deployment, this would be replaced with a dynamic lookup
if company_input:
    peers_data = {
        "Metric": [
            "Revenue (Bn USD)",
            "Revenue Growth YoY (%)",
            "EBITDA (Bn USD)",
            "EBITDA Margin (%)"
        ],
        f"{company_input} (2023)": [34.90, 3.0, 7.80, 22.4],
        f"{company_input} (2024)": [36.00, 3.2, 8.10, 22.5],
        "MSA Safety (2023)": [1.40, 5.3, 0.28, 20.0],
        "MSA Safety (2024)": [1.47, 5.0, 0.30, 20.4],
        "3M Company (2023)": [32.10, 1.2, 7.00, 21.8],
        "3M Company (2024)": [32.50, 1.2, 7.10, 21.8],
        "Joyson Safety (2023)": [7.20, 4.0, 1.10, 15.3],
        "Joyson Safety (2024)": [7.50, 4.2, 1.15, 15.3],
        "Avon Protection (2023)": [0.30, -3.2, 0.06, 20.0],
        "Avon Protection (2024)": [0.32, 6.7, 0.07, 21.9]
    }

    df = pd.DataFrame(peers_data)

    # Description Table
    descriptions = {
        "Company": [
            company_input,
            "MSA Safety",
            "3M Company",
            "Joyson Safety",
            "Avon Protection"
        ],
        "Business Description": [
            f"{company_input} is a global technology and manufacturing company offering safety and productivity solutions.",
            "MSA Safety designs and manufactures industry-leading safety products including gas detection and fall protection.",
            "3M offers personal protective equipment including respirators, eyewear, and fall protection solutions.",
            "Joyson Safety produces automotive safety systems like airbags and seatbelts for OEMs worldwide.",
            "Avon Protection makes high-performance protective gear for military, law enforcement, and industrial markets."
        ]
    }

    desc_df = pd.DataFrame(descriptions)

    # Show tables
    st.subheader("Business Descriptions")
    st.dataframe(desc_df)

    st.subheader("Peer Financials")
    st.dataframe(df)

    # CSV Download
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Financials as CSV",
        data=csv,
        file_name=f"{company_input}_Peer_Financials.csv",
        mime='text/csv'
    )
else:
    st.info("Enter a company name above to generate the peer data.")
