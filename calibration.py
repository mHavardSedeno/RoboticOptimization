#######################################################
# TwoBars robot demo
import math
import numpy

# >>> from importlib import reload
# >>> import demo,robot

##################################################
# Definition of a RR robot with approximate architecture
import robot

# >>> nominal_architecture = [0,0,3,2]
# >>> 5r = robot.TwoBars(nominal_architecture,seed=1,man_var=0,mes_var=0,eps_cmd=2)
# >>> 5r = robot.TwoBars(nominal_architecture,seed=1,man_var=0.2,mes_var=0.02)

##################################################
# CALIBRATION

# RR kinematic functions
def f_5R(architecture,pose,command):
    [a1,a2,l11, l12, l21, l22] = architecture
    [x1,x2] = pose
    [q1,q2] = numpy.radians(command)
    f1 = x1 - pow((a1[0]+l11*numpy.cos(q1)),2) + x2 - pow((a1[1]+l11*numpy.sin(q1)), 2) - l12
    f2 = x1 - pow((a2[0]+l11*numpy.cos(q1)),2) + x2 - pow((a2[1]+l22*numpy.sin(q2)), 2) - l21
    return [f1,f2]

# Actuation of the robot in order to generate measures for calibration
def make_measurements(5r,commands,col='black',mar='*'):
    5r.actuate(commands[0])
    if col!='black':
        5r.pen_down(col)
    measures=[]
    print('   Taking measures ...')
    for q in commands:
        5r.actuate(q)
        x = 5r.measure_pose()
        5r.ax.plot([x[0]],[x[1]],color=col,marker=mar)
        measures.append((x,q))
    if col!='black':
        5r.pen_up()
    5r.go_home()
    return measures

# >>> commands = [[q,q] for q in range(0,100,10)]
# >>> measures = demo.make_measurements(5r,commands,col='red')

# >>> commands = [[q1,q2] for q1 in range(0,181,45) for q2 in range(0,181,30)]
# >>> measures = demo.make_measurements(5r,commands,col='blue',mar='o')

# calibration from measurements
from scipy.optimize import least_squares

def calibrate(kinematic_functions,nominal_architecture,measures):
    # error function ----
    def errors(a):
        err=[]
        for (x,q) in measures:
            for fi in kinematic_functions(a,x,q):
                err.append(fi)
        return err
    # -------------------
    print('   Calibration processing ...')
    sol = least_squares(errors,nominal_architecture)
    print('   status : ',sol.message)
    print('   error : ',sol.cost)
    print('   result : ',sol.x)
    return sol.x

# >>> calibrated_architecture = demo.calibrate(demo.f_RR,nominal_architecture,measures)
# >>> 5r.get_architecture()
