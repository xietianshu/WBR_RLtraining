from ..wheel_legged.wheel_legged_config import WheelLeggedCfg, WheelLeggedCfgPPO

class WheelLeggedRoughCfg(WheelLeggedCfg):
    class env(WheelLeggedCfg.env):
        num_observations = 27 + 11*7
        num_privileged_obs = num_observations + 3 + 6 * 5 + 3 + 3
        
    class terrain(WheelLeggedCfg.terrain):
        curriculum = True
        selected = False

class WheelLeggedRoughCfgPPO(WheelLeggedCfgPPO):
    class runner(WheelLeggedCfgPPO.runner):
        # logging
        experiment_name = "wheel_legged_rough"

    class policy(WheelLeggedCfgPPO.policy):
        num_encoder_obs = WheelLeggedRoughCfg.env.obs_history_length * WheelLeggedRoughCfg.env.num_observations