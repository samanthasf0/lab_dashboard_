# lab_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

# ------------------ APP HEADER ------------------
st.title(" Lab Data Dashboard")
st.subheader("Developed by Samantha Sulbaran | University of Houston Chemical Engineering")
st.markdown("---")

# ------------------ UPLOAD DATA ------------------
st.header("Upload Lab Data")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.dataframe(df.head())

    # ------------------ SUMMARY STATS ------------------
    st.subheader("Summary Statistics")
    st.write(df.describe())

    # ------------------ PLOT DATA ------------------
    st.subheader("Data Plots")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    if len(numeric_cols) >= 2:
        x_col = st.selectbox("Select X-axis", numeric_cols, index=0)
        y_col = st.selectbox("Select Y-axis", numeric_cols, index=1)
        
        fig, ax = plt.subplots()
        ax.scatter(df[x_col], df[y_col], color='blue')
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} vs {x_col}")
        st.pyplot(fig)

        # ------------------ LINEAR REGRESSION ------------------
        st.subheader("Linear Regression")
        coeffs = np.polyfit(df[x_col], df[y_col], 1)
        slope, intercept = coeffs
        st.write(f"Slope: {slope:.4f}, Intercept: {intercept:.4f}")

        # Plot regression line
        y_fit = slope * df[x_col] + intercept
        fig2, ax2 = plt.subplots()
        ax2.scatter(df[x_col], df[y_col], color='blue', label='Data')
        ax2.plot(df[x_col], y_fit, color='red', label='Fit')
        ax2.set_xlabel(x_col)
        ax2.set_ylabel(y_col)
        ax2.set_title(f"{y_col} vs {x_col} (with Fit)")
        ax2.legend()
        st.pyplot(fig2)

    else:
        st.info("Not enough numeric columns to plot.")

    # ------------------ EXPORT PDF ------------------
    st.subheader("Export PDF Report")
    if st.button("Generate PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Chemical Engineering Lab Report", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, df.to_string())
        pdf.output("lab_report.pdf")
        st.success("PDF generated: lab_report.pdf")
