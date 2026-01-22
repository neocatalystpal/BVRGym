from jsb_gym.envs.BaseEnv import BVRBase
from jsb_gym.envs.config import baseEnv_conf

env = BVRBase(baseEnv_conf)
obs = env.reset()

done = False
while not done:
    action = env.action_space.sample()  # Sample a random action
    obs, reward, done, info = env.step(action)
    env.log_tacview()
print(info)
print("View data in Tacview from data_output/tacview/")

