import sys
import os
import requests
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


st.set_page_config(
    page_title="StockLens AI – Stock Analysis Assistant ",
    page_icon="📊",
    
)

st.title('📊 StockLens.AI')

# Function to format market cap value
def format_market_cap(value):
  if value >= 1_000_000_000_000:
    return f"{value / 1_000_000_000_000:.1f}T"
  elif value >= 1_000_000_000:
    return f"{value / 1_000_000_000:.1f}B"
  elif value >= 1_000_000:
    return f"{value / 1_000_000:.1f}M"
  else:
    return str(value)

labels = ['Apple', 'Microsoft', 'Amazon', 'Tesla','Nvidia']
cols = st.columns(len(labels))

for col, label in zip(cols, labels):
  with col:
    if st.button(label):
      st.session_state['stock_input'] = label

stock_input = st.text_input("Try another companies:", key="stock_input")

company = stock_input

if company:
  with st.spinner('Fetching stock data...'):
    try:
      url = "http://127.0.0.1:8000/stocks/analyze"
      response = requests.post(url,json={'company':company})

      if response.status_code == 200:
        result = response.json()
        st.subheader(f"Stock Analysis for {company.upper()}")
        st.write(f"- **Current Price**: {round(result['stock_price'],2)}")
        st.write(f"- **Market Cap**: {format_market_cap(result['market_cap'])}")
        st.write(f"- **52 Week High/Low**: {int(round(float(result['week_52_high'])))}/{int(round(float(result['week_52_low'])))}")
        st.write(f"- **Analyst Rating**: {result['analyst_rating']:.1f}")
        news = result['recent_news'][0]
        st.write(f"- **Recent News**: {news['summary']}")
        decision_color = {
          "buy": "#52a447",   
          "sell": "#d9534f",  
          "hold": "#0275d8"   
        }
        decision = result['trade_decision'].lower()
        color = decision_color.get(decision, "#444") 

        st.markdown(f"""<p style=' font-size:18px;color:#fff; background-color: {color}; padding:10px; border-radius:4px; font-weight:500;'>Trade Decision: <span style='font-size:20px; text-transform:uppercase;'>{decision}</span></p>""", unsafe_allow_html=True)
        st.write(f"**Explanation**: {result['explanation']} ")

        with st.expander(label='Research Summary'):
          st.markdown(f"""
            <p>{result['research_summary']}</p>
            """,unsafe_allow_html=True
          )

      
      else:
        st.error(f"Backend error: {response.status_code}")
    
    except Exception as e:
      st.error(f"Failed to connect to backend: {e}")