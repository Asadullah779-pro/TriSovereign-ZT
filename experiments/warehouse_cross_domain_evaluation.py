import csv
import os

from experiments.warehouse_experiment_context import (
    create_warehouse_experiment_context
)


def run_warehouse_legitimate_test():

    context = create_warehouse_experiment_context()

    robot_gateway = context["robot_gateway"]
    robot = context["robot"]
    child = context["child"]

    print("\nWAREHOUSE LEGITIMATE OPERATION")
    print("------------------------------")

    success, reason = robot_gateway.execute_command(
        capsule=child,
        requested_action="CARRY",
        requested_zone="Warehouse-Corridor",
        requested_task_id="WAREHOUSE-TASK-001",
        requested_resource="Package-X",
        requested_purpose="PACKAGE_TRANSFER",
        requested_destination="Loading-Bay-2"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    assert success is True, (
        f"Expected legitimate warehouse operation to be allowed, "
        f"but received: {reason}"
    )

    assert reason == "ROBOT_MOVED", (
        f"Expected ROBOT_MOVED, but received: {reason}"
    )

    return success, reason


def run_warehouse_zone_attack():

    context = create_warehouse_experiment_context()

    robot_gateway = context["robot_gateway"]
    child = context["child"]

    print("\nWAREHOUSE UNAUTHORIZED ZONE ATTACK")
    print("----------------------------------")

    success, reason = robot_gateway.execute_command(
        capsule=child,
        requested_action="CARRY",
        requested_zone="Restricted-Storage",
        requested_task_id="WAREHOUSE-TASK-001",
        requested_resource="Package-X",
        requested_purpose="PACKAGE_TRANSFER",
        requested_destination="Loading-Bay-2"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    assert success is False, (
        f"Expected unauthorized warehouse zone to be blocked, "
        f"but received: {reason}"
    )

    assert reason == "ROBOT_ZONE_NOT_ALLOWED", (
        f"Expected ROBOT_ZONE_NOT_ALLOWED, but received: {reason}"
    )

    return success, reason


def run_warehouse_destination_attack():

    context = create_warehouse_experiment_context()

    robot_gateway = context["robot_gateway"]
    child = context["child"]

    print("\nWAREHOUSE DESTINATION MANIPULATION ATTACK")
    print("-----------------------------------------")

    success, reason = robot_gateway.execute_command(
        capsule=child,
        requested_action="CARRY",
        requested_zone="Warehouse-Corridor",
        requested_task_id="WAREHOUSE-TASK-001",
        requested_resource="Package-X",
        requested_purpose="PACKAGE_TRANSFER",
        requested_destination="Loading-Bay-9"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    assert success is False, (
        f"Expected destination manipulation to be blocked, "
        f"but received: {reason}"
    )

    assert reason == "DESTINATION_MISMATCH", (
        f"Expected DESTINATION_MISMATCH, but received: {reason}"
    )

    return success, reason


def run_warehouse_resource_attack():

    context = create_warehouse_experiment_context()

    robot_gateway = context["robot_gateway"]
    child = context["child"]

    print("\nWAREHOUSE RESOURCE MANIPULATION ATTACK")
    print("--------------------------------------")

    success, reason = robot_gateway.execute_command(
        capsule=child,
        requested_action="CARRY",
        requested_zone="Warehouse-Corridor",
        requested_task_id="WAREHOUSE-TASK-001",
        requested_resource="Package-Y",
        requested_purpose="PACKAGE_TRANSFER",
        requested_destination="Loading-Bay-2"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    assert success is False, (
        f"Expected resource manipulation to be blocked, "
        f"but received: {reason}"
    )

    assert reason == "RESOURCE_MISMATCH", (
        f"Expected RESOURCE_MISMATCH, but received: {reason}"
    )

    return success, reason


def run_warehouse_purpose_attack():

    context = create_warehouse_experiment_context()

    robot_gateway = context["robot_gateway"]
    child = context["child"]

    print("\nWAREHOUSE PURPOSE MANIPULATION ATTACK")
    print("-------------------------------------")

    success, reason = robot_gateway.execute_command(
        capsule=child,
        requested_action="CARRY",
        requested_zone="Warehouse-Corridor",
        requested_task_id="WAREHOUSE-TASK-001",
        requested_resource="Package-X",
        requested_purpose="PACKAGE_DISPOSAL",
        requested_destination="Loading-Bay-2"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    assert success is False, (
        f"Expected purpose manipulation to be blocked, "
        f"but received: {reason}"
    )

    assert reason == "PURPOSE_MISMATCH", (
        f"Expected PURPOSE_MISMATCH, but received: {reason}"
    )

    return success, reason


def run_warehouse_cross_task_attack():

    context = create_warehouse_experiment_context()

    robot_gateway = context["robot_gateway"]
    child = context["child"]

    print("\nWAREHOUSE CROSS-TASK AUTHORITY ATTACK")
    print("-------------------------------------")

    success, reason = robot_gateway.execute_command(
        capsule=child,
        requested_action="CARRY",
        requested_zone="Warehouse-Corridor",
        requested_task_id="WAREHOUSE-TASK-999",
        requested_resource="Package-X",
        requested_purpose="PACKAGE_TRANSFER",
        requested_destination="Loading-Bay-2"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    assert success is False, (
        f"Expected cross-task authority misuse to be blocked, "
        f"but received: {reason}"
    )

    assert reason == "CROSS_TASK_AUTHORITY_MISUSE", (
        f"Expected CROSS_TASK_AUTHORITY_MISUSE, but received: {reason}"
    )

    return success, reason


def run_warehouse_revocation_test():

    context = create_warehouse_experiment_context()

    robot_gateway = context["robot_gateway"]
    state = context["state"]
    child = context["child"]

    print("\nWAREHOUSE TASK REVOCATION TEST")
    print("------------------------------")

    state.revoke_task("WAREHOUSE-TASK-001")

    success, reason = robot_gateway.execute_command(
        capsule=child,
        requested_action="CARRY",
        requested_zone="Warehouse-Corridor",
        requested_task_id="WAREHOUSE-TASK-001",
        requested_resource="Package-X",
        requested_purpose="PACKAGE_TRANSFER",
        requested_destination="Loading-Bay-2"
    )

    print(
        "Task Status:",
        state.get_task_status("WAREHOUSE-TASK-001")
    )
    print("Allowed:", success)
    print("Reason:", reason)

    assert success is False, (
        f"Expected revoked warehouse task to be blocked, "
        f"but received: {reason}"
    )

    assert reason == "TASK_NOT_ACTIVE", (
        f"Expected TASK_NOT_ACTIVE, but received: {reason}"
    )

    return success, reason


def run_warehouse_stale_version_test():

    context = create_warehouse_experiment_context()

    robot_gateway = context["robot_gateway"]
    state = context["state"]
    child = context["child"]

    print("\nWAREHOUSE STALE VERSION TEST")
    print("----------------------------")

    state.update_version("WAREHOUSE-TASK-001")

    success, reason = robot_gateway.execute_command(
        capsule=child,
        requested_action="CARRY",
        requested_zone="Warehouse-Corridor",
        requested_task_id="WAREHOUSE-TASK-001",
        requested_resource="Package-X",
        requested_purpose="PACKAGE_TRANSFER",
        requested_destination="Loading-Bay-2"
    )

    print(
        "Trusted Task Version:",
        state.get_current_version("WAREHOUSE-TASK-001")
    )
    print("Capsule Version:", child.version)
    print("Allowed:", success)
    print("Reason:", reason)

    assert success is False, (
        f"Expected stale warehouse capsule to be blocked, "
        f"but received: {reason}"
    )

    assert reason == "STALE_VERSION", (
        f"Expected STALE_VERSION, but received: {reason}"
    )

    return success, reason


def run_warehouse_action_attack():

    context = create_warehouse_experiment_context()

    robot_gateway = context["robot_gateway"]
    child = context["child"]

    print("\nWAREHOUSE UNAUTHORIZED ACTION ATTACK")
    print("------------------------------------")

    success, reason = robot_gateway.execute_command(
        capsule=child,
        requested_action="DELETE_PACKAGE",
        requested_zone="Warehouse-Corridor",
        requested_task_id="WAREHOUSE-TASK-001",
        requested_resource="Package-X",
        requested_purpose="PACKAGE_TRANSFER",
        requested_destination="Loading-Bay-2"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    assert success is False, (
        f"Expected unauthorized warehouse action to be blocked, "
        f"but received: {reason}"
    )

    assert reason == "ROBOT_ACTION_NOT_ALLOWED", (
        f"Expected ROBOT_ACTION_NOT_ALLOWED, but received: {reason}"
    )

    return success, reason


if __name__ == "__main__":

    results = []

    test_cases = [
        (
            "Legitimate Carry",
            "ALLOW",
            "ROBOT_MOVED",
            run_warehouse_legitimate_test
        ),
        (
            "Unauthorized Zone",
            "BLOCK",
            "ROBOT_ZONE_NOT_ALLOWED",
            run_warehouse_zone_attack
        ),
        (
            "Destination Manipulation",
            "BLOCK",
            "DESTINATION_MISMATCH",
            run_warehouse_destination_attack
        ),
        (
            "Resource Manipulation",
            "BLOCK",
            "RESOURCE_MISMATCH",
            run_warehouse_resource_attack
        ),
        (
            "Purpose Manipulation",
            "BLOCK",
            "PURPOSE_MISMATCH",
            run_warehouse_purpose_attack
        ),
        (
            "Cross-Task Authority Misuse",
            "BLOCK",
            "CROSS_TASK_AUTHORITY_MISUSE",
            run_warehouse_cross_task_attack
        ),
        (
            "Task Revocation",
            "BLOCK",
            "TASK_NOT_ACTIVE",
            run_warehouse_revocation_test
        ),
        (
            "Stale Version",
            "BLOCK",
            "STALE_VERSION",
            run_warehouse_stale_version_test
        ),
        (
            "Unauthorized Action",
            "BLOCK",
            "ROBOT_ACTION_NOT_ALLOWED",
            run_warehouse_action_attack
        )
    ]

    for (
        test_name,
        expected_decision,
        expected_reason,
        test_function
    ) in test_cases:

        success, reason = test_function()

        observed_decision = (
            "ALLOW" if success else "BLOCK"
        )

        passed = (
            observed_decision == expected_decision
            and reason == expected_reason
        )

        results.append({
            "test_name": test_name,
            "expected_decision": expected_decision,
            "observed_decision": observed_decision,
            "expected_reason": expected_reason,
            "observed_reason": reason,
            "passed": passed
        })

    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    results_dir = os.path.join(
        project_root,
        "results"
    )

    os.makedirs(results_dir, exist_ok=True)

    output_path = os.path.join(
        results_dir,
        "warehouse_cross_domain_results.csv"
    )

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "test_name",
                "expected_decision",
                "observed_decision",
                "expected_reason",
                "observed_reason",
                "passed"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    passed_count = sum(
        1 for result in results
        if result["passed"]
    )

    print("\nWAREHOUSE CROSS-DOMAIN SUMMARY")
    print("------------------------------")
    print("Total tests:", len(results))
    print("Passed:", passed_count)
    print("Failed:", len(results) - passed_count)
    print("Results saved to:", output_path)

    assert passed_count == len(results), (
        "One or more warehouse cross-domain tests failed."
    )