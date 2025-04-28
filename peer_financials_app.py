import streamlit as st
import requests
import pandas as pd
import io

# -- SETTINGS --
COMPANIES_HOUSE_API_KEY = st.secrets["companies_house_api_key"]
BASE_URL = "https://api.company-information.service.gov.uk"

# -- FUNCTIONS --

def search_company(name):
    url = f"{BASE_URL}/search/companies?q={name}"
    response = requests.get(url, auth=(COMPANIES_HOUSE_API_KEY, ''))
    if response.status_code == 200:
        items = response.json().get("items", [])
        if items:
            return items[0]["company_number"], items[0]["title"]
    return None, None

def get_company_info(company_number):
    url = f"{BASE_URL}/company/{company_number}"
    response = requests.get(url, auth=(COMPANIES_HOUSE_API_KEY, ''))
    if response.status_code == 200:
        return response.json()
    return {}

def get_latest_accounts(company_number):
    url = f"{BASE_URL}/company/{company_number}/filing-history?category=accounts"
    response = requests.get(url, auth=(COMPANIES_HOUSE_API_KEY, ''))
    if response.status_code == 200:
        items = response.json().get("items", [])
        financials = []
        for item in items:
            if 'description' in item and 'links' in item:
                date = item.get('date', 'Unknown Date')
                description = item.get('description', 'No Description')
                financials.append({
                    'Date': date,
                    'Description': description
                })
        return financials
    return []

def mock_financials():
    """Mocked financial data for display (Replace with real parser if available)."""
    import random
    years = ['2022', '2021', '2020']
    data = {
        "Year": years,
        "Revenue (£)": [random.randint(10, 50) * 1_000_000 for _ in years],
        "Net Profit (£)": [random.randint(1, 10) * 1_000_000 for _ in years],
        "Total Assets (£)": [random.randint(50, 200) * 1_000_000 for _ in years]
    }
    return pd.DataFrame(data)

def get_peers_mock(company_name):
    """Mocked peer companies - can later link based on SIC code."""
    return [f"{company_name} Holdings Ltd", f"{company_name} Global Ltd", f"{company_name} Solutions Plc"]

# -- STREAMLIT APP --

st.title("📊 Peer Financials Benchmarking (UK) — Premium Version")

company_name = st.text_input("Enter a Company Name:")

if st.button("Find Peers and Financials"):
    if not company_name:
        st.error("Please enter a valid company name.")
    else:
        company_number, matched_name = search_company(company_name)
        
        if company_number:
            st.success(f"Found Company: {matched_name} (No. {company_number})")
            
            company_info = get_company_info(company_number)
            peers = get_peers_mock(company_name)
            financials_df = mock_financials()
            
            st.subheader("🏢 Company Description:")
            st.write(company_info.get("sic_codes", ["No description available"]))
            
            st.subheader("👥 Suggested Peers:")
            st.write(", ".join(peers))
            
            st.subheader("📈 Financials (Mocked Data for Now)")
            st.dataframe(financials_df)
            
            st.subheader("📊 Financial Trends:")
            st.line_chart(financials_df.set_index('Year')[["Revenue (£)", "Net Profit (£)", "Total Assets (£)"]])
            
            # Download Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                financials_df.to_excel(writer, index=False, sheet_name='Financials')
                worksheet = writer.sheets['Financials']
                for idx, col in enumerate(financials_df):
                    series = financials_df[col]
                    max_len = max((
                        series.astype(str).map(len).max(),
                        len(str(series.name))
                    )) + 2
                    worksheet.set_column(idx, idx, max_len)
            st.download_button(
                label="📥 Download Financials as Excel",
                data=output.getvalue(),
                file_name=f"{company_name}_financials.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        else:
            st.error("Company not found. Try a slightly different spelling.")

