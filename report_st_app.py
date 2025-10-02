import streamlit as st
import numpy as np
from supervised import AutoML
import pandas as pd
from pathlib import Path
from rdkit import Chem
from mordred import Calculator, descriptors

## Helper Functions
def load_automl():
    return AutoML(results_path="./automl_results")

def automl_predict(X):
    return automl.predict(X)

def smiles_to_mol(smi):
    mol = Chem.MolFromSmiles(smi)
    return Chem.AddHs(mol) if mol is not None else None

def calculate_descriptors(smiles):
    desc_names = pd.read_csv("./utils/list_2d_mordred_descriptors.csv", sep=',')
    col_headers = desc_names["descriptors"].values.tolist()
    mols = []
    calc = Calculator(descriptors, ignore_3D=True)
    for smile in smiles:
        mols.append(smiles_to_mol(smile))
    desc_df = calc.pandas(mols)
    desc_df.columns = col_headers
    return desc_df

def calculate_resolution(rts, peak_width):
    rts = np.array(rts)
    return 1.18 * ((rts[:,None] - rts)/ (2 * peak_width))

def load_method_params(method_name):
    return pd.read_csv(f"./methods/{method_name}.csv", sep=",")

def preprocess(desc_df):
    return desc_df

def check_features():
    return None

## Generic lists
method_list = [
    "BEH_acidic_4min",
    "BEH_acidic_6min",
    "BEH_neutral_4min",
    "BEH_neutral_6min",
    "Biphenyl_acidic_4min",
    "Biphenyl_acidic_6min",
    "Biphenyl_neutral_4min",
    "Biphenyl_neutral_6min",
    "HSS_acidic_4min",
    "HSS_acidic_6min",
    "HSS_neutral_4min",
    "HSS_neutral_6min",
    "Other"
]

eluent_list = [
    "water",
    "methanol",
    "acetonitrile"
]

additive_list = [
    "formic acid",
    "trifluoroacetic acid",
    "ammonium acetate",
    "ammonium formate"
]

column_list = [
    "BEH"
]

## Streamlit App

st.title("LC RT Prediction")

# Enter structures as SMILES
input_text = st.text_area("Please enter SMILES strings with each one on a new line:", "", key="smiles_text_area")

tool_type = st.radio("Select the type of prediction to perform", ["Predict LC RT", "Predict Best LC Method", "Optimise LC Method"])

if tool_type == "Predict LC RT":
    
    # Input method or choose from dropdown
    method_input = st.selectbox("Choose the LC method from the list below", method_list, key="method_input_selectbox")

    other_method_flag = False
    
    if method_input == "Other":

        st.error("Not yet implemented!")

        st.write("Column and Flow Parameters")
        column = st.selectbox()
        column_length = st.number_input()
        column_diameter = st.number_input()
        column_particle_size = st.number_input()
        column_temp = st.number_input()
        flowrate = st.number_input()

        st.write("Mobile Phase A")
        num_components = st.number_input("Number of components", min_value=1, value=2, key="mpa_num_comps")

        for x in range(num_components):
            col1, col2 = st.columns([1,1])
            with col1:
                component_name = st.selectbox(f"Component {x+1}", eluent_list, index=0, key=f"mpa_comp_{x}")
            with col2:
                component_amount = st.number_input(f"Quantity of {x+1} in % or mM as appropriate", key=f"mpa_comp_amount_{x}")

        st.write("Mobile Phase B")
        num_components = st.number_input("Number of components", min_value=1, value=2, key="mpb_num_comps")

        for x in range(num_components):
            col1, col2 = st.columns([1,1])
            with col1:
                component_name = st.selectbox(f"Component {x+1}", eluent_list, index=2, key=f"mpb_comp_{x}")
            with col2:
                component_amount = st.number_input(f"Quantity of {x+1} in % or mM as appropriate", key=f"mpb_comp_amount_{x}")

        # add gradient input tool (editable table?)

        method_params = None
        other_method_flag = True

    # Predict RTs
    if st.button("Predict LC RT(s)"):
        
        automl = load_automl()
        
        smiles = input_text.splitlines()
        
        molecular_descriptors = calculate_descriptors(smiles)

        if not other_method_flag:
            method_params = load_method_params(method_input)

        run_time = method_params["run time"]
        
        method_params = pd.concat([method_params] * len(smiles), axis=0, ignore_index=True)
        features_df = pd.concat((molecular_descriptors,method_params), axis=1)

        predict_df = pd.DataFrame(automl_predict(features_df) * run_time)
        predict_df.columns = smiles
        st.table(predict_df)

elif tool_type == "Predict Best LC Method":
    if st.button("Predict Best Method"):
        automl = load_automl()
        
        smiles = input_text.splitlines()
        
        molecular_descriptors = calculate_descriptors(smiles)

        results = {}

        for method in method_list:
            if method != "Other":
                method_params = load_method_params(method)
                method_params = pd.concat([method_params] * len(smiles), axis=0, ignore_index=True)
                features_df = pd.concat((molecular_descriptors,method_params), axis=1)
                results[method] = automl_predict(features_df)
        
        for method in results:
            resolutions = calculate_resolution(results[method], peak_width=0.015)
            resolutions = pd.DataFrame(resolutions, columns=smiles, index=smiles)
            st.write(f"Results for {method}")
            st.table(resolutions)

elif tool_type == "Optimise LC Method":
    st.error("Not yet implemented!")

    # checkboxes for parameters to optimise
    # column, temp, flowrate, method length, gradient, MPs

    columns = st.multiselect("Column Type", column_list)
    column_lengths = st.multiselect("Column Lengths (mm)", [50,100,150])
    column_ids = st.multiselect("Column IDs (mm)", [1,2.1,4.6])
    column_temps = st.multiselect("Column Temperatures (°C)", [30,35,40,45,50])
    flowrates = st.multiselect("Flow rates (mL/min)", np.arange(0.2,1.6,0.1))


    






