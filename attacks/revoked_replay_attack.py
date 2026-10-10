from copy import deepcopy
from experiments.experiment_context import create_experiment_context


def run_revoked_replay_attack(
    attack_runner
):
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]
    trusted_state = context["state"]

    print("\nREVOKED CAPSULE REPLAY ATTACK")
    print("----------------------------")

    revoked_capsule = deepcopy(child_capsule)


    clock.set_time("10:15")

    # Doctor/security authority revokes the task.
    trusted_state.revoke_task(
        revoked_capsule.task_id
    )

    print(
        "Task Status:",
        trusted_state.get_task_status(
            revoked_capsule.task_id
        )
    )

    success, reason = robot_gateway.authorize_command(
        capsule=revoked_capsule,
        robot_id=robot.robot_id,
        requested_action="CARRY",
        requested_zone="Corridor-A"
    )

    print("Allowed:", success)
    print("Reason:", reason)

    attack_runner.record_result(
        attack_category="Capsule Forgery / Tampering / Replay",
        attack_variant="Revoked Capsule Replay",
        expected_result="BLOCK",
        actual_result="ALLOW" if success else "BLOCK",
        reason=reason,
        expected_reason="TASK_NOT_ACTIVE"
    )




    return success, reason