import numpy as np    

class PN:
    def __init__(self):
        pass

    def load_PN_parameters(self):

        # targets flight dynamics model 
        self.tgt = None
        # position 
        self.lat_tgt = None
        self.long_tgt = None 
        self.alt_tgt = None

        self.dist_to_tgt = None
        self.dist_to_tgt_old = None
        self.altitude_to_tgt = None
        self.altitude_to_tgt_old = None

        self.sim_time_old = None
        
        self.position_tgt_NED = np.zeros(3)
        self.velocity_tgt_NED = np.zeros(3)
        self.velocity_NED = np.zeros(3)

        self.velocity_relative_NED = np.zeros(3)
        self.rotation_vector = np.zeros(3)
        self.acceleration_cmd_NED = np.zeros(3)

        self.velocity_NED_PN = np.zeros(3)

        self.velocity_NE = np.zeros(3)
        self.velocity_NE_PN = np.zeros(3)

        self.velocity_HD = np.zeros(3)
        self.velocity_HD_PN = np.zeros(3)

        self.velocity_SD = np.zeros(3)
        self.velocity_SD_PN = np.zeros(3)


    def PN(self):
        # set heading and pitch 
        self.position_tgt_NED[0] = self.tgt_east
        self.position_tgt_NED[1] = self.tgt_north
        self.position_tgt_NED[2] = self.tgt_down

        self.velocity_tgt_NED[0] = self.tgt.get_v_east()
        self.velocity_tgt_NED[1] = self.tgt.get_v_north()
        self.velocity_tgt_NED[2] = self.tgt.get_v_down()

        #self.position_tgt_NED = self.position_tgt_NED + self.velocity_tgt_NED * self.dt_PN

        self.velocity_NED[0] = self.get_v_east()
        self.velocity_NED[1] = self.get_v_north()
        self.velocity_NED[2] = self.get_v_down()
        
        self.velocity_relative_NED = self.velocity_tgt_NED - self.velocity_NED

        self.rotation_vector = (np.cross(self.position_tgt_NED,self.velocity_relative_NED)) / (self.position_tgt_NED @ self.position_tgt_NED)
        
        self.acceleration_cmd_NED = self.conf.PN['N'] * np.cross(self.velocity_relative_NED , self.rotation_vector)

        self.velocity_NED_PN = self.velocity_NED + self.acceleration_cmd_NED*self.conf.PN['dt']

        # get heading 
        self.velocity_NE[0] = self.velocity_NED[0].copy()
        self.velocity_NE[1] = self.velocity_NED[1].copy()

        self.velocity_NE_PN[0] = self.velocity_NED_PN[0].copy()
        self.velocity_NE_PN[1] = self.velocity_NED_PN[1].copy()

        heading = self.tk.angle_between(v1=self.velocity_NE, v2= self.velocity_NE_PN, in_deg= True)

        if np.cross(self.velocity_NE, self.velocity_NE_PN)[2] < 0:
            self.heading_ref = self.heading_ref + heading
        else:
            self.heading_ref = self.heading_ref - heading
        
        self.heading_ref = self.tk.truncate_heading(self.heading_ref)

        self.theta_ref = -np.clip(a=self.acceleration_cmd_NED[2], a_min = self.conf.PN['theta_min'], a_max = self.conf.PN['theta_max'])
        
        self.velocity_relative_NED_norm = np.linalg.norm(self.velocity_relative_NED)
        self.time_to_impact = self.position_tgt_NED_norm/self.velocity_relative_NED_norm
        self.altitude_ref = self.tgt.get_altitude() - self.velocity_tgt_NED[2]*self.time_to_impact
