# ifc_viewer_3d.py
from PyQt5.QtWidgets import QOpenGLWidget    # provides QGLWidget, a special OpenGL QWidget
import OpenGL.GL as gl
import numpy as np
from PyQt5.QtGui import (QOpenGLBuffer, QOpenGLShaderProgram,
    QOpenGLShader)
"""
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QColor, QOpenGLVersionProfile
from PyQt5.QtCore import QTimer
from PyQt5 import QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np"""


class IFCViewer3D(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triangle, PyQt5, OpenGL ES 2.0")
        self.resize(300, 300)
    def initializeGL(self):
        gl.glClearColor(0.5, 0.8, 0.7, 1.0)
        vertShaderSrc = """
            attribute vec3 aPosition;
            void main()
            {
                gl_Position = vec4(aPosition, 1.0);
            }
        """
        fragShaderSrc = """
            void main()
            {
                gl_FragColor = vec4(0.5, 0.2, 0.9, 1.0);
            }
        """
        program = QOpenGLShaderProgram()
        program.addShaderFromSourceCode(QOpenGLShader.Vertex, vertShaderSrc)
        program.addShaderFromSourceCode(QOpenGLShader.Fragment, fragShaderSrc)
        program.link()
        program.bind()
        vertPositions = np.array([
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0], dtype=np.float32)
        vertPosBuffer = QOpenGLBuffer()
        vertPosBuffer.create()
        vertPosBuffer.bind()
        vertPosBuffer.allocate(vertPositions, len(vertPositions) * 4)
        program.bindAttributeLocation("aPosition", 0)
        program.setAttributeBuffer(0, gl.GL_FLOAT, 0, 3)
        program.enableAttributeArray(0)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)