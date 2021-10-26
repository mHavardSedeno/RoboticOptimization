import robot, COVreader, os, fileinput

x = [(-3,15), (5,-2), (18,-18), (5,17), (12,-19), (-7, 14), (-10, 9), (12, 8), (-19, -5), (4, 3)]

def modify_mbx(x):

    with open('5R.mbx', 'r') as input_file, open('5R'+str(x)+'.mbx', 'w') as output_file:
        for line in input_file:
            if 'x1=' in line:
                output_file.write('x1='+str(x[0])+';\n')
            elif 'x2=' in line:
                output_file.write('x2='+str(x[1])+';\n')
            else:
                output_file.write(line)





modify_mbx([1,2])
