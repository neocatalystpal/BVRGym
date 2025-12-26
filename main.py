from jsb_gym.envs.BaseEnv import BVRBase
from jsb_gym.envs.config import baseEnv_conf

env = BVRBase(baseEnv_conf)
obs = env.reset()

print("Initial Observation:", obs)

for i in range(200):
    action = env.action_space.sample()  # Sample a random action
    obs, reward, done, info = env.step(action)
    env.log_tacview()
    print(f"Step {i+1} - Observation: {obs}, Reward: {reward}, Done: {done}")
    if i == 18:
        env.done = True


