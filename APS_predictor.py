import streamlit as st
import numpy as np
from download_button_file import download_button
import importlib

def pred_with_sparse(A,train_ind,train_labels,t=1,eps=0.0000001,inter=1):
    N=A.shape[0]
    m=np.max(train_labels)+1
    U=np.zeros((N,m))
    U[train_ind,train_labels]=1
    #w=np.matmul(A,np.sum(A,axis=0))#-diagn
    V=np.matmul(A,np.matmul(A.T,U))#-U*diagn[:,None]
    w=np.sum(V,axis=1)
    #print(sum(w==0))
    Wtot=np.matmul(w,U)
    Q=np.matmul(V.T,U)/Wtot
    f=1/Q[range(m),range(m)]
    lgQ=np.log(Q+eps*(Q==0))
    #F=np.matmul(V,lgQ*f[:,None])-(w[:,None]*np.matmul(f,Q))
    F=np.matmul(V/w[:,None],lgQ*f[:,None])-(np.matmul(f,Q))
    test_ind=list(set(range(N))-set(train_ind))
    #print(np.array(test_ind))
    return np.argmax(F[test_ind,:],axis=1)


def village_kernel_pred(X,W,y,train_ind,symmetrize=0,insig=1,wt=1):
    Y=np.matmul(X,W)
    B=distance_sq(Y,y)*insig*wt
    if symmetrize:        
        A1=np.exp(-B+np.min(B,axis=1)[:,None])
        A2=np.exp(-B+np.min(B[train_ind,:],axis=0))
        A=A1/np.sum(A1,axis=1)[:,None]+A2/np.sum(A2[train_ind,:],axis=0)
    else:
        A=np.exp(-B)
    return A

def distance_sq(x,y):
    return -2*np.matmul(x,y.T)+np.sum(x*x,axis=1)[:,None]+np.sum(y*y,axis=1)



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
        multi_values = st.checkbox(
        "Use Multiple Values", False, help="Pen Digits Dataset")
        if multi_values:
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
            print('Here:'+str(All_pars.shape))
        else:
            colslens=[]
            All_pars=[]
            for i in range(7):
    
                a=int(i/2)
                b=i-2*a
                if b==0:
                    colslens.append(st.columns((1, 1)))
                All_pars.append(colslens[a][b].number_input('Par '+str(i),min_value=-10000000000.0000001,format='%f', max_value=1000000000.9999999,step=0.00000001,value=0.1))
                

    

        #lenses=set(lens_input)
                    
    
    #with st.form("parameters"):
    if uploaded_file or Sample_data:
        with st.form(key="my_form"):

            run=st.form_submit_button(label="Predict")
