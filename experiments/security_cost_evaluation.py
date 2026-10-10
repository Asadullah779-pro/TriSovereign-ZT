import time
import statistics

from experiments.experiment_context import create_experiment_context


def _calculate_stats(measurements):

    return {
        "mean": statistics.mean(measurements),
        "median": statistics.median(measurements),
        "stdev": statistics.stdev(measurements),
        "p95": statistics.quantiles(
            measurements,
            n=100
        )[94]
    }


def run_security_cost_evaluation(iterations=1000):

    print("\nSECURITY COST EVALUATION")
    print("------------------------------------")
    print(f"Iterations: {iterations}")

    # ---------------------------------
    # A. Core lineage security validation
    # ---------------------------------

    context = create_experiment_context()

    taf = context["taf"]
    child_capsule = context["child"]

    core_measurements = []

    for _ in range(iterations):

        start_time = time.perf_counter_ns()

        allowed, reason = taf.validate_full_lineage(
            child_capsule
        )

        end_time = time.perf_counter_ns()

        if not allowed:
            raise RuntimeError(
                f"Core validation failed: {reason}"
            )

        core_measurements.append(
            (end_time - start_time) / 1_000_000
        )

    core_stats = _calculate_stats(
        core_measurements
    )

    # ---------------------------------
    # B. Audit logging cost
    # ---------------------------------

    context = create_experiment_context()

    logger = context["logger"]

    logging_measurements = []

    for _ in range(iterations):

        start_time = time.perf_counter_ns()

        logger.log_event(
            task_id="TASK-PERFORMANCE",
            actor="Performance-Test",
            decision="ALLOW",
            reason="PERFORMANCE_MEASUREMENT",
            component="PERFORMANCE"
        )

        end_time = time.perf_counter_ns()

        logging_measurements.append(
            (end_time - start_time) / 1_000_000
        )

    logging_stats = _calculate_stats(
        logging_measurements
    )

    # ---------------------------------
    # C. Full gateway authorization
    # ---------------------------------

    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]

    clock.set_time("10:15")

    gateway_measurements = []

    for _ in range(iterations):

        start_time = time.perf_counter_ns()

        allowed, reason = robot_gateway.authorize_command(
            capsule=child_capsule,
            robot_id=robot.robot_id,
            requested_action="CARRY",
            requested_zone="Corridor-A",
            requested_task_id=child_capsule.task_id,
            requested_resource=child_capsule.resource,
            requested_purpose=child_capsule.purpose,
            requested_destination=child_capsule.destination
        )

        end_time = time.perf_counter_ns()

        if not allowed:
            raise RuntimeError(
                f"Gateway authorization failed: {reason}"
            )

        gateway_measurements.append(
            (end_time - start_time) / 1_000_000
        )

    gateway_stats = _calculate_stats(
        gateway_measurements
    )

    # ---------------------------------
    # Results
    # ---------------------------------

    print("\nA. CORE LINEAGE SECURITY VALIDATION")
    print(
        f"Mean: {core_stats['mean']:.6f} ms"
    )
    print(
        f"Median: {core_stats['median']:.6f} ms"
    )
    print(
        f"Standard Deviation: "
        f"{core_stats['stdev']:.6f} ms"
    )
    print(
        f"95th Percentile: "
        f"{core_stats['p95']:.6f} ms"
    )

    print("\nB. AUDIT LOGGING")
    print(
        f"Mean: {logging_stats['mean']:.6f} ms"
    )
    print(
        f"Median: {logging_stats['median']:.6f} ms"
    )
    print(
        f"Standard Deviation: "
        f"{logging_stats['stdev']:.6f} ms"
    )
    print(
        f"95th Percentile: "
        f"{logging_stats['p95']:.6f} ms"
    )

    print("\nC. FULL GATEWAY AUTHORIZATION")
    print(
        f"Mean: {gateway_stats['mean']:.6f} ms"
    )
    print(
        f"Median: {gateway_stats['median']:.6f} ms"
    )
    print(
        f"Standard Deviation: "
        f"{gateway_stats['stdev']:.6f} ms"
    )
    print(
        f"95th Percentile: "
        f"{gateway_stats['p95']:.6f} ms"
    )

    return {
        "core_security": core_stats,
        "audit_logging": logging_stats,
        "full_gateway": gateway_stats
    }

if __name__ == "__main__":
    run_security_cost_evaluation(
        iterations=1000
    )