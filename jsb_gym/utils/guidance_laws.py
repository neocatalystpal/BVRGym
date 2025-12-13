import numpy as np    
import pymap3d as pm
from jsb_gym.utils.geometry import angle_between

class PN:
    def __init__(self, conf):
        self.N = conf.missile_navigation.N
        self.dt = conf.missile_navigation.dt
        


    def get_target_ENU(self, missile):
        # The local coordinate origin
        lat0 = missile.get_lat_gc_deg() # deg
        lon0 = missile.get_long_gc_deg()  # deg
        h0 = missile.get_altitude()     # meters

        # The point of interest
        lat = missile.target.get_lat_gc_deg() # deg
        lon = missile.target.get_long_gc_deg()  # deg
        h = missile.target.get_altitude()     # meters

        east, north , up = pm.geodetic2enu(lat, lon, h, lat0, lon0, h0)
        
        return np.array([east, north, up])
    
    def get_target_v_ENU(self, missile):
        v_east =missile.target.get_v_east()
        v_north = missile.target.get_v_north()
        v_up = missile.target.get_v_up()

        return np.array([v_east, v_north, v_up])

    def get_v_ENU(self, missile):
        v_east = missile.get_v_east()
        v_north = missile.get_v_north()
        v_up = missile.get_v_up()

        return np.array([v_east, v_north, v_up])

    def get_heading_rel_direction(self, v1,v2):
        if np.cross(v1, v2)[2] < 0:
            return 1
        return -1


    def get_guidance(self, missile):
        taget_ENU = self.get_target_NED(missile)
        
        target_v_ENU = self.get_target_v_NED(missile)

        v_ENU = self.get_v_NED(missile)
        
        v_rel_ENU = target_v_ENU - v_ENU

        rotation_vector = (np.cross(taget_ENU, v_rel_ENU)) / (taget_ENU @ taget_ENU)
        
        acc_cmd_ENU = self.N * np.cross(v_rel_ENU , rotation_vector)

        v_ENU_PN = v_ENU + acc_cmd_ENU*self.dt
        
        # get heading
        v1 = v_ENU[:-1]
        v2 = v_ENU_PN[:-1]
        
        heading_PN = angle_between(v1, v2, in_deg= True)

        hrd = self.get_heading_rel_direction(v1, v2)
        
        heading_cmd = (missile.get_psi() +  hrd * heading_PN) %360
        
        pitch = angle_between(v1, v_ENU, in_deg= True)

        pitch_PN = angle_between(v2, v_ENU_PN, in_deg= True)
        
        pitch_diff = pitch_PN - pitch
    
        pitch_cmd = missile.get_theta() + pitch_diff

        return heading_cmd, pitch_cmd