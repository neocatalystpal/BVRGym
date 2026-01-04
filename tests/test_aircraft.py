
from jsb_gym.simObjects.config import f16_config
from jsb_gym.simObjects.aircraft import F16BVR

F16 = F16BVR(f16_config)

F16.reset(lat=34.2007, long=-118.358, alt=3000, vel=250, heading=90)

for _ in range(1000):
    action = [270, 4000, 0.5]  # heading, altitude, throttle
    F16.step(action)
    print(f"Time: {F16.get_sim_time_sec():.2f} sec, Lat: {F16.get_lat_gc_deg():.4f}, Long: {F16.get_long_gc_deg():.4f}, Altitude: {F16.get_altitude():.2f} m, Mach: {F16.get_mach():.4f}, Heading: {F16.get_psi():.2f} deg")


# run from BVRGYM directory using: 
#  python -m tests.test_aircraft