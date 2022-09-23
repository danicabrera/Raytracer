import numpy as np

DIR_LIGHT = 0
POINT_LIGHT = 1
AMBIENT_LIGHT = 2

class DirectionalLight(object):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = direction / np.linalg.norm(direction)
        self.intensity = intensity
        self.color = color
        self.lightType = DIR_LIGHT

    def getColor(self, intersect, raytracer):
        light_dir = np.array(self.direction) * -1
        intensity = np.dot(intersect.normal, light_dir) * self.intensity
        intensity = float(max(0, intensity))

        diffuseColor = np.array([intensity * self.color[0],
                                 intensity * self.color[1],
                                 intensity * self.color[2]])

        # Iluminacion especular
        # R = 2 * (N . L) * N - L
        reflect = 2 * np.dot(intersect.normal, light_dir)
        reflect = np.multiply(reflect, intersect.normal)
        reflect = np.subtract(reflect, light_dir)
        reflect = reflect / np.linalg.norm(reflect)

        view_dir = np.subtract(raytracer.camPosition, intersect.point)
        view_dir = view_dir / np.linalg.norm(view_dir)

        spec_intensity = self.intensity * max(0, np.dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = np.array([spec_intensity * self.color[0],
                              spec_intensity * self.color[1],
                              spec_intensity * self.color[2]])
        # Shadows
        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return (diffuseColor + specColor) * (1 - shadow_intensity)

class AmbientLight(object):
    def __init__(self, intensity = 0.1, color = (1,1,1)):
        self.intensity = intensity
        self.color = color
        self.lightType = AMBIENT_LIGHT

    def getColor(self, intersect, raytracer):
        return np.array(self.color) * self.intensity

class PointLight(object):
    def __init__(self, point, constant = 1.0, linear = 0.1, quad = 0.05, color = (1,1,1)):
        self.point = point
        self.constant = constant
        self.linear = linear
        self.quad = quad
        self.color = color
        self.lightType = POINT_LIGHT

    def getColor(self, intersect, raytracer):
        diffuseColor = np.array([0,0,0])

        light_dir = np.subtract(self.point, intersect.point)
        light_dir = light_dir / np.linalg.norm(light_dir)

        # att = 1 / (Kc + Kl * d + Kq * d * d)
        #lightDistance = np.linalg.norm(np.subtract(self.point, intersect.point))
        #attenuation = 1.0 / (self.constant + self.linear * lightDistance + self.quad * lightDistance ** 2)
        attenuation = 1.0
        intensity = np.dot(intersect.normal, light_dir) * attenuation
        intensity = float(max(0, intensity))

        diffuseColor = np.array([intensity * self.color[0],
                                 intensity * self.color[1],
                                 intensity * self.color[2]])


        # Iluminacion especular
        # R = 2 * (N . L) * N - L
        reflect = 2 * np.dot(intersect.normal, light_dir)
        reflect = np.multiply(reflect, intersect.normal)
        reflect = np.subtract(reflect, light_dir)
        reflect = reflect / np.linalg.norm(reflect)

        view_dir = np.subtract( raytracer.camPosition, intersect.point)
        view_dir = view_dir / np.linalg.norm(view_dir)

        spec_intensity = attenuation * max(0,np.dot(view_dir, reflect)) ** intersect.sceneObj.material.spec
        specColor = np.array([spec_intensity * self.color[0],
                              spec_intensity * self.color[1],
                              spec_intensity * self.color[2]])

        #Shadows
        shadow_intensity = 0
        shadow_intersect = raytracer.scene_intersect(intersect.point, light_dir, intersect.sceneObj)
        if shadow_intersect:
            shadow_intensity = 1

        return (diffuseColor + specColor) * (1 - shadow_intensity)
