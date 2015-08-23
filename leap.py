import os, sys,inspect, thread, time
sys.path += ["/usr/lib/Leap", "../lib/x64", "../lib"]
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Leap import *;

class LeapListener(Leap.Listener):

    def on_init(self,controller):
        print("inited");

    def on_connect(self,controller):
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_exit(self,controller):
        print("exited");

    def on_disconnect(self,controller):
        print("disconnect");

    def on_frame(self, controller):
        print("on frame")
        frame = controller.frame();
        global hands 
        hands = frame.hands
        
listener = LeapListener();

controller = Leap.Controller();

controller.add_listener(listener)

def drawInit():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glViewport(0,0,640,480)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-550,550,-550,550,-300,300)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def arm_pos_gen(hand):
    yield hand.arm.wrist_position
    yield hand.arm.elbow_position

def drawSphere(radius,pos):
    glPushMatrix()
    OpenGL.GL.glTranslate(pos.x,pos.y,pos.z)
    color = [1.,0.,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    glutSolidSphere(radius,550,550)
    glPopMatrix()

def draw():
    drawInit()
    glColor3f(1,0,0)
    for hand in hands:
        for pos in arm_pos_gen(hand):
            drawSphere(20,pos)
        for finger in hand.fingers:
            for b in range(0,4):
                pos = finger.bone(b).center
                drawSphere(10,pos)
    glutSwapBuffers()

def main1():
    glutInit();
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_ALPHA|GLUT_DEPTH)
    glutInitWindowSize(640,480)
    glutInitWindowPosition(0,0)
    windows = glutCreateWindow("testWindow")
    glClearColor(0.,0.,0.,1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING);
    glEnable(GL_LIGHT0);

    ambientLight = [ 0.2, 0.2, 0.2, 1.0 ];
    diffuseLight =  [ 0.8, 0., 0., 1.0 ] 
    specularLight = [  1.0, 0, 0, 1.0 ]
    position =[   -0, 1.0,400.0, 1.0 ]

    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight);
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLight);
    glLightfv(GL_LIGHT0, GL_POSITION, position);
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()

if __name__ == "__main__":
    main()
    controller.remove_listener(listener);
