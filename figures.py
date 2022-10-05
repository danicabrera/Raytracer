import numpy as np

WHITE = (1,1,1)
BLACK = (0,0,0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
class Intersect(object):
    def __init__(self, distance, point, normal, texcoords, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.sceneObj = sceneObj

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0,  texture =None,matType = 0):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.matType = matType


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = np.subtract(self.center, orig)
        tca = np.dot(L, dir)
        d = (np.linalg.norm(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        # P = O + t0 * D
        P = np.add(orig, t0 * np.array(dir))
        normal = np.subtract(P, self.center)
        normal = normal / np.linalg.norm(normal)

        u = 1 - ((np.arctan2(normal[2], normal[0]) / (2 * np.pi)) + 0.5)
        v = np.arccos(-normal[1]) / np.pi

        uvs = (u, v)

        return Intersect(distance=t0,
                         point=P,
                         normal=normal,
                         texcoords=uvs,
                         sceneObj=self)

class Plane(object):
    def __init__(self, position, normal, material):
        self.material = material
        self.position = position
        self.normal = normal / np.linalg.norm(normal)

    def ray_intersect(self, orig, dir):

        denominador = np.dot(dir, self.normal)

        if abs(denominador) > 0.0001:
            numerador = np.dot(np.subtract(self.position,orig), self.normal)
            t = numerador/denominador

            if t >0:
                # P = O + t * D
                P = np.add(orig, t * np.array(dir))
                # normal = np.add(P, t)
                # normal = normal / np.linalg.norm(normal)

                return Intersect(distance=t,
                                 point=P,
                                 normal=self.normal,
                                 texcoords=None,
                                 sceneObj=self)

class AABB(object):
    #Axis Align Bounding Box
    #OBB
    #Oriented Bounding Box
    def __init__(self, position,  size, material):
        self.size = size
        self.position = position
        self.material = material

        self.planes = []
        halfSizes = [0,0,0]
        halfSizes[0] = size[0] /2
        halfSizes[1] = size[1] / 2
        halfSizes[2] = size[2] / 2



        self.planes.append(Plane( np.add(position, (halfSizes[0], 0, 0)), (1,0,0), material))
        self.planes.append(Plane( np.add(position, (-halfSizes[0], 0, 0)), (-1, 0, 0), material))

        self.planes.append(Plane( np.add(position, (0, halfSizes[1] , 0)), (0, 1, 0), material))
        self.planes.append(Plane( np.add(position, (0, -halfSizes[1] , 0)), (0, -1, 0), material))

        self.planes.append(Plane( np.add(position, (0, 0, halfSizes[2])), (0, 0, 1), material))
        self.planes.append(Plane( np.add(position, (0, 0, -halfSizes[2])), (0, 0, -1), material))

        #Bounds
        self.BoundsMin = [0,0,0]
        self.BoundsMax = [0,0,0]

        epsilon = 0.001
        for i in range(3):
            self.BoundsMin[i] = self.position[i] - (epsilon + halfSizes[i])
            self.BoundsMax[i] = self.position[i] + (epsilon + halfSizes[i])


    def ray_intersect(self, orig, dir):

        intersect = None
        t = float('inf')
        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)
            if planeInter is not None:
                planePoint = planeInter.point

                if self.BoundsMin[0] <= planePoint[0] <= self.BoundsMax[0]:
                    if self.BoundsMin[1] <= planePoint[1] <= self.BoundsMax[1]:
                        if self.BoundsMin[2] <= planePoint[2] <= self.BoundsMax[2]:

                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                # Tex Coord
                                u, v = 0,0

                                if abs(plane.normal[0]) > 0:
                                    #mapeo uvs
                                    u = (planeInter.point[1] - self.BoundsMin[1]) / self.size[1]
                                    v = (planeInter.point[2] - self.BoundsMin[2]) / self.size[2]
                                elif abs(plane.normal[1]):
                                    u = (planeInter.point[0] - self.BoundsMin[0]) / self.size[0]
                                    v = (planeInter.point[2] - self.BoundsMin[2]) / self.size[2]
                                elif abs(plane.normal[2]):
                                    u = (planeInter.point[0] - self.BoundsMin[0]) / self.size[1]
                                    v = (planeInter.point[1] - self.BoundsMin[1]) / self.size[1]



        if intersect is None:
            return None

        return Intersect(distance=t,
                         point=intersect.point,
                         normal=intersect.normal,
                         texcoords=(u,v),
                         sceneObj=self)

class Disk(object):
    def __init__(self, position, radius, normal, material):
        self.position = position
        self.radius = radius
        self.normal  = normal
        self.material = material
        self.plane = Plane(position,normal, material)

    def ray_intersect(self, orig, dir):
        intersect = self.plane.ray_intersect(orig, dir)
        if intersect is None:
            return None
        contactDistance = np.subtract(intersect.point, self.plane.position)
        contactDistance = np.linalg.norm(contactDistance)
        if contactDistance > self.radius:
            return None

        return Intersect(distance=intersect.distance,
                         point=intersect.point,
                         normal=self.plane.normal,
                         texcoords=None,
                         sceneObj=self)

class Triangle(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal  = normal
        self.material = material
        self.plane = Plane(position,normal, material)

    def ray_intersect(self, orig, dir):
        intersect = self.plane.ray_intersect(orig, dir)
        if intersect is None:
            return None
        contactDistance = np.subtract(intersect.point, self.plane.position)
        contactDistance = np.linalg.norm(contactDistance)
        if contactDistance > self.radius:
            return None

        return Intersect(distance=intersect.distance,
                         point=intersect.point,
                         normal=self.plane.normal,
                         texcoords=None,
                         sceneObj=self)

class HalfSphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material


    def ray_intersect(self, orig, dir):
        L = np.subtract(self.center, orig)
        tca = np.dot(L, dir)
        d = (np.linalg.norm(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None



        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc


        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        # P = O + t0 * D
        P = np.add(orig, t0 * np.array(dir))


        normal = np.subtract(P, self.center)
        normal = normal / np.linalg.norm(normal)

        u = 1 - ((np.arctan2(normal[2], normal[0]) / (2 * np.pi)) + 0.5)
        v = np.arccos(-normal[1]) / np.pi

        uvs = (u, v)

        return Intersect(distance=t0,
                         point=P,
                         normal=normal,
                         texcoords=uvs,
                         sceneObj=self)


class Capsule(object):
    def __init__(self, position, size, material):
        self.size = size
        self.position = position
        self.material = material
        self.radius = size[0]

        AABB(position, size, material)

    def ray_intersect(self):
        pass