from gl import Raytracer, V3
from figures import *
from texture import *
from lights import *


width = 256
height = 256

# Materiales
earth = Material(texture = Texture("earthDay .bmp"))
marble = Material(texture = Texture("whiteMarble.bmp"), spec = 64, ior= 1.5, matType= REFLECTIVE)
white = Material(diffuse = (0.9,0.8,0.9), texture = Texture("whiteMarble.bmp"), spec = 32, ior = 1.5, matType= OPAQUE)
brick = Material(diffuse = (0.7, 0.3, 0.4), spec=16)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)
glass = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 1.5, matType = TRANSPARENT)



rtx = Raytracer(width, height)
rtx.envMap = Texture("parkingLot.bmp")
rtx.lights.append( AmbientLight( intensity=0.3))
rtx.lights.append( DirectionalLight(direction = (1,2,1), intensity=0.95 ))

#Cubos
# rtx.scene.append(AABB(position=(2,-2,-10), size=(2,2,2), material=brick))
# rtx.scene.append(AABB(position=(-2,-2,-10), size=(2,2,2), material=stoned))
#
# rtx.scene.append(AABB(position=(1,0,-5), size=(1,1,1), material=mirror))
# rtx.scene.append(AABB(position=(-1,0,-5), size=(1,1,1), material=glass))
# rtx.scene.append(Sphere(center=V3(0,0,5), radius=2, material=brick))
# rtx.scene.append(AABB(position=(0,0,-8), size=(2,2,2), material=glass))

rtx.scene.append( HalfSphere(V3(0,0,-10), 2, glass))


rtx.glRender()

rtx.glFinish("output.bmp")