from experiments.experiment_context import create_experiment_context

import csv
import os

def create_fresh_context():
    """
    Create a fresh isolated TriSovereign-ZT environment
    for one attack-matrix case.
    """
    return create_experiment_context()

ATTACK_DIMENSIONS = [
    "zone",
    "resource",
    "source",
    "destination",
    "purpose",
    "action",
    "data",
    "robot",
    "time",
]

DELEGATION_DEPTHS = [
    1,
    2,
    5,
    10,
]

SECURITY_TEST_CATEGORIES = [
    "lineage_tampering",
    "proposal_containment",
    "task_state",
    "robot_gateway",
    "tool_data_gateway",
]

ATTACK_POSITIONS = [
    "child",
    "parent",
    "intermediate_ancestor",
    "root",
]



ATTACK_MUTATIONS = {
    "zone": "Unauthorized-Zone",
    "resource": "Unauthorized-Resource",
    "source": "Unauthorized-Source",
    "destination": "Unauthorized-Destination",
    "purpose": "UNAUTHORIZED_PURPOSE",
    "action": "UNAUTHORIZED_ACTION",
    "data": "Unauthorized-Data",
    "robot": "Unauthorized-Robot",
    "time": "11:00",
}
def create_result_row(
    category,
    test_name,
    depth,
    allowed,
    reason,
    final_capsule=None,
    attack_dimension=None,
    attack_position=None
):
    """
    Create one standardized result row for the
    consolidated Priority #2 security evaluation.
    """

    return {
        "category": category,
        "test_name": test_name,
        "depth": depth,
        "attack_dimension": attack_dimension,
        "attack_position": attack_position,
        "final_capsule": final_capsule,
        "allowed": allowed,
        "reason": reason,
    }

def collect_consolidated_results():
    """
    Collect all Priority #2 security evaluation results
    into one standardized list.
    """
    results = []

    # ------------------------------------------
    # 1. LINEAGE TAMPERING TESTS
    # ------------------------------------------

    lineage_results = run_attack_matrix()

    for result in lineage_results:
        results.append(
            create_result_row(
                category="lineage_tampering",
                test_name="post_signature_tampering",
                depth=result["depth"],
                allowed=result["allowed"],
                reason=result["reason"],
                final_capsule=result["final_capsule"],
                attack_dimension=result["attack_dimension"],
                attack_position=result["attack_position"],
            )
        )

    # ------------------------------------------
    # 2. PROPOSAL CONTAINMENT TESTS
    # ------------------------------------------

    for depth in DELEGATION_DEPTHS:
        for attack_dimension in ATTACK_DIMENSIONS:

            result = run_single_proposal_attack(
                attack_dimension=attack_dimension,
                depth=depth
            )

            results.append(
                create_result_row(
                    category="proposal_containment",
                    test_name="malicious_delegation_proposal",
                    depth=result["depth"],
                    allowed=result["allowed"],
                    reason=result["reason"],
                    attack_dimension=result["attack_dimension"],
                )
            )

    # ------------------------------------------
    # 3. LEGITIMATE DEPTH CONTROLS
    # ------------------------------------------

    for depth in DELEGATION_DEPTHS:
        result = run_legitimate_depth_control(
            depth
        )

        results.append(
            create_result_row(
                category="legitimate_control",
                test_name="legitimate_delegation_chain",
                depth=result["depth"],
                allowed=result["allowed"],
                reason=result["reason"],
                final_capsule=result["final_capsule"],
            )
        )

    # ------------------------------------------
    # 4. TRUSTED TASK-STATE TESTS
    # ------------------------------------------

    state_tests = [
        (
            "task_revocation",
            run_task_revocation_attack
        ),
        (
            "stale_version",
            run_stale_version_attack
        ),
        (
            "completed_task",
            run_completed_task_attack
        ),
    ]

    for test_name, test_function in state_tests:
        for depth in DELEGATION_DEPTHS:

            result = test_function(
                depth
            )

            results.append(
                create_result_row(
                    category="task_state",
                    test_name=test_name,
                    depth=result["depth"],
                    allowed=result["allowed"],
                    reason=result["reason"],
                    final_capsule=result["final_capsule"],
                )
            )

    # ------------------------------------------
    # 5. ROBOT GATEWAY SECURITY TESTS
    # ------------------------------------------

    robot_gateway_tests = [
        (
            "cross_task_misuse",
            run_cross_task_attack
        ),
        (
            "unauthorized_robot",
            run_robot_identity_attack
        ),
        (
            "unauthorized_action",
            run_robot_action_attack
        ),
        (
            "unauthorized_zone",
            run_robot_zone_attack
        ),
        (
            "resource_misuse",
            run_resource_misuse_attack
        ),
        (
            "purpose_misuse",
            run_purpose_misuse_attack
        ),
        (
            "destination_misuse",
            run_destination_misuse_attack
        ),
        (
            "invalid_signature",
            run_invalid_signature_attack
        ),
        (
            "expired_capsule",
            run_expired_capsule_attack
        ),
        (
            "not_yet_valid_capsule",
            run_not_yet_valid_capsule_attack
        ),
    ]

    for test_name, test_function in robot_gateway_tests:
        for depth in DELEGATION_DEPTHS:

            result = test_function(
                depth
            )

            results.append(
                create_result_row(
                    category="robot_gateway",
                    test_name=test_name,
                    depth=result["depth"],
                    allowed=result["allowed"],
                    reason=result["reason"],
                    final_capsule=result["final_capsule"],
                )
            )

    # ------------------------------------------
    # 6. TOOL/DATA GATEWAY SECURITY TESTS
    # ------------------------------------------

    for depth in DELEGATION_DEPTHS:

        result = run_unauthorized_data_attack(
            depth
        )

        results.append(
            create_result_row(
                category="tool_data_gateway",
                test_name="unauthorized_data",
                depth=result["depth"],
                allowed=result["allowed"],
                reason=result["reason"],
                final_capsule=result["final_capsule"],
            )
        )

    return results

def save_consolidated_results(results):
    """
    Save all consolidated Priority #2 evaluation
    results to one CSV file.
    """

    results_directory = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "results"
    )

    os.makedirs(
        results_directory,
        exist_ok=True
    )

    output_path = os.path.join(
        results_directory,
        "priority2_consolidated_security_results.csv"
    )

    fieldnames = [
        "category",
        "test_name",
        "depth",
        "attack_dimension",
        "attack_position",
        "final_capsule",
        "allowed",
        "reason",
    ]

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    return output_path

def summarize_results_by_category(results):
    """
    Summarize consolidated Priority #2 results
    by experimental category.
    """

    summary = {}

    for result in results:
        category = result["category"]

        if category not in summary:
            summary[category] = {
                "total": 0,
                "allowed": 0,
                "blocked": 0,
            }

        summary[category]["total"] += 1

        if result["allowed"] is True:
            summary[category]["allowed"] += 1

        elif result["allowed"] is False:
            summary[category]["blocked"] += 1

    return summary

def summarize_results_by_depth(results):
    """
    Summarize consolidated Priority #2 results
    by delegation depth.
    """

    summary = {}

    for result in results:
        depth = result["depth"]

        if depth not in summary:
            summary[depth] = {
                "total": 0,
                "allowed": 0,
                "blocked": 0,
            }

        summary[depth]["total"] += 1

        if result["allowed"] is True:
            summary[depth]["allowed"] += 1

        elif result["allowed"] is False:
            summary[depth]["blocked"] += 1

    return summary

def save_summary_results(
    category_summary,
    depth_summary
):
    """
    Save category-level and depth-level Priority #2
    summaries to CSV files.
    """

    results_directory = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "results"
    )

    os.makedirs(
        results_directory,
        exist_ok=True
    )

    category_path = os.path.join(
        results_directory,
        "priority2_category_summary.csv"
    )

    with open(
        category_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "category",
                "total",
                "blocked",
                "allowed",
            ]
        )

        for category, counts in category_summary.items():
            writer.writerow(
                [
                    category,
                    counts["total"],
                    counts["blocked"],
                    counts["allowed"],
                ]
            )

    depth_path = os.path.join(
        results_directory,
        "priority2_depth_summary.csv"
    )

    with open(
        depth_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "depth",
                "total",
                "blocked",
                "allowed",
            ]
        )

        for depth, counts in sorted(
            depth_summary.items()
        ):
            writer.writerow(
                [
                    depth,
                    counts["total"],
                    counts["blocked"],
                    counts["allowed"],
                ]
            )

    return category_path, depth_path

def summarize_rejection_reasons(results):
    """
    Count rejection reasons across Priority #2
    security cases.
    """

    reason_summary = {}

    for result in results:
        if result["category"] == "legitimate_control":
            continue

        if result["allowed"] is not False:
            continue

        reason = result["reason"]

        if reason not in reason_summary:
            reason_summary[reason] = 0

        reason_summary[reason] += 1

    return reason_summary

def save_rejection_reason_summary(
    reason_summary
):
    """
    Save Priority #2 rejection-reason counts
    to a CSV file.
    """

    results_directory = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "results"
    )

    os.makedirs(
        results_directory,
        exist_ok=True
    )

    output_path = os.path.join(
        results_directory,
        "priority2_rejection_reason_summary.csv"
    )

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "reason",
                "count",
            ]
        )

        for reason, count in sorted(
            reason_summary.items()
        ):
            writer.writerow(
                [
                    reason,
                    count,
                ]
            )

    return output_path

def validate_result_consistency(
    results,
    category_summary,
    depth_summary,
    reason_summary
):
    """
    Verify that all Priority #2 result summaries
    are internally consistent.
    """

    total_cases = len(results)

    category_total = sum(
        counts["total"]
        for counts in category_summary.values()
    )

    depth_total = sum(
        counts["total"]
        for counts in depth_summary.values()
    )

    security_results = [
        result
        for result in results
        if result["category"] != "legitimate_control"
    ]

    blocked_security = sum(
        1
        for result in security_results
        if result["allowed"] is False
    )

    reason_total = sum(
        reason_summary.values()
    )

    legitimate_results = [
        result
        for result in results
        if result["category"] == "legitimate_control"
    ]

    legitimate_allowed = sum(
        1
        for result in legitimate_results
        if result["allowed"] is True
    )

    checks = {
        "category_total_matches": (
            category_total == total_cases
        ),
        "depth_total_matches": (
            depth_total == total_cases
        ),
        "reason_total_matches_blocked_security": (
            reason_total == blocked_security
        ),
        "all_security_cases_blocked": (
            blocked_security == len(security_results)
        ),
        "all_legitimate_controls_allowed": (
            legitimate_allowed == len(legitimate_results)
        ),
    }

    return checks
def apply_attack_mutation(capsule, attack_dimension):
    """
    Apply one authority-drift mutation to a capsule.
    """

    if attack_dimension == "zone":
        capsule.allowed_zones.append(
            ATTACK_MUTATIONS["zone"]
        )

    elif attack_dimension == "resource":
        capsule.resource = ATTACK_MUTATIONS["resource"]

    elif attack_dimension == "source":
        capsule.source = ATTACK_MUTATIONS["source"]

    elif attack_dimension == "destination":
        capsule.destination = ATTACK_MUTATIONS["destination"]

    elif attack_dimension == "purpose":
        capsule.purpose = ATTACK_MUTATIONS["purpose"]

    elif attack_dimension == "action":
        capsule.allowed_actions.append(
            ATTACK_MUTATIONS["action"]
        )

    elif attack_dimension == "data":
        capsule.allowed_data.append(
            ATTACK_MUTATIONS["data"]
        )

    elif attack_dimension == "robot":
        capsule.authorized_robot = ATTACK_MUTATIONS["robot"]

    elif attack_dimension == "time":
        capsule.valid_until = ATTACK_MUTATIONS["time"]

    else:
        raise ValueError(
            f"Unknown attack dimension: {attack_dimension}"
        )

    return capsule

def capsule_authority_snapshot(capsule):
    """
    Return the security-relevant authority fields of a capsule.
    """
    return {
        "resource": capsule.resource,
        "source": capsule.source,
        "destination": capsule.destination,
        "purpose": capsule.purpose,
        "actions": list(capsule.allowed_actions),
        "zones": list(capsule.allowed_zones),
        "data": list(capsule.allowed_data),
        "robot": capsule.authorized_robot,
        "valid_from": capsule.valid_from,
        "valid_until": capsule.valid_until,
    }

def get_chain_start(context):
    """
    Return the delegating parent capsule from a fresh
    TriSovereign-ZT experiment context.
    """
    parent = context["parent"]

    if not parent.can_delegate:
        raise ValueError(
            "Chain-start capsule is not allowed to delegate."
        )

    return parent
def create_legitimate_child(context, parent, holder_name):
    """
    Create one legitimate child capsule that remains
    within the authority of its parent.
    """

    authorization_service = context["authorization_service"]

    allowed, reason, child = (
        authorization_service.request_delegation(
            parent_capsule=parent,
            current_holder=holder_name,
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
            can_delegate=True,
            version=parent.version
        )
    )

    if not allowed:
        raise RuntimeError(
            f"Legitimate delegation failed: {reason}"
        )

    return child

def build_delegation_chain(context, depth):
    """
    Build a legitimate delegation chain of the requested depth.

    Depth 1 means one new capsule below the chain-start parent.
    """
    parent = get_chain_start(context)
    chain = [parent]

    for level in range(1, depth + 1):
        child = create_legitimate_child(
            context,
            parent,
            f"Matrix-Agent-{level}"
        )

        chain.append(child)
        parent = child

    return chain

def select_attack_target(context, chain, attack_position):
    """
    Select the capsule that will be maliciously modified
    for a given attack position.
    """

    if attack_position == "child":
        return chain[-1]

    elif attack_position == "parent":
        if len(chain) < 2:
            raise ValueError(
                "Parent attack requires at least one child."
            )
        return chain[-2]

    elif attack_position == "intermediate_ancestor":
        if len(chain) < 3:
            raise ValueError(
                "Intermediate-ancestor attack requires "
                "a sufficiently deep delegation chain."
            )

        return chain[len(chain) // 2]

    elif attack_position == "root":
        return context["root"]

    else:
        raise ValueError(
            f"Unknown attack position: {attack_position}"
        )

def run_single_lineage_attack(
    attack_dimension,
    depth,
    attack_position
):
    """
    Build a legitimate chain, mutate one capsule,
    and validate the final capsule through the full TAF.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    target = select_attack_target(
        context,
        chain,
        attack_position
    )

    apply_attack_mutation(
        target,
        attack_dimension
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["taf"].validate_full_lineage(
            final_capsule
        )
    )

    return {
        "attack_dimension": attack_dimension,
        "depth": depth,
        "attack_position": attack_position,
        "target_capsule": target.capsule_id,
        "final_capsule": final_capsule.capsule_id,
        "allowed": allowed,
        "reason": reason,
    }

def run_single_proposal_attack(
    attack_dimension,
    depth
):
    """
    Build a legitimate chain and submit a malicious
    child proposal through the normal authorization path.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    parent = chain[-1]

    proposal = (
        context["manager"].create_unsigned_capsule(
            task_id=parent.task_id,
            original_issuer=parent.original_issuer,
            current_holder="Malicious-Matrix-Agent",
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
    )

    apply_attack_mutation(
        proposal,
        attack_dimension
    )

    allowed, reason = (
        context["taf"].validate_delegation_proposal(
            parent,
            proposal
        )
    )

    return {
        "attack_dimension": attack_dimension,
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
    }

def run_legitimate_depth_control(depth):
    """
    Build a legitimate delegation chain and verify that
    the final capsule has a valid full lineage.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["taf"].validate_full_lineage(
            final_capsule
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_task_revocation_attack(depth):
    """
    Build a legitimate delegation chain, revoke its task,
    and test whether the Robot Gateway blocks subsequent
    robot authorization.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    context["state"].revoke_task(
        final_capsule.task_id
    )

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_stale_version_attack(depth):
    """
    Build a legitimate delegation chain, advance the trusted
    task version, and verify that the existing descendant is
    rejected by the Robot Gateway as stale.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    context["state"].update_version(
        final_capsule.task_id
    )

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_completed_task_attack(depth):
    """
    Build a legitimate delegation chain, complete its task,
    and verify that subsequent robot authorization is blocked.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    context["state"].complete_task(
        final_capsule.task_id
    )

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_cross_task_attack(depth):
    """
    Build a legitimate delegation chain and attempt to use
    its final capsule for a different task identifier.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id="UNAUTHORIZED-TASK",
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }
def run_robot_identity_attack(depth):
    """
    Build a legitimate delegation chain and attempt to
    authorize a different robot using the final capsule.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id="UNAUTHORIZED-ROBOT",
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_robot_action_attack(depth):
    """
    Build a legitimate delegation chain and attempt an
    unauthorized robot action using the final capsule.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action="UNAUTHORIZED_ACTION",
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_robot_zone_attack(depth):
    """
    Build a legitimate delegation chain and attempt to
    authorize operation in an unauthorized zone.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone="UNAUTHORIZED-ZONE",
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_resource_misuse_attack(depth):
    """
    Build a legitimate delegation chain and attempt to
    authorize access to a different resource.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource="UNAUTHORIZED-RESOURCE",
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }
def run_purpose_misuse_attack(depth):
    """
    Build a legitimate delegation chain and attempt to
    authorize operation for a different purpose.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose="UNAUTHORIZED_PURPOSE"
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_destination_misuse_attack(depth):
    """
    Build a legitimate delegation chain and attempt to
    authorize operation for a different destination.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination="UNAUTHORIZED-DESTINATION",
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_invalid_signature_attack(depth):
    """
    Build a legitimate delegation chain, tamper with the
    final signed capsule, and verify that the Robot Gateway
    rejects its invalid signature.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    # Tamper with the signed capsule after issuance.
    final_capsule.destination = "TAMPERED-DESTINATION"

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_expired_capsule_attack(depth):
    """
    Build a legitimate delegation chain, move simulated
    time beyond its validity window, and verify that the
    Robot Gateway rejects the expired capsule.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    context["clock"].set_time(
        "10:31"
    )

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_not_yet_valid_capsule_attack(depth):
    """
    Build a legitimate delegation chain, move simulated
    time before its validity window, and verify that the
    Robot Gateway rejects the not-yet-valid capsule.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    context["clock"].set_time(
        "09:59"
    )

    allowed, reason = (
        context["robot_gateway"].authorize_command(
            capsule=final_capsule,
            robot_id=final_capsule.authorized_robot,
            requested_action=final_capsule.allowed_actions[0],
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_destination=final_capsule.destination,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def run_unauthorized_data_attack(depth):
    """
    Build a legitimate delegation chain and attempt to
    access unauthorized data through the Tool/Data Gateway.
    """

    context = create_fresh_context()

    chain = build_delegation_chain(
        context,
        depth
    )

    final_capsule = chain[-1]

    allowed, reason = (
        context["gateway"].authorize_request(
            capsule=final_capsule,
            requested_action=final_capsule.allowed_actions[0],
            requested_data="UNAUTHORIZED-DATA",
            requested_zone=final_capsule.allowed_zones[0],
            requested_task_id=final_capsule.task_id,
            requested_resource=final_capsule.resource,
            requested_purpose=final_capsule.purpose
        )
    )

    return {
        "depth": depth,
        "allowed": allowed,
        "reason": reason,
        "final_capsule": final_capsule.capsule_id,
    }

def valid_attack_positions_for_depth(depth):
    """
    Return attack positions that are meaningful for
    the requested delegation depth.
    """
    positions = [
        "child",
        "parent",
        "root",
    ]

    if depth >= 2:
        positions.append(
            "intermediate_ancestor"
        )

    return positions

def run_attack_matrix():
    """
    Execute the systematic authority-drift attack matrix.
    """
    results = []

    for depth in DELEGATION_DEPTHS:
        positions = valid_attack_positions_for_depth(
            depth
        )

        for attack_position in positions:
            for attack_dimension in ATTACK_DIMENSIONS:

                try:
                    result = run_single_lineage_attack(
                        attack_dimension=attack_dimension,
                        depth=depth,
                        attack_position=attack_position
                    )

                    result["execution_status"] = "SUCCESS"

                except Exception as error:
                    result = {
                        "attack_dimension": attack_dimension,
                        "depth": depth,
                        "attack_position": attack_position,
                        "target_capsule": None,
                        "final_capsule": None,
                        "allowed": None,
                        "reason": str(error),
                        "execution_status": "ERROR",
                    }

                results.append(result)

    return results

def save_attack_matrix_results(results):
    """
    Save systematic attack-matrix results to CSV.
    """

    results_directory = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "results"
    )

    os.makedirs(
        results_directory,
        exist_ok=True
    )

    output_path = os.path.join(
        results_directory,
        "large_scale_attack_matrix_results.csv"
    )

    fieldnames = [
        "attack_dimension",
        "depth",
        "attack_position",
        "target_capsule",
        "final_capsule",
        "allowed",
        "reason",
        "execution_status",
    ]

    with open(
        output_path,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    return output_path

if __name__ == "__main__":
    print("\nCONSOLIDATED PRIORITY #2 TEST")
    print("-----------------------------")

    results = collect_consolidated_results()

    total_cases = len(results)

    legitimate_results = [
        result
        for result in results
        if result["category"] == "legitimate_control"
    ]

    security_results = [
        result
        for result in results
        if result["category"] != "legitimate_control"
    ]

    blocked_security = sum(
        1
        for result in security_results
        if result["allowed"] is False
    )

    allowed_security = sum(
        1
        for result in security_results
        if result["allowed"] is True
    )

    allowed_legitimate = sum(
        1
        for result in legitimate_results
        if result["allowed"] is True
    )

    blocked_legitimate = sum(
        1
        for result in legitimate_results
        if result["allowed"] is False
    )

    print("Total cases:", total_cases)
    print("Security cases:", len(security_results))
    print("Security blocked:", blocked_security)
    print("Security allowed:", allowed_security)
    print("Legitimate controls:", len(legitimate_results))
    print("Legitimate allowed:", allowed_legitimate)
    print("Legitimate blocked:", blocked_legitimate)

    output_path = save_consolidated_results(
        results
    )

    print(
        "Consolidated CSV:",
        output_path
    )

    category_summary = summarize_results_by_category(
        results
    )

    print("\nCATEGORY SUMMARY")
    print("----------------")

    for category, counts in category_summary.items():
        print(
            f"{category}"
            f" | Total: {counts['total']}"
            f" | Blocked: {counts['blocked']}"
            f" | Allowed: {counts['allowed']}"
        )

    depth_summary = summarize_results_by_depth(
        results
    )

    print("\nDEPTH SUMMARY")
    print("-------------")

    for depth, counts in sorted(
        depth_summary.items()
    ):
        print(
            f"Depth {depth}"
            f" | Total: {counts['total']}"
            f" | Blocked: {counts['blocked']}"
            f" | Allowed: {counts['allowed']}"
        )

    category_path, depth_path = save_summary_results(
        category_summary,
        depth_summary
    )

    print("\nSUMMARY FILES")
    print("-------------")
    print(
        "Category summary:",
        category_path
    )
    print(
        "Depth summary:",
        depth_path
    )
    reason_summary = summarize_rejection_reasons(
        results
    )

    print("\nREJECTION REASON SUMMARY")
    print("------------------------")

    for reason, count in sorted(
            reason_summary.items()
    ):
        print(
            f"{reason} | Count: {count}"
        )

    reason_path = save_rejection_reason_summary(
        reason_summary
    )

    print(
        "\nRejection reason summary:",
        reason_path
    )
    consistency_checks = validate_result_consistency(
        results,
        category_summary,
        depth_summary,
        reason_summary
    )

    print("\nCONSISTENCY CHECK")
    print("-----------------")

    for check_name, passed in consistency_checks.items():
        print(
            f"{check_name} | "
            f"{'PASS' if passed else 'FAIL'}"
        )