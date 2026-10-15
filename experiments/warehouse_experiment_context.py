from security.capsule_manager import CapsuleManager
from security.trusted_state import TrustedAuthorityState
from security.audit_logger import AuditLogger
from security.capsule_registry import CapsuleRegistry
from security.taf import TransitiveAuthorityFirewall
from security.authorization_service import AuthorizationService
from security.simulated_clock import SimulatedClock

from gateways.tool_data_gateway import ToolDataGateway
from gateways.robot_gateway import RobotGateway

from robot.robot_simulator import RobotSimulator

from tools.inventory_tool import InventoryTool
from tools.delivery_info_tool import DeliveryInfoTool
from tools.door_access_tool import DoorAccessTool

from agents.agent_a import AgentA
from agents.agent_b import AgentB
from agents.agent_c import AgentC

def create_warehouse_experiment_context():

    manager = CapsuleManager()
    state = TrustedAuthorityState()
    logger = AuditLogger()
    clock = SimulatedClock("14:15")
    registry = CapsuleRegistry()

    state.register_task(
        task_id="WAREHOUSE-TASK-001",
        version=1
    )

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

    robot = RobotSimulator(
        robot_id="Warehouse-R1",
        starting_location="Storage-A"
    )

    robot_gateway.register_robot(robot)

    inventory_tool = InventoryTool()
    delivery_info_tool = DeliveryInfoTool()
    door_access_tool = DoorAccessTool()

    gateway.register_tool(
        "inventory",
        inventory_tool
    )

    gateway.register_tool(
        "door_access",
        door_access_tool
    )

    gateway.register_tool(
        "delivery_info",
        delivery_info_tool
    )

    root = manager.create_capsule(
        task_id="WAREHOUSE-TASK-001",
        original_issuer="Warehouse-Manager-01",
        current_holder="Warehouse-Manager-01",
        parent_capsule_id=None,
        resource="Package-X",
        source="Storage-A",
        destination="Loading-Bay-2",
        purpose="PACKAGE_TRANSFER",

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
            "Storage-A",
            "Warehouse-Corridor",
            "Loading-Bay-2"
        ],

        allowed_data=[
            "Inventory-Availability",
            "Delivery-Room",
            "Delivery-Status"
        ],

        authorized_robot="Warehouse-R1",
        valid_from="14:00",
        valid_until="14:30",
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

    issued, reason, agent_a_capsule = (
        authorization_service.request_delegation(
            parent_capsule=root,
            current_holder="Agent-A",
            resource="Package-X",
            source="Storage-A",
            destination="Loading-Bay-2",
            purpose="PACKAGE_TRANSFER",

            allowed_actions=[
                "CHECK_INVENTORY"
            ],

            allowed_zones=[
                "Storage-A"
            ],

            allowed_data=[
                "Inventory-Availability"
            ],

            authorized_robot="Warehouse-R1",
            valid_from="14:00",
            valid_until="14:30",
            can_delegate=False,
            version=1
        )
    )

    if not issued:
        raise RuntimeError(
            f"Warehouse Agent-A authority issuance failed: {reason}"
        )

    agent_a = AgentA(
        agent_id="Agent-A",
        tool_data_gateway=gateway,
        authority_capsule=agent_a_capsule
    )

    issued, reason, parent = (
        authorization_service.request_delegation(
            parent_capsule=root,
            current_holder="Agent-B",
            resource="Package-X",
            source="Storage-A",
            destination="Loading-Bay-2",
            purpose="PACKAGE_TRANSFER",

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
                "Storage-A",
                "Warehouse-Corridor",
                "Loading-Bay-2"
            ],

            allowed_data=[
                "Delivery-Room",
                "Delivery-Status"
            ],

            authorized_robot="Warehouse-R1",
            valid_from="14:00",
            valid_until="14:30",
            can_delegate=True,
            version=1
        )
    )

    if not issued:
        raise RuntimeError(
            f"Warehouse Agent-B authority issuance failed: {reason}"
        )

    agent_b = AgentB(
        agent_id="Agent-B",
        tool_data_gateway=gateway,
        authority_capsule=parent
    )

    issued, reason, child = (
        authorization_service.request_delegation(
            parent_capsule=parent,
            current_holder="Agent-C",
            resource="Package-X",
            source="Storage-A",
            destination="Loading-Bay-2",
            purpose="PACKAGE_TRANSFER",

            allowed_actions=[
                "PICK_UP",
                "CARRY",
                "DELIVER"
            ],

            allowed_zones=[
                "Storage-A",
                "Warehouse-Corridor",
                "Loading-Bay-2"
            ],

            allowed_data=[
                "Delivery-Room"
            ],

            authorized_robot="Warehouse-R1",
            valid_from="14:05",
            valid_until="14:25",
            can_delegate=False,
            version=1
        )
    )

    if not issued:
        raise RuntimeError(
            f"Warehouse Agent-C authority issuance failed: {reason}"
        )

    agent_c = AgentC(
        agent_id="Agent-C",
        robot_gateway=robot_gateway,
        authority_capsule=child
    )

    return {
        "manager": manager,
        "state": state,
        "logger": logger,
        "clock": clock,
        "registry": registry,
        "taf": taf,
        "authorization_service": authorization_service,
        "gateway": gateway,
        "robot_gateway": robot_gateway,
        "robot": robot,
        "inventory_tool": inventory_tool,
        "delivery_info_tool": delivery_info_tool,
        "door_access_tool": door_access_tool,
        "root": root,
        "agent_a_capsule": agent_a_capsule,
        "parent": parent,
        "child": child,
        "agent_a": agent_a,
        "agent_b": agent_b,
        "agent_c": agent_c
    }


if __name__ == "__main__":
    context = create_warehouse_experiment_context()

    print("\nWAREHOUSE EXPERIMENT CONTEXT")
    print("----------------------------")
    print(
        "Task Status:",
        context["state"].get_task_status("WAREHOUSE-TASK-001")
    )
    print(
        "Task Version:",
        context["state"].get_current_version("WAREHOUSE-TASK-001")
    )
    print("Root:", context["root"].current_holder)
    print("Agent A:", context["agent_a"].agent_id)
    print("Agent B:", context["agent_b"].agent_id)
    print("Agent C:", context["agent_c"].agent_id)
    print("Robot:", context["robot"].robot_id)
    print("Resource:", context["root"].resource)
    print("Source:", context["root"].source)
    print("Destination:", context["root"].destination)
    print("Purpose:", context["root"].purpose)