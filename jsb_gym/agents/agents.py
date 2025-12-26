from jsb_gym.simObjects.aircraft import F16BVR
from jsb_gym.simObjects.missiles import AAMBVR


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
    
    def reset_ammo(self):    
        self.ammo = {}
        if self.agent_parameters.ammo > 0:
            for i in range(self.agent_parameters.ammo):
                self.ammo[str(i)] = AAMBVR(self.missile_simObj_conf)


    

