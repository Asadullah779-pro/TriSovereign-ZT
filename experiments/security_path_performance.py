import time
import statistics
import csv
import os

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


def _measure_path(
        robot_gateway,
        capsule,
        robot_id,
        requested_action,
        requested_zone,
        requested_task_id,
        requested_resource,
        requested_purpose,
        requested_destination,
        iterations,
        expected_success,
        expected_reason=None
):
    measurements = []

    last_success = None
    last_reason = None

    for _ in range(iterations):

        start_time = time.perf_counter_ns()

        success, reason = robot_gateway.authorize_command(
            capsule=capsule,
            robot_id=robot_id,
            requested_action=requested_action,
            requested_zone=requested_zone,
            requested_task_id=requested_task_id,
            requested_resource=requested_resource,
            requested_purpose=requested_purpose,
            requested_destination=requested_destination
        )

        end_time = time.perf_counter_ns()

        if success != expected_success:
            raise RuntimeError(
                f"Unexpected authorization result: "
                f"{success}, {reason}"
            )

        if (
            expected_reason is not None
            and reason != expected_reason
        ):
            raise RuntimeError(
                f"Unexpected rejection reason: "
                f"{reason}. "
                f"Expected: {expected_reason}"
            )

        measurements.append(
            (end_time - start_time) / 1_000_000
        )

        last_success = success
        last_reason = reason

    return (
        _calculate_stats(measurements),
        last_success,
        last_reason
    )


def run_security_path_performance(
        batches=10,
        iterations=1000
):
    print("\nSECURITY PATH PERFORMANCE EVALUATION")
    print("------------------------------------")
    print("Batches:", batches)
    print("Iterations Per Batch:", iterations)

    path_names = [
        "legitimate",
        "cross_task",
        "robot_identity",
        "action",
        "zone",
        "resource",
        "purpose",
        "destination"
    ]

    batch_results = {
        path_name: []
        for path_name in path_names
    }

    for batch_number in range(1, batches + 1):

        print(f"\nBatch {batch_number}")

        context = create_experiment_context()

        robot_gateway = context["robot_gateway"]
        child = context["child"]
        robot = context["robot"]
        clock = context["clock"]

        clock.set_time("10:15")

        test_cases = [
            {
                "name": "legitimate",
                "robot_id": robot.robot_id,
                "action": "CARRY",
                "zone": "Corridor-A",
                "task_id": child.task_id,
                "resource": child.resource,
                "purpose": child.purpose,
                "destination": child.destination,
                "expected_success": True,
                "expected_reason": None
            },
            {
                "name": "cross_task",
                "robot_id": robot.robot_id,
                "action": "CARRY",
                "zone": "Corridor-A",
                "task_id": "TASK-OTHER",
                "resource": child.resource,
                "purpose": child.purpose,
                "destination": child.destination,
                "expected_success": False,
                "expected_reason":
                    "CROSS_TASK_AUTHORITY_MISUSE"
            },
            {
                "name": "robot_identity",
                "robot_id": "Robot-Unauthorized",
                "action": "CARRY",
                "zone": "Corridor-A",
                "task_id": child.task_id,
                "resource": child.resource,
                "purpose": child.purpose,
                "destination": child.destination,
                "expected_success": False,
                "expected_reason":
                    "ROBOT_NOT_AUTHORIZED"
            },
            {
                "name": "action",
                "robot_id": robot.robot_id,
                "action": "DELETE_RECORD",
                "zone": "Corridor-A",
                "task_id": child.task_id,
                "resource": child.resource,
                "purpose": child.purpose,
                "destination": child.destination,
                "expected_success": False,
                "expected_reason":
                    "ROBOT_ACTION_NOT_ALLOWED"
            },
            {
                "name": "zone",
                "robot_id": robot.robot_id,
                "action": "CARRY",
                "zone": "Restricted-Storage",
                "task_id": child.task_id,
                "resource": child.resource,
                "purpose": child.purpose,
                "destination": child.destination,
                "expected_success": False,
                "expected_reason":
                    "ROBOT_ZONE_NOT_ALLOWED"
            },
            {
                "name": "resource",
                "robot_id": robot.robot_id,
                "action": "CARRY",
                "zone": "Corridor-A",
                "task_id": child.task_id,
                "resource": "Medicine-Y",
                "purpose": child.purpose,
                "destination": child.destination,
                "expected_success": False,
                "expected_reason":
                    "RESOURCE_MISMATCH"
            },
            {
                "name": "purpose",
                "robot_id": robot.robot_id,
                "action": "CARRY",
                "zone": "Corridor-A",
                "task_id": child.task_id,
                "resource": child.resource,
                "purpose": "UNAUTHORIZED_PURPOSE",
                "destination": child.destination,
                "expected_success": False,
                "expected_reason":
                    "PURPOSE_MISMATCH"
            },
            {
                "name": "destination",
                "robot_id": robot.robot_id,
                "action": "CARRY",
                "zone": "Corridor-A",
                "task_id": child.task_id,
                "resource": child.resource,
                "purpose": child.purpose,
                "destination": "Room-999",
                "expected_success": False,
                "expected_reason":
                    "DESTINATION_MISMATCH"
            }
        ]

        for test_case in test_cases:

            stats, success, reason = _measure_path(
                robot_gateway=robot_gateway,
                capsule=child,
                robot_id=test_case["robot_id"],
                requested_action=test_case["action"],
                requested_zone=test_case["zone"],
                requested_task_id=test_case["task_id"],
                requested_resource=test_case["resource"],
                requested_purpose=test_case["purpose"],
                requested_destination=test_case["destination"],
                iterations=iterations,
                expected_success=
                    test_case["expected_success"],
                expected_reason=
                    test_case["expected_reason"]
            )

            batch_results[
                test_case["name"]
            ].append(stats["mean"])

            print(
                f"{test_case['name']}: "
                f"result={success} | "
                f"reason={reason} | "
                f"mean={stats['mean']:.6f} ms | "
                f"p95={stats['p95']:.6f} ms"
            )

    print("\nSECURITY PATH SUMMARY")
    print("------------------------------------")

    final_results = []

    for path_name in path_names:
        means = batch_results[path_name]

        overall_mean = statistics.mean(means)
        overall_median = statistics.median(means)
        overall_stdev = statistics.stdev(means)

        final_results.append({
            "path": path_name,
            "mean_ms": overall_mean,
            "median_batch_mean_ms": overall_median,
            "between_batch_stdev_ms": overall_stdev,
            "min_batch_mean_ms": min(means),
            "max_batch_mean_ms": max(means)
        })

        print(f"\nPath: {path_name}")
        print(
            f"Overall Mean: "
            f"{overall_mean:.6f} ms"
        )
        print(
            f"Median Batch Mean: "
            f"{overall_median:.6f} ms"
        )
        print(
            f"Between-Batch SD: "
            f"{overall_stdev:.6f} ms"
        )
        print(
            f"Minimum Batch Mean: "
            f"{min(means):.6f} ms"
        )
        print(
            f"Maximum Batch Mean: "
            f"{max(means):.6f} ms"
        )

    # Save summary results to CSV
    results_directory = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "results"
    )

    os.makedirs(
        results_directory,
        exist_ok=True
    )

    output_file = os.path.join(
        results_directory,
        "security_path_performance_results.csv"
    )

    with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
    ) as csv_file:

        fieldnames = [
            "path",
            "mean_ms",
            "median_batch_mean_ms",
            "between_batch_stdev_ms",
            "min_batch_mean_ms",
            "max_batch_mean_ms"
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(final_results)

    print(
        f"\nResults saved to: {output_file}"
    )

    return final_results


if __name__ == "__main__":
    run_security_path_performance(
        batches=10,
        iterations=1000
    )