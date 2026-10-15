import time
import statistics
import csv
import os
from concurrent.futures import ThreadPoolExecutor

from experiments.experiment_context import create_experiment_context

def run_concurrent_scalability_evaluation(
        worker_counts=None,
        requests_per_worker=100,
        batches=10
):
    print("\nCONCURRENT SCALABILITY EVALUATION")
    print("------------------------------------")

    if worker_counts is None:
        worker_counts = [1, 2, 4, 8, 16, 32]

    final_results = []

    for worker_count in worker_counts:

        batch_mean_latencies = []
        batch_p95_latencies = []
        batch_throughputs = []

        total_requests = (
            worker_count * requests_per_worker
        )

        print(
            f"\nConcurrent Workers: {worker_count}"
        )
        print(
            f"Requests Per Worker: {requests_per_worker}"
        )
        print(
            f"Total Requests Per Batch: {total_requests}"
        )

        for batch_number in range(1, batches + 1):

            context = create_experiment_context()

            robot_gateway = context["robot_gateway"]
            child_capsule = context["child"]
            robot = context["robot"]
            clock = context["clock"]

            clock.set_time("10:15")

            def authorize_request():

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

                elapsed_ms = (
                    end_time - start_time
                ) / 1_000_000

                return success, reason, elapsed_ms

            start_batch = time.perf_counter()

            with ThreadPoolExecutor(
                    max_workers=worker_count
            ) as executor:

                futures = []

                for _ in range(total_requests):
                    futures.append(
                        executor.submit(
                            authorize_request
                        )
                    )

                results = [
                    future.result()
                    for future in futures
                ]

            end_batch = time.perf_counter()

            successful_requests = sum(
                1
                for success, _, _ in results
                if success
            )

            if successful_requests != total_requests:
                failed_reasons = [
                    reason
                    for success, reason, _ in results
                    if not success
                ]

                raise RuntimeError(
                    "Not all legitimate concurrent requests "
                    f"were allowed. Failures: {failed_reasons}"
                )

            latencies = [
                latency
                for _, _, latency in results
            ]

            total_time = (
                end_batch - start_batch
            )

            mean_latency = statistics.mean(
                latencies
            )

            p95_latency = statistics.quantiles(
                latencies,
                n=100
            )[94]

            throughput = (
                total_requests / total_time
            )

            batch_mean_latencies.append(
                mean_latency
            )

            batch_p95_latencies.append(
                p95_latency
            )

            batch_throughputs.append(
                throughput
            )

            print(
                f"Batch {batch_number}: "
                f"mean={mean_latency:.6f} ms | "
                f"p95={p95_latency:.6f} ms | "
                f"throughput={throughput:.2f} req/s"
            )

        overall_mean_latency = statistics.mean(
            batch_mean_latencies
        )

        overall_p95_latency = statistics.mean(
            batch_p95_latencies
        )

        latency_stdev = statistics.stdev(
            batch_mean_latencies
        )

        mean_throughput = statistics.mean(
            batch_throughputs
        )

        throughput_stdev = statistics.stdev(
            batch_throughputs
        )

        final_results.append({
            "workers": worker_count,
            "requests_per_worker": requests_per_worker,
            "total_requests_per_batch": total_requests,
            "mean_latency_ms": overall_mean_latency,
            "mean_batch_p95_ms": overall_p95_latency,
            "latency_stdev_ms": latency_stdev,
            "mean_throughput": mean_throughput,
            "throughput_stdev": throughput_stdev
        })

        print(
            f"\nWorkers {worker_count} Summary:"
        )
        print(
            f"Mean Latency: "
            f"{overall_mean_latency:.6f} ms"
        )
        print(
            f"Mean Batch P95: "
            f"{overall_p95_latency:.6f} ms"
        )
        print(
            f"Between-Batch Latency SD: "
            f"{latency_stdev:.6f} ms"
        )
        print(
            f"Mean Throughput: "
            f"{mean_throughput:.2f} requests/second"
        )
        print(
            f"Throughput SD: "
            f"{throughput_stdev:.2f}"
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
        "concurrent_scalability_results.csv"
    )

    with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
    ) as csv_file:

        fieldnames = [
            "workers",
            "requests_per_worker",
            "total_requests_per_batch",
            "mean_latency_ms",
            "mean_batch_p95_ms",
            "latency_stdev_ms",
            "mean_throughput",
            "throughput_stdev"
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
    run_concurrent_scalability_evaluation(
        worker_counts=[1, 2, 4, 8, 16, 32],
        requests_per_worker=100,
        batches=10
    )