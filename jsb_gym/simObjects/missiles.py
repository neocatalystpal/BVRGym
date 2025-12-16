import numpy as np
from jsb_gym.simObjects.FDMObject import FDMObject
from jsb_gym.utils.guidance_laws import PN
import time
from jsb_gym.utils.autopilot import MissilePIDAutopilot

class AAMBVR(FDMObject):
    def __init__(self, conf):
        super().__init__(conf)
        self.conf = conf
        self.missile_control = MissilePIDAutopilot(self)
        self.PN = PN(conf)
        self.missile_simulation_config = self.conf.missile_simulation

    def reset(self, lat, long, alt, vel, heading):
        super().reset(lat, long, alt, vel, heading)
        self.target = None
        self.target_lost = False
        self.target_hit = False
        self.active = False
        self.alive = True
        
        self.lost_count = 0
        self.target_NED_norm_min = None
        self.target_NED_norm_old = None

    def is_alive(self):
        return self.alive

    def is_ready_to_launch(self):
        return not self.active and self.alive and not self.target_lost and not self.target_hit

    def is_tracking_target(self):
        return self.active and self.alive and not self.target_lost and not self.target_hit

    def is_target_hit(self):
        return not self.active and not self.alive and not self.target_lost and self.target_hit

    def is_traget_lost(self):
        return not self.active and not self.alive and self.target_lost and not self.target_hit


    def set_target(self, target):
        ''' 
        Set target aircraft object 
        Input: simObject
        '''
        self.target = target

    def launch(self):
        pass


    def is_mach_low(self):
        return self.get_Mach() < self.conf.PN['target_lost_below_mach'] and self.acceleration_stage_done()

    def is_alt_low(self):
        return self.get_altitude() < self.conf.PN['target_lost_below_alt']

    def is_target_lost(self):
        # check if missile missed         
        if (self.position_tgt_NED_norm_old != None) \
            and (self.position_tgt_NED_norm_old < self.position_tgt_NED_norm) \
            and (self.position_tgt_NED_norm < 3e3):
            self.count_lost += 1
            if self.count_lost > self.conf.PN['count_lost']:
                #self.target_lost = True
                return True
            else:
                return False
        else:
            self.count_lost = 0
            return False

    def step(self):        
        for _ in range(self.missile_simulation_config.Sim_time_step):
            
            self._step()


    def _step(self):

        heading_cmd, altitude_cmd = self.PN.get_guidance(self)
        
        for _ in range(self.missile_simulation_config.Control_time_step):
            
            aileron_cmd, elevator_cmd, rudder_cmd, throttle_cmd	= self.missile_control.get_control_input(heading_cmd, altitude_cmd)
            self.command_missile(aileron_cmd, elevator_cmd, rudder_cmd, throttle_cmd)  
            self.fdm.run()
            if self.conf.fg_sleep_time is not None:
                time.sleep(self.conf.fg_sleep_time)



    def command_missile(self, aileron_cmd, elevator_cmd, rudder_cmd, throttle_cmd):

        self.set_aileron(aileron_cmd)
        self.set_elevator(elevator_cmd)
        self.set_rudder(rudder_cmd)
        # todo velocity control. for now set 0.49 throttle at the imput 
        self.set_throttle(throttle_cmd)



    def is_within_warhead_range(self):
        return self.position_tgt_NED_norm <= self.conf.PN['warhead']



