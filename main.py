from gateways.robot_gateway import RobotGateway
from security.audit_logger import AuditLogger
from security.capsule_manager import CapsuleManager
from security.trusted_state import TrustedAuthorityState
from security.taf import TransitiveAuthorityFirewall
from gateways.tool_data_gateway import ToolDataGateway
from robot.robot_simulator import RobotSimulator
from tools.inventory_tool import InventoryTool
from tools.delivery_info_tool import DeliveryInfoTool
from tools.door_access_tool import DoorAccessTool
from agents.agent_a import AgentA
from agents.agent_b import AgentB
from agents.agent_c import AgentC
from experiments.normal_delivery import run_normal_delivery
from experiments.revocation_test import run_revocation_test
from security.simulated_clock import SimulatedClock
from experiments.expiration_test import run_expiration_test
from experiments.replay_version_test import run_replay_version_test
from security.capsule_registry import CapsuleRegistry
from experiments.lineage_test import run_lineage_test
from experiments.cross_task_test import run_cross_task_test
from attacks.attack_runner import AttackRunner
from attacks.destination_drift_attack import run_destination_drift_attack
from attacks.resource_drift_attack import run_resource_drift_attack
from attacks.source_drift_attack import run_source_drift_attack
from attacks.time_expansion_attack import run_time_expansion_attack
from attacks.unauthorized_delegation_attack import run_unauthorized_delegation_attack
from attacks.action_expansion_attack import run_action_expansion_attack
from attacks.data_expansion_attack import run_data_expansion_attack
from attacks.robot_expansion_attack import run_robot_expansion_attack
from attacks.fake_parent_attack import run_fake_parent_attack
from attacks.prompt_destination_attack import run_prompt_destination_attack
from attacks.prompt_zone_attack import run_prompt_zone_attack
from attacks.prompt_data_attack import run_prompt_data_attack
from attacks.prompt_tool_misuse_attack import run_prompt_tool_misuse_attack
from attacks.prompt_bypass_attack import run_prompt_bypass_attack
from attacks.forged_capsule_attack import run_forged_capsule_attack
from attacks.tampered_capsule_attack import run_tampered_capsule_attack
from attacks.expired_replay_attack import run_expired_replay_attack
from attacks.revoked_replay_attack import run_revoked_replay_attack
from attacks.old_version_replay_attack import run_old_version_replay_attack
from attacks.cross_task_capsule_attack import run_cross_task_capsule_attack
from attacks.cross_task_resource_attack import run_cross_task_resource_attack
from attacks.robot_destination_attack import run_robot_destination_attack
from attacks.robot_zone_attack import run_robot_zone_attack
from attacks.robot_after_revocation_attack import run_robot_after_revocation_attack
from security.authorization_service import AuthorizationService
from experiments.legitimate_request_suite import run_legitimate_request_suite
from experiments.experiment_context import create_experiment_context
from experiments.performance_evaluation import (
    run_performance_evaluation,
    run_repeated_performance_evaluation
)
from experiments.scalability_evaluation import (
    run_scalability_evaluation,
    run_repeated_scalability_evaluation
)
from experiments.delegation_depth_evaluation import (
    run_delegation_depth_evaluation,
    run_repeated_delegation_depth_evaluation
)
from experiments.security_cost_evaluation import (
    run_security_cost_evaluation
)


# ==========================================
# CREATE SECURITY COMPONENTS
# ==========================================

manager = CapsuleManager()
state = TrustedAuthorityState()
logger = AuditLogger()
clock = SimulatedClock("10:15")
registry = CapsuleRegistry()
attack_runner = AttackRunner()

# Register the hospital task
state.register_task("TASK-001", version=1)


# ==========================================
# CONNECT SECURITY COMPONENTS
# ==========================================

taf = TransitiveAuthorityFirewall(
    manager,
    state,
    registry,
    logger
)
authorization_service = AuthorizationService(
    capsule_manager=manager,
    taf=taf,
    capsule_registry=registry
)
gateway = ToolDataGateway(
    manager,
    state,
    logger,
    clock
)


robot_gateway = RobotGateway(
    manager,
    state,
    logger,
    clock
)


# ==========================================
# CREATE ROBOT AND TOOLS
# ==========================================

robot = RobotSimulator(
    robot_id="Robot-R1",
    starting_location="Pharmacy-A"
)
robot_gateway.register_robot(robot)

inventory_tool = InventoryTool()
delivery_info_tool = DeliveryInfoTool()
door_access_tool = DoorAccessTool()

gateway.register_tool("inventory", inventory_tool)
gateway.register_tool("door_access", door_access_tool)
gateway.register_tool("delivery_info", delivery_info_tool)
# ==========================================
# CREATE AGENTS
# ==========================================








# ==========================================
# ROOT AUTHORITY CAPSULE - DOCTOR
# ==========================================

root = manager.create_capsule(
    task_id="TASK-001",
    original_issuer="Doctor-01",
    current_holder="Doctor-01",
    parent_capsule_id=None,
    resource="Medicine-X",
    source="Pharmacy-A",
    destination="Room-205",
    purpose="MEDICINE_DELIVERY",

    allowed_actions=[
        "CHECK_INVENTORY",
        "PICK_UP",
        "CARRY",
        "DELIVER",
        "REQUEST_ACCESS",
        "READ_DELIVERY_INFO",
        "UPDATE_DELIVERY_STATUS"
    ],

    allowed_zones=[
        "Pharmacy-A",
        "Corridor-A",
        "Room-205"
    ],

    allowed_data=[
        "Inventory-Availability",
        "Delivery-Room",
        "Delivery-Status"
    ],

    authorized_robot="Robot-R1",
    valid_from="10:00",
    valid_until="10:30",
    can_delegate=True,
    version=1
)
registry.register_capsule(root)
state.register_trusted_root_principal(
    root.original_issuer
)

state.register_trusted_root_capsule(
    root.capsule_id
)
# ==========================================
# AUTHORITY CAPSULE - AGENT A
# ==========================================
issued, reason, agent_a_capsule = authorization_service.request_delegation(
    parent_capsule=root,
    current_holder="Agent-A",

    resource="Medicine-X",
    source="Pharmacy-A",
    destination="Room-205",
    purpose="MEDICINE_DELIVERY",

    allowed_actions=[
        "CHECK_INVENTORY"
    ],

    allowed_zones=[
        "Pharmacy-A"
    ],

    allowed_data=[
        "Inventory-Availability"
    ],

    authorized_robot="Robot-R1",

    valid_from="10:00",
    valid_until="10:30",

    can_delegate=False,
    version=1
)

if not issued:
    raise RuntimeError(
        f"Agent-A authority issuance failed: {reason}"
    )
agent_a = AgentA(
    agent_id="Agent-A",

    tool_data_gateway=gateway,
    authority_capsule=agent_a_capsule
)
# ==========================================
# PARENT AUTHORITY CAPSULE - AGENT B
# ==========================================
state.register_trusted_root_principal(
    root.original_issuer
)

state.register_trusted_root_capsule(
    root.capsule_id
)

issued, reason, parent = authorization_service.request_delegation(
    parent_capsule=root,
    current_holder="Agent-B",

    resource="Medicine-X",
    source="Pharmacy-A",
    destination="Room-205",
    purpose="MEDICINE_DELIVERY",

    allowed_actions=[
        "CHECK_INVENTORY",
        "PICK_UP",
        "CARRY",
        "DELIVER",
        "REQUEST_ACCESS",
        "READ_DELIVERY_INFO",
        "UPDATE_DELIVERY_STATUS"
    ],

    allowed_zones=[
        "Pharmacy-A",
        "Corridor-A",
        "Room-205"
    ],

    allowed_data=[
        "Delivery-Room",
        "Delivery-Status"
    ],

    authorized_robot="Robot-R1",

    valid_from="10:00",
    valid_until="10:30",

    can_delegate=True,
    version=1
)

if not issued:
    raise RuntimeError(
        f"Agent-B authority issuance failed: {reason}"
    )

agent_b = AgentB(
    agent_id="Agent-B",
    tool_data_gateway=gateway,
    authority_capsule=parent
)

# ==========================================
# CHILD AUTHORITY CAPSULE - AGENT C
# ==========================================

issued, reason, child = authorization_service.request_delegation(
    parent_capsule=parent,
    current_holder="Agent-C",

    resource="Medicine-X",
    source="Pharmacy-A",
    destination="Room-205",
    purpose="MEDICINE_DELIVERY",

    allowed_actions=[
        "PICK_UP",
        "CARRY",
        "DELIVER"
    ],

    allowed_zones=[
        "Pharmacy-A",
        "Corridor-A",
        "Room-205"
    ],

    allowed_data=[
        "Delivery-Room"
    ],

    authorized_robot="Robot-R1",

    valid_from="10:05",
    valid_until="10:25",

    can_delegate=False,
    version=1
)

if not issued:
    raise RuntimeError(
        f"Agent-C authority issuance failed: {reason}"
    )

agent_c = AgentC(
    agent_id="Agent-C",
    robot_gateway=robot_gateway,
    authority_capsule=child
)


# ==========================================
# REGISTER TRUSTED CAPSULES
# ==========================================

registry.register_capsule(root)
# Register trusted root authority

registry.register_capsule(agent_a_capsule)
registry.register_capsule(parent)
registry.register_capsule(child)
# ==========================================
# AGENT A AUTHORITY VALIDATION TEST
# ==========================================

print("\nAGENT A AUTHORITY VALIDATION")
print("----------------------------")

print("Root Actions:", root.allowed_actions)
print("Agent A Actions:", agent_a_capsule.allowed_actions)

agent_a_allowed, agent_a_reason = taf.validate_delegation(
    root,
    agent_a_capsule
)

print("Allowed:", agent_a_allowed)
print("Reason:", agent_a_reason)


# ==========================================
# FULL LINEAGE VALIDATION TEST
# ==========================================

lineage_allowed, lineage_reason = taf.validate_full_lineage(child)

print("\nFULL LINEAGE VALIDATION TEST")
print("----------------------------")
print("Starting Capsule:", child.capsule_id)
print("Starting Holder:", child.current_holder)
print("Allowed:", lineage_allowed)
print("Reason:", lineage_reason)


# ==========================================
# NORMAL TAF VALIDATION
# ==========================================

allowed, reason = taf.validate_delegation(
    parent,
    child
)

print("\nFULL TAF TEST")
print("----------------------------")
print("Parent Capsule:", parent.capsule_id)
print("Parent Holder:", parent.current_holder)
print("Child Capsule:", child.capsule_id)
print("Child Holder:", child.current_holder)
print("Task Status:", state.get_task_status("TASK-001"))
print("Task Version:", state.get_current_version("TASK-001"))
print("----------------------------")
print("Allowed:", allowed)
print("Reason:", reason)


# ==========================================
# ATTACK TEST - ZONE EXPANSION
# ==========================================

malicious_child = manager.create_capsule(
    task_id="TASK-001",
    original_issuer="Doctor-01",
    current_holder="Agent-C",
    parent_capsule_id=parent.capsule_id,

    resource="Medicine-X",
    source="Pharmacy-A",
    destination="Room-205",
    purpose="MEDICINE_DELIVERY",

    allowed_actions=[
        "CARRY",
        "DELIVER"
    ],

    allowed_zones=[
        "Corridor-A",
        "Room-205",
        "Restricted-Storage"
    ],

    allowed_data=[
        "Delivery-Room"
    ],

    authorized_robot="Robot-R1",

    valid_from="10:05",
    valid_until="10:25",

    can_delegate=False,
    version=1
)

attack_allowed, attack_reason = taf.validate_delegation(
    parent,
    malicious_child
)

print("\nFULL TAF ATTACK TEST")
print("----------------------------")
print("Parent Zones:", parent.allowed_zones)
print("Child Zones:", malicious_child.allowed_zones)

print(
    "Child Signature Valid:",
    manager.verify_signature(malicious_child)
)

print("----------------------------")
print("Allowed:", attack_allowed)
print("Reason:", attack_reason)


# ==========================================
# RECORD ZONE EXPANSION ATTACK
# ==========================================
attack_runner.record_result(
    attack_category="Transitive Authority Drift",
    attack_variant="Zone Expansion",
    expected_result="BLOCK",
    actual_result="ALLOW" if attack_allowed else "BLOCK",
    reason=attack_reason,
    expected_reason="ZONE_EXPANSION"
)


# ==========================================
# LOG SECURITY DECISION
# ==========================================

decision = "ALLOW" if attack_allowed else "BLOCK"

event = logger.log_event(
    task_id=malicious_child.task_id,
    actor=malicious_child.current_holder,
    decision=decision,
    reason=attack_reason,
    parent_capsule_id=parent.capsule_id,
    child_capsule_id=malicious_child.capsule_id,
    component="TAF"
)
print("\nAUDIT LOG")
print("----------------------------")
print(event)


# ==========================================
# TOOL / DATA GATEWAY TESTS
# ==========================================

print("\nTOOL/DATA GATEWAY TESTS")
print("----------------------------")

allowed, reason = gateway.authorize_request(
    child,
    requested_action="DELIVER"
)

print("TEST 1 - Allowed Action")
print("Allowed:", allowed)
print("Reason:", reason)


allowed, reason = gateway.authorize_request(
    child,
    requested_action="DELIVER",
    requested_data="Full-Medical-Record"
)

print("\nTEST 2 - Unauthorized Data Access")
print("Requested Data: Full-Medical-Record")
print("Allowed:", allowed)
print("Reason:", reason)


# ==========================================
# ROBOT GATEWAY TESTS
# ==========================================

print("\nROBOT GATEWAY TESTS")
print("----------------------------")

allowed, reason = robot_gateway.authorize_command(
    capsule=child,
    robot_id="Robot-R1",
    requested_action="CARRY",
    requested_zone="Corridor-A"
)

print("TEST 1 - Legitimate Robot Command")
print("Robot: Robot-R1")
print("Action: CARRY")
print("Zone: Corridor-A")
print("Allowed:", allowed)
print("Reason:", reason)


allowed, reason = robot_gateway.authorize_command(
    capsule=child,
    robot_id="Robot-R1",
    requested_action="CARRY",
    requested_zone="Restricted-Storage"
)

print("\nTEST 2 - Unauthorized Robot Zone")
print("Robot: Robot-R1")
print("Action: CARRY")
print("Zone: Restricted-Storage")
print("Allowed:", allowed)
print("Reason:", reason)


# ==========================================
# ROBOT SIMULATOR TEST
# ==========================================

print("\nROBOT SIMULATOR TEST")
print("----------------------------")

robot.show_status()

success, message = robot.pick_up("Medicine-X")
print("\nPick Up:", success, message)

success, message = robot.move_to("Corridor-A")
print("Move:", success, message)

success, message = robot.move_to("Room-205")
print("Move:", success, message)

success, message = robot.deliver()
print("Deliver:", success, message)

robot.show_status()


# ==========================================
# SECURE ROBOT EXECUTION TEST
# ==========================================

print("\nSECURE ROBOT EXECUTION TEST")
print("----------------------------")

secure_robot = RobotSimulator(
    robot_id="Robot-R1",
    starting_location="Pharmacy-A"
)
robot_gateway.register_robot(secure_robot)

print("Starting Location:", secure_robot.location)

success, reason = robot_gateway.execute_command(
    capsule=child,
    requested_action="CARRY",
    requested_zone="Corridor-A"
)

print("\nTEST 1 - Authorized Movement")
print("Success:", success)
print("Reason:", reason)
print("Robot Location:", secure_robot.location)


success, reason = robot_gateway.execute_command(
    capsule=child,
    requested_action="CARRY",
    requested_zone="Restricted-Storage"
)

print("\nTEST 2 - Unauthorized Movement")
print("Success:", success)
print("Reason:", reason)
print("Robot Location:", secure_robot.location)


# ==========================================
# INVENTORY TOOL TEST
# ==========================================

print("\nINVENTORY TOOL TEST")
print("----------------------------")

available, result = inventory_tool.check_inventory(
    "Pharmacy-A",
    "Medicine-X"
)

print("TEST 1 - Available Medicine")
print("Pharmacy: Pharmacy-A")
print("Medicine: Medicine-X")
print("Available:", available)
print("Quantity:", result)


available, result = inventory_tool.check_inventory(
    "Pharmacy-A",
    "Medicine-Z"
)

print("\nTEST 2 - Unavailable Medicine")
print("Pharmacy: Pharmacy-A")
print("Medicine: Medicine-Z")
print("Available:", available)
print("Result:", result)


# ==========================================
# DELIVERY INFORMATION TOOL TEST
# ==========================================

print("\nDELIVERY INFORMATION TOOL TEST")
print("----------------------------")

found, result = delivery_info_tool.get_delivery_info("TASK-001")

print("TEST 1 - Get Delivery Information")
print("Found:", found)
print("Information:", result)


found, destination = delivery_info_tool.get_destination("TASK-001")

print("\nTEST 2 - Get Destination")
print("Found:", found)
print("Destination:", destination)


success, message = delivery_info_tool.update_status(
    "TASK-001",
    "IN_PROGRESS"
)

print("\nTEST 3 - Update Status")
print("Success:", success)
print("Result:", message)

found, result = delivery_info_tool.get_delivery_info("TASK-001")

print("New Status:", result["status"])


# ==========================================
# DOOR ACCESS TOOL TEST
# ==========================================

print("\nDOOR ACCESS TOOL TEST")
print("----------------------------")

found, status = door_access_tool.get_door_status("Room-205")

print("TEST 1 - Initial Door Status")
print("Door: Room-205")
print("Status:", status)


success, message = door_access_tool.request_access("Room-205")

print("\nTEST 2 - Request Access")
print("Success:", success)
print("Result:", message)

found, status = door_access_tool.get_door_status("Room-205")

print("New Status:", status)


success, message = door_access_tool.close_door("Room-205")

print("\nTEST 3 - Close Door")
print("Success:", success)
print("Result:", message)

found, status = door_access_tool.get_door_status("Room-205")

print("Final Status:", status)


# ==========================================
# SECURE DOOR ACCESS TEST
# ==========================================

print("\nSECURE DOOR ACCESS TEST")
print("----------------------------")

door_access_tool.close_door("Room-205")
door_access_tool.close_door("Restricted-Storage")


allowed, reason = gateway.authorize_request(
    capsule=parent,
    requested_action="REQUEST_ACCESS",
    requested_zone="Room-205"
)

if allowed:
    door_success, door_reason = door_access_tool.request_access(
        "Room-205"
    )
else:
    door_success, door_reason = False, reason

print("TEST 1 - Authorized Door")
print("Zone: Room-205")
print("Security Allowed:", allowed)
print("Security Reason:", reason)
print("Door Action:", door_success, door_reason)

found, status = door_access_tool.get_door_status("Room-205")

print("Door Status:", status)


allowed, reason = gateway.authorize_request(
    capsule=parent,
    requested_action="REQUEST_ACCESS",
    requested_zone="Restricted-Storage"
)

if allowed:
    door_success, door_reason = door_access_tool.request_access(
        "Restricted-Storage"
    )
else:
    door_success, door_reason = False, reason

print("\nTEST 2 - Unauthorized Door")
print("Zone: Restricted-Storage")
print("Security Allowed:", allowed)
print("Security Reason:", reason)
print("Door Action:", door_success, door_reason)

found, status = door_access_tool.get_door_status(
    "Restricted-Storage"
)

print("Door Status:", status)


# ==========================================
# AGENT A TEST
# ==========================================

print("\nAGENT A TEST")
print("----------------------------")

success, result = agent_a.process_delivery_request(
    task_id="TASK-001",
    resource="Medicine-X",
    source="Pharmacy-A",
    destination="Room-205"
)

print("\nAgent A Success:", success)
print("Agent A Result:", result)


# ==========================================
# AGENT B TEST
# ==========================================

print("\nAGENT B TEST")
print("----------------------------")

agent_a_success, delivery_plan = agent_a.process_delivery_request(
    task_id="TASK-001",
    resource="Medicine-X",
    source="Pharmacy-A",
    destination="Room-205"
)

if agent_a_success:

    agent_b_success, logistics_task = agent_b.process_delivery_plan(
        delivery_plan
    )

    print("\nAgent B Success:", agent_b_success)
    print("Agent B Result:", logistics_task)

else:
    print("Agent A failed:", delivery_plan)

# ==========================================
# AGENT B SECURE DOOR ACCESS TEST
# ==========================================

print("\nAGENT B SECURE DOOR ACCESS TEST")
print("----------------------------")

door_success, door_reason = agent_b.request_door_access(
    task_id="TASK-001",
    resource="Medicine-X",
    destination="Room-205"
)

print("Success:", door_success)
print("Reason:", door_reason)
print(
    "Door Status:",
    door_access_tool.get_door_status("Room-205")
)
print("\nAGENT B SECURE DELIVERY INFORMATION TEST")
print("----------------------------")

info_success, info_result = agent_b.get_delivery_information(
    task_id="TASK-001",
    resource="Medicine-X"
)

print("Success:", info_success)
print("Result:", info_result)
print("\nAGENT B SECURE DELIVERY STATUS UPDATE TEST")
print("----------------------------")

status_success, status_result = agent_b.update_delivery_status(
    task_id="TASK-001",
    resource="Medicine-X",
    new_status="IN_PROGRESS"
)

print("Success:", status_success)
print("Result:", status_result)
print(
    "New Delivery Status:",
    delivery_info_tool.deliveries["TASK-001"]["status"]
)
# ==========================================
# AGENT C TEST
# ==========================================

print("\nAGENT C TEST")
print("----------------------------")

agent_a_success, delivery_plan = agent_a.process_delivery_request(
    task_id="TASK-001",
    resource="Medicine-X",
    source="Pharmacy-A",
    destination="Room-205"
)

if agent_a_success:

    agent_b_success, logistics_task = agent_b.process_delivery_plan(
        delivery_plan
    )

    if agent_b_success:

        agent_c_success, robot_operation = agent_c.prepare_robot_operation(
            logistics_task
        )

        print("\nAgent C Success:", agent_c_success)
        print("Agent C Result:", robot_operation)

    else:
        print("Agent B failed:", logistics_task)

else:
    print("Agent A failed:", delivery_plan)

# ==========================================
# AGENT C SECURE ROBOT EXECUTION TEST
# ==========================================

print("\nAGENT C SECURE ROBOT EXECUTION TEST")
print("----------------------------")

# Reset robot for a clean test
robot.location = "Pharmacy-A"
robot.carrying = None
robot.status = "IDLE"

if agent_c_success:

    command_success, command_reason = agent_c.execute_robot_command(
        robot_operation=robot_operation,
        action="PICK_UP",
        zone="Pharmacy-A"
    )

    print("Success:", command_success)
    print("Reason:", command_reason)
    print("Robot Location:", robot.location)
    print(
        "Robot Carrying:",
        robot_gateway.get_robot("Robot-R1").carrying
    )

else:
    print("Agent C preparation failed:", robot_operation)

# ==========================================
# AGENT C UNAUTHORIZED ZONE TEST
# ==========================================

print("\nAGENT C UNAUTHORIZED ZONE TEST")
print("----------------------------")

# Reset robot to an authorized starting location
robot.location = "Pharmacy-A"
robot.carrying = "Medicine-X"
robot.status = "CARRYING"

print("Starting Location:", robot.location)
print("Attempted Zone: Restricted-Storage")

blocked_success, blocked_reason = agent_c.execute_robot_command(
    robot_operation=robot_operation,
    action="CARRY",
    zone="Restricted-Storage"
)

print("Success:", blocked_success)
print("Reason:", blocked_reason)
print("Robot Location After Attempt:", robot.location)
print("Robot Status:", robot.status)
# ==========================================
# SECURE END-TO-END DELIVERY TEST
# ==========================================

print("\nSECURE END-TO-END DELIVERY TEST")
print("----------------------------")

delivery_robot = RobotSimulator(
    robot_id="Robot-R1",
    starting_location="Pharmacy-A"
)
robot_gateway.register_robot(delivery_robot)

print("Starting Location:", delivery_robot.location)
print("Starting Cargo:", delivery_robot.carrying)


success, reason = robot_gateway.execute_command(
    capsule=child,
    requested_action="PICK_UP",
    requested_zone="Pharmacy-A"
)

print("\nSTEP 1 - PICK UP")
print("Success:", success)
print("Reason:", reason)
print("Robot Carrying:", delivery_robot.carrying)


success, reason = robot_gateway.execute_command(
    capsule=child,
    requested_action="CARRY",
    requested_zone="Corridor-A"
)

print("\nSTEP 2 - MOVE TO CORRIDOR")
print("Success:", success)
print("Reason:", reason)
print("Robot Location:", delivery_robot.location)


success, reason = robot_gateway.execute_command(
    capsule=child,
    requested_action="CARRY",
    requested_zone="Room-205"
)

print("\nSTEP 3 - MOVE TO DESTINATION")
print("Success:", success)
print("Reason:", reason)
print("Robot Location:", delivery_robot.location)


success, reason = robot_gateway.execute_command(
    capsule=child,
    requested_action="DELIVER",
    requested_zone="Room-205"
)

print("\nSTEP 4 - DELIVER")
print("Success:", success)
print("Reason:", reason)
print("Robot Carrying:", delivery_robot.carrying)
print("Final Location:", delivery_robot.location)


# ==========================================
# NORMAL DELIVERY EXPERIMENT
# ==========================================

print("\nNORMAL DELIVERY WORKFLOW TEST")
print("----------------------------")

normal_delivery_robot = RobotSimulator(
    robot_id="Robot-R1",
    starting_location="Pharmacy-A"
)
robot_gateway.register_robot(normal_delivery_robot)

success, result = run_normal_delivery(
    agent_a=agent_a,
    agent_b=agent_b,
    agent_c=agent_c,
    taf=taf,
    parent_capsule=parent,
    child_capsule=child,
    robot_gateway=robot_gateway


)

print("\nExperiment Success:", success)
print("Experiment Result:", result)
print("Final Robot Location:", normal_delivery_robot.location)
print("Final Robot Cargo:", normal_delivery_robot.carrying)

found, delivery_record = delivery_info_tool.get_delivery_info(
    "TASK-001"
)

print("Final Delivery Status:", delivery_record["status"])


# ==========================================
# MALICIOUS DELEGATION WORKFLOW TEST
# ==========================================

print("\nMALICIOUS DELEGATION WORKFLOW TEST")
print("----------------------------")

attack_robot = RobotSimulator(
    robot_id="Robot-R1",
    starting_location="Pharmacy-A"
)
robot_gateway.register_robot(attack_robot)
success, result = run_normal_delivery(
    agent_a=agent_a,
    agent_b=agent_b,
    agent_c=agent_c,
    taf=taf,
    parent_capsule=parent,
    child_capsule=malicious_child,
    robot_gateway=robot_gateway


)

print("\nAttack Workflow Success:", success)
print("Attack Workflow Result:", result)
print("Robot Location:", attack_robot.location)
print("Robot Cargo:", attack_robot.carrying)


# ==========================================
# REVOCATION EXPERIMENT
# ==========================================

print("\nREVOCATION WORKFLOW TEST")
print("----------------------------")

state.register_task("TASK-001", version=1)

revocation_robot = RobotSimulator(
    robot_id="Robot-R1",
    starting_location="Pharmacy-A"
)
robot_gateway.register_robot(revocation_robot)

(
    success,
    result,
    final_task_status,
    final_robot_status,
    final_robot_location,
    final_robot_cargo
) = run_revocation_test()

print("\nRevocation Test Success:", success)
print("Revocation Test Result:", result)
print("Final Task Status:", final_task_status)
print("Final Robot Status:", final_robot_status)
print("Final Robot Location:", final_robot_location)
print("Final Robot Cargo:", final_robot_cargo)


# ==========================================
# CAPSULE EXPIRATION EXPERIMENT
# ==========================================

print("\nCAPSULE EXPIRATION WORKFLOW TEST")
print("----------------------------")

expiration_robot = RobotSimulator(
    robot_id="Robot-R1",
    starting_location="Pharmacy-A"
)
robot_gateway.register_robot(expiration_robot)

success, result = run_expiration_test()

print("\nExpiration Test Success:", success)
print("Expiration Test Result:", result)
print("Final Robot Location:", expiration_robot.location)
print("Final Robot Cargo:", expiration_robot.carrying)
print("Restored Simulated Time:", clock.get_time())


# ==========================================
# STALE VERSION / REPLAY EXPERIMENT
# ==========================================

print("\nSTALE VERSION / REPLAY WORKFLOW TEST")
print("----------------------------")

replay_robot = RobotSimulator(
    robot_id="Robot-R1",
    starting_location="Pharmacy-A"
)
robot_gateway.register_robot(replay_robot)

success, result, final_task_version = run_replay_version_test()

print("\nReplay Test Success:", success)
print("Replay Test Result:", result)
print(
    "Final Task Version:",
    final_task_version
)
print("Old Capsule Version:", child.version)
print("Final Robot Location:", replay_robot.location)
print("Final Robot Cargo:", replay_robot.carrying)


# ==========================================
# AUTHORITY LINEAGE EXPERIMENT
# ==========================================

print("\nAUTHORITY LINEAGE WORKFLOW TEST")
print("----------------------------")

success, result = run_lineage_test(
    taf=taf,
    manager=manager,
    trusted_state=state
)

print("\nLineage Test Success:", success)
print("Lineage Test Result:", result)


# ==========================================
# CROSS-TASK AUTHORITY MISUSE EXPERIMENT
# ==========================================

print("\nCROSS-TASK AUTHORITY MISUSE WORKFLOW TEST")
print("----------------------------")

cross_task_robot = RobotSimulator(
    robot_id="Robot-R1",
    starting_location="Pharmacy-A"
)
robot_gateway.register_robot(cross_task_robot)

cross_task_success, cross_task_result = run_cross_task_test(
    robot_gateway=robot_gateway,
    robot=cross_task_robot,
    capsule=child,
    trusted_state=state,
    clock=clock
)

print("\nCross-Task Test Success:", cross_task_success)
print("Cross-Task Test Result:", cross_task_result)
print("Final Robot Location:", cross_task_robot.location)
print("Final Robot Cargo:", cross_task_robot.carrying)


# ==========================================
# DESTINATION DRIFT ATTACK
# ==========================================

run_destination_drift_attack(
    attack_runner=attack_runner
)


# ==========================================
# RESOURCE DRIFT ATTACK
# ==========================================

run_resource_drift_attack(
    attack_runner=attack_runner
)

# ==========================================
# SOURCE DRIFT ATTACK
# ==========================================

run_source_drift_attack(
    attack_runner=attack_runner
)
# ==========================================
# AUTOMATED ATTACK RUNNER RESULTS
# ==========================================
# ==========================================
# TIME EXPANSION ATTACK
# ==========================================

run_time_expansion_attack(
    attack_runner=attack_runner
)

# ==========================================
# UNAUTHORIZED DELEGATION ATTACK
# ==========================================

run_unauthorized_delegation_attack(
    attack_runner=attack_runner
)

# ==========================================
# ACTION EXPANSION ATTACK
# ==========================================

run_action_expansion_attack(
    attack_runner=attack_runner
)
# ==========================================
# DATA EXPANSION ATTACK
# ==========================================

run_data_expansion_attack(
    attack_runner=attack_runner
)

# ==========================================
# ROBOT EXPANSION ATTACK
# ==========================================

run_robot_expansion_attack(
    attack_runner=attack_runner
)

# ==========================================
# FAKE PARENT AUTHORITY ATTACK
# ==========================================

run_fake_parent_attack(
    attack_runner=attack_runner
)

# ==========================================
# PROMPT INJECTION - DESTINATION MANIPULATION
# ==========================================

run_prompt_destination_attack(
    attack_runner=attack_runner
)

# ==========================================
# PROMPT INJECTION - ZONE MANIPULATION
# ==========================================

run_prompt_zone_attack(
    attack_runner=attack_runner
)


# ==========================================
# PROMPT INJECTION - DATA MANIPULATION
# ==========================================

run_prompt_data_attack(
    attack_runner=attack_runner
)
# ==========================================
# PROMPT INJECTION - TOOL MISUSE
# ==========================================

run_prompt_tool_misuse_attack(
    attack_runner=attack_runner
)


# ==========================================
# PROMPT INJECTION - SECURITY BYPASS
# ==========================================

run_prompt_bypass_attack(
    attack_runner=attack_runner
)

# ==========================================
# FORGED CAPSULE ATTACK
# ==========================================

forged_allowed, forged_reason = (
    run_forged_capsule_attack(
        attack_runner=attack_runner
    )
)


# ==========================================
# TAMPERED CAPSULE ATTACK
# ==========================================

tampered_allowed, tampered_reason = (
    run_tampered_capsule_attack(
        attack_runner=attack_runner
    )
)


# ==========================================
# EXPIRED CAPSULE REPLAY ATTACK
# ==========================================

expired_replay_allowed, expired_replay_reason = (
    run_expired_replay_attack(
        attack_runner=attack_runner
    )
)


# ==========================================
# REVOKED CAPSULE REPLAY ATTACK
# ==========================================

revoked_replay_allowed, revoked_replay_reason = (
    run_revoked_replay_attack(
        attack_runner=attack_runner
    )
)


# ==========================================
# OLD-VERSION CAPSULE REPLAY ATTACK
# ==========================================

old_version_allowed, old_version_reason = (
    run_old_version_replay_attack(
        attack_runner=attack_runner
    )
)

# ==========================================
# CROSS-TASK CAPSULE MISUSE
# ==========================================

run_cross_task_capsule_attack(
    attack_runner=attack_runner
)


# ==========================================
# CROSS-TASK RESOURCE MISUSE
# ==========================================

cross_task_resource_allowed, cross_task_resource_reason = (
    run_cross_task_resource_attack(
        attack_runner=attack_runner
    )
)


# ==========================================
# ROBOT DESTINATION MANIPULATION
# ==========================================

robot_destination_allowed, robot_destination_reason = (
    run_robot_destination_attack(
        attack_runner=attack_runner
    )
)


# ==========================================
# ROBOT RESTRICTED ZONE
# ==========================================

robot_zone_allowed, robot_zone_reason = (
    run_robot_zone_attack(
        attack_runner=attack_runner
    )
)


# ==========================================
# ROBOT CONTINUES AFTER REVOCATION
# ==========================================

robot_after_revocation_allowed, robot_after_revocation_reason = (
    run_robot_after_revocation_attack(
        attack_runner=attack_runner
    )
)

# ==========================================
# SECURE AUTHORITY ISSUANCE TEST
# ==========================================

print("\nSECURE AUTHORITY ISSUANCE TEST")
print("----------------------------")
# Create a completely isolated experiment environment
issuance_context = create_experiment_context()

authorization_service = issuance_context["authorization_service"]
parent = issuance_context["parent"]
manager = issuance_context["manager"]
registry = issuance_context["registry"]


# ==========================================
# TEST 1 - LEGITIMATE AUTHORITY REQUEST
# ==========================================

issued, issuance_reason, secure_capsule = (
    authorization_service.request_delegation(
        parent_capsule=parent,
        current_holder="Agent-C-Secure",

        resource=parent.resource,
        source=parent.source,
        destination=parent.destination,
        purpose=parent.purpose,

        allowed_actions=[
            "CARRY",
            "DELIVER"
        ],

        allowed_zones=[
            "Corridor-A",
            "Room-205"
        ],

        allowed_data=[
            "Delivery-Room"
        ],

        authorized_robot=parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=parent.version
    )
)

print("\nTEST 1 - LEGITIMATE REQUEST")
print("Issued:", issued)
print("Reason:", issuance_reason)

if secure_capsule is not None:
    print("Capsule ID:", secure_capsule.capsule_id)

    print(
        "Signature Valid:",
        manager.verify_signature(secure_capsule)
    )

    print(
        "Registered:",
        registry.capsule_exists(
            secure_capsule.capsule_id
        )
    )


# ==========================================
# TEST 2 - MALICIOUS AUTHORITY REQUEST
# ==========================================

issued_attack, issuance_attack_reason, rejected_capsule = (
    authorization_service.request_delegation(
        parent_capsule=parent,
        current_holder="Agent-C-Malicious",

        resource=parent.resource,
        source=parent.source,
        destination=parent.destination,
        purpose=parent.purpose,

        allowed_actions=[
            "CARRY",
            "DELIVER"
        ],

        allowed_zones=[
            "Corridor-A",
            "Room-205",
            "Restricted-Storage"
        ],

        allowed_data=[
            "Delivery-Room"
        ],

        authorized_robot=parent.authorized_robot,

        valid_from="10:05",
        valid_until="10:25",

        can_delegate=False,
        version=parent.version
    )
)

print("\nTEST 2 - MALICIOUS REQUEST")
print("Attempted Extra Zone: Restricted-Storage")
print("Issued:", issued_attack)
print("Reason:", issuance_attack_reason)
print("Returned Capsule:", rejected_capsule)


# ==========================================
# TRUSTED ROOT AUTHORITY ATTACK TEST
# ==========================================

print("\nTRUSTED ROOT AUTHORITY ATTACK TEST")
print("----------------------------------")

# Create a fake root authority.
# The attacker uses the same identity as issuer and holder,
# and the capsule has a valid cryptographic signature.
fake_root = manager.create_capsule(
    task_id="TASK-001",
    original_issuer="Fake-Doctor",
    current_holder="Fake-Doctor",
    parent_capsule_id=None,
    resource="Medicine-X",
    source="Pharmacy-A",
    destination="Room-205",
    purpose="MEDICINE_DELIVERY",
    allowed_actions=[
        "PICK_UP",
        "CARRY",
        "DELIVER",
        "REQUEST_ACCESS"
    ],
    allowed_zones=[
        "Pharmacy-A",
        "Corridor-A",
        "Room-205"
    ],
    allowed_data=[
        "Delivery-Room",
        "Delivery-Status"
    ],
    authorized_robot="Robot-R1",
    valid_from="10:00",
    valid_until="10:30",
    can_delegate=True,
    version=1
)

# Register the capsule so the test does not fail merely
# because the capsule is missing from the registry.
registry.register_capsule(fake_root)

print("Fake Root ID:", fake_root.capsule_id)
print("Fake Root Issuer:", fake_root.original_issuer)
print(
    "Signature Valid:",
    manager.verify_signature(fake_root)
)
print(
    "Capsule Registered:",
    registry.capsule_exists(fake_root.capsule_id)
)
print(
    "Trusted Principal:",
    state.is_trusted_root_principal(
        fake_root.original_issuer
    )
)
print(
    "Trusted Root Capsule:",
    state.is_trusted_root_capsule(
        fake_root.capsule_id
    )
)

fake_root_allowed, fake_root_reason = (
    taf.validate_full_lineage(fake_root)
)

print("Allowed:", fake_root_allowed)
print("Reason:", fake_root_reason)

# ==========================================
# ROBOT GATEWAY BINDING TESTS
# ==========================================

print("\nROBOT GATEWAY BINDING TESTS")
print("----------------------------")

# Make sure the task is active and the correct
# version is being used for these tests.
# Create a completely isolated experiment environment
binding_context = create_experiment_context()

robot_gateway = binding_context["robot_gateway"]
child = binding_context["child"]
clock = binding_context["clock"]

clock.set_time("10:15")


# TEST 1 - WRONG RESOURCE
allowed_resource, reason_resource = (
    robot_gateway.authorize_command(
        capsule=child,
        robot_id=child.authorized_robot,
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=child.task_id,
        requested_resource="Medicine-Y",
        requested_destination=child.destination,
        requested_purpose=child.purpose
    )
)

print("\nTEST 1 - WRONG RESOURCE")
print("Authorized Resource:", child.resource)
print("Requested Resource: Medicine-Y")
print("Allowed:", allowed_resource)
print("Reason:", reason_resource)


# TEST 2 - WRONG PURPOSE
allowed_purpose, reason_purpose = (
    robot_gateway.authorize_command(
        capsule=child,
        robot_id=child.authorized_robot,
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=child.task_id,
        requested_resource=child.resource,
        requested_destination=child.destination,
        requested_purpose="UNAUTHORIZED_PURPOSE"
    )
)

print("\nTEST 2 - WRONG PURPOSE")
print("Authorized Purpose:", child.purpose)
print("Requested Purpose: UNAUTHORIZED_PURPOSE")
print("Allowed:", allowed_purpose)
print("Reason:", reason_purpose)


# TEST 3 - WRONG DESTINATION
allowed_destination, reason_destination = (
    robot_gateway.authorize_command(
        capsule=child,
        robot_id=child.authorized_robot,
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=child.task_id,
        requested_resource=child.resource,
        requested_destination="Room-305",
        requested_purpose=child.purpose
    )
)

print("\nTEST 3 - WRONG DESTINATION")
print("Authorized Destination:", child.destination)
print("Requested Destination: Room-305")
print("Allowed:", allowed_destination)
print("Reason:", reason_destination)

# TEST 4 - WRONG ROBOT
allowed_robot, reason_robot = (
    robot_gateway.authorize_command(
        capsule=child,
        robot_id="Robot-R2",
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=child.task_id,
        requested_resource=child.resource,
        requested_destination=child.destination,
        requested_purpose=child.purpose
    )
)

print("\nTEST 4 - WRONG ROBOT")
print("Authorized Robot:", child.authorized_robot)
print("Requested Robot: Robot-R2")
print("Allowed:", allowed_robot)
print("Reason:", reason_robot)
# ==========================================
# TOOL/DATA GATEWAY BINDING TESTS
# ==========================================

print("\nTOOL/DATA GATEWAY BINDING TESTS")
print("--------------------------------")

# Make sure TASK-001 is active and using
# the correct version for these tests.
# Create a completely isolated experiment environment
tool_binding_context = create_experiment_context()

gateway = tool_binding_context["gateway"]
parent = tool_binding_context["parent"]
clock = tool_binding_context["clock"]

clock.set_time("10:15")


# TEST 1 - WRONG TASK
allowed_task, reason_task = gateway.authorize_request(
    capsule=parent,
    requested_action="REQUEST_ACCESS",
    requested_zone="Room-205",
    requested_task_id="TASK-002",
    requested_resource=parent.resource,
    requested_purpose=parent.purpose
)

print("\nTEST 1 - WRONG TASK")
print("Authorized Task:", parent.task_id)
print("Requested Task: TASK-002")
print("Allowed:", allowed_task)
print("Reason:", reason_task)


# TEST 2 - WRONG RESOURCE
allowed_resource_tool, reason_resource_tool = (
    gateway.authorize_request(
        capsule=parent,
        requested_action="REQUEST_ACCESS",
        requested_zone="Room-205",
        requested_task_id=parent.task_id,
        requested_resource="Medicine-Y",
        requested_purpose=parent.purpose
    )
)

print("\nTEST 2 - WRONG RESOURCE")
print("Authorized Resource:", parent.resource)
print("Requested Resource: Medicine-Y")
print("Allowed:", allowed_resource_tool)
print("Reason:", reason_resource_tool)


# TEST 3 - WRONG PURPOSE
allowed_purpose_tool, reason_purpose_tool = (
    gateway.authorize_request(
        capsule=parent,
        requested_action="REQUEST_ACCESS",
        requested_zone="Room-205",
        requested_task_id=parent.task_id,
        requested_resource=parent.resource,
        requested_purpose="UNAUTHORIZED_PURPOSE"
    )
)

print("\nTEST 3 - WRONG PURPOSE")
print("Authorized Purpose:", parent.purpose)
print("Requested Purpose: UNAUTHORIZED_PURPOSE")
print("Allowed:", allowed_purpose_tool)
print("Reason:", reason_purpose_tool)

print("\nAUTOMATED LEGITIMATE REQUEST TESTING")
print("------------------------------------")

legitimate_results = run_legitimate_request_suite()

print("\nAUTOMATED ATTACK RUNNER")
print("----------------------------")

attack_runner.show_results()

summary = attack_runner.get_summary()

print("\nATTACK SUMMARY")
print("----------------------------")
print("Total Attacks:", summary["total_attacks"])
print("Blocked Attacks:", summary["blocked_attacks"])
print("Allowed Attacks:", summary["allowed_attacks"])
print("Successful Tests:", summary["successful_tests"])
print("Failed Tests:", summary["failed_tests"])
print(
    "Blocking Rate:",
    f'{summary["blocking_rate"]:.2f}%'
)
print(
    "Exact Test Success Rate:",
    f'{summary["exact_test_success_rate"]:.2f}%'
)


print("\nAUTHORIZATION PERFORMANCE EVALUATION")
print("------------------------------------")

run_performance_evaluation(
    iterations=1000
)
run_repeated_performance_evaluation(
    batches=10,
    iterations=1000
)
run_scalability_evaluation()
run_delegation_depth_evaluation(
    iterations=1000
)
run_repeated_delegation_depth_evaluation(
    batches=10,
    iterations=1000
)
run_repeated_scalability_evaluation(
    batches=10
)
run_security_cost_evaluation(
    iterations=1000
)