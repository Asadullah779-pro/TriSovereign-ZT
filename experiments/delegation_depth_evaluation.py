import time
import statistics

from experiments.experiment_context import create_experiment_context


def run_delegation_depth_evaluation(iterations=1000):

    print("\nDELEGATION DEPTH EVALUATION")
    print("------------------------------------")

    depths = [1, 2, 5, 10, 20, 50]

    results = []

    for depth in depths:

        context = create_experiment_context()

        manager = context["manager"]
        registry = context["registry"]
        taf = context["taf"]
        root = context["root"]

        current_parent = root

        # Build the delegation chain.
        for level in range(1, depth + 1):

            child = manager.create_capsule(
                task_id=current_parent.task_id,
                original_issuer=current_parent.original_issuer,
                current_holder=f"Depth-Agent-{level}",
                parent_capsule_id=current_parent.capsule_id,
                resource=current_parent.resource,
                source=current_parent.source,
                destination=current_parent.destination,
                purpose=current_parent.purpose,
                allowed_actions=current_parent.allowed_actions.copy(),
                allowed_zones=current_parent.allowed_zones.copy(),
                allowed_data=current_parent.allowed_data.copy(),
                authorized_robot=current_parent.authorized_robot,
                valid_from=current_parent.valid_from,
                valid_until=current_parent.valid_until,
                can_delegate=True,
                version=current_parent.version
            )

            registry.register_capsule(child)

            current_parent = child

        deepest_capsule = current_parent

        measurements = []

        last_allowed = False
        last_reason = None

        for _ in range(iterations):

            start_time = time.perf_counter_ns()

            allowed, reason = taf.validate_full_lineage(
                deepest_capsule
            )

            end_time = time.perf_counter_ns()

            elapsed_ms = (
                end_time - start_time
            ) / 1_000_000

            measurements.append(elapsed_ms)

            last_allowed = allowed
            last_reason = reason

        mean_latency = statistics.mean(measurements)
        median_latency = statistics.median(measurements)

        p95_latency = statistics.quantiles(
            measurements,
            n=100
        )[94]

        results.append({
            "depth": depth,
            "mean_latency_ms": mean_latency,
            "median_latency_ms": median_latency,
            "p95_latency_ms": p95_latency
        })

        print(f"\nDelegation Depth: {depth}")
        print(
            "Lineage Result:",
            last_allowed,
            last_reason
        )
        print(
            f"Mean Validation Latency: "
            f"{mean_latency:.6f} ms"
        )
        print(
            f"Median Validation Latency: "
            f"{median_latency:.6f} ms"
        )
        print(
            f"95th Percentile: "
            f"{p95_latency:.6f} ms"
        )

    return results

def run_repeated_delegation_depth_evaluation(
        batches=10,
        iterations=1000
):

    print("\nREPEATED DELEGATION DEPTH EVALUATION")
    print("------------------------------------")

    depths = [1, 2, 5, 10, 20, 50]

    final_results = []

    for depth in depths:

        batch_means = []

        print(f"\nDelegation Depth: {depth}")

        for batch_number in range(1, batches + 1):

            context = create_experiment_context()

            manager = context["manager"]
            registry = context["registry"]
            taf = context["taf"]
            root = context["root"]

            current_parent = root

            # Build a fresh authority chain for this batch.
            for level in range(1, depth + 1):

                child = manager.create_capsule(
                    task_id=current_parent.task_id,
                    original_issuer=current_parent.original_issuer,
                    current_holder=f"Depth-Agent-{level}",
                    parent_capsule_id=current_parent.capsule_id,
                    resource=current_parent.resource,
                    source=current_parent.source,
                    destination=current_parent.destination,
                    purpose=current_parent.purpose,
                    allowed_actions=current_parent.allowed_actions.copy(),
                    allowed_zones=current_parent.allowed_zones.copy(),
                    allowed_data=current_parent.allowed_data.copy(),
                    authorized_robot=current_parent.authorized_robot,
                    valid_from=current_parent.valid_from,
                    valid_until=current_parent.valid_until,
                    can_delegate=True,
                    version=current_parent.version
                )

                registry.register_capsule(child)
                current_parent = child

            deepest_capsule = current_parent

            measurements = []

            for _ in range(iterations):

                start_time = time.perf_counter_ns()

                allowed, reason = taf.validate_full_lineage(
                    deepest_capsule
                )

                end_time = time.perf_counter_ns()

                if not allowed:
                    raise RuntimeError(
                        f"Lineage validation failed: {reason}"
                    )

                elapsed_ms = (
                    end_time - start_time
                ) / 1_000_000

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

        final_results.append({
            "depth": depth,
            "mean_ms": overall_mean,
            "median_ms": overall_median,
            "stdev_ms": overall_stdev,
            "min_batch_mean_ms": min(batch_means),
            "max_batch_mean_ms": max(batch_means)
        })

        print(f"Depth {depth} Summary:")
        print(
            f"Overall Mean: "
            f"{overall_mean:.6f} ms"
        )
        print(
            f"Median Batch Mean: "
            f"{overall_median:.6f} ms"
        )
        print(
            f"Standard Deviation: "
            f"{overall_stdev:.6f} ms"
        )
        print(
            f"Minimum Batch Mean: "
            f"{min(batch_means):.6f} ms"
        )
        print(
            f"Maximum Batch Mean: "
            f"{max(batch_means):.6f} ms"
        )

    return final_results

if __name__ == "__main__":
    run_repeated_delegation_depth_evaluation(
        batches=10,
        iterations=1000
    )