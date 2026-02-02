import gymnasium as gym
from gymnasium import spaces

import numpy as np

from jsb_gym.agents.config import blue_agent, red_agent
from jsb_gym.agents.agents import RLBVRAgent, BTBVRAgent

from jsb_gym.utils.geospatial import dinstance_between_agents, bearing_between_agents, to_360
from jsb_gym.utils.loggers import TacviewLogger

from jsb_gym.utils.scale import scale_between_inv, scale_between

from jsb_gym.bts.bts import BVRBT

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
        self.observation = {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        self.blue_agent = RLBVRAgent(blue_agent, self)
        
        self.red_agent = BTBVRAgent(red_agent, self)
        
        self.red_agent.load_BT(BVRBT)
        
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
        self.update_observation()
        obs_nn = self.from_obs2nn(self.blue_agent)
        
        if self.state is None:
            self.state = np.tile(obs_nn, (self.obs_shape[0], 1))
        else:
            self.state = np.roll(self.state, shift=-1, axis=0)
            self.state[-1,:] = obs_nn

    def update_observation(self):
        
        self.observation['bearing'] = to_360(bearing_between_agents(self.blue_agent, self.blue_agent.target))
        self.observation['heading'] = self.blue_agent.simObj.get_psi()
        self.observation['mach'] = self.blue_agent.simObj.get_mach()
        self.observation['altitude'] = self.blue_agent.simObj.get_altitude()

        self.observation['d'] = dinstance_between_agents(self.blue_agent, self.blue_agent.target)

        self.observation['enemy_bearing'] = to_360(bearing_between_agents(self.red_agent, self.red_agent.target)) 

        self.observation['enemy_heading'] = self.red_agent.simObj.get_psi()
        self.observation['enemy_mach'] = self.red_agent.simObj.get_mach()
        self.observation['enemy_altitude'] = self.red_agent.simObj.get_altitude()

        # Track active missiles for both agents
        self.observation['own_missile_active'] = 1 if self.blue_agent.is_own_missile_active() else 0
        self.observation['enemy_missile_active'] = 1 if self.red_agent.is_own_missile_active() else 0
        

    def step(self, action):
        # apply action to agent
        action = self.from_nn2agent(action, self.blue_agent)
        
        for i in range(self.conf.step_length):
            # If step_length is 10, this should result aplllying action for 10 sim seconds, unless you changed the sim step time in FDM config
            self.blue_agent.apply_action(action)
            self.red_agent.apply_action()
            # get new observation
            self.update_state()
            
            self.done = self.is_done()
            # calculate reward
            # check done
            
            self.reward = self.get_reward(self.done)
            if self.done:
                break
        return self.state, self.reward, self.done, self.max_episode_time_passed(), {'done': self.done, 'trunk': self.max_episode_time_passed()}

    def get_red_agent_actions(self):
        pass

    def from_obs2nn(self, agent):
        
        bearing_sin = np.sin(np.radians(self.observation['bearing']))
        bearing_cos = np.cos(np.radians(self.observation['bearing']))
        heading_sin = np.sin(np.radians(self.observation['heading']))
        heading_cos = np.cos(np.radians(self.observation['heading']))
        
        mach = scale_between(self.observation['mach'], a_min = 0.1, a_max = 1.5)
        altitude = scale_between(self.observation['altitude'], a_min = agent.simObj.conf.aircraft_limits.alt_min,
                               a_max = agent.simObj.conf.aircraft_limits.alt_max )
        d = scale_between(self.observation['d'], a_min = 0.0, a_max = 120e3)
        
        enemy_bearing_sin= np.sin(np.radians(self.observation['enemy_bearing']))
        enemy_bearing_cos= np.cos(np.radians(self.observation['enemy_bearing']))
        enemy_heading_sin = np.sin(np.radians(self.observation['enemy_heading']))
        enemy_heading_cos = np.cos(np.radians(self.observation['enemy_heading']))
        
        enemy_mach = scale_between(self.observation['enemy_mach'], a_min = 0.1, a_max = 1.5)
        enemy_altitude = scale_between(self.observation['enemy_altitude'], a_min = agent.simObj.conf.aircraft_limits.alt_min,
                               a_max = agent.simObj.conf.aircraft_limits.alt_max )
        
        return np.array([bearing_sin, bearing_cos, heading_sin, heading_cos, mach, altitude, d, enemy_bearing_sin, enemy_bearing_cos, 
                         enemy_heading_sin, enemy_heading_cos, enemy_mach, enemy_altitude, 
                         self.observation['own_missile_active'], self.observation['enemy_missile_active']])
        
        
        

    
    def from_nn2agent(self, action, agent):
        # heading 
        action[0] = scale_between_inv(action[0],
                                      a_min= agent.simObj.conf.aircraft_limits.psi_min,
                                        a_max= agent.simObj.conf.aircraft_limits.psi_max)        
        # altitude 
        action[1] = scale_between_inv(action[1],
                                      a_min= agent.simObj.conf.aircraft_limits.alt_min,
                                        a_max= agent.simObj.conf.aircraft_limits.alt_max)
        # throttle full thrust without or with afterburner 
        action[2] = 0.49 if action[2] <= 0.0 else 0.69
        return action


    def get_reward(self, is_done):
        """Enhanced reward function with tactical bonuses for better training"""
        reward = 0
        
        # Terminal rewards (highest priority)
        if is_done:
            # Win condition: Enemy shot down
            if self.red_agent.healthPoints <= 0.0:
                reward += 1000.0
            # Loss condition: Blue agent shot down
            elif self.blue_agent.healthPoints <= 0.0:
                reward -= 1000.0
            # Timeout: Stalemate
            else:
                reward -= 100.0
        
        # Distance-based reward: Encourage closing to attack range
        dist = self.observation['d']
        max_distance = 120e3
        distance_reward = (max_distance - dist) / max_distance * 10.0
        reward += max(0, distance_reward)
        
        # Tactical positioning: Reward getting behind enemy (low relative bearing)
        rel_bearing_error = abs(self.observation['bearing'] - self.observation['heading'])
        if rel_bearing_error > 180:
            rel_bearing_error = 360 - rel_bearing_error
        positioning_reward = (90 - rel_bearing_error) / 90.0 * 5.0 if rel_bearing_error < 90 else 0
        reward += max(0, positioning_reward)
        
        # Missile launch reward: Encourage tactical launches
        if self.blue_agent.is_own_missile_active():
            reward += 50.0
        
        # Altitude advantage reward: Higher is better for energy management
        alt_diff = (self.observation['altitude'] - self.observation['enemy_altitude']) / 5000.0
        reward += max(-2, min(2, alt_diff))  # Clamp to [-2, 2]
        
        # Speed advantage reward: Mach number matters in BVR
        mach_diff = (self.observation['mach'] - self.observation['enemy_mach']) * 5.0
        reward += max(-2, min(2, mach_diff))  # Clamp to [-2, 2]
        
        return reward

    def is_done(self):
        for agent in self.all_agents:
            if agent.healthPoints <= 0.0:
                return True
            
        
        if self.max_episode_time_passed():
            return True 
        return False
    
    def max_episode_time_passed(self):
        if self.blue_agent.simObj.get_sim_time_sec() >= self.conf.max_episode_time:
            return True 
        return False
               

