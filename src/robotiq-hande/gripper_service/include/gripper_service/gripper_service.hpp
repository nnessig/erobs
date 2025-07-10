#pragma once

#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "robotiq_driver/serial_interface.hpp"
#include "robotiq_driver/gripper_command.hpp"
#include "pdf_beamtime_interfaces/srv/gripper_control_msg.hpp"

class GripperService : public rclcpp::Node
{
public:
  GripperService();

private:
  void gripper_controller(
    const std::shared_ptr<pdf_beamtime_interfaces::srv::GripperControlMsg::Request> request,
    std::shared_ptr<pdf_beamtime_interfaces::srv::GripperControlMsg::Response> response);

  std::shared_ptr<robotiq_driver::SerialInterface> gripper_;
  rclcpp::Service<pdf_beamtime_interfaces::srv::GripperControlMsg>::SharedPtr service_;
};
