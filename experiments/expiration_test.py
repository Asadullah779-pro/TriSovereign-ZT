from experiments.experiment_context import create_experiment_context
def run_expiration_test():
    # Create a completely isolated experiment environment
    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    robot = context["robot"]
    capsule = context["child"]
    trusted_state = context["state"]
    clock = context["clock"]

    print("\nCAPSULE EXPIRATION EXPERIMENT")
    print("----------------------------")



    # Move simulated time beyond the capsule's valid time
    clock.set_time("10:30")

    print("Capsule Valid From:", capsule.valid_from)
    print("Capsule Valid Until:", capsule.valid_until)
    print("Current Simulated Time:", clock.get_time())

    # Try to use the expired capsule
    success, reason = robot_gateway.execute_command(
        capsule=capsule,
        requested_action="PICK_UP",
        requested_zone="Pharmacy-A"
    )

    print("\nEXPIRED CAPSULE ATTEMPT")
    print("Success:", success)
    print("Reason:", reason)
    print("Robot Location:", robot.location)
    print("Robot Carrying:", robot.carrying)

    # Restore the normal simulated time
    clock.set_time("10:15")

    if success:
        return False, "EXPIRED_CAPSULE_WAS_ACCEPTED"

    if reason != "CAPSULE_EXPIRED_OR_NOT_YET_VALID":
        return False, f"UNEXPECTED_BLOCK_REASON: {reason}"

    return True, "EXPIRED_CAPSULE_SUCCESSFULLY_BLOCKED"