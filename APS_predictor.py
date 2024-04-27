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
        fens_input=[]
        #with st.form("Lenses"):
        colslens=[]
        for i in range(Nl):

            a=int(i/2)
            b=i-2*a
            if b==0:
                colslens.append(st.columns((1, 1)))
            lens_input.append(colslens[a][b].selectbox(
            "Lens "+str(i+1)+":", ["PCA", "IsolationForest", "L2 Norm"], index=0))
        lenses=set(lens_input)
            
    
    #with st.form("parameters"):
    if uploaded_file or Sample_data:
        st.markdown("## Hyper Parameters")

        cols = st.columns((1, 1))
        villages = cols[0].number_input('Number of villages',min_value=1, max_value=data.shape[0],step=1,value=np.minimum(200,X.shape[0]))
        neighbors = cols[1].number_input('Number of nearest neighbors',min_value=1, max_value=data.shape[0],step=1,value=np.minimum(20,X.shape[0]))
        #new_method=st.checkbox('Use new method',False)
        with st.form(key="my_form"):

            run=st.form_submit_button(label="Cluster")
