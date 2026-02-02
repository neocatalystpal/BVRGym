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
    # Enhanced hyperparameters for better training
    n_envs = 32  # Increased from 14 for more diverse experience
    total_timesteps = 5_000_000  # Increased from 2M for longer training
    
    vec_env = make_vec_env(BVRBase, n_envs=n_envs, vec_env_cls=SubprocVecEnv, env_kwargs={'conf': baseEnv_conf})
    
    # Optimized PPO parameters
    model = PPO(
        "MlpPolicy",
        vec_env,
        verbose=1,
        tensorboard_log="runs",
        learning_rate=3e-4,  # Standard RL learning rate
        n_steps=2048,  # More steps before update
        batch_size=256,  # Larger batches for stability
        n_epochs=20,  # More epochs per update
        gamma=0.99,  # Standard discount factor
        gae_lambda=0.95,  # GAE parameter
        clip_range=0.2,  # PPO clip range
        ent_coef=0.01,  # Entropy coefficient for exploration
    )
    
    # Train with callback for monitoring
    model.learn(total_timesteps=total_timesteps, callback=GymCallback())

    # Save final model
    model.save("trained/BVRBase_PPO_5M_improved")


if __name__ == "__main__":
    main()