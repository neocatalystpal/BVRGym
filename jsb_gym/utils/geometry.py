import numpy as np

def translate_semi_to_full_circle(angle):
        '''
        From
        [-pi , pi]
        to 
        [0 , 2pi] 
        '''
        #print(np.degrees(angle))
        if angle < 0.0:
            return 2*np.pi + angle
        else:
            return angle

def unit_vector(vector):
        return vector / np.linalg.norm(vector)       

def angle_between(v1, v2, in_deg = False):
        ''' Return angle between 0 to 180 deg, or 0 to pi '''
        ''' [1,0,0] and [-1,  1, 0] = 135 deg'''
        ''' [1,0,0] and [-1, -1, 0] = 135 deg'''
        v1_u = unit_vector(v1)
        v2_u = unit_vector(v2)
        angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
        if in_deg:
            return np.degrees(angle)
        return angle