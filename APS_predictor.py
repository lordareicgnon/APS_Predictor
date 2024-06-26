import streamlit as st
import numpy as np
from download_button_file import download_button
import importlib

Headers1="pCa, kfca, IbarNCX, ks, koCa, ec50SR, Vmax_SRCaP, Kmf, Kmr, M-CaSR-diastolic, M-CaSR-release, M-CaSR-Vmax, M-CaSR-tau, M-CaT-diastolic, M-CaT-systolic, M-CaT-tau, Acceptable"

Headers2="pCa, kfca, IbarNCX, ks, koCa, ec50SR, Vmax_SRCaP, Kmf, Kmr"

par_names=['pCa', 'kfca', 'IbarNCX', 'ks', 'koCa', 'ec50SR', 'Vmax_SRCaP', 'Kmf', 'Kmr']

condi_names=['M-CaSR-diastolic', 'M-CaSR-release',	 'M-CaSR-Vmax', 'M-CaSR-tau', 'M-CaT-diastolic'	, 'M-CaT-systolic', 'M-CaT-tau']

def list2csv2D(lst,headers='',lst2=None):
    strng=headers
    N=len(lst)
    j=0
    for ls in lst:
        strng+='\n'+str(ls)[1:-1]
        if lst2 is not None:
            strng+=','+str(lst2[i])[1:-1]
        
    return strng
        

def predict(A,B,Q,eps=0.0000001):
    V=np.matmul(A,B)
    if len(A.shape)==1:
        w=np.sum(V)
        Vow=V/w
    else:
        w=np.sum(V,axis=1)
        Vow=V/w[:,None]
    m=Q.shape[0]
    f=1/Q[range(m),range(m)]
    lgQ=np.log(Q+eps*(Q==0))
    F=np.matmul(Vow,lgQ*f[:,None])-(np.matmul(f,Q))
    if len(A.shape)==1:
        return np.argmax(F)
    else:
        return np.argmax(F,axis=1)

def village_kernel_predict(X_test,W,y,minA2,sumA2):
    Y=np.matmul(X_test,W)
    B=distance_sq(Y,y)
    A2=np.exp(-B+minA2)
    if len(X_test.shape)>1:
        A1=np.exp(-B+np.min(B,axis=1)[:,None])
        A=A1/np.sum(A1,axis=1)[:,None]+A2/sumA2
    else:
        A1=np.exp(-B+np.min(B))
        A=A1/np.sum(A1)+A2/sumA2
    return A

def distance_sq(x,y):
    if len(x.shape)==1:
        return-2*np.matmul(x,y.T)+np.sum(x*x)+np.sum(y*y,axis=1)

    else:

        return -2*np.matmul(x,y.T)+np.sum(x*x,axis=1)[:,None]+np.sum(y*y,axis=1)

def repeated_stuff(X,W,y,labels):
    U=np.zeros((len(labels),2))
    U[range(len(labels)),labels]=1
    Y=np.matmul(X,W)
    B=distance_sq(Y,y)
    A1=np.exp(-B+np.min(B,axis=1)[:,None])
    minA2=np.min(B,axis=0)
    A2=np.exp(-B+minA2)
    sumA2=np.sum(A2,axis=0)
    A=A1/np.sum(A1,axis=1)[:,None]+A2/sumA2
    w=np.matmul(A,np.sum(A,axis=0))#-diagn
    B=np.matmul(A.T,U)
    V=np.matmul(A,B)
    Wtot=np.matmul(w,U)
    Q=np.matmul(V.T,U)/Wtot
    return [minA2,sumA2,B,Q]


run=0
st.write("""
# APS Predictor
""")

runmapperplus=1
if runmapperplus:
    st.markdown("## Upload data")
    see_results=0
    uploaded_file='False'
    with st.expander("ℹ️ More information"):
        st.write("Upload data in CSV format with no headers.")
    #with st.sidebar:
    Sample_data = st.checkbox(
        "Manually put values", False)


    if not Sample_data:
        


        uploaded_file = st.file_uploader("Upload CSV", type=".csv")
        #st.write(uploaded_file)
        if uploaded_file:
            data = np.loadtxt(uploaded_file, delimiter=',')
            file_name=uploaded_file.name

    else:
        multi_values = st.checkbox(
        "Use Multiple Values", False)
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
            for i in range(9):
    
                colslens.append(st.columns((1, 1, 1)))
                mn=colslens[i][0].number_input(par_names[i]+': Min',min_value=-10000000000.0000001,format='%f', max_value=1000000000.9999999,step=0.00000001,value=0.1)
                mx=colslens[i][1].number_input(par_names[i]+': Max',min_value=-10000000000.0000001,format='%f', max_value=1000000000.9999999,step=0.00000001,value=0.7)
                stp=colslens[i][2].number_input(par_names[i]+': Steps',min_value=1, max_value=100,step=1,value=2)
                grids.append(np.linspace(mn, mx, stp))
                totsize=totsize*grids[0].shape[0]
                print(grids[i])
            Parcheck=np.meshgrid(grids[0],grids[1],grids[2],grids[3],grids[4],grids[5],grids[6],grids[7],grids[8])
            All_pars=[]
            for p in range(9):
                All_pars.append(list(np.reshape(Parcheck[0],totsize)))
            All_pars=np.array(All_pars).T
            print('Here:'+str(All_pars.shape))
        else:
            colslens=[]
            All_pars=[]
            for i in range(9):
    
                a=int(i/2)
                b=i-2*a
                if b==0:
                    colslens.append(st.columns((1, 1)))
                All_pars.append(colslens[a][b].number_input(par_names[i]+':',min_value=-10000000000.0000001,format='%f', max_value=1000000000.9999999,step=0.00000001,value=0.1))
            All_pars=np.array(All_pars)   

    

        #lenses=set(lens_input)
                    
    
    #with st.form("parameters"):
    if uploaded_file or Sample_data:
        with st.form(key="my_form"):

            run=st.form_submit_button(label="Predict")
            if run:
                X=np.load('Whole_filtered_APS_Data.npy')
                X_trans=(X-np.mean(X,axis=0))/np.std(X,axis=0)
                X_test=(All_pars-np.mean(X,axis=0))/np.std(X,axis=0)
                #X_test=X_trans.copy()
                labels_fin=np.ones(len(X_test))
                target=np.load('APS_target.npy')
                all_pred_labels=np.zeros((len(X_test),8))
                for cn in range(7):
                    W=np.load('all_data_W_condi'+str(cn)+'_9d.npy')
                    y=np.load('all_data_y_condi'+str(cn)+'_9d.npy')
                    [minA2,sumA2,B,Q]=repeated_stuff(X_trans,W,y,target[:,cn])
                    A=village_kernel_predict(X_test,W,y,minA2,sumA2)   
                    labels=predict(A,B,Q)
                    if (len(All_pars.shape)==1):
                        lbls=['Not Satisfied', 'Satisfied']
                        st.write("##### "+condi_names[cn]+": "+lbls[labels])
                    else:
                        all_pred_labels[:,cn]=labels
                        labels_fin=labels_fin*labels
                #labels_str=str(labels_fin)[1:-1]
                #st.write(str(sum(labels_fin)))
                #st.write(str(sum(labels_fin*(np.sum(target,axis=1)==7))))
                if (len(All_pars.shape)>1):
                    all_pred_labels[:,7]=labels_fin
                    file_str=list2csv2D(All_pars.tolist(),headers=Headers1,lst2=all_pred_labels.tolist())
                    download_button(file_str,'Predicted_Val.csv','Download Results')    

