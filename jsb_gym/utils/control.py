
import numpy as np
from utils.navigation import roll_circle_clip

class PID:
	"""
	Discrete PID control
	"""

	def __init__(self, PID_gains):

		self.Kp=PID_gains.P
		self.Ki=PID_gains.I
		self.Kd=PID_gains.D
		self.Derivator=PID_gains.Deriv
		self.Integrator=PID_gains.Integ
		self.Integrator_max=PID_gains.Integ_max
		self.Integrator_min=PID_gains.Integ_min

		self.set_point=0.0
		self.error=0.0

	def update(self,current_value):
		"""
		Calculate PID output value for given reference input and feedback
		"""

		self.error = self.set_point - current_value

		self.P_value = self.Kp * self.error
		self.D_value = self.Kd * ( self.error - self.Derivator)
		self.Derivator = self.error

		self.Integrator = self.Integrator + self.error

		if self.Integrator > self.Integrator_max:
			self.Integrator = self.Integrator_max
		elif self.Integrator < self.Integrator_min:
			self.Integrator = self.Integrator_min

		self.I_value = self.Integrator * self.Ki

		PID = self.P_value + self.I_value + self.D_value

		return PID

	def setPoint(self,set_point):
		"""
		Initilize the setpoint of PID
		"""
		self.set_point = set_point
		self.Integrator=0
		self.Derivator=0

	def setIntegrator(self, Integrator):
		self.Integrator = Integrator

	def setDerivator(self, Derivator):
		self.Derivator = Derivator

	def setKp(self,P):
		self.Kp=P

	def setKi(self,I):
		self.Ki=I

	def setKd(self,D):
		self.Kd=D

	def getPoint(self):
		return self.set_point

	def getError(self):
		return self.error

	def getIntegrator(self):
		return self.Integrator

	def getDerivator(self):
		return self.Derivator

class AircraftPIDController:
	"""
	Aircraft PID controller class
	"""

	def __init__(self, aircraft):
		self.aircraft = aircraft
		self.aircraft_PID_Gains = aircraft.aircraft_PID_Gains
		self.aircraft_navigation = aircraft.aircraft_navigation
		self.aircraft_limits = aircraft.aircraft_limits
		self.reset_controllers()
	
	def reset_controllers(self):
		
		self.roll_PID = PID(self.aircraft_PID_Gains.Roll)
		self.roll_sec_PID = PID(self.aircraft_PID_Gains.Roll_sec)
		self.pitch_PID = PID(self.aircraft_PID_Gains.Pitch)
		self.rudder_theta_PID = PID(self.aircraft_PID_Gains.Rudder_theta)
		self.rudder_psi_PID = PID(self.aircraft_PID_Gains.Rudder_psi)
		self.elevator_psi_PID = PID(self.aircraft_PID_Gains.Elevator_psi)

		self.rudder_cmd = 0.0
		self.elevator_cmd = 0.0
		self.aileron_cmd = 0.0

		self.alt_act_space = self.aircraft_navigation.Alt_act_space_min
		self.head_act_space = self.aircraft_navigation.Head_act_space_min
		self.theta_act_space = self.aircraft_navigation.Theta_act_space_min


	def set_roll_PID(self, roll_ref, secondary_pid=False):
        # make sure within range
		roll_ref = np.clip(roll_ref, self.aircraft_limits.phi_min, self.aircraft_limits)
        
        # save for recording and other stuff
        
        # get reference value for control input 
		diff = roll_circle_clip(roll_ref)
        
		if secondary_pid:
			cmd = -self.roll_sec_PID.update(current_value=diff)
		else:
			cmd = -self.roll_PID.update(current_value=diff)

		self.aileron_cmd = np.clip(a = cmd, a_min = -1, a_max= 1)


	def get_control_input(self, diff_head, diff_alt):
        
		
		if abs(diff_head) >= self.head_act_space and abs(diff_alt) <= self.alt_act_space:
            
			# create larger altitude action space
			self.alt_act_space = self.aircraft_navigation.Alt_act_space_max
            # decide which direction to roll 
			roll_rot_dir = 1 if diff_head >= 0 else -1

			self.set_roll_PID(roll_ref= roll_rot_dir * (self.aircraft_navigation.Roll_max))
            # if roll is close to the limit 
			if self.aircraft_navigation.Roll_max - abs(self.aircraft.get_phi()) < 30:
                
				self.elevator_cmd = -0.3
			else:
				self.elevator_cmd = -0.9

			self.head_act_space = self.aircraft_navigation.Head_act_space_min

		else:
            # decrease margine adjust heading a bit 
			self.alt_act_space = self.aircraft_navigation.Alt_act_space_min
			theta_ref = np.degrees(np.arctan2(diff_alt, self.aircraft_navigation.Tan_ref))
			theta_ref = np.clip(a= theta_ref, a_min = self.aircraft_navigation.Dive_theta_max , a_max = self.aircraft_navigation.Climb_theta_max)

			if abs(diff_alt) > 1.5e3:

				self.theta_act_space = self.aircraft_navigation.Theta_act_space_max
                #self.conf.ctrl['theta_act_space'] = self.conf.ctrl['theta_act_space_max']
				self.set_roll_PID(roll_ref= 0.0)        

			elif abs(diff_alt) < 1.5e3 and abs(self.aircraft.get_theta()) > self.theta_act_space:
                
				self.theta_act_space = self.aircraft_navigation.Theta_act_space_min
				self.set_roll_PID(roll_ref= 0.0)
			else:
				self.theta_act_space = self.aircraft_navigation.Theta_act_space_max
				
				roll_rot_dir = 1 if diff_head >= 0 else -1
                
				if abs(diff_head) < 10:
                    
					self.set_roll_PID(roll_ref= roll_rot_dir * abs(diff_head), secondary_pid=True)
				else:
					self.set_roll_PID(roll_ref= roll_rot_dir * abs(diff_head)*3)
            
			self.set_pitch_PID(theta_ref)
			self.head_act_space = self.aircraft_navigation.Head_act_space_max

		return self.aileron_cmd, self.elevator_cmd, self.rudder_cmd			

        
	def set_pitch_PID(self, theta_ref):
		theta_ref = np.clip(theta_ref, self.aircraft_limits.theta_min, self.aircraft_limits.theta_max)
		diff = theta_ref - self.aircraft.get_theta()
		cmd = self.pitch_PID.update(current_value= diff)
		cmd = np.clip(a = cmd, a_min = -1, a_max= 1)
		self.elevator_cmd = cmd
