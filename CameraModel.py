import pickle

class CameraModel(object):
    def __init__(self, cam_name):
        self.name = cam_name
        # self.cam_mtx, self.dist_mtx = self.get_camera_matricies()
        self.is_oak = True if self.name == 'cam_oak' else False
        self.src = self.get_source()

    def __hash__(self):
        return hash(str(self))

    def get_camera_matricies(self):
        with open(f'./cameras/{self.name}/calibration.pkl', 'rb') as f:
            cc = pickle.load(f)
            camera_matrix = cc[0]
            distortion_matrix = cc[1]
        
        return (camera_matrix, distortion_matrix)
    
    def get_source(self):
        if self.name == 'cam_onn':
            return 0
        elif self.name == 'cam_121':
            return 'http://192.168.1.121:81/stream'
        elif self.name == 'cam_122':
            return 'http://192.168.1.122:81/stream'
        else:
            return None