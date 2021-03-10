from svgpathtools import svg2paths, wsvg

output_width = 200.0 #mm, ~8.5in
output_height = 250.0 #mm, ~11in
input_width = 1.0
input_height = 1.0
scale_x = 1.0
scale_y = 1.0
x_offset = 50 #mm from right edge of plotter
y_offset = 50 #mm from bottom edge
drawing_z = 0.1 #mm
lift_offset = 2 #mm
feed_drawing = 1000.0 #mm/min?
feed_z_move = 200.0 # mm/min

# Only works for continuous paths
def emit_path_code(path, scale_x = 1.0, scale_y = 1.0):
    # print("; ------Start of Path----------")
    # lift pen just to be safe
    print("G1 Z{:.2f} F{:.1f};".format(drawing_z + lift_offset, feed_z_move))
    for i in range(0, len(path)):
        line = path[i] 
        # lines in this library use complex numbers to store (x,y) as x + yj, hence the real and imag parts below
        x = line.start.real * scale_x + x_offset
        y = line.start.imag * scale_y + y_offset
        print("G1 X{:.2f} Y{:.2f} F{:.1f};".format(x, y, feed_drawing))
        if (i == 0):
            # start of path, put pen down
            print ("G1 Z{:.2f} F{:.1f};".format(drawing_z, feed_z_move))
        if i == len(path) - 1:
            x = line.end.real * scale_x + x_offset
            y = line.end.imag * scale_y + y_offset
            #for the last line we want to move to the end of it
            print("G1 X{:.2f} Y{:.2f} F{:.1f};".format(x, y, feed_drawing))
            # and then lift the pen off the paper
            print("G1 Z{:.2f} F{:.1f};".format(drawing_z + lift_offset, feed_z_move))
    #print("; --------End of Path----------")    

if __name__ == "__main__":
    paths, attributes, svgattributes = svg2paths('resources/topo_test.svg', return_svg_attributes=True)
    input_width = int(str(svgattributes["width"]).replace("px", "")) # hmmm
    input_height = int(str(svgattributes["height"]).replace("px", ""))
    #print(";Input Width: " + str(input_width))
    #print(";Input Height: " + str(input_height))
    scale_x = output_width / input_width
    scale_y = output_height / input_height
    # for i in range(0, len(paths)):
    #     emit_path_code(paths[i])
    # print(paths[i])
    # print(attributes[i]['stroke'])
    start_gcode = "G28 X0. Y0. Z0.;\nG1 Z{:.2f} F{:.1f};".format(drawing_z + lift_offset, feed_z_move)
    print(start_gcode)
    for i in range(0, len(paths)):
        emit_path_code(paths[i], scale_x, scale_y)
    
