# A streamlit web app that automates the EDA(exploratory Data Analysis) process
from PIL import Image
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import streamlit as st  # Streamlit Framework
import pandas as pd  # for creating DataFrames and series
import numpy as np  # statistics purposes
import plotly.express as px
import seaborn as sns  # plots
import matplotlib.pyplot as plt  # plots
from scipy import stats  # for statistical scores
from streamlit_option_menu import option_menu  # For implementation of options
from st_aggrid import AgGrid  # for implementation of AgGrid
import altair as alt  # Data Visualization


# navigation bar
selected = option_menu(
    menu_title="Main Menu",
    options=["Analytics", "Dashboard"],
    icons=["graph-up-arrow", "kanban"],
    default_index=0,
    orientation='horizontal'
)

if selected == "Analytics":

    # Page title
    st.title("EDA Automation")
    # Creating the sidebar
    # st.sidebar.multiselect("columns", columns(df))
    # Mid page
    st.markdown("### Select your file")
    file = st.file_uploader("upload your csv")
    try:
        df = pd.read_csv(file)
        # st.write(df)
        AgGrid(df)
        st.markdown("## About your Dataset")
        st.info(df.dtypes)
        st.subheader("Statistical Description of Data")
        st.write(df.describe())
        cols = df.columns

        # stats
        st.markdown("# Statistics ")
        st.caption(
            "Choose the columns on the sidebar to plot the statistical scores and conclusions")
        x_axis = st.selectbox("Select X-axis", (df.columns))
        y_axis = st.selectbox("Select Y_axis", (df.columns))

        def pearson():
            pearson_coef, p_val = stats.pearsonr(df[x_axis], df[y_axis])
            st.write("The Pearson Correlation Coefficient is",
                     pearson_coef, " with a P-value of P =", p_val)
            if p_val < 0.001:
                st.write(
                    "The p value is less than 0.001 that implies that there is a strong correlation")
            if 0.01 < p_val < 0.05:
                st.write(
                    "The p value is less than 0.05 that implies that there is moderate correlation")
            if 0.05 < p_val < 0.1:
                st.write(
                    "The p value is less than 0.1 that implies that these is weak correlation ")
            if p_val > 0.1:
                st.write(
                    "The p value is more than 0.1 that implies there is no significant correlation")

        if st.button("get score"):
            pearson()
        # value counts

        st.subheader("Know Your Value counts")
        vals = st.selectbox("Select the column", (df.columns))
        st.write(df[vals].value_counts().to_frame())

        # Grouping
        group_selection = st.multiselect(
            "Select the columns that you want to group", (df.columns))
        group_by_cols = st.multiselect(
            "Select the columns that you want to group by", (group_selection))

        grouped = df.groupby(group_by_cols, as_index=False).mean()
        st.write(grouped)

    except ValueError as ve:
        st.write("")


if selected == "Dashboard":  # x axis and y axis
    file = st.file_uploader("upload your csv")
    try:
        df = pd.read_csv(file)
        df = df.rename(
            columns={'long': 'lon', 'latitude': 'Latitude', 'longitude': 'Longitude'})
        x_axis = st.sidebar.selectbox("select X-axis column", (df.columns))
        y_axis = st.sidebar.selectbox("select Y-axis column", (df.columns))

        # Chart elements
        chart = st.sidebar.selectbox(
            "Choose your Chart", ("Line chart", "Map Chart", "Bar Chart", "Area Chart", "Box plot", "Violin Plot"))

        def plot():
            st.markdown("# Plot")
            if chart == "Line chart":
                fig, ax = plt.subplots()
                ax = sns.lineplot(x=x_axis, y=y_axis, data=df)
                st.pyplot(fig)

            if chart == "Box plot":
                fig, ax = plt.subplots()
                ax = sns.boxplot(x=x_axis, y=y_axis, data=df)
                st.pyplot(fig)

            if chart == "Area Chart":
                c = alt.Chart(df).mark_area().encode(x=x_axis, y=y_axis)
                st.altair_chart(c, use_container_width=True)

            if chart == "Map Chart":
                map_df = pd.DataFrame(
                    df[[x_axis, y_axis]], columns=['lat', 'lon'])
                st.map(map_df)
            if chart == 'Bar Chart':
                bar_df = pd.DataFrame(df[[x_axis, y_axis]])
                st.bar_chart(bar_df)

            if chart == 'Violin Plot':
                fig, ax = plt.subplots()
                ax = sns.violinplot(data=df, x=x_axis, y=y_axis)
                st.pyplot(fig)
        if st.sidebar.button("plot"):
            plot()
    except ValueError as ve:
        st.write("")
