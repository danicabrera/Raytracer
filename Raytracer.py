from gl import Raytracer, V3
from figures import *
from texture import *
from lights import *


width = 1024
height = 1024

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
rtx.lights.append( PointLight(point=(0,5,-120)))

rtx.scene.append(Plane(position=(0,-14,0), normal=(0,1,0), material=stone))
rtx.scene.append(Plane(position=(-25,-15,-25), normal=(20,1,-6), material=white))
rtx.scene.append(Plane(position=(25,-15,-25), normal=(-20,1,-6), material=white))
rtx.scene.append(Plane(position=(0,25,0), normal=(0,-1,0), material=stone))
rtx.scene.append(Plane(position=(0,5,-120), normal=(0,2,80), material=brick))
#Cubos
# rtx.scene.append(AABB(position=(2,-2,-10), size=(2,2,2), material=brick))
# rtx.scene.append(AABB(position=(-2,-2,-10), size=(2,2,2), material=stoned))
#
rtx.scene.append(AABB(position=(1,0,-5), size=(1,1,1), material=mirror))
rtx.scene.append(AABB(position=(-1,0,-5), size=(1,1,1), material=glass))
# rtx.scene.append(AABB(position=(2,2,-10), size=(2,2,2), material=marble))


rtx.glRender()

rtx.glFinish("output.bmp")