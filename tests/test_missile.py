
from jsb_gym.simObjects.config import f16_config, AAM_config
from jsb_gym.simObjects.aircraft import F16BVR
from jsb_gym.simObjects.missiles import AAMBVR

AAM_config.data_output_xml = 'data_output/flightgear_red.xml'
f16_config.data_output_xml = 'data_output/flightgear.xml'
AAM_config.fg_sleep_time = 0.001
f16_config.fg_sleep_time = 0.001


AIM = AAMBVR(AAM_config)
F16 = F16BVR(f16_config)


F16.reset(lat=59, long=18, alt=3000, vel=250, heading=0)

AIM.reset(lat=58.8, long=18, alt=5000, vel=250, heading=0)
AIM.set_target(F16)


for _ in range(1000):
    action = [270, 4000, 0.5]  # heading, altitude, throttle
    F16.step(action)
    AIM.step()

    #print(f"Time: {F16.get_sim_time_sec():.2f} sec, Lat: {F16.get_lat_gc_deg():.4f}, Long: {F16.get_long_gc_deg():.4f}, Altitude: {F16.get_altitude():.2f} m, Mach: {F16.get_mach():.4f}, Heading: {F16.get_psi():.2f} deg")
    print(AIM.PN.distance_to_target)

# run from BVRGYM directory using: 
#  python -m tests.test_missile