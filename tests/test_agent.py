
from jsb_gym.agents.config import blue_agent
from jsb_gym.agents.agents import Blue_BVRAgent



# reset initial position of agent
blue_agent.lat = 59.0
blue_agent.long = 18.0
blue_agent.alt = 3000.0
blue_agent.vel = 250.0
blue_agent.heading = 0.0

agent = Blue_BVRAgent(blue_agent)
print(f"Agent initialized with ammo count: {len(agent.ammo)}")