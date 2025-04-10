import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Strain Rosette Calculator with Mohr's Circle")
st.markdown("""
This app calculates the in-plane strains (εₓ, εᵧ, γₓᵧ) from a 3-element strain rosette,
plots Mohr's Circle, and shows principal strains and angle of principal strain orientation.
""")

# Input fields
col1, col2, col3 = st.columns(3)
with col1:
    theta_a = st.number_input("θₐ (degrees)", value=0.0)
    eps_a = st.number_input("εₐ (×10⁻⁶)", value=0.0)
with col2:
    theta_b = st.number_input("θᵦ (degrees)", value=45.0)
    eps_b = st.number_input("εᵦ (×10⁻⁶)", value=0.0)
with col3:
    theta_c = st.number_input("θ𝑐 (degrees)", value=90.0)
    eps_c = st.number_input("ε𝑐 (×10⁻⁶)", value=0.0)

# Calculation
def calculate_strains(theta_a, theta_b, theta_c, eps_a, eps_b, eps_c):
    theta_a = np.radians(theta_a)
    theta_b = np.radians(theta_b)
    theta_c = np.radians(theta_c)

    A = [
        [np.cos(theta_a)**2, np.sin(theta_a)**2, np.sin(theta_a)*np.cos(theta_a)],
        [np.cos(theta_b)**2, np.sin(theta_b)**2, np.sin(theta_b)*np.cos(theta_b)],
        [np.cos(theta_c)**2, np.sin(theta_c)**2, np.sin(theta_c)*np.cos(theta_c)]
    ]
    B = [eps_a, eps_b, eps_c]

    return np.linalg.solve(A, B)

# Mohr's Circle Plot
def plot_mohrs_circle(eps_x, eps_y, gamma_xy):
    center = (eps_x + eps_y) / 2
    radius = np.sqrt(((eps_x - eps_y) / 2)**2 + (gamma_xy / 2)**2)

    eps1 = center + radius
    eps2 = center - radius
    theta_p_rad = 0.5 * np.arctan2(gamma_xy, eps_x - eps_y)
    theta_p_deg = np.degrees(theta_p_rad)

    # Plotting
    fig, ax = plt.subplots(figsize=(7, 7))
    circle = plt.Circle((center, 0), radius, color='lightcoral', alpha=0.5)
    ax.add_artist(circle)

    # Shear direction flipped (positive downward)
    ax.plot([eps_x, eps_y], [-gamma_xy / 2, gamma_xy / 2], 'ko--')
    ax.plot(center, 0, 'ko', label='Center')
    ax.plot(eps1, 0, 'ro', label='ε₁')
    ax.plot(eps2, 0, 'bo', label='ε₂')

    ax.set_aspect('equal')
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_xlabel('Normal Strain (×10⁻⁶)')
    ax.set_ylabel('Shear Strain / 2 (×10⁻⁶) → downward')
    ax.set_title("Mohr's Circle for Strain")
    ax.set_xlim(center - radius * 1.2, center + radius * 1.2)
    ax.set_ylim(-radius * 1.2, radius * 1.2)
    ax.invert_yaxis()  # Positive shear down
    ax.legend()
    st.pyplot(fig)

    return eps1, eps2, theta_p_deg

# Button and output
if st.button("Calculate Strains"):
    try:
        eps_x, eps_y, gamma_xy = calculate_strains(theta_a, theta_b, theta_c, eps_a, eps_b, eps_c)
        st.success("Calculated Strains:")
        st.write(f"**εₓ** = {eps_x:.2f} ×10⁻⁶")
        st.write(f"**εᵧ** = {eps_y:.2f} ×10⁻⁶")
        st.write(f"**γₓᵧ** = {gamma_xy:.2f} ×10⁻⁶")

        eps1, eps2, theta_p = plot_mohrs_circle(eps_x, eps_y, gamma_xy)

        st.success("Principal Strains:")
        st.write(f"**ε₁** = {eps1:.2f} ×10⁻⁶")
        st.write(f"**ε₂** = {eps2:.2f} ×10⁻⁶")
        st.write(f"**θₚ (angle to principal axis)** = {theta_p:.2f}°")

    except Exception as e:
        st.error(f"Error: {e}")
