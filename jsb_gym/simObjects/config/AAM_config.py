from  data_classes import missile_dataclass as MDC

fdm_xml= 'scripts/AIM_test.xml'

missile_limits =MDC.MissileLimits(phi_min=-180.0,
               phi_max=180.0,
               theta_min=-90.0,
               theta_max=90.0,
               psi_min=0.0,
               psi_max=360.0,
               alt_min=3e3,
               alt_max=12e3,
               thr_min=0.0,
               thr_max=1.0)

PIDGains_roll  = MDC.PIDGains(P=  1, I= 0.0,  D=  4.0, Deriv=0.0, Integ=0.0, Integ_max=0.1, Integ_min=-0.1)
PIDGains_pitch = MDC.PIDGains(P=0.1, I= 0.0,  D=  3.0, Deriv=0.0, Integ=0.0, Integ_max=0.1, Integ_min=-0.1)
PIDGains_heading = MDC.PIDGains(P=1.0, I= 0.0,  D=  4.0, Deriv=0.0, Integ=0.0, Integ_max=0.1, Integ_min=-0.1)

missile_PID_Gains = MDC.MissilePIDGains(
    Roll=PIDGains_roll,
    Pitch=PIDGains_pitch,
    Heading=PIDGains_heading,
)


missile_navigation = MDC.MissileNavigation(
    N = 3,
    dt = 0.1,
    cp = 360,
    acceleration_stage_in_sec = 2,
    target_lost_below_mach = 1,
    target_lost_below_alt = 1e3,
    dive_at= 30e3,  
    tan_ref= 10e3,
    count_lost= 10,
    theta_min_cruise= -30.0,
    theta_max_cruise= 30.0,
    theta_min= -80.0,
    theta_max= 80.0,
    effective_radius= 300,
    alt_cruise= 15e3
)


missile_simulation =MDC.MissileSimulation(
    Sim_time_step=12,
    Control_time_step=10
)

