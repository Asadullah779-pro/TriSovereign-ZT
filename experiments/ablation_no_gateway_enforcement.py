from experiments.experiment_context import create_experiment_context
from ablations.no_gateway_enforcement import NoGatewayEnforcement
import csv
import os

def run_unauthorized_zone_test():

    print("\n==========================================")
    print("ABLATION #4 - UNAUTHORIZED ROBOT ZONE")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_gateway = full_context["robot_gateway"]
    full_robot = full_context["robot"]
    full_capsule = full_context["child"]

    # Request movement to a zone outside
    # the capsule's authorized zone scope.
    full_allowed, full_reason = full_gateway.execute_command(
        capsule=full_capsule,
        requested_action="CARRY",
        requested_zone="Restricted-Storage",
        requested_task_id=full_capsule.task_id,
        requested_resource=full_capsule.resource,
        requested_destination=full_capsule.destination,
        requested_purpose=full_capsule.purpose
    )

    # ==========================================
    # NO-GATEWAY-ENFORCEMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_robot = ablation_context["robot"]
    ablation_capsule = ablation_context["child"]

    no_gateway = NoGatewayEnforcement()

    # Register the same trusted robot with the
    # ablated gateway.
    no_gateway.register_robot(
        ablation_robot
    )

    ablation_allowed, ablation_reason = no_gateway.execute_command(
        capsule=ablation_capsule,
        requested_action="CARRY",
        requested_zone="Restricted-Storage",
        requested_task_id=ablation_capsule.task_id,
        requested_resource=ablation_capsule.resource,
        requested_destination=ablation_capsule.destination,
        requested_purpose=ablation_capsule.purpose
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Gateway-Enforcement Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Unauthorized robot zone",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_unauthorized_action_test():

    print("\n==========================================")
    print("ABLATION #4 - UNAUTHORIZED ROBOT ACTION")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_gateway = full_context["robot_gateway"]
    full_capsule = full_context["child"]

    # Agent-C is not authorized for this action.
    requested_action = "DELETE_RECORD"

    full_allowed, full_reason = full_gateway.execute_command(
        capsule=full_capsule,
        requested_action=requested_action,
        requested_zone="Pharmacy-A",
        requested_task_id=full_capsule.task_id,
        requested_resource=full_capsule.resource,
        requested_destination=full_capsule.destination,
        requested_purpose=full_capsule.purpose
    )

    # ==========================================
    # NO-GATEWAY-ENFORCEMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_robot = ablation_context["robot"]
    ablation_capsule = ablation_context["child"]

    no_gateway = NoGatewayEnforcement()

    no_gateway.register_robot(
        ablation_robot
    )

    ablation_allowed, ablation_reason = no_gateway.execute_command(
        capsule=ablation_capsule,
        requested_action=requested_action,
        requested_zone="Pharmacy-A",
        requested_task_id=ablation_capsule.task_id,
        requested_resource=ablation_capsule.resource,
        requested_destination=ablation_capsule.destination,
        requested_purpose=ablation_capsule.purpose
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Gateway-Enforcement Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Unauthorized robot action",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_expired_capsule_test():

    print("\n==========================================")
    print("ABLATION #4 - EXPIRED CAPSULE EXECUTION")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_gateway = full_context["robot_gateway"]
    full_capsule = full_context["child"]
    full_clock = full_context["clock"]

    # Move simulated time beyond the capsule's
    # validity interval.
    full_clock.set_time("10:30")

    full_allowed, full_reason = full_gateway.execute_command(
        capsule=full_capsule,
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=full_capsule.task_id,
        requested_resource=full_capsule.resource,
        requested_destination=full_capsule.destination,
        requested_purpose=full_capsule.purpose
    )

    # ==========================================
    # NO-GATEWAY-ENFORCEMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_robot = ablation_context["robot"]
    ablation_capsule = ablation_context["child"]
    ablation_clock = ablation_context["clock"]

    # Same expired execution condition.
    ablation_clock.set_time("10:30")

    no_gateway = NoGatewayEnforcement()

    no_gateway.register_robot(
        ablation_robot
    )

    ablation_allowed, ablation_reason = no_gateway.execute_command(
        capsule=ablation_capsule,
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=ablation_capsule.task_id,
        requested_resource=ablation_capsule.resource,
        requested_destination=ablation_capsule.destination,
        requested_purpose=ablation_capsule.purpose
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Gateway-Enforcement Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Expired capsule execution",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_revoked_task_execution_test():

    print("\n==========================================")
    print("ABLATION #4 - REVOKED TASK EXECUTION")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_gateway = full_context["robot_gateway"]
    full_capsule = full_context["child"]
    full_state = full_context["state"]

    # Revoke the task AFTER the valid capsule
    # has already been created.
    full_state.revoke_task(
        full_capsule.task_id
    )

    full_allowed, full_reason = full_gateway.execute_command(
        capsule=full_capsule,
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=full_capsule.task_id,
        requested_resource=full_capsule.resource,
        requested_destination=full_capsule.destination,
        requested_purpose=full_capsule.purpose
    )

    # ==========================================
    # NO-GATEWAY-ENFORCEMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_robot = ablation_context["robot"]
    ablation_capsule = ablation_context["child"]
    ablation_state = ablation_context["state"]

    # Same revocation condition.
    ablation_state.revoke_task(
        ablation_capsule.task_id
    )

    no_gateway = NoGatewayEnforcement()

    no_gateway.register_robot(
        ablation_robot
    )

    ablation_allowed, ablation_reason = no_gateway.execute_command(
        capsule=ablation_capsule,
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=ablation_capsule.task_id,
        requested_resource=ablation_capsule.resource,
        requested_destination=ablation_capsule.destination,
        requested_purpose=ablation_capsule.purpose
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Gateway-Enforcement Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "attack": "Revoked task execution",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }

def run_legitimate_execution_control():

    print("\n==========================================")
    print("ABLATION #4 - LEGITIMATE EXECUTION CONTROL")
    print("==========================================")

    # ==========================================
    # FULL TRISOVEREIGN-ZT
    # ==========================================

    full_context = create_experiment_context()

    full_gateway = full_context["robot_gateway"]
    full_capsule = full_context["child"]

    full_allowed, full_reason = full_gateway.execute_command(
        capsule=full_capsule,
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=full_capsule.task_id,
        requested_resource=full_capsule.resource,
        requested_destination=full_capsule.destination,
        requested_purpose=full_capsule.purpose
    )

    # ==========================================
    # NO-GATEWAY-ENFORCEMENT ABLATION
    # ==========================================

    ablation_context = create_experiment_context()

    ablation_robot = ablation_context["robot"]
    ablation_capsule = ablation_context["child"]

    no_gateway = NoGatewayEnforcement()

    no_gateway.register_robot(
        ablation_robot
    )

    ablation_allowed, ablation_reason = no_gateway.execute_command(
        capsule=ablation_capsule,
        requested_action="CARRY",
        requested_zone="Corridor-A",
        requested_task_id=ablation_capsule.task_id,
        requested_resource=ablation_capsule.resource,
        requested_destination=ablation_capsule.destination,
        requested_purpose=ablation_capsule.purpose
    )

    print("\nFull TriSovereign-ZT")
    print("Allowed:", full_allowed)
    print("Reason:", full_reason)

    print("\nNo-Gateway-Enforcement Ablation")
    print("Allowed:", ablation_allowed)
    print("Reason:", ablation_reason)

    return {
        "control": "Legitimate robot execution",
        "full_allowed": full_allowed,
        "full_reason": full_reason,
        "ablation_allowed": ablation_allowed,
        "ablation_reason": ablation_reason
    }


if __name__ == "__main__":

    zone_result = run_unauthorized_zone_test()
    action_result = run_unauthorized_action_test()
    expired_result = run_expired_capsule_test()
    revoked_result = run_revoked_task_execution_test()
    legitimate_result = run_legitimate_execution_control()

    csv_rows = [
        {
            "case_type": "ATTACK",
            "case_name": zone_result["attack"],
            "full_allowed": zone_result["full_allowed"],
            "full_reason": zone_result["full_reason"],
            "ablation_allowed": zone_result["ablation_allowed"],
            "ablation_reason": zone_result["ablation_reason"]
        },
        {
            "case_type": "CAPABILITY_CONTROL",
            "case_name": action_result["attack"],
            "full_allowed": action_result["full_allowed"],
            "full_reason": action_result["full_reason"],
            "ablation_allowed": action_result["ablation_allowed"],
            "ablation_reason": action_result["ablation_reason"]
        },
        {
            "case_type": "ATTACK",
            "case_name": expired_result["attack"],
            "full_allowed": expired_result["full_allowed"],
            "full_reason": expired_result["full_reason"],
            "ablation_allowed": expired_result["ablation_allowed"],
            "ablation_reason": expired_result["ablation_reason"]
        },
        {
            "case_type": "ATTACK",
            "case_name": revoked_result["attack"],
            "full_allowed": revoked_result["full_allowed"],
            "full_reason": revoked_result["full_reason"],
            "ablation_allowed": revoked_result["ablation_allowed"],
            "ablation_reason": revoked_result["ablation_reason"]
        },
        {
            "case_type": "CONTROL",
            "case_name": legitimate_result["control"],
            "full_allowed": legitimate_result["full_allowed"],
            "full_reason": legitimate_result["full_reason"],
            "ablation_allowed": legitimate_result["ablation_allowed"],
            "ablation_reason": legitimate_result["ablation_reason"]
        }
    ]

    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    results_dir = os.path.join(
        project_root,
        "results"
    )

    os.makedirs(
        results_dir,
        exist_ok=True
    )

    output_file = os.path.join(
        results_dir,
        "ablation_no_gateway_enforcement_results.csv"
    )

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        fieldnames = [
            "case_type",
            "case_name",
            "full_allowed",
            "full_reason",
            "ablation_allowed",
            "ablation_reason"
        ]

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(csv_rows)

    print("\n==========================================")
    print("ABLATION #4 RESULTS SAVED")
    print("==========================================")
    print("Total rows:", len(csv_rows))
    print("Output file:", output_file)