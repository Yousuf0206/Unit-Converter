import streamlit as st
import requests

# App configuration
st.set_page_config(
    page_title="Universal Unit Converter",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# API configuration (Get your free API key from https://fixer.io)
API_KEY = "781ae419858e7d376c407c0414a628d5"
BASE_URL = "http://data.fixer.io/api/latest"

# Conversion functions
def convert_currency(amount, from_curr, to_curr):
    try:
        response = requests.get(f"{BASE_URL}?access_key={API_KEY}")
        data = response.json()
        rates = data['rates']
        return amount * rates[to_curr] / rates[from_curr]
    except Exception as e:
        st.error(f"Error converting currency: {e}")
        return None

def convert_units(value, from_unit, to_unit, category):
    conversions = {
        'length': {
            'meter': 1,
            'kilometer': 1000,
            'centimeter': 0.01,
            'mile': 1609.34,
            'inch': 0.0254
        },
        'weight': {
            'kilogram': 1,
            'gram': 0.001,
            'pound': 0.453592,
            'ounce': 0.0283495
        },
        'temperature': {
            'celsius': lambda c: (c * 9/5) + 32,  # to fahrenheit
            'fahrenheit': lambda f: (f - 32) * 5/9  # to celsius
        }
    }
    
    try:
        if category == 'temperature':
            if from_unit == 'celsius' and to_unit == 'fahrenheit':
                return conversions[category][from_unit](value)
            elif from_unit == 'fahrenheit' and to_unit == 'celsius':
                return conversions[category][from_unit](value)
            else:
                return value
        else:
            base_value = value * conversions[category][from_unit]
            return base_value / conversions[category][to_unit]
    except KeyError:
        return None

# UI Components
def main():
    st.title("📐 Universal Unit Converter")
    st.markdown("---")

    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        category = st.selectbox(
            "Select Conversion Type",
            ["Currency", "Length", "Weight", "Temperature"]
        )

    # Main conversion area
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.subheader("Input")
        amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1)

    with col3:
        st.subheader("Result")
        
    # Conversion parameters
    if category == "Currency":
        currencies = ["USD", "EUR", "GBP", "JPY", "CAD"]
        with col1:
            from_unit = st.selectbox("From", currencies)
        with col2:
            st.markdown("<h2 style='text-align: center;'>➔</h2>", unsafe_allow_html=True)
        with col3:
            to_unit = st.selectbox("To", currencies)
            result = convert_currency(amount, from_unit, to_unit)
    
    else:
        units = {
            "Length": ["meter", "kilometer", "centimeter", "mile", "inch"],
            "Weight": ["kilogram", "gram", "pound", "ounce"],
            "Temperature": ["celsius", "fahrenheit"]
        }
        with col1:
            from_unit = st.selectbox("From", units[category])
        with col2:
            st.markdown("<h2 style='text-align: center;'>➔</h2>", unsafe_allow_html=True)
        with col3:
            to_unit = st.selectbox("To", units[category])
            result = convert_units(amount, from_unit, to_unit, category.lower())

    # Display result
    if result is not None:
        with col3:
            st.markdown(f"""
            <div style="padding: 20px; background-color: #2e2e2e; border-radius: 10px;">
                <h3 style="color: #4CAF50; margin: 0;">
                    {amount:.2f} {from_unit} = {result:.2f} {to_unit}
                </h3>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()