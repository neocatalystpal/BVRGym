from jsb_gym.envs.BaseEnv import BVRBase
from jsb_gym.envs.config import baseEnv_conf

from stable_baselines3.common.env_util import make_vec_env
from torch.utils.tensorboard import SummaryWriter
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3 import PPO


class GymCallback(BaseCallback):
    def __init__(self):
        super().__init__()
        self.writer = SummaryWriter("runs/BVRBase")

    def _on_step(self):
        infos = self.locals.get("infos", [])
        for info in infos:
            if info["done"]:
                self.writer.add_scalar("env/trunk", info["trunk"], global_step=self.num_timesteps)
        return True


def main():
    vec_env = make_vec_env(BVRBase, n_envs=14, vec_env_cls=SubprocVecEnv, env_kwargs={'conf': baseEnv_conf})        
    model = PPO("MlpPolicy", vec_env, verbose=1, tensorboard_log="runs")
    model.learn(total_timesteps=2_000_000, callback=GymCallback())

    model.save("trained/BVRBase_PPO_2M")


if __name__ == "__main__":
    main()