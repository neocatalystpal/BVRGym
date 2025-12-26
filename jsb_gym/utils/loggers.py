import os
import pandas as pd

class TacviewLogger:
    def __init__(self, env):
        self.tacview_output_dir = env.conf.tacview_output_dir
        #os.makedirs(self.tacview_output_dir, exist_ok=True)
        self.env = env
        self.data_logs = {}
        for i in self.env.all_agents:
            self.data_logs[i.conf.agent_name] = {}
            self.data_logs[i.conf.agent_name] = {'name':i.conf.agent_name, 'aircraft_name': i.conf.aircraft_name, 'team': i.conf.team}
            self.data_logs[i.conf.agent_name][i.conf.agent_name] = []
            for j in i.ammo.keys():
                self.data_logs[i.conf.agent_name][j] = []

    def log_flight_data(self):

        for i in self.env.all_agents:
            self.data_logs[i.conf.agent_name][i.conf.agent_name].append(self.get_current_data(i))
            
            #for j in i.ammo.keys():
            #    if i.ammo[j].is_tracking_target():
            #        data_logger(data_loggs[i.name][j], i.ammo[j], time_ref=i.fdm)


    def get_current_data(self, agent):
        log = {
        "Time": agent.simObj.get_sim_time_sec(),
        "Longitude": agent.simObj.get_long_gc_deg(),
        "Latitude": agent.simObj.get_lat_gc_deg(),
        "Altitude": agent.simObj.get_altitude(),
        "Roll (deg)": agent.simObj.get_phi(),
        "Pitch (deg)": agent.simObj.get_theta(),
        "Yaw (deg)": agent.simObj.get_psi(),
        }
        return log

    def save_logs(self):
        for i in self.data_logs:
            pd.DataFrame(self.data_logs[i][i]).to_csv(f"{self.tacview_output_dir}/{self.data_logs[i]['aircraft_name']} ({self.data_logs[i]['name']}) [{self.data_logs[i]['team']}].csv", index=False)
        #pd.DataFrame(data_loggs['f16r']).to_csv("Tacview/F-16 (Randy) [Red].csv", index=False)