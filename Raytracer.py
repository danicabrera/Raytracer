from gl import Raytracer, V3
from figures import *
from texture import *
from lights import *


width = 1024
height = 1024

# Materiales

brick = Material(diffuse = (0.7, 0.3, 0.4), spec=16)
stoned = Material(diffuse = (0.3, 0.4, 0.5), spec=8)
mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)
Blackmirror = Material(diffuse = (0.3, 0.3, 0.3), spec = 64, matType = REFLECTIVE)
glass = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 1.5, matType = TRANSPARENT)
sapphire = Material(diffuse = (0.2, 0.2, 0.9), spec = 64, ior = 1.778, matType = TRANSPARENT)



rtx = Raytracer(width, height)
rtx.envMap = Texture("Fondo.bmp")
rtx.lights.append( AmbientLight( intensity=0.1))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity=0.8 ))
#rtx.lights.append(PointLight(point=(-3, 5, 0)))


rtx.scene.append( Sphere(V3(-6,0,-10), 1, brick)  )
rtx.scene.append( Sphere(V3(-3,0,-10), 1, stoned)  )
rtx.scene.append( Sphere(V3(0,-5,-10), 1, mirror)  )
rtx.scene.append( Sphere(V3(0,5,-10), 1, Blackmirror)  )
rtx.scene.append( Sphere(V3(0,0,-10), 1, glass)  )
rtx.scene.append( Sphere(V3(3,0,-10), 1, glass)  )
rtx.scene.append( Sphere(V3(6,0,-10), 1, sapphire)  )


rtx.glRender()

rtx.glFinish("output.bmp")