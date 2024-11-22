import streamlit as st

def Gen_Eff(V, CL, IL, K, Rsh, Ra):
    # Check for valid resistances and current values
    if Rsh <= 0 or Ra <= 0:
        return None, "Resistance values must be greater than zero."
    
    if IL <= 0:
        return None, "Full load current (IL) must be greater than zero."

    # Calculate Shunt field current (Ish)
    Ish = V / Rsh
    
    # Calculate Armature current (Ia)
    Ia = K * IL - Ish

    # Calculate Core losses (CUL)
    CUL = Ish*2 * Rsh + Ia*2 * Ra
    
    # Calculate Efficiency (Eff)
    if K * V * IL == 0:  # Prevent division by zero in the efficiency calculation
        return None, "Invalid motor parameters, calculation results in zero denominator."
    
    Eff = ((K * V * IL - CL - CUL) / (K * V * IL)) * 100
    
    return Eff, CUL

# Set up the page title and description
st.title("DC Shunt Motor Efficiency Calculator")
st.write("""
    This web app calculates the efficiency and core losses of a DC shunt motor at various loads.
    Enter the parameters below to compute the results.
""")

# Create input fields for the parameters
V = st.number_input("Voltage (V)", min_value=0.0, step=0.1)
CL = st.number_input("Core Losses (CL) in Watts", min_value=0.0, step=0.1)
IL = st.number_input("Full Load Current (IL) in Amps", min_value=0.0, step=0.1)
K = st.number_input("Loading on Generator (K)", min_value=0.0, step=0.1)
Rsh = st.number_input("Shunt Field Resistance (Rsh) in Ohms", min_value=0.0, step=0.1)
Ra = st.number_input("Armature Resistance (Ra) in Ohms", min_value=0.0, step=0.1)

# Button to trigger the calculation
if st.button("Calculate Efficiency"):
    # Calculate the efficiency and core losses
    Eff, CUL_or_error = Gen_Eff(V, CL, IL, K, Rsh, Ra)
    
    if Eff is None:
        # Display the error message if there's an issue with the input values
        st.error(CUL_or_error)
    else:
        # Display the results if the calculation is successful
        st.write(f"Efficiency: {Eff:.2f}%")
        st.write(f"Core Losses (CUL): {CUL_or_error:.2f} W")