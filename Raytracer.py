from gl import Raytracer, V3
from figures import *
from lights import *


width = 512
height = 512

# Materiales

brick = Material(diffuse = (0.8, 0.3, 0.3), spec=64)
stone = Material(diffuse = (0.4, 0.4, 0.4), spec=32)
grass = Material(diffuse = (0.3, 1, 0.3), spec=16)


rtx = Raytracer(width, height)

rtx.lights.append( AmbientLight( intensity=0.2))
rtx.lights.append( DirectionalLight(direction = (0,0,-1), intensity=0.5 ))
#rtx.lights.append(PointLight(point=(-3, 5, 0)))


rtx.scene.append( Sphere(V3(-3,0,-10), 1.5, brick)  )
rtx.scene.append( Sphere(V3(0,0,-10), 1.5, stone)  )
rtx.scene.append( Sphere(V3(3,0,-10), 1.5, grass)  )


rtx.glRender()

rtx.glFinish("output.bmp")