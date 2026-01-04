from jsb_gym.simObjects.aircraft import F16BVR
from jsb_gym.simObjects.missiles import AAMBVR
import numpy as np

class BaseBVRAgent():
    def __init__(self, conf, env):
        self.conf = conf
        # agent level configurations
        self.agent_parameters = conf.agent_parameters
        self.aircraft_simObj_conf =  conf.aircraft_simObj_conf
        self.missile_simObj_conf  =  conf.missile_simObj_conf
        
        # flight dynamics model level configurations
        self.simObj = F16BVR(self.aircraft_simObj_conf)
        self.reset_agent()
        self.reset_ammo()

        # environment reference to access other agents etc.
        self.env = env

        self.healthPoints = 1.0
        self.target = None

    def reset_agent(self):
        self.simObj.reset(
            lat=self.agent_parameters.lat,
            long=self.agent_parameters.long,
            alt=self.agent_parameters.alt,
            vel=self.agent_parameters.vel,
            heading=self.agent_parameters.heading)

    def set_target(self, target_agent):
        self.target = target_agent        

    def is_own_missile_active(self):
        return any(self.ammo[i].active for i in self.ammo.keys()) 

    def apply_action(self, action):
        self.simObj.step(action)
        self.apply_missile_action()

    def apply_missile_action(self):
        for i in self.ammo:
            if self.ammo[i].is_active():
                self.ammo[i].step()

    def launch_missile(self):
        if not self.is_own_missile_active():
            for i in self.ammo:
                if self.ammo[i].is_ready_to_launch():
                    self.ammo[i].set_target(self.target)
                    self.ammo[i].launch(self)
                    break

    
    def reset_ammo(self):    
        self.ammo = {}
        if self.agent_parameters.ammo > 0:
            for i in range(self.agent_parameters.ammo):
                self.ammo[str(i)] = AAMBVR(self.missile_simObj_conf)


class BTBVRAgent(BaseBVRAgent):

    def load_BT(self, BT_model):
        self.BT = BT_model(self)

    def apply_BT_action(self):
        self.BT.tick()
        heading = self.BT.heading
        altitude = self.BT.altitude
        throttle = 0.49
        if self.BT.launch_missile:
            self.launch_missile()
        action = np.array([heading, altitude, throttle])
        self.apply_action(action)



    '''
    def f16_missile_launch(self, blue_armed = False):

        angle = self.get_angle_to_enemy(enemy_red= True, cache_angle=True)
        if blue_armed:    
            if any([(self.aim_block[key].is_tracking_target()) for key in self.aim_block]):
                # some are currently active 
                #print('Blue: active missile ')
                pass
            else:
                # if within firing range
                # and firing angle  
                if abs(angle) < 35 and self.f16f16r_sep < 60e3:
                    #print('Launch blue missiles') 
                    for key in self.aim_block:
                        #print('Blue: Ready to launch, ',key , self.aim_block[key].is_ready_to_launch())
                        if self.aim_block[key].is_ready_to_launch():
                            lat, long, alt, vel, heading = self.get_init_state_AIM(self.f16)
                            self.aim_block[key].reset(lat, long, alt, vel, heading)
                            self.aim_block[key].reset_target(self.f16r, set_active=True)
                            break
    '''
