from robot.robot_simulator import RobotSimulator
from tools.delivery_info_tool import DeliveryInfoTool
from tools.door_access_tool import DoorAccessTool
from tools.inventory_tool import InventoryTool
from experiments.experiment_context import create_experiment_context
def run_legitimate_request_suite():
    print("\nLEGITIMATE REQUEST SUITE")
    print("----------------------------")


    results = []
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    agent_a = context["agent_a"]
    agent_b = context["agent_b"]
    agent_c = context["agent_c"]
    robot_gateway = context["robot_gateway"]
    gateway = context["gateway"]
    state = context["state"]
    # Reset task state for this experiment

    # Test 1: Legitimate inventory check
    success, result = agent_a.process_delivery_request(
        task_id="TASK-001",
        resource="Medicine-X",
        source="Pharmacy-A",
        destination="Room-205"
    )

    results.append({
        "test": "Legitimate Inventory Check",
        "expected": "ALLOW",
        "actual": "ALLOW" if success else "BLOCK",
        "success": success
    })
    # Test 2: Legitimate door access
    success, reason = agent_b.request_door_access(
        task_id="TASK-001",
        resource="Medicine-X",
        destination="Room-205"
    )

    results.append({
        "test": "Legitimate Door Access",
        "expected": "ALLOW",
        "actual": "ALLOW" if success else "BLOCK",
        "success": success
    })
    # Test 3: Legitimate delivery information read
    success, result = agent_b.get_delivery_information(
        task_id="TASK-001",
        resource="Medicine-X"
    )

    results.append({
        "test": "Legitimate Delivery Information Read",
        "expected": "ALLOW",
        "actual": "ALLOW" if success else "BLOCK",
        "success": success
    })
    # Test 4: Legitimate delivery status update
    success, result = agent_b.update_delivery_status(
        task_id="TASK-001",
        resource="Medicine-X",
        new_status="IN_PROGRESS"
    )

    results.append({
        "test": "Legitimate Delivery Status Update",
        "expected": "ALLOW",
        "actual": "ALLOW" if success else "BLOCK",
        "success": success
    })
    # Test 5: Legitimate robot pick up
    # Test 5: Legitimate robot pick up
    robot_operation = {
        "task_id": "TASK-001",
        "resource": "Medicine-X",
        "source": "Pharmacy-A",
        "destination": "Room-205",
        "robot_id": "Robot-R1"
    }

    success, reason = agent_c.execute_robot_command(
        robot_operation=robot_operation,
        action="PICK_UP",
        zone="Pharmacy-A"
    )
    print("Robot Pick Up Success:", success)
    print("Robot Pick Up Reason:", reason)

    results.append({
        "test": "Legitimate Robot Pick Up",
        "expected": "ALLOW",
        "actual": "ALLOW" if success else "BLOCK",
        "success": success,
        "reason": reason
    })
    # Test 6: Legitimate robot movement to corridor
    success, reason = agent_c.execute_robot_command(
        robot_operation=robot_operation,
        action="CARRY",
        zone="Corridor-A"
    )

    results.append({
        "test": "Legitimate Robot Carry to Corridor",
        "expected": "ALLOW",
        "actual": "ALLOW" if success else "BLOCK",
        "success": success,
        "reason": reason
    })
    # Test 7: Legitimate robot movement to destination
    success, reason = agent_c.execute_robot_command(
        robot_operation=robot_operation,
        action="CARRY",
        zone="Room-205"
    )

    results.append({
        "test": "Legitimate Robot Carry to Destination",
        "expected": "ALLOW",
        "actual": "ALLOW" if success else "BLOCK",
        "success": success,
        "reason": reason
    })

    # Test 8: Legitimate robot delivery
    success, reason = agent_c.execute_robot_command(
        robot_operation=robot_operation,
        action="DELIVER",
        zone="Room-205"
    )

    results.append({
        "test": "Legitimate Robot Delivery",
        "expected": "ALLOW",
        "actual": "ALLOW" if success else "BLOCK",
        "success": success,
        "reason": reason
    })

    # Calculate legitimate-request results
    total_requests = len(results)
    allowed_requests = sum(
        1 for result in results
        if result["actual"] == "ALLOW"
    )
    false_blocks = total_requests - allowed_requests

    false_block_rate = (
        (false_blocks / total_requests) * 100
        if total_requests > 0
        else 0
    )

    print("\nLEGITIMATE REQUEST RESULTS")
    print("----------------------------")

    for result in results:
        print(
            f'{result["test"]} | '
            f'Expected: {result["expected"]} | '
            f'Actual: {result["actual"]} | '
            f'Success: {result["success"]}'
        )

    print("\nLEGITIMATE REQUEST SUMMARY")
    print("----------------------------")
    print("Total Legitimate Requests:", total_requests)
    print("Correctly Allowed:", allowed_requests)
    print("False Blocks:", false_blocks)
    print(f"False-Block Rate: {false_block_rate:.2f}%")

    return results

if __name__ == "__main__":
    run_legitimate_request_suite()