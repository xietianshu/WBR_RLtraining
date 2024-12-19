# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

from wheel_legged_gym.envs.base.legged_robot_config import (
    LeggedRobotCfg,
    LeggedRobotCfgPPO,
)


class WheelLeggedCfg(LeggedRobotCfg):

    class init_state(LeggedRobotCfg.init_state):
        pos = [0.0, 0.0, 0.6]  # x,y,z [m]
        default_joint_angles = {  # target angles when action = 0.0
            "HipR": 0.5,
            "KneeR": 1.5,
            "HubR": 0.0,
            "HipL": -0.5,
            "KneeL": -1.5,
            "HubL": 0.0,
        }

    class control(LeggedRobotCfg.control):
        pos_action_scale = 0.5
        vel_action_scale = 10.0
        # PD Drive parameters:
        stiffness = {
                    "HipL": 40.0,
                    "KneeL": 40.0,
                    "HubL": 0.0,
                    "HipR": 40.0,
                    "KneeR": 40.0,
                    "HubR": 0.0,
                    }  # [N*m/rad]
        damping = {
                    "HipL": 1.0,
                    "KneeL": 1.0,
                    "HubL": 0.5,
                    "HipR": 1.0,
                    "KneeR": 1.0,
                    "HubR": 0.5,
                    }     # [N*m*s/rad]

    class asset(LeggedRobotCfg.asset):
        file = "{WHEEL_LEGGED_GYM_ROOT_DIR}/resources/robots/wheeled_legged/urdf/wheeled_legged.urdf"
        name = "WheelLegged"
        # offset = 0.0
        # l1 = 0.26
        # l2 = 0.26
        penalize_contacts_on = []
        terminate_after_contacts_on = ["base_link", "Tigh", "Shank"]
        self_collisions = 1  # 1 to disable, 0 to enable...bitwise filter
        flip_visual_attachments = False


class WheelLeggedCfgPPO(LeggedRobotCfgPPO):
    class runner(LeggedRobotCfgPPO.runner):
        # logging
        experiment_name = "wheel_legged"
