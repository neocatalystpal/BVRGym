tacview_output_dir = 'data_output/tacview'

observation_shape = (40, 15)
action_shape = (3,)

# Increased from 600s (10 min) to 1800s (30 min) for complex strategy development
max_episode_time = 60*30

step_length = 1