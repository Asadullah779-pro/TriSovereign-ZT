
from experiments.experiment_context import create_experiment_context

def run_cross_task_resource_attack(
    attack_runner
):

    print("\nCROSS-TASK RESOURCE MISUSE ATTACK")
    print("----------------------------")
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    manager = context["manager"]
    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]


    clock.set_time("10:15")

    attempted_resource = "Medicine-Y"

    print("Authorized Resource:", child_capsule.resource)
    print("Attempted Resource:", attempted_resource)

    success, reason = robot_gateway.authorize_command(
        capsule=child_capsule,
        robot_id=robot.robot_id,
        requested_action="CARRY",
        requested_zone="Room-205",
        requested_task_id=child_capsule.task_id,
        requested_resource=attempted_resource
    )

    print(
        "Signature Valid:",
        manager.verify_signature(child_capsule)
    )
    print("Allowed:", success)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Cross-Task Authority Misuse & Compromised Robot",
        attack_variant="Cross-Task Resource Misuse",
        expected_result="BLOCK",
        actual_result="ALLOW" if success else "BLOCK",
        reason=reason,
        expected_reason="RESOURCE_MISMATCH"
    )

    return success, reason