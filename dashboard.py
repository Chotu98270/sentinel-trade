import streamlit as st
import pandas as pd

st.title(" Sentinel Trade Dashboard")

# Read log file
try:
    with open("log.txt", "r") as f:
        lines = f.readlines()
except:
    lines = []

#METRICS (TOP)
if len(lines) > 0:
    last_line = lines[-1]

    try:
        profit_part = last_line.split("Profit:")[1]
        profit_value = profit_part.split("(")[0].strip()

        col1, col2 = st.columns(2)
        col1.metric(" Balance", "10000")  # (static for now)
        col2.metric(" Profit", profit_value)

    except:
        st.write("No data yet")

#  Convert log → table
data = []
for line in lines:
    parts = line.strip().split("|")
    data.append([p.strip() for p in parts])

df = pd.DataFrame(data)

if not df.empty and len(df.columns) == 6:
    df.columns = ["Action", "Price", "RSI", "Balance", "Net Worth", "Profit"]

#  COLOR FUNCTIONS
def color_action(val):
    if "BUY" in val:
        return "color: green"
    elif "SELL" in val:
        return "color: red"
    return "color: gray"

def color_profit(val):
    try:
        num = float(val.replace("Profit:", "").split()[0])
        if num > 0:
            return "color: green"
        elif num < 0:
            return "color: red"
    except:
        pass
    return ""

#  Styled Table (ONE ONLY )
st.subheader(" Trade History")

if not df.empty:
    styled_df = df.style.applymap(color_action, subset=["Action"]) \
                         .applymap(color_profit, subset=["Profit"])
    st.dataframe(styled_df)
else:
    st.write("No trades yet")

#  Last trade
if len(lines) > 0:
    st.subheader(" Last Trade")
    st.write(lines[-1])

#  Profit graph
profits = []

for line in lines:
    if "Profit:" in line:
        try:
            p = float(line.split("Profit:")[1].split("(")[0])
            if len(profits) == 0 or p != profits[-1]:
                profits.append(p)
        except:
            pass

st.subheader(" Profit Graph")

if len(profits) > 0:
    st.line_chart(profits)
else:
    st.write("No profit data yet")