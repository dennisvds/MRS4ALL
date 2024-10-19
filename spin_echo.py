import vpython as vp
import numpy as np
from helper import set_scene
import time

# Initialize the scene
set_scene(axes=True, back_color=vp.color.white, zoom_out_factor=1)

# Create a sphere representing the center of the system
center = vp.vector(0, 0, 0)

M0 = 3  # Initial magnetization along the z-axis
T2 = 0.1  # Spin-spin relaxation time (arbitrary units)

# Create an arrow representing the bulk magnetization (Mz along z-axis initially)
magnetization = vp.arrow(pos=center, axis=vp.vector(0, 0, 1)*M0, color=vp.color.red, shaftwidth=0.1)

# Create multiple spins in the xy-plane (initially hidden)
num_spins = 10
spins = [vp.arrow(pos=center, axis=vp.vector(0.5, 0, 0), color=vp.color.blue, shaftwidth=0.05) for _ in range(num_spins)]
for spin in spins:
    spin.visible = False  # Initially hide the spins

# 90-degree pulse rotates the magnetization into the x-y plane
def pulse_90():
    magnetization.rotate(angle=np.pi / 2, axis=vp.vector(0, 1, 0), origin=center)  # π/2 pulse
    for spin in spins:
        spin.visible = True  # Show spins after the 90° pulse

# Function to gradually dephase spins (spins spread out in transverse plane)
def dephase_spins():
    dt = 0.01  # Time step for dephasing
    T = 2  # Total time for dephasing
    n_steps = int(T / dt)  # Number of steps for dephasing
    max_theta = np.pi/2  # Maximum angle for dephasing
    spin_speeds = np.linspace(-max_theta/n_steps, max_theta/n_steps, num=num_spins)  # Varying speeds for each spin
    decay_rate = M0 / T2  # Rate of decay of the magnetization
    for t in np.arange(0, T, dt):
        for i, spin in enumerate(spins):
            # Simulate varying speeds for each spin
            spin_speed = spin_speeds[i]
            spin.rotate(angle=spin_speed, axis=vp.vector(0, 0, 1), origin=center)  # Rotate spins
        vp.rate(100)  # Control the speed of the animation

        # Gradually decay the magnetization vector (bulk signal decay)
        magnetization.length = M0 * np.exp(-t * decay_rate * 0.02)  # Adjust decay rate for visibility
        time.sleep(0.08)  # Slow down the dephasing

def pulse_180():
    magnetization.rotate(angle=np.pi, axis=vp.vector(0, 1, 0), origin=center)  # π pulse
    for spin in spins:
        spin.visible = True  # Show spins after the 180° pulse
    # Flip the spins by 180 degrees
    for spin in spins:
        spin.rotate(angle=np.pi, axis=vp.vector(0, 1, 0), origin=center)
    

    
# Function to rephase spins afte

# Main simulation loop
while True:
    time.sleep(1)  # Pause for 1 second between cycles
    # Step 1: Apply the 90° pulse
    pulse_90()
    vp.rate(100)  # Control the speed of the animation
    time.sleep(1)  # Wait for a second to visualize the pulse
    
    # Step 2: Dephase spins
    dephase_spins()

    # Step 3: Apply a 180° pulse to refocus the spins
    pulse_180()

    break
