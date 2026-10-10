import time
import statistics

from experiments.experiment_context import create_experiment_context


def run_performance_evaluation(iterations=1000):

    print("\nPERFORMANCE EVALUATION")
    print("----------------------------")

    context = create_experiment_context()

    robot_gateway = context["robot_gateway"]
    child_capsule = context["child"]
    robot = context["robot"]
    clock = context["clock"]

    clock.set_time("10:15")

    measurements = []
    baseline_measurements = []
    blocked_measurements = []

    # Legitimate authorization measurements
    for _ in range(iterations):

        start_time = time.perf_counter_ns()

        success, reason = robot_gateway.authorize_command(
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

        elapsed_ms = (end_time - start_time) / 1_000_000
        measurements.append(elapsed_ms)

    # Direct robot baseline measurements
    for _ in range(iterations):

        robot.location = "Pharmacy-A"

        start_time = time.perf_counter_ns()

        robot.move_to("Corridor-A")

        end_time = time.perf_counter_ns()

        elapsed_ms = (end_time - start_time) / 1_000_000
        baseline_measurements.append(elapsed_ms)

    # Blocked authorization measurements
    for _ in range(iterations):

        start_time = time.perf_counter_ns()

        blocked_success, blocked_reason = robot_gateway.authorize_command(
            capsule=child_capsule,
            robot_id=robot.robot_id,
            requested_action="CARRY",
            requested_zone="Restricted-Storage",
            requested_task_id=child_capsule.task_id,
            requested_resource=child_capsule.resource,
            requested_purpose=child_capsule.purpose,
            requested_destination=child_capsule.destination
        )

        end_time = time.perf_counter_ns()

        elapsed_ms = (end_time - start_time) / 1_000_000
        blocked_measurements.append(elapsed_ms)

    # Legitimate authorization statistics
    mean_latency = statistics.mean(measurements)
    median_latency = statistics.median(measurements)
    min_latency = min(measurements)
    max_latency = max(measurements)
    stdev_latency = statistics.stdev(measurements)

    p95_latency = statistics.quantiles(
        measurements,
        n=100
    )[94]

    # Baseline statistics
    baseline_mean = statistics.mean(baseline_measurements)
    added_latency = mean_latency - baseline_mean

    # Blocked request statistics
    blocked_mean = statistics.mean(blocked_measurements)
    blocked_median = statistics.median(blocked_measurements)

    blocked_p95 = statistics.quantiles(
        blocked_measurements,
        n=100
    )[94]

    # Results
    print("Iterations:", iterations)
    print("Last Authorization Result:", success, reason)
    print(f"Mean Latency: {mean_latency:.6f} ms")
    print(f"Median Latency: {median_latency:.6f} ms")
    print(f"Standard Deviation: {stdev_latency:.6f} ms")
    print(f"Minimum Latency: {min_latency:.6f} ms")
    print(f"Maximum Latency: {max_latency:.6f} ms")
    print(f"95th Percentile: {p95_latency:.6f} ms")
    print(f"Direct Robot Baseline Mean: {baseline_mean:.6f} ms")
    print(f"Added Latency vs Direct Robot Baseline: {added_latency:.6f} ms")

    print("\nBLOCKED REQUEST PERFORMANCE")
    print("----------------------------")
    print("Last Blocked Result:", blocked_success, blocked_reason)
    print(f"Blocked Mean Latency: {blocked_mean:.6f} ms")
    print(f"Blocked Median Latency: {blocked_median:.6f} ms")
    print(f"Blocked 95th Percentile: {blocked_p95:.6f} ms")

    return measurements

def run_repeated_performance_evaluation(batches=10, iterations=1000):

    print("\nREPEATED PERFORMANCE EVALUATION")
    print("------------------------------------")
    print("Batches:", batches)
    print("Iterations Per Batch:", iterations)

    batch_means = []

    for batch_number in range(1, batches + 1):

        context = create_experiment_context()

        robot_gateway = context["robot_gateway"]
        child_capsule = context["child"]
        robot = context["robot"]
        clock = context["clock"]

        clock.set_time("10:15")

        measurements = []

        for _ in range(iterations):

            start_time = time.perf_counter_ns()

            success, reason = robot_gateway.authorize_command(
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

            elapsed_ms = (end_time - start_time) / 1_000_000
            measurements.append(elapsed_ms)

        batch_mean = statistics.mean(measurements)
        batch_means.append(batch_mean)

        print(
            f"Batch {batch_number}: "
            f"{batch_mean:.6f} ms"
        )

    overall_mean = statistics.mean(batch_means)
    overall_median = statistics.median(batch_means)
    overall_stdev = statistics.stdev(batch_means)
    min_batch_mean = min(batch_means)
    max_batch_mean = max(batch_means)

    print("\nREPEATED PERFORMANCE SUMMARY")
    print("------------------------------------")
    print(f"Overall Mean: {overall_mean:.6f} ms")
    print(f"Median Batch Mean: {overall_median:.6f} ms")
    print(f"Standard Deviation Between Batches: {overall_stdev:.6f} ms")
    print(f"Minimum Batch Mean: {min_batch_mean:.6f} ms")
    print(f"Maximum Batch Mean: {max_batch_mean:.6f} ms")

    return batch_means