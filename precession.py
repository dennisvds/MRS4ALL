from helper import *
import vpython as vp
import numpy as np

# Initialize scene
set_scene(axes=True, back_color=vp.color.white, zoom_out_factor=1)

# Create sphere (center point)
sphere = vp.sphere(pos=vp.vector(0, 0, 0), radius=0.5, color=vp.color.blue)

# Create arrow with the center at the sphere's center
arrow_axis = vp.vector(0, 0, 2)
arrow = vp.arrow(pos=sphere.pos - arrow_axis / 2, axis=arrow_axis, color=vp.color.red, shaftwidth=0.1)

# Enable trace at the top of the arrow (the tip)
tip_trail = vp.curve(color=vp.color.red, radius=0.02)  # This will act as the trace

# Tilt the arrow with a given angle
tilt_angle = np.radians(30)
arrow.rotate(angle=tilt_angle, axis=vp.vector(1, 0, 0), origin=sphere.pos)

# Default gyromagnetic ratio
gyromagnetic_ratio = 42.58e6  # Gyromagnetic ratio in Hz/T (for protons)

# Text output for B0 field and Larmor frequency next to the slider
B_text_output = vp.wtext(text=f"B0: {3.0:.2f} T\n")
w_text_output = vp.wtext(text=f"Larmor Frequency: {gyromagnetic_ratio * 3.0:.2e} Hz\n")

# Slider to control the B0 field
slider = vp.slider(min=0, max=7.0, value=3.0, length=300, bind=lambda s: None, text="B0 Field Strength (T)")

# Function to update gyromagnetic ratio based on the selected checkbox
def update_ratio(new_ratio, selected_checkbox):
    global gyromagnetic_ratio
    gyromagnetic_ratio = new_ratio
    # Uncheck all other checkboxes
    for checkbox in checkboxes:
        if checkbox != selected_checkbox:
            checkbox.checked = False
    update_text()  # Update the displayed values

# Function to update the displayed text values
def update_text():
    B = slider.value
    w_larmor = gyromagnetic_ratio * B
    B_text_output.text = f"B0: {B:.2f} T\n"
    w_text_output.text = f"Larmor Frequency: {w_larmor:.2e} Hz\n"

# Create checkboxes with exclusive selection behavior (only one can be selected at a time)
checkboxes = []
checkbox_proton = vp.checkbox(bind=lambda: update_ratio(42.58e6, checkbox_proton), text="Proton (42.58 MHz/T)", checked=True)
checkboxes.append(checkbox_proton)
checkbox_carbon = vp.checkbox(bind=lambda: update_ratio(10.71e6, checkbox_carbon), text="Carbon-13 (10.71 MHz/T)", checked=False)
checkboxes.append(checkbox_carbon)
checkbox_sodium = vp.checkbox(bind=lambda: update_ratio(11.26e6, checkbox_sodium), text="Sodium-23 (11.26 MHz/T)", checked=False)
checkboxes.append(checkbox_sodium)
checkbox_phosphorus = vp.checkbox(bind=lambda: update_ratio(17.23e6, checkbox_phosphorus), text="Phosphorus-31 (17.23 MHz/T)", checked=False)
checkboxes.append(checkbox_phosphorus)
checkbox_helium = vp.checkbox(bind=lambda: update_ratio(-32.43e6, checkbox_helium), text="Helium-3 (-32.43 MHz/T)", checked=False)
checkboxes.append(checkbox_helium)

# Bind the slider to the update function
slider.bind(lambda: update_text())

# Rotation around z-axis with Larmor frequency
dt = 0.01
while True:
    vp.rate(100)

    # Get the value from the slider
    B = slider.value  # Set B0 field from slider
    
    # Recalculate Larmor frequency based on the new B0 field
    w_larmor = gyromagnetic_ratio * B

    # Scale the larmor frequency to make it visible
    rotation_freq = w_larmor / 1e8

    # Rotate the arrow
    arrow.rotate(angle=rotation_freq * dt, axis=vp.vector(0, 0, 1), origin=sphere.pos)

    # Get the tip position of the arrow (top of the arrow)
    tip_pos = arrow.pos + arrow.axis

    # Update the trace to follow the tip
    tip_trail.append(pos=tip_pos)
    
    # Limit the trail length to prevent it from being too long
    if tip_trail.npoints > 50: 
        tip_trail.pop(0)

    # Update text next to the slider
    update_text()
