#include "gripper_service/gripper_service.hpp"

using std::placeholders::_1;
using std::placeholders::_2;

GripperService::GripperService()
: Node("gripper_service")
{
  const std::string kComPort = "/dev/ttyUSB0";
  const uint8_t kSlaveID = 0x09;

  gripper_ = std::make_shared<robotiq_driver::SerialInterface>();

  if (!gripper_->connect(kComPort, kSlaveID))
  {
    RCLCPP_ERROR(this->get_logger(), "Failed to connect to gripper.");
    throw std::runtime_error("Gripper connection failed.");
  }

  gripper_->activate();

  service_ = this->create_service<pdf_beamtime_interfaces::srv::GripperControlMsg>(
    "gripper_control",
    std::bind(&GripperService::gripper_controller, this, _1, _2));

  RCLCPP_INFO(this->get_logger(), "Gripper service ready.");
}

void GripperService::gripper_controller(
  const std::shared_ptr<pdf_beamtime_interfaces::srv::GripperControlMsg::Request> request,
  std::shared_ptr<pdf_beamtime_interfaces::srv::GripperControlMsg::Response> response)
{
  RCLCPP_INFO(this->get_logger(), "Received command: %s (%d)", request->command.c_str(), request->grip);

  if (request->command == "deactivate")
  {
    gripper_->deactivate();
    response->results = 0;
    return;
  }

  robotiq_driver::GripperCommand cmd;
  cmd.position = std::clamp(request->grip, 0, 100);
  cmd.speed = 100;
  cmd.force = 100;

  if (!gripper_->sendCommand(cmd))
  {
    RCLCPP_ERROR(this->get_logger(), "Failed to send gripper command.");
    response->results = 1;
    return;
  }

  response->results = 0;
}
