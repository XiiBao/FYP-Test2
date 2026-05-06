import streamlit as st
import pysd
import pandas as pd
import matplotlib.pyplot as plt

st.title("☕Caffiene Alertness Simulator")

# User input (Slider/Filter)
target_alertness = st.slider(
    "Select Target Alertness",
    min_value=0.0,
    max_value=1.0,
    value=0.05,
    step=0.01
)

model = pysd.read_vensim('Caffeine.mdl')

results = model.run(
    params={'Target alertness': target_alertness},
    return_columns=['Intake rate', 'Metabolization rate']
)

# 🔹 Show raw data
st.subheader("Simulation Data")
st.write(results)

# 🔹 Plot using matplotlib
fig, ax = plt.subplots()
results.plot(ax=ax)
ax.set_ylabel('Rate')
ax.set_xlabel('Time')

st.pyplot(fig) 

