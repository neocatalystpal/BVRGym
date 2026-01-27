
from jsb_gym.simObjects.config import f16_config
from jsb_gym.simObjects.aircraft import F16BVR

f16_config.data_output_xml = 'data_output/flightgear.xml'
f16_config.fg_sleep_time= 0.005
f16_config.aircraft_simulation.Sim_time_step = 1

F16 = F16BVR(f16_config)

F16.reset(lat=34.2007, long=-118.358, alt=5000, vel=250, heading=90)

for _ in range(1000):
    if _ > 500:
        action = [270, 4000, 0.69]  # heading, altitude, throttle
    else:
        action = [0, 3000, 0.49]  # heading, altitude, throttle

    F16.step(action)
    F16.print_status()


# run from BVRGYM directory using: 
#  python -m tests.test_aircraft