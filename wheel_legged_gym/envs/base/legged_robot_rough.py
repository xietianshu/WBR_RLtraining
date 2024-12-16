from .legged_robot import LeggedRobot
from .legged_robot_config import LeggedRobotCfg
import torch
class LeggedRobotRough(LeggedRobot):
    def __init__(self, cfg: LeggedRobotCfg, sim_params, physics_engine, sim_device, headless):
        super().__init__(cfg, sim_params, physics_engine, sim_device, headless)

    def compute_proprioception_observations(self):
        # note that observation noise need to modified accordingly !!!
        heights = (
                torch.clip(
                    self.root_states[:, 2].unsqueeze(1) - 0.5 - self.measured_heights,
                    -1,
                    1.0,
                )
                * self.obs_scales.height_measurements
            )
        obs_buf = torch.cat(
            (
                # self.base_lin_vel * self.obs_scales.lin_vel,
                self.base_ang_vel * self.obs_scales.ang_vel,
                self.projected_gravity,
                self.commands[:, :3] * self.commands_scale,
                (self.dof_pos - self.default_dof_pos) * self.obs_scales.dof_pos,
                self.dof_vel * self.obs_scales.dof_vel,
                self.actions,
                heights
            ),
            dim=-1,
        )
        return obs_buf

    def compute_observations(self):
        """Computes observations"""
        self.obs_buf = self.compute_proprioception_observations()

        if self.cfg.env.num_privileged_obs is not None:
            heights = (
                torch.clip(
                    self.root_states[:, 2].unsqueeze(1) - 0.5 - self.measured_heights,
                    -1,
                    1.0,
                )
                * self.obs_scales.height_measurements
            )
            self.privileged_obs_buf = torch.cat(
                (
                    self.base_lin_vel * self.obs_scales.lin_vel,
                    self.obs_buf[:, :-77],
                    self.last_actions[:, :, 0],
                    self.last_actions[:, :, 1],
                    self.dof_acc * self.obs_scales.dof_acc,
                    heights,
                    self.torques * self.obs_scales.torque,
                    (self.base_mass - self.base_mass.mean()).view(self.num_envs, 1),
                    self.base_com,
                    self.default_dof_pos - self.raw_default_dof_pos,
                    self.friction_coef.view(self.num_envs, 1),
                    self.restitution_coef.view(self.num_envs, 1),
                ),
                dim=-1,
            )

        # add noise if needed
        if self.add_noise:
            self.obs_buf += (
                2 * torch.rand_like(self.obs_buf) - 1
            ) * self.noise_scale_vec

        update_idx = (
            (self.envs_steps_buf / self.cfg.control.decimation)
            % self.cfg.env.obs_history_dec
        ) == 0
        self.obs_history[update_idx, :] = torch.cat(
            (self.obs_history[update_idx, self.num_obs :], self.obs_buf[update_idx, :]),
            dim=-1,
        )