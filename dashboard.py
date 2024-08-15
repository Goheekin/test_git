import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page title
st.title("Vaping Business Sales Dashboard")

# Upload the Excel file
uploaded_file = st.file_uploader("Upload the synthetic dataset Excel file", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Read the uploaded file
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)

    # Ensure 'Date_Sold' is a datetime object
    df['Date_Sold'] = pd.to_datetime(df['Date_Sold'])

    # Extract month and quarter
    df['Month'] = df['Date_Sold'].dt.strftime('%b')  # Short month name (Jan, Feb, ...)
    df['Quarter'] = df['Date_Sold'].dt.to_period('Q')

    # Visualization 1: Number of stock sold based on month in 2023
    monthly_sales = df.groupby('Month')['Num_Stock_Sold'].sum()
    
    # Sort the months in calendar order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_sales = monthly_sales.reindex(month_order)

    # Visualization 2: Number of stock sold by quarter
    quarterly_sales = df.groupby('Quarter')['Num_Stock_Sold'].sum()

    # Display the two graphs in a single row
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Number of Stock Sold Based on Month in 2023")
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        sns.barplot(x=monthly_sales.index, y=monthly_sales.values, palette="coolwarm", ax=ax1)
        ax1.set_title("Number of Stock Sold by Month in 2023")
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Total Number of Stock Sold")

        # Add data labels
        for i in ax1.containers:
            ax1.bar_label(i, fmt='%.0f')

        # Highlight the border
        for spine in ax1.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(1.5)

        st.pyplot(fig1)

    with col2:
        st.subheader("Number of Stock Sold by Quarter in 2023")
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.barplot(x=quarterly_sales.index.astype(str), y=quarterly_sales.values, palette="viridis", ax=ax2)
        ax2.set_title("Number of Stock Sold by Quarter in 2023")
        ax2.set_xlabel("Quarter")
        ax2.set_ylabel("Total Number of Stock Sold")

        # Add data labels
        for i in ax2.containers:
            ax2.bar_label(i, fmt='%.0f')

        # Highlight the border
        for spine in ax2.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(1.5)

        st.pyplot(fig2)

    # Visualization 3: Top 10 Fruit Flavors by Number of Stock Sold
    st.subheader("Top 10 Fruit Flavors by Number of Stock Sold in 2023")
    top_flavors = df.groupby('Product_Name')['Num_Stock_Sold'].sum().nlargest(10)
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_flavors.values, y=top_flavors.index, palette="Set2", ax=ax3)
    ax3.set_title("Top 10 Fruit Flavors by Number of Stock Sold")
    ax3.set_xlabel("Total Number of Stock Sold")
    ax3.set_ylabel("Fruit Flavors")

    # Add data labels
    for i in ax3.containers:
        ax3.bar_label(i, fmt='%.0f')

    # Highlight the border
    for spine in ax3.spines.values():
        spine.set_edgecolor('black')
        spine.set_linewidth(1.5)

    st.pyplot(fig3)

    # Display raw data if needed
    if st.checkbox("Show Raw Data"):
        st.subheader("Raw Data")
        st.write(df)
