import py_trees as pt 
from jsb_gym.BT.reactive_seq import ReactiveSeq
import numpy as np 

        

class BT_utils(object):
    def __init__(self, env):
        self.env = env

    def is_missile_active(self, red_missile = False):
        active, name = self.env.is_missile_active(red_missile)
        return active, name

    def get_angle_to_enemy(self, from_red_perspective = False, offset = 0, heading_cockpit = False):
        #offset = -45
        if from_red_perspective:
            # enemy 
            fdm_tgt_lat = self.env.f16.get_lat_gc_deg()
            fdm_tgt_long = self.env.f16.get_long_gc_deg()
            # own 
            fdm_lat = self.env.f16r.get_lat_gc_deg()
            fdm_long = self.env.f16r.get_long_gc_deg()
            own_psi = self.env.f16r.get_psi()
            
        else:
            # enemy 
            fdm_tgt_lat = self.env.f16r.get_lat_gc_deg()
            fdm_tgt_long = self.env.f16r.get_long_gc_deg()
            # own 
            fdm_lat = self.env.f16.get_lat_gc_deg()
            fdm_long = self.env.f16.get_long_gc_deg()
            own_psi = self.env.f16.get_psi()

               
        ref_yaw = self.env.gtk.get_bearing(fdm_lat, fdm_long, fdm_tgt_lat, fdm_tgt_long)
        #print(ref_yaw)
        if heading_cockpit:
            ref_yaw = self.env.tk.get_heading_difference(psi_ref= ref_yaw, psi_deg= own_psi)
            return ref_yaw
        else:
            return ref_yaw + offset

    def get_distance_to_enemy(self, from_red_perspective = False):
        if from_red_perspective:
            dist = self.env.get_distance_to_enemy(fdm1=self.env.f16r, fdm2=self.env.f16, scale=False)
        else:
            dist = self.env.get_distance_to_enemy(fdm1=self.env.f16, fdm2=self.env.f16r, scale=False)
        return dist



class MAW_own_condition(pt.behaviour.Behaviour):
    def __init__(self, name, agent):
        super(MAW_own_condition, self).__init__(name)
        self.agent = agent

    def no_own_active_missile(self):
        active = self.agent.is_own_missile_active()
        if active:
            return False
        else:
            return True

    def update(self):
        if self.no_own_active_missile():
            return pt.common.Status.SUCCESS
        else:
            return pt.common.Status.FAILURE


class MAW_guide_evade_action(pt.behaviour.Behaviour):
    def __init__(self, name, agent):
        super(MAW_guide_evade_action, self).__init__(name)
        self.agent = agent
        self.heading = None
        self.altitude = None
        self.launch_missile = False
        


    def update(self):
        # evade in flank 
        self.heading = self.bt_utils.get_angle_to_enemy(from_red_perspective = self.red_team, offset = 45)
        # set 6 km altitude 
        self.altitude = 7e3
        
        #self.heading = None
        #self.altitude = None
        self.launch_missile = False
        return pt.common.Status.RUNNING


class BaseBT(object):
    def __init__(self, agent):
        self.agent = agent
        self.BTState = None
        self.BTState_old = None
        self.RootSuccess = False 
        self.root = ReactiveSeq("ReactiveSeq")
        



        #self.heading = None
        #self.altitude = None
        #self.launch_missile = False
        self.use_memory = False
        #self.bt_utils = BT_utils(env)
        #self.red_team = red_team

        '''Missile awerness system MAW'''        
        self.MAW_own = pt.composites.Selector(name = "13", memory = self.use_memory)
        self.MAW_own_con = MAW_own_condition('13C', self.agent)
        self.MAW_guide_evade_act = MAW_guide_evade_action('13A', self.bt_utils, self.red_team)
        self.MAW_own.add_children([self.MAW_own_con, self.MAW_guide_evade_act])
        
        self.MAW2 = pt.composites.Sequence(name = "12", memory = self.use_memory) #2
        self.MAW_evade_act = MAW_evade_action('12A', self.bt_utils, self.red_team)
        self.MAW2.add_children([self.MAW_own, self.MAW_evade_act])

        self.MAW = pt.composites.Selector(name = "11", memory = self.use_memory) # 1
        self.MAW_con = MAW_condition('11C', self.bt_utils, self.red_team)
        self.MAW.add_children([self.MAW_con, self.MAW2])

        '''Missile guidance'''
        self.guide = pt.composites.Selector(name = "21", memory = self.use_memory) # 1
        self.guide_own_con = MAW_own_condition('21C', self.bt_utils, self.red_team)
        self.guide_own_act = Guide_own_action('21A', self.bt_utils, self.red_team)
        self.guide.add_children([self.guide_own_con, self.guide_own_act])

        '''launch'''
        self.launch = pt.composites.Selector(name = "31", memory = self.use_memory) # 1
        self.launch_con = Launch_condition('31C', self.bt_utils, self.red_team)
        self.launch_act = Launch_action('31A', self.bt_utils, self.red_team)
        self.launch.add_children([self.launch_con, self.launch_act])

        '''pursue'''
        self.pursue = pt.composites.Selector(name= "41", memory = self.use_memory) # 1
        self.pursue_con = Pursue_condition('41C', self.bt_utils, self.red_team)
        self.pursue_act = Pursue_action('41A', self.bt_utils, self.red_team)
        self.pursue.add_children([self.pursue_con, self.pursue_act])

        '''root'''
        self.root.add_children([self.MAW, self.guide, self.launch, self.pursue])
        #tree = pt.trees.BehaviourTree(self.root)
        #print(ascii_tree(self.root))

    def tick(self):
        #print('-'*10)
        self.root.tick_once()
        self.BTState = self.root.tip().name
        #print('-')
        #if self.BTState != self.BTState_old:
        if self.BTState == '13A':
            self.heading = self.MAW_guide_evade_act.heading
            self.altitude = self.MAW_guide_evade_act.altitude
            self.launch_missile = self.MAW_guide_evade_act.launch_missile
        elif self.BTState == '12A':
            self.heading = self.MAW_evade_act.heading
            self.altitude = self.MAW_evade_act.altitude
            self.launch_missile = self.MAW_evade_act.launch_missile
        elif self.BTState == '21A':
            self.heading = self.guide_own_act.heading
            self.altitude = self.guide_own_act.altitude
            self.launch_missile = self.guide_own_act.launch_missile
        elif self.BTState == '31A':
            self.heading = self.launch_act.heading
            self.altitude = self.launch_act.altitude
            self.launch_missile = self.launch_act.launch_missile
        elif self.BTState == '41A':
            self.heading = self.pursue_act.heading
            self.altitude = self.pursue_act.altitude
            self.launch_missile = self.pursue_act.launch_missile
        else:
            print('Unexpected state')
            exit()

        if self.BTState != self.BTState_old:
            print(self.BTState)
            #print(self.heading)
            #print(self.altitude)
            #print('Red:  BT launch missile ', self.launch_missile)

        self.BTState_old = self.BTState

class MAW_condition(pt.behaviour.Behaviour):
    def __init__(self, name, bt_utils, red_team):
        super(MAW_condition, self).__init__(name)
        self.bt_utils = bt_utils
        self.red_team = red_team

    def no_incomming_missile(self):
        # return status about the blue teams missiles 
        active, name = self.bt_utils.is_missile_active(red_missile = not self.red_team)
        #print(active)
        if active:
            return False
        else:
            return True

    def update(self):
        #print('Tick 11C')
        if self.no_incomming_missile():
            return pt.common.Status.SUCCESS
        else:
            return pt.common.Status.FAILURE
        




class MAW_evade_action(pt.behaviour.Behaviour):
    def __init__(self, name, bt_utils, red_team):
        super(MAW_evade_action, self).__init__(name)
        self.bt_utils = bt_utils
        self.heading = None
        self.altitude = None
        self.launch_missile = False
        self.red_team = red_team
        #offset = -180

    def update(self):
        # evade in 180 oposite direction from 
        self.heading = self.bt_utils.get_angle_to_enemy(from_red_perspective = self.red_team, offset = 180)
        # set 6 km altitude 
        self.altitude = 8e3
        self.launch_missile = False

        return pt.common.Status.RUNNING

class Guide_own_action(pt.behaviour.Behaviour):
    def __init__(self, name, bt_utils, red_team):
        super(Guide_own_action, self).__init__(name)
        self.bt_utils = bt_utils
        self.red_team = red_team
        self.heading = None
        self.altitude = None
        self.launch_missile = False
    
    def update(self):
        
        self.heading = self.bt_utils.get_angle_to_enemy(from_red_perspective = self.red_team, offset = 45)
        self.altitude = 8e3
        self.launch_missile = False
        return pt.common.Status.RUNNING

class Pursue_condition(pt.behaviour.Behaviour):
    def __init__(self, name, bt_utils, red_team):
        super(Pursue_condition, self).__init__(name)
        self.bt_utils = bt_utils
        self.red_team = red_team   

    def enemy_not_alive(self):
        return False

    def update(self):
        #self.feedback_message = "MAW_condition"
        if self.enemy_not_alive():
            return pt.common.Status.SUCCESS
        else:
            return pt.common.Status.FAILURE

class Pursue_action(pt.behaviour.Behaviour):
    def __init__(self, name, bt_utils, red_team):
        super(Pursue_action, self).__init__(name)
        self.bt_utils = bt_utils
        self.heading = None
        self.altitude = None
        self.launch_missile = False
        self.red_team = red_team

    def update(self):
        
        self.heading = self.bt_utils.get_angle_to_enemy(from_red_perspective = self.red_team, offset = 0)
        self.altitude = 10e3
        self.launch_missile = False
        return pt.common.Status.RUNNING

class Launch_condition(pt.behaviour.Behaviour):
    def __init__(self, name, bt_utils, red_team):
        super(Launch_condition, self).__init__(name)
        self.bt_utils = bt_utils
        self.red_team = red_team

    def is_in_launch_range(self):
        dist = self.bt_utils.get_distance_to_enemy(from_red_perspective = self.red_team)
        head_cockpit = self.bt_utils.get_angle_to_enemy(from_red_perspective = self.red_team, offset = 0, heading_cockpit = True)
        #print('distance: ', round(dist))
        if dist < 60e3 and abs(head_cockpit) < 35:
            return True
        else:
            return False

    def not_in_launch_position(self):
        # return status about the blue teams missile 
        if self.is_in_launch_range():
            return False
        else:
            return True

    def update(self):
        self.feedback_message = "MAW_condition"
        if self.not_in_launch_position():
            return pt.common.Status.SUCCESS
        else:
            return pt.common.Status.FAILURE

class Launch_action(pt.behaviour.Behaviour):
    def __init__(self, name, bt_utils, red_team):
        super(Launch_action, self).__init__(name)
        self.bt_utils = bt_utils
        self.heading = None
        self.altitude = None
        self.launch_missile = False
        self.red_team = red_team

    def update(self):
        self.heading = self.bt_utils.get_angle_to_enemy(from_red_perspective = self.red_team, offset = 0)
        self.altitude = 10e3
        self.launch_missile = True

        return pt.common.Status.RUNNING
