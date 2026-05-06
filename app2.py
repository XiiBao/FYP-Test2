import streamlit as st
import pysd
import pandas as pd
import matplotlib.pyplot as plt
import os

# ========================
# FILE PATH
# ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'Customer.mdl')

st.title("👥 Staff Dynamics Simulator")

# ========================
# SIDEBAR SLIDERS (MUST COME FIRST)
# ========================
st.sidebar.header("⚙️ Model Parameters")

hiring_rate = st.sidebar.slider(
    "Hiring Rate (People/Month)", 0.0, 2.0, 0.1, 0.1
)

attrition_rate = st.sidebar.slider(
    "Attrition Rate (%)", 0.0, 0.2, 0.05, 0.01
)

complaint_sensitivity = st.sidebar.slider(
    "Complaint Sensitivity", 0.0, 1.0, 0.5, 0.1
)

resolution_capacity = st.sidebar.slider(
    "Resolution Capacity (Complaints/Person/Month)", 0.0, 0.5, 0.2, 0.05
)

service_impact_factor = st.sidebar.slider(
    "Service Impact Factor", 0.0, 1.0, 0.5, 0.1
)

# ========================
# LOAD & RUN MODEL
# ========================
try:
    model = pysd.read_vensim(file_path)

    results = model.run(
        params={
            'hiring_rate': hiring_rate,
            'attrition_rate': attrition_rate,
            'complaint_sensitivity': complaint_sensitivity,
            'resolution_capacity': resolution_capacity,
            'service_impact_factor': service_impact_factor
        },
        return_columns=[
            'staff_count',
            'complaints',
            'response_time',
            'senior_availability'
        ]
    )

except Exception as e:
    st.error(f"❌ Error loading model: {str(e)}")
    st.info("Make sure Customer.mdl is valid and in the same directory")
    st.stop()

# ========================
# KEY METRICS
# ========================
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

final_staff = results['staff_count'].iloc[-1]
final_complaints = results['complaints'].iloc[-1]
final_response_time = results['response_time'].iloc[-1]
final_availability = results['senior_availability'].iloc[-1]

with col1:
    st.metric("Final Staff Count", f"{final_staff:.1f} people")

with col2:
    st.metric("Final Complaints", f"{final_complaints:.1f}")

with col3:
    st.metric("Response Time", f"{final_response_time:.2f} hours")

with col4:
    st.metric("Senior Availability", f"{final_availability:.1%}")

# ========================
# CHARTS
# ========================
st.subheader("📈 Simulation Results")

# Chart 1: Staff Count
fig1, ax1 = plt.subplots()
ax1.plot(results.index, results['staff_count'])
ax1.set_title('Staff Count Over Time')
ax1.set_xlabel('Time (Months)')
ax1.set_ylabel('Staff Count')
st.pyplot(fig1)

# Chart 2: Complaints
fig2, ax2 = plt.subplots()
ax2.plot(results.index, results['complaints'])
ax2.set_title('Complaints Over Time')
ax2.set_xlabel('Time (Months)')
ax2.set_ylabel('Complaints')
st.pyplot(fig2)

# Chart 3: Response Time
fig3, ax3 = plt.subplots()
ax3.plot(results.index, results['response_time'])
ax3.set_title('Response Time Over Time')
ax3.set_xlabel('Time (Months)')
ax3.set_ylabel('Response Time (Hours)')
st.pyplot(fig3)

# Chart 4: Senior Availability
fig4, ax4 = plt.subplots()
ax4.plot(results.index, results['senior_availability'])
ax4.set_title('Senior Availability Over Time')
ax4.set_xlabel('Time (Months)')
ax4.set_ylabel('Availability')
st.pyplot(fig4)

# ========================
# COMBINED CHART
# ========================
fig5, ax5 = plt.subplots()
ax5.plot(results.index, results['staff_count'], label='Staff')
ax5.plot(results.index, results['complaints'], label='Complaints')
ax5.plot(results.index, results['response_time'], label='Response Time')

ax5.set_title('Combined View')
ax5.set_xlabel('Time')
ax5.legend()

st.pyplot(fig5)

# ========================
# DATA TABLE
# ========================
st.subheader("📋 Data Table")

if st.checkbox("Show detailed data"):
    st.dataframe(results.round(2))

# ========================
# DOWNLOAD BUTTON
# ========================
csv = results.to_csv()

st.download_button(
    label="📥 Download Results (CSV)",
    data=csv,
    file_name="simulation_results.csv",
    mime="text/csv"
)