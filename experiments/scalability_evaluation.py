import time
import statistics

from experiments.experiment_context import create_experiment_context


def run_scalability_evaluation():

    print("\nSCALABILITY EVALUATION")
    print("------------------------------------")

    workload_sizes = [
        100,
        500,
        1000,
        5000,
        10000
    ]

    results = []

    for workload_size in workload_sizes:

        context = create_experiment_context()

        robot_gateway = context["robot_gateway"]
        child_capsule = context["child"]
        robot = context["robot"]
        clock = context["clock"]

        clock.set_time("10:15")

        successful_requests = 0

        start_time = time.perf_counter()

        for _ in range(workload_size):

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

            if success:
                successful_requests += 1

        end_time = time.perf_counter()

        total_time = end_time - start_time

        average_latency_ms = (
            total_time / workload_size
        ) * 1000

        throughput = workload_size / total_time

        results.append({
            "workload": workload_size,
            "successful": successful_requests,
            "total_time": total_time,
            "average_latency_ms": average_latency_ms,
            "throughput": throughput
        })

        print(f"\nWorkload: {workload_size}")
        print(f"Successful Requests: {successful_requests}")
        print(f"Total Time: {total_time:.6f} seconds")
        print(
            f"Average Latency: "
            f"{average_latency_ms:.6f} ms/request"
        )
        print(
            f"Throughput: "
            f"{throughput:.2f} requests/second"
        )

    return results

def run_repeated_scalability_evaluation(batches=10):

    print("\nREPEATED SCALABILITY EVALUATION")
    print("------------------------------------")

    workload_sizes = [
        100,
        500,
        1000,
        5000,
        10000
    ]

    final_results = []

    for workload_size in workload_sizes:

        latency_batch_means = []
        throughput_batch_values = []

        print(f"\nWorkload: {workload_size}")

        for batch_number in range(1, batches + 1):

            context = create_experiment_context()

            robot_gateway = context["robot_gateway"]
            child_capsule = context["child"]
            robot = context["robot"]
            clock = context["clock"]

            clock.set_time("10:15")

            successful_requests = 0

            start_time = time.perf_counter()

            for _ in range(workload_size):

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

                if success:
                    successful_requests += 1

            end_time = time.perf_counter()

            total_time = end_time - start_time

            average_latency_ms = (
                total_time / workload_size
            ) * 1000

            throughput = workload_size / total_time

            if successful_requests != workload_size:
                raise RuntimeError(
                    "Not all legitimate requests were allowed."
                )

            latency_batch_means.append(
                average_latency_ms
            )

            throughput_batch_values.append(
                throughput
            )

            print(
                f"Batch {batch_number}: "
                f"{average_latency_ms:.6f} ms/request | "
                f"{throughput:.2f} requests/second"
            )

        mean_latency = statistics.mean(
            latency_batch_means
        )

        median_latency = statistics.median(
            latency_batch_means
        )

        latency_stdev = statistics.stdev(
            latency_batch_means
        )

        mean_throughput = statistics.mean(
            throughput_batch_values
        )

        throughput_stdev = statistics.stdev(
            throughput_batch_values
        )

        final_results.append({
            "workload": workload_size,
            "mean_latency_ms": mean_latency,
            "median_latency_ms": median_latency,
            "latency_stdev_ms": latency_stdev,
            "mean_throughput": mean_throughput,
            "throughput_stdev": throughput_stdev
        })

        print(f"Workload {workload_size} Summary:")
        print(
            f"Mean Latency: "
            f"{mean_latency:.6f} ms/request"
        )
        print(
            f"Median Latency: "
            f"{median_latency:.6f} ms/request"
        )
        print(
            f"Latency Standard Deviation: "
            f"{latency_stdev:.6f} ms"
        )
        print(
            f"Mean Throughput: "
            f"{mean_throughput:.2f} requests/second"
        )
        print(
            f"Throughput Standard Deviation: "
            f"{throughput_stdev:.2f}"
        )

    return final_results

if __name__ == "__main__":
    run_repeated_scalability_evaluation(
        batches=10
    )