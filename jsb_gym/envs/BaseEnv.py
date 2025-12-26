import gymnasium as gym
from gymnasium import spaces

import numpy as np

from jsb_gym.agents.config import blue_agent, red_agent
from jsb_gym.agents.agents import BaseBVRAgent

from jsb_gym.utils.geospatial import dinstance_between_agents, bearing_between_agents, to_360
from jsb_gym.utils.loggers import TacviewLogger

class BVRBase(gym.Env):
    def __init__(self, conf):
        # Environment config file 
        super().__init__()
        self.conf = conf
        self.obs_shape = conf.observation_shape
        self.act_shape = conf.action_shape

        self.observation_space = spaces.Box(low=-1.0, high=1.0, shape=self.obs_shape, dtype=np.float32)
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=self.act_shape, dtype=np.float32)        

        self.state = None
        self.done = False
        self.tacview_logger = None

    def reset(self):
        
        self.blue_agent = BaseBVRAgent(blue_agent, self)
        self.red_agent = BaseBVRAgent(red_agent, self)

        self.all_agents = [self.blue_agent, self.red_agent]

        self.blue_agent.set_target(self.red_agent)
        self.red_agent.set_target(self.blue_agent)

        self.update_state()

        return self.state, {}

    def log_tacview(self):

        if self.conf.tacview_output_dir is not None:
            if self.tacview_logger is None:
                self.tacview_logger = TacviewLogger(self)
            elif self.done:
                self.tacview_logger.save_logs()
            else:
                self.tacview_logger.log_flight_data()
        
        
            


    def update_state(self):
        if self.state is None:
            self.state = np.tile(self.get_observation(), (self.obs_shape[0], 1))
        else:
            self.state = np.roll(self.state, shift=-1, axis=0)
            self.state[-1,:] = self.get_observation()

    def get_observation(self):
        
        bearing = to_360(bearing_between_agents(self.blue_agent, self.red_agent))
        # enemy missile active 
        # own missile active
        heading = self.blue_agent.simObj.get_psi()
        mach = self.blue_agent.simObj.get_mach()
        altitude = self.blue_agent.simObj.get_altitude()

        d = dinstance_between_agents(self.blue_agent, self.red_agent)

        enemy_bearing = to_360(bearing_between_agents(self.red_agent, self.blue_agent)) 

        enemy_heading = self.red_agent.simObj.get_psi()
        enemy_mach = self.red_agent.simObj.get_mach()
        enemy_altitude = self.red_agent.simObj.get_altitude()

        return np.array([
            bearing,
            heading,
            mach,
            altitude,
            d,
            enemy_bearing,
            enemy_heading,
            enemy_mach,
            enemy_altitude
        ], dtype=np.float32)


    def step(self, action):
        # apply action to agent
        self.blue_agent.apply_action(action)
        self.red_agent.apply_action(action)
        # step sim objects
        # get new observation
        # calculate reward
        # check done
        done = False
        reward = 0.0

        return None, reward, done, None


    def from_env2NN(self, agent_state):
        """
        Convert agent state to environment state representation.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def from_NN2env(self, env_state):
        """
        Convert environment state to agent state representation.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")



    def get_reward(self, is_done):

        if is_done:
            if not self.f16r_alive:
                return 1
                #return self.conf.general['sim_time_max']/self.conf.general['r_step']
            elif not self.f16_alive:
                return -1
                #return -self.conf.general['sim_time_max']/self.conf.general['r_step']
            else:
                return -1
        else:
            return 0

    def is_done(self):
        
        # if 
        # check if any missile hit target or lost
        # 
        # check if f16 is alive
        # check if f16 hit ground
        # check if all missiles lost
        # check if max time reached
        
        # both out of missiles 
        pass
 


               

    def render(self):
        pass
        # visualize the environment

