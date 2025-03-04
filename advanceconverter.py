import streamlit as st
import requests
from datetime import datetime

# ======================
# APP CONFIGURATION
# ======================
st.set_page_config(
    page_title="Nexus Converter Pro",
    page_icon="🔁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================
# CUSTOM CSS STYLING
# ======================
st.markdown("""
 
    <style>
    /* Base educational theme */
    :root {
        --primary: #2C3E50;     /* Professional Navy */
        --secondary: #2980B9;   /* Trustworthy Blue */
        --accent: #16A085;      /* Fresh Teal */
        --light: #FDFEFE;       /* Clean White */
        --background: #EAEDED;   /* Soft Gray */
    }

    /* Main container styling */
    .stApp {
        background: var(--accent) !important;
        font-family:  Roboto Slab , sans-serif !important;
    }
    
    /* Card styling */
    .conversion-card {
        background: var(--primary) !important;
        border-radius: 12px !important;
        padding: 2rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.9) !important;
        border: 1px solid rgba(0, 0, 0, 2) !important;
    }

    /* Input fields */
    .stNumberInput input, .stSelectbox select {
        background: var(--secondary) !important;
        border: 2px solid #D0D3D4 !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        transition: all 0.2s ease !important;
    }

    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: var(--secondary) !important;
        box-shadow: 0 0 0 3px rgba(41, 128, 185, 0.1) !important;
    }

    /* Tabs styling */
    [data-baseweb="tab-list"] {
        gap: 10px !important;
        padding: 8px !important;
    }

    [data-baseweb="tab"] {
        background: var(--primary) !important;
        color: var(--secondary) !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        transition: all 0.2s ease !important;
        border: 1px solid #D0D3D4 !important;
    }

    [data-baseweb="tab"][aria-selected="true"] {
        background: var(--secondary) !important;
        color: var(--light) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }

    /* Result box */
    .result-box {
        background: var(--primary) !important;    #E8F6F3
        padding: 1.5rem !important;
        border-radius: 8px !important;
        border-left: 4px solid var(--primary) !important;
        margin-top: 1.5rem !important;
    }

    /* Button styling */
    .stButton>button {
        background: var(--secondary) !important;
        color: var(--light) !important;
        border-radius: 8px !important;
        padding: 0.8rem 1.5rem !important;
        transition: all 0.2s ease !important;
        border: none !important;
        width: 100% !important;
    }

    .stButton>button:hover {
        background: #2471A3 !important;
        transform: translateY(-1px) !important;
    }

    /* Title styling */
    h1 {
        color: var(--primary) !important;
        border-bottom: 3px solid var(--primary);
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem !important;
    }

    /* Divider styling */
    hr {
        border-color: var(--primary) !important;
        margin: 1.5rem 0 !important;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .stNumberInput, .stSelectbox {
            width: 100% !important;
            margin: 0.5rem 0 !important;
        }
    }
    </style>

          
            """, unsafe_allow_html=True)


# ======================
# API CONFIGURATION
# ======================
API_KEY = "8e4bc4e1f13b1f4c56e0becb"  # Replace with your API key
CURRENCY_API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

# ======================
# CONVERSION FUNCTIONS
# ======================
def get_currency_rates():
    try:
        response = requests.get(CURRENCY_API_URL)
        data = response.json()
        return data.get('conversion_rates', {})
    except Exception as e:
        st.error(f"Error fetching currency rates: {str(e)}")
        return {}

def convert_units(value, from_unit, to_unit, category):
    conversion_matrix = {
        'length': {
            'meters': 1,
            'kilometers': 1000,
            'centimeters': 0.01,
            'miles': 1609.34,
            'inches': 0.0254,
            'yards': 0.9144,
            'millimeters': 0.001
        },
        'weight': {
            'kilograms': 1,
            'grams': 0.001,
            'pounds': 0.453592,
            'ounces': 0.0283495,
            'tons': 907.185,
            'carats': 0.0002
        },
        'temperature': {
            'celsius': {'celsius': lambda x: x,
                       'fahrenheit': lambda x: (x * 9/5) + 32,
                       'kelvin': lambda x: x + 273.15},
            'fahrenheit': {'fahrenheit': lambda x: x,
                          'celsius': lambda x: (x - 32) * 5/9,
                          'kelvin': lambda x: (x - 32) * 5/9 + 273.15},
            'kelvin': {'kelvin': lambda x: x,
                      'celsius': lambda x: x - 273.15,
                      'fahrenheit': lambda x: (x - 273.15) * 9/5 + 32}
        },
        'digital': {
            'bits': 1,
            'bytes': 8,
            'kilobytes': 8192,
            'megabytes': 8388608,
            'gigabytes': 8589934592,
            'terabytes': 8796093022208
        },
        'energy': {
            'joules': 1,
            'calories': 4.184,
            'kilowatt-hours': 3600000,
            'electronvolts': 1.60218e-19,
            'btu': 1055.06
        }
    }

    try:
        if category == 'temperature':
            return conversion_matrix[category][from_unit][to_unit](value)
        else:
            base_value = value * conversion_matrix[category][from_unit]
            return base_value / conversion_matrix[category][to_unit]
    except KeyError:
        return None

# ======================
# UI COMPONENTS
# ======================
def main():
    st.title("🔁 Nexus Converter Pro")
    st.markdown("---")
    
    categories = {
        "💱 Currency": "currency",
        "📏 Length": "length",
        "⚖️ Weight": "weight",
        "🌡️ Temperature": "temperature",
        "💻 Digital": "digital",
        "⚡ Energy": "energy"
    }
    
    tabs = st.tabs(list(categories.keys()))
    
    for tab, (display_name, category) in zip(tabs, categories.items()):
        with tab:
            with st.container():
                st.markdown('<div class="conversion-card">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 3])
                
                # Input Column
                with col1:
                    amount = st.number_input(
                        f"Enter value ({display_name.split()[1]})",
                        min_value=0.0,
                        value=1.0,
                        step=0.1,
                        key=f"input_{category}"
                    )
                    
                    unit_sets = {
                        'currency': ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "INR"],
                        'length': ["meters", "kilometers", "centimeters", "miles", "inches", "yards", "millimeters"],
                        'weight': ["kilograms", "grams", "pounds", "ounces", "tons", "carats"],
                        'temperature': ["celsius", "fahrenheit", "kelvin"],
                        'digital': ["bits", "bytes", "kilobytes", "megabytes", "gigabytes", "terabytes"],
                        'energy': ["joules", "calories", "kilowatt-hours", "electronvolts", "btu"]
                    }
                    
                    from_unit = st.selectbox(
                        "From",
                        unit_sets[category],
                        key=f"from_{category}"
                    )
                
                # Arrow Column
                with col2:
                    st.markdown("<h1 style='text-align: center; margin-top: 35px;'>➔</h1>", 
                              unsafe_allow_html=True)
                
                # Result Column
                with col3:
                    to_unit = st.selectbox(
                        "To",
                        unit_sets[category],
                        key=f"to_{category}"
                    )
                    
                    result = None
                    if category == 'currency':
                        rates = get_currency_rates()
                        if rates:
                            if from_unit in rates and to_unit in rates:
                                result = amount * rates[to_unit] / rates[from_unit]
                            else:
                                st.error("Selected currency not available in rates")
                        else:
                            st.error("Failed to fetch currency rates")
                    else:
                        result = convert_units(amount, from_unit, to_unit, category)
                
                # Display Result
                if result is not None:
                    with col3:
                        st.markdown(f"""
                        <div class="result-box">
                            <h2 style="margin: 0; color: white;">
                                {amount:.4f} {from_unit} =<br>
                                {result:.4f} {to_unit}
                            </h2>
                            {f'<p style="margin: 5px 0 0; font-size: 0.8em;">Rate updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>' if category == 'currency' else ''}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Conversion not possible. Check unit selections.")
                
                st.markdown('</div>', unsafe_allow_html=True)

# ======================
# MAIN EXECUTION
# ======================
if __name__ == "__main__":
    main()