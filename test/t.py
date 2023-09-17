import dearpygui.dearpygui as dpg
import math
import pywavefront

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

# load the mesh data from an OBJ file
mesh = pywavefront.Wavefront('tea/model.obj')

# get the vertex data from the mesh
verticies = []
for name, material in mesh.materials.items():
    verticies.extend(material.vertices)

colors = [
    [255,   0,   0, 150],
    [255, 255,   0, 150],
    [255, 255, 255, 150],
    [255,   0, 255, 150],
    [  0, 255,   0, 150],
    [  0, 255, 255, 150],
    [  0,   0, 255, 150],
    [  0, 125,   0, 150],
    [128,   0,   0, 150],
    [128,  70,   0, 150],
    [128, 255, 255, 150],
    [128,   0, 128, 150]
]

with dpg.window(label="tutorial", width=550,height=550):

    with dpg.drawlist(width=500,height=500):

        with dpg.draw_layer(tag="main pass", depth_clipping=True,
                            perspective_divide=True,
                            cull_mode=dpg.mvCullMode_Back):

            with dpg.draw_node(tag="mesh"):

                # draw triangles using the vertex data of your mesh
                for i in range(0,len(verticies),9):
                    v1 = verticies[i:i+3]
                    v2 = verticies[i+3:i+6]
                    v3 = verticies[i+6:i+9]
                    dpg.draw_triangle(v1,v2,v3,color=[0.0],fill=colors[i//9%len(colors)])

x_rot = 0
y_rot = 0
z_rot = 0

view = dpg.create_fps_matrix([0, 0, 50], 0.0, 0.0)
proj = dpg.create_perspective_matrix(math.pi*45.0/180.0, 1.0, 0.1, 100)
model = dpg.create_rotation_matrix(math.pi*x_rot/180.0 , [1, 0, 0])*\
                        dpg.create_rotation_matrix(math.pi*y_rot/180.0 , [0, 1, 0])*\
                        dpg.create_rotation_matrix(math.pi*z_rot/180.0 , [0, 0, 1])

dpg.set_clip_space("main pass", 0,0,500,500, -1.0, 1.0)
dpg.apply_transform("mesh", proj*view*model)

dpg.show_viewport()
while dpg.is_dearpygui_running():
    y_rot +=.1
    x_rot +=.1
    z_rot +=.1
    dpg.render_dearpygui_frame()

dpg.destroy_context()
