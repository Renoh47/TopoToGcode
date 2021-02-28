from svgpathtools import svg2paths, wsvg

output_width = 200 #mm
output_height = 270 #mm
input_width = 1.0
input_height = 1.0


def emit_path_code(path, x):
    print("------Start of Path----------")
    for i in range(0, len(path)):
        line = path[i] 
        # lines in this library use complex numbers to store (x,y) as x + yj, hence the real and imag parts below
        print("X{:.2f} Y{:.2f};".format(line.start.real, line.start.imag))
        if i == len(path) - 1:
            print("x: " + "{:.2f}".format(line.end.real) + "          y: " + "{:.2f}".format(line.end.imag))
    print("--------End of Path----------")    

if __name__ == "__main__":
    paths, attributes, svgattributes = svg2paths('resources/topo_test.svg', return_svg_attributes=True)
    input_width = int(str(svgattributes["width"]).replace("px", "")) # yuck
    input_height = int(str(svgattributes["height"]).replace("px", ""))
    print("Input Width: " + str(input_width))
    print("Input Height: " + str(input_height))
    # for i in range(0, len(paths)):
    #     emit_path_code(paths[i])
    # print(paths[i])
    # print(attributes[i]['stroke'])
    emit_path_code(paths[0])
