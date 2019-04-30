import torch
from torch import __init__


def output_random_target(robot):
    """
    Get a target state point generated by a random control on the robot
    """
    for ctrl in robot.parameters():
        ctrl.data = torch.rand(robot.dim_ctrl)
    with torch.autograd.set_grad_enabled(False):
        random_target = robot.forward()
    # Rerandomize
    for ctrl in robot.parameters():
        ctrl.data = torch.rand(robot.dim_ctrl)
    return random_target


def load_cmd(robot, cmd):
    """
    Go from the command to its implementation in the robot
    """
    for current_ctrl, given_ctrl in zip(robot.parameters(), cmd):
        current_ctrl.data.copy_(given_ctrl)


class QuadTargetCost(torch.nn.Module):
    """
    Final target cost as a quadratic on the final state
    """

    def __init__(self, quad_cost, target):
        super(QuadTargetCost, self).__init__()
        self.quad_cost = quad_cost
        self.target = target

    def forward(self, input):
        target_cost = 0.5 * \
            (input - self.target).dot(torch.mv(self.quad_cost, input - self.target))
        return target_cost