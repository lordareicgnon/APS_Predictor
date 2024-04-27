import streamlit as st
import numpy as np
from download_button_file import download_button
import importlib

run=0
st.write("""
# APS Predictor
""")

runmapperplus=1
if runmapperplus:
    st.markdown("## Upload data for Clustering")
    see_results=0
    uploaded_file='False'
    with st.expander("ℹ️ More information"):
        st.write("Upload data in CSV format with no headers.")
    #with st.sidebar:
    Sample_data = st.checkbox(
        "Predict for the following range", False, help="Pen Digits Dataset")


    if not Sample_data:
        


        uploaded_file = st.file_uploader("Upload CSV", type=".csv")
        #st.write(uploaded_file)
        if uploaded_file:
            data = np.loadtxt(uploaded_file, delimiter=',')
            file_name=uploaded_file.name

    else:
        res=[]
        gn=[]
        cls=[]
        for i in range(7):
            cls.append(st.columns((1, 1)))
        for i in range(7):
            st.markdown("## Parameter "+str(i)+" Range")
            res.append(cls[i][0].number_input('Resolution',min_value=1, max_value=100,step=1,value=8))
            gn.append(cls[i][1].number_input('Gain',min_value=0.0000001, max_value=0.9999999,value=0.6))
            #min = cols[0].number_input('Mininum value',min_value=-10000000000, max_value=1000000000000,value=0.00000001)
            #max = cols[1].number_input('Maximum value',min_value=-10000000000, max_value=1000000000000,value=0.00000001)
            #max = cols[1].number_input('Steps',min_value=2, max_value=1000,step=1,value=2)
            
    
    #with st.form("parameters"):
    if uploaded_file or Sample_data:
        st.markdown("## Hyper Parameters")

        cols = st.columns((1, 1))
        villages = cols[0].number_input('Number of villages',min_value=1, max_value=data.shape[0],step=1,value=np.minimum(200,X.shape[0]))
        neighbors = cols[1].number_input('Number of nearest neighbors',min_value=1, max_value=data.shape[0],step=1,value=np.minimum(20,X.shape[0]))
        #new_method=st.checkbox('Use new method',False)
        with st.form(key="my_form"):

            run=st.form_submit_button(label="Cluster")
