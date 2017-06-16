import mdl
import os
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = new_matrix()
    ident(tmp)
    step = 0.1

    basename = "anim"
    frames = 1
    vdict = []

    for i in range(len(commands)):
        a = commands[i]
        cmd = a[0]
        args = []
        if len(a) > 1:
            args = a[1:]

        if cmd == "basename":
            basename = args[0]

        elif cmd == "frames":
            frames = args[0]

        elif cmd == "vary":
            vdict.append(args)

    #generate frametable                                                                                                                                                                                                                      
    ftable = []

    for j in range(frames):
        fdict = {}
        for vals in vdict:
            knobname = vals[0]
            vals = vals[1:]
            if vals[0] <= j and vals[1] >= j:
                percentcomplete = float(j - vals[0]) / float(vals[1] - vals[0])
                interpolate = vals[2] + float(vals[3] - vals[2]) * percentcomplete
                fdict[knobname] = interpolate
        ftable.append(fdict)
    #print "FTABLE: " + str(ftable)
    #main drawing loop         

    for frame in range(frames):
        
        fd = ftable[frame]
        #print "FD " + str(frame)
        print fd
        tmp = new_matrix()
        ident(tmp)
        stack = [] 
        stack.append([ x[:] for x in tmp ])
 #       print "STACK BEFORE FOR:"
 #       print stack

        for command in commands:
            #print command
            c = command[0]
            args = command[1:]

            if c == 'box':
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, color)
                tmp = []
            elif c == 'sphere':
 #               print "SPHEREARGS:"
 #               print args
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step)
#                print "TOP OF STACK:"
#                print stack[-1]
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, color)
#                print "TMP:"
#                print tmp
                #print screen
                tmp = []
            elif c == 'torus':
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, color)
                tmp = []
            elif c == 'move':
                x = 1
                if args[-1] in fd.keys():
                    x = fd[args[-1]]
#                    print "MOVEKNOB:"
#                    print x
                tmp = make_translate(args[0]*x, args[1]*x, args[2]*x)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []

            elif c == 'scale':
                x = 1
                if args[-1] in fd.keys():
                    x = fd[args[-1]]
#                    print "SCALEKNOB:"
#                    print x
                tmp = make_scale(args[0]*x, args[1]*x, args[2]*x)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                x = 1
                if args[-1] in fd.keys():
                    x = fd[args[-1]]
                    #print "X " + str(x)
#                    print "ROTATEKNOB:"
#                    print x
                theta = args[1]*x * (math.pi/180)
                if args[0] == 'x':
                   tmp = make_rotX(theta)
                elif args[0] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
#                print "PUSHSTACK:"
#                print stack[-1]
                stack.append([l[:] for l in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
        save_extension(screen, "anim/%s%03d.png" % (basename,frame))
        clear_screen(screen) 
#        print "SCREEN"
#        print screen
    os.system('convert anim/%s*.png %s.gif' % (basename,basename))
