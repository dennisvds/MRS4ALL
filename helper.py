import vpython as vp
import numpy as np
import matplotlib.pyplot as plt

# Unit vectors and origin
xhat = vp.vector(1, 0, 0)
yhat = vp.vector(0, 1, 0)
zhat = vp.vector(0, 0, 1)
origin = vp.vector(0, 0, 0)

def draw_axes(length=1, showlabels=True, visible = True):
    """
    Draw axes in a 3D scene.

    Parameters:
    - length (float): The length of the axes. Default is 1.
    - showlabels (bool): Whether to show labels for the axes. Default is True.

    Returns:
    axes
    """
    global scene_axis_scale
    scene_axis_scale = length
    if visible:
        clr = vp.vector(0, 102/255, 0)
        xaxis = vp.arrow(pos=origin, axis=length * xhat, color=clr, round=True)
        yaxis = vp.arrow(pos=origin, axis=length * yhat, color=clr, round=True)
        zaxis = vp.arrow(pos=origin, axis=length * zhat, color=clr, round=True)
        if showlabels and visible:
            vp.text(text="x", billboard=True, color=xaxis.color, height=0.2*length,
                pos=xaxis.pos + xaxis.axis + vp.vector(0, 0.06 * length, 0), box=False)
            vp.text(text="y", billboard=True, color=yaxis.color, height=0.2*length,
                pos=yaxis.pos + yaxis.axis + vp.vector(0.06 * length, 0, 0), box=False)
            vp.text(text="z", billboard=True, color=zaxis.color, height=0.2*length,
                pos=zaxis.pos + zaxis.axis + vp.vector(0.06 * length, 0, 0), box=False)
        return xaxis, yaxis, zaxis
    else:
        return None
    
def set_scene(axes=True, axes_length=1, zoom_out_factor = 3, scene_arrow_scale = None, back_color=vp.color.white, title=None, caption=True):

    """
    Sets up the scene for visualization.

    Parameters:
    - axes (bool): Whether to display axes in the scene. Default is True.
    - back_color (vp.color): The background color of the scene. Default is vp.color.white.
    -zoom_out_factor: size of size compared to the arrow size axis system; default: axes fill 1/3rd of scene
    -scene_arrow_scale: initially auto-scales all arrows to this size. If None, first arrow initialized by a Vector will
    draw itself with a size equal to  axes unit vector and scale this value accordingly. Can be overridden by object argument arrow_scale
    Returns:
    None
    """
    scene = vp.canvas()
    scene.width = vp.scene.height = 800
    global global_arrow_scale
    global_arrow_scale = scene_arrow_scale
    scene.background = back_color
    vp.local_light(pos=vp.vector(15, 0, 0), color=vp.color.white)
    scene.up = vp.vector(0, 0, 1)
    scene.forward = vp.vector(-1, 0, 0)  # bug fix when choosing scene.up in z-direction: without this, the camera doesn't see the scene
    scene.camera.pos = zoom_out_factor* axes_length*vp.vector(2, -2, 2)
    # center is at (0,0,0) so camera looking direction = -camera.pos:
    scene.camera.axis = -scene.camera.pos
    # Note: need to call draw_axes to determine scale of unit vector arrows, which in turn sets global scaling factor
    if axes:
        axes = draw_axes(length=axes_length, showlabels=True, visible=True)
    else:
        axes = draw_axes(length=axes_length, showlabels=False, visible=False)
    if title is not None:
        scene.title = title
    if caption:
        s = "Drag right mouse button to rotate view\n"
        s += "Drag right + left mouse button or mouse wheel to zoom in and out\n"
        s += "Drag left mouse button + Shift to translate view"
        s += "\n\n"
        scene.caption = s   # Display instructions on how to interact with the scene
    return scene

