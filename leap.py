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
        for hand in frame.hands:
            for finger in hand.fingers:
                for b in range(0,4):
                    bone = finger.bone(b)
                    print(bone)

        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                print "Speed:%f direction:%s\n" % (swipe.speed,swipe.position)

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

def draw():
    drawInit()
    glColor3f(1,0,0)
    for hand in hands:
        armElbow = hand.arm.wrist_position
        glPushMatrix()
        OpenGL.GL.glTranslate(1.5*armElbow.x,armElbow.y,armElbow.z)
        glutSolidSphere(70,550,550)
        glPopMatrix()
    glutSwapBuffers()

def main():

    glutInit();
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_ALPHA|GLUT_DEPTH)
    glutInitWindowSize(640,480)
    glutInitWindowPosition(0,0)
    windows = glutCreateWindow("testWindow")
    glClearColor(0.,0.,0.,1.)
    glShadeModel(GL_SMOOTH)
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutMainLoop()


   # controller.remove_listener(listener);
if __name__ == "__main__":
    main()
