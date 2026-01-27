
from jsb_gym.simObjects.config import f16_config, AAM_config
from jsb_gym.simObjects.aircraft import F16BVR
from jsb_gym.simObjects.missiles import AAMBVR

AAM_config.data_output_xml = 'data_output/flightgear_red.xml'
f16_config.data_output_xml = 'data_output/flightgear.xml'
AAM_config.fg_sleep_time = 0.0005
f16_config.fg_sleep_time = 0.0005
AAM_config.missile_performance.effective_radius = 1
AAM_config.missile_simulation.Sim_time_step = 1
f16_config.aircraft_simulation.Sim_time_step = 1


#self.blue_agent = RLBVRAgent(blue_agent, self)
AIM = AAMBVR(AAM_config)
F16 = F16BVR(f16_config)


F16.reset(lat=59, long=18, alt=3000, vel=250, heading=180)

AIM.reset(lat=58.4, long=18, alt=10000, vel=250, heading=0)
AIM.set_target(F16)


for _ in range(1000):
    action = [150, 4000, 0.5]  # heading, altitude, throttle
    F16.step(action)
    AIM.step()

    if AIM.PN.distance_to_target < 600:
        print("Close to target!, distance:", AIM.PN.distance_to_target)
        input("Press Enter to continue a step...")
    AIM.print_status()

# run from BVRGYM directory using: 
#  python -m tests.test_missile