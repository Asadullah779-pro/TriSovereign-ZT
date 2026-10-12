from experiments.experiment_context import create_experiment_context
from baselines.root_bounded_baseline import (
    RootBoundedAuthorizationBaseline
)


def run_test():

    print("\nB3 ROOT-BOUNDED BASELINE TEST")
    print("-----------------------------")

    # Create isolated experiment context
    context = create_experiment_context()

    manager = context["manager"]
    state = context["state"]
    registry = context["registry"]
    root = context["root"]
    parent = context["parent"]

    # Create B3 baseline
    baseline = RootBoundedAuthorizationBaseline(
        capsule_manager=manager,
        trusted_state=state,
        capsule_registry=registry
    )

    # Create a legitimate child proposal.
    # The child inherits the parent's authority,
    # which should also remain inside the root boundary.
    child = manager.create_unsigned_capsule(
        task_id=parent.task_id,
        original_issuer=parent.original_issuer,
        current_holder="Agent-C",
        parent_capsule_id=parent.capsule_id,

        resource=parent.resource,
        source=parent.source,
        destination=parent.destination,
        purpose=parent.purpose,

        allowed_actions=list(parent.allowed_actions),
        allowed_zones=list(parent.allowed_zones),
        allowed_data=list(parent.allowed_data),

        authorized_robot=parent.authorized_robot,

        valid_from=parent.valid_from,
        valid_until=parent.valid_until,

        can_delegate=False,
        version=parent.version
    )

    # Ask B3 to validate the proposal
    allowed, reason = baseline.validate_delegation_proposal(
        parent,
        child
    )

    print("\nRoot:")
    print("ID:", root.capsule_id)
    print("Holder:", root.current_holder)

    print("\nImmediate Parent:")
    print("ID:", parent.capsule_id)
    print("Holder:", parent.current_holder)

    print("\nB3 Result")
    print("Allowed:", allowed)
    print("Reason:", reason)

    # Expected result
    expected_allowed = True
    expected_reason = "ROOT_BOUNDED_AUTHORIZATION_VALID"

    print("\nExpected")
    print("Allowed:", expected_allowed)
    print("Reason:", expected_reason)

    success = (
        allowed == expected_allowed
        and reason == expected_reason
    )

    print("\nTEST PASSED:", success)

    return success


if __name__ == "__main__":
    run_test()