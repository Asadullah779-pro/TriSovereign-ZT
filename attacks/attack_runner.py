class AttackRunner:

    def __init__(self):
        self.results = []

    def record_result(
            self,
            attack_category,
            attack_variant,
            expected_result,
            actual_result,
            reason,
            expected_reason=None
    ):
        result_correct = (
                expected_result == actual_result
        )

        reason_correct = (
                expected_reason is None
                or expected_reason == reason
        )

        success = (
                result_correct
                and reason_correct
        )

        result = {
            "attack_category": attack_category,
            "attack_variant": attack_variant,
            "expected_result": expected_result,
            "actual_result": actual_result,
            "expected_reason": expected_reason,
            "reason": reason,
            "test_success": success
        }

        self.results.append(result)

        return result

    def show_results(self):
        print("\nATTACK RUNNER RESULTS")
        print("----------------------------")

        for result in self.results:
            print(
                result["attack_category"],
                "|",
                result["attack_variant"],
                "| Expected:",
                result["expected_result"],
                "| Actual:",
                result["actual_result"],
                "| Expected Reason:",
                result["expected_reason"],
                "| Actual Reason:",
                result["reason"],
                "| Success:",
                result["test_success"]
            )

    def get_results(self):
        return self.results

    def get_summary(self):
        total_attacks = len(self.results)

        blocked_attacks = sum(
            1
            for result in self.results
            if result["actual_result"] == "BLOCK"
        )

        allowed_attacks = sum(
            1
            for result in self.results
            if result["actual_result"] == "ALLOW"
        )

        successful_tests = sum(
            1
            for result in self.results
            if result["test_success"]
        )

        failed_tests = (
                total_attacks - successful_tests
        )

        if total_attacks == 0:
            blocking_rate = 0
            exact_test_success_rate = 0
        else:
            blocking_rate = (
                                    blocked_attacks / total_attacks
                            ) * 100

            exact_test_success_rate = (
                                              successful_tests / total_attacks
                                      ) * 100

        return {
            "total_attacks": total_attacks,
            "blocked_attacks": blocked_attacks,
            "allowed_attacks": allowed_attacks,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "blocking_rate": blocking_rate,
            "exact_test_success_rate": exact_test_success_rate
        }