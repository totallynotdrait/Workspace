import dearpygui.dearpygui as dpg

dpg.create_context()

def print_on_close():
    print("window closed")

def create_window():
    with dpg.window(label="another window", height=150, width=200, on_close=print_on_close):
        dpg.add_text("hello from the other window")

with dpg.window(label="Header Window", height=300, width=300):
    dpg.add_button(label="Click me!!", callback=create_window)


dpg.create_viewport(title='Custom Title', width=1593, height=562)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()