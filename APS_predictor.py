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
        #lens_input=[]
        grids=[]
        totsize=1
        for i in range(7):

            colslens.append(st.columns((1, 1, 1)))
            mn=colslens[i][0].number_input('Par '+str(i)+' Min',min_value=-10000000000.0000001,format='%f', max_value=1000000000.9999999,step=0.00000001,value=0.1)
            mx=colslens[i][1].number_input('Par '+str(i)+' Max',min_value=-10000000000.0000001,format='%f', max_value=1000000000.9999999,step=0.00000001,value=0.7)
            stp=colslens[i][2].number_input('Par '+str(i)+' Steps',min_value=1, max_value=100,step=1,value=8)
            grids.append(np.linspace(mn, mx, stp))
            totsize=totsize*grids[0].shape[0]
            print(grids[i])
        Parcheck=np.meshgrid(grids[0],grids[1],grids[2],grids[3],grids[4],grids[5],grids[6])
        All_pars=[]
        for p in range(7):
            All_pars.append(list(np.reshape(Parcheck[0],totsize)))
        All_pars=np.array(All_pars).T
        print(All_pars.shape)

        #lenses=set(lens_input)
                    
    
    #with st.form("parameters"):
    if uploaded_file or Sample_data:
        st.markdown("## Hyper Parameters")

        cols = st.columns((1, 1))
        villages = cols[0].number_input('Number of villages',min_value=1, max_value=data.shape[0],step=1,value=np.minimum(200,X.shape[0]))
        neighbors = cols[1].number_input('Number of nearest neighbors',min_value=1, max_value=data.shape[0],step=1,value=np.minimum(20,X.shape[0]))
        #new_method=st.checkbox('Use new method',False)
        with st.form(key="my_form"):

            run=st.form_submit_button(label="Cluster")
