from jsb_gym.utils.control import AircraftPIDController
from jsb_gym.TAU.aircraft_base import Aircraft
from jsb_gym.utils.navigation import delta_heading


class F16BVR(Aircraft):
    def __init__(self, conf):
        super().__init__(conf)
        
        self.aircraft_control = AircraftPIDController(self)
        self.aircraft_simulation_config = conf.aircraft_simulation_config
        self.set_retract_gear()

        self.alt_ref = self.get_altitude()
        self.theta_ref = self.get_theta()
        self.psi_ref = self.get_psi()


    def step(self, action):
        for _ in range(self.aircraft_simulation_config.Sim_time_step):
            
            self._step(action)
        self.count += 1


    def _step(self, action):

        # heading betwen 0-360 deg
        # altitude in meters
        # throttle between 0-1 
        action_heading = action[0]
        action_altitude = action[1]
        action_throttle = action[2]

        diff_head = delta_heading(action_heading,self.get_psi() )
        diff_alt = action_altitude - self.get_altitude()

        for _ in range(self.aircraft_simulation_config.Control_time_step):
            aileron_cmd, elevator_cmd, rudder_cmd	= self.aircraft_control.get_control_input(diff_head, diff_alt)
            self.command_aircraft(aileron_cmd, elevator_cmd, rudder_cmd, action_throttle)    
            self.fdm.run()


    def command_aircraft(self, aileron_cmd, elevator_cmd, rudder_cmd, throttle_cmd):

        self.set_aileron(aileron_cmd)
        self.set_elevator(elevator_cmd)
        self.set_rudder(rudder_cmd)
        # todo velocity control. for now set 0.49 throttle at the imput 
        self.set_throttle(throttle_cmd)