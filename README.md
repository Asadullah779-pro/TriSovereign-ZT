# TriSovereign-ZT

**TriSovereign-ZT: A Cross-Domain Zero-Trust Security Framework for Human–AI-Agent–Robot Workforces in Future Enterprises and Autonomous Cities**

## Overview

TriSovereign-ZT is a research prototype for enforcing bounded authority across workflows involving human principals, AI agents, digital resources, and robotic actuators.

The framework uses task-scoped Authority Capsules, a Transitive Authority Firewall (TAF), trusted task state, full-lineage validation, and execution-boundary gateways to prevent delegated authority from expanding beyond its authorized scope.

The prototype is evaluated primarily in a hospital logistics scenario in which AI agents delegate authority for medicine delivery and a simulated robot performs physical actions. A second smart-warehouse/logistics scenario evaluates cross-domain portability of the same core security architecture.

The repository includes legitimate and adversarial evaluations, a four-design authorization baseline comparison, component-ablation experiments, a systematic security attack matrix, performance and scalability evaluations, a four-model LLM-agent containment experiment, and a cross-domain warehouse evaluation.

## Repository Structure

```text
TriSovereign-ZT/
├── ablations/      # Security-component ablation implementations
├── agents/         # Agent-related prototype components
├── attacks/        # Controlled adversarial test cases
├── baselines/      # Alternative authorization designs used for comparison
├── data/           # Trial-level experimental data, including LLM outputs
├── experiments/    # Experimental and evaluation scripts
├── gateways/       # Tool/Data and Robot Gateway enforcement
├── results/        # Experimental result CSV and figure files
├── robot/          # Simulated robot components
├── security/       # Authority Capsules, TAF, trusted state, and security logic
├── tools/          # Prototype tool implementations
├── main.py         # Main prototype entry point
└── requirements.txt
```

Runtime logs and local development files are excluded from version control through `.gitignore`.

## Requirements and Installation

The prototype was developed and evaluated using Python 3.11.5.

### Python Setup

Create and activate a Python virtual environment, then install the required Python dependencies:

```bash
pip install -r requirements.txt
```

The current Python dependency is listed in `requirements.txt`.

### Local LLM Setup

The multi-model LLM-agent experiment uses Ollama through its local HTTP API. The reported evaluation uses four local models:

- `qwen3:1.7b`
- `llama3.2:3b`
- `gemma3:4b`
- `phi4-mini:3.8b`

Install Ollama separately and download the four models:

```bash
ollama pull qwen3:1.7b
ollama pull llama3.2:3b
ollama pull gemma3:4b
ollama pull phi4-mini:3.8b
```

Make sure Ollama is running before executing the LLM experiments. The prototype expects the Ollama API at:

```text
http://localhost:11434
```

The core authorization, baseline, ablation, security, performance, scalability, and cross-domain experiments do not require Ollama.

## Running the Experiments

Run commands from the repository root directory.

### Baseline Comparison

The baseline experiment compares four authorization designs:

- B1 Signed Local Authorization
- B2 Immediate-Parent Authorization
- B3 Root-Bounded Authorization
- B4 Full TriSovereign-ZT

The adversarial comparison contains 11 authority-drift cases, including nine direct authority-drift cases and two ancestor-tampering cases. Legitimate delegation and invalid-signature controls are also evaluated.

```bash
python experiments/baseline_comparison.py
```

The experiment writes its detailed results to:

```text
results/baseline_comparison_results.csv
```

In the reported adversarial comparison, B1 blocked 0/11 cases, B2 blocked 9/11, B3 blocked 10/11, and B4 blocked 11/11. These results apply to the implemented baseline test cases.

### Component Ablation Experiments

Four component-ablation experiments evaluate the contribution of scope containment, full-lineage validation, trusted task state, and Robot Gateway enforcement.

**Scope-containment ablation:**

```bash
python experiments/ablation_no_containment.py
```

**Full-lineage-validation ablation:**

```bash
python experiments/ablation_no_lineage.py
```

**Trusted-task-state ablation:**

```bash
python experiments/ablation_no_task_state.py
```

**Robot-Gateway-enforcement ablation:**

```bash
python experiments/ablation_no_gateway_enforcement.py
```

The corresponding CSV outputs are stored in the `results/` directory.

Across the implemented component-ablation cases, the full configuration blocked all 19 tested attacks, while the corresponding ablated configurations allowed the targeted attacks.

### Legitimate Request Evaluation

The legitimate-request suite evaluates eight authorized operations across the prototype workflow, including inventory access, door access, delivery-information access and update, and robot pickup, movement, and delivery operations.

```bash
python experiments/legitimate_request_suite.py
```

The suite reports the number of legitimate requests correctly allowed and the resulting false-block rate.

In the reported evaluation, all 8 implemented legitimate operations were allowed.

### Controlled Security Attack Evaluation

The controlled security evaluation contains 25 attack cases organized into five attack families:

1. Transitive Authority Drift
2. Unauthorized Delegation / Authority Expansion
3. Prompt-Injection-Induced Manipulation
4. Capsule Forgery / Tampering / Replay
5. Cross-Task Authority Misuse / Robot Manipulation

Each family contains five controlled attack cases. The evaluation checks both the authorization decision and the expected rejection reason.

```bash
python experiments/security_attack_evaluation.py
```

The script reports the total number of attacks, blocked and allowed attacks, exact test successes and failures, blocking rate, and exact test success rate.

In the reported evaluation, all 25 implemented controlled attacks were blocked with the expected outcomes. These results apply to the implemented attack cases and stated threat model and should not be interpreted as a general security guarantee.

### Systematic Security Attack Matrix

The systematic security matrix extends the controlled security evaluation across multiple security dimensions, delegation depths, attack positions, trusted task-state conditions, and execution-boundary checks.

The matrix contains 231 executions: 227 security/adversarial cases and 4 legitimate controls. The evaluated categories include lineage tampering, proposal-containment violations, trusted task-state violations, Robot Gateway enforcement, and Tool/Data Gateway enforcement.

```bash
python experiments/large_scale_attack_matrix.py
```

The detailed matrix is written to:

```text
results/large_scale_attack_matrix_results.csv
```

The experiment also produces:

```text
results/priority2_consolidated_security_results.csv
results/priority2_category_summary.csv
results/priority2_depth_summary.csv
results/priority2_rejection_reason_summary.csv
```

In the reported evaluation, all 227 security/adversarial cases were blocked and all 4 legitimate controls were allowed. These results apply to the implemented test matrix and stated threat model and should not be interpreted as a universal security guarantee.

### Security-Processing Performance

The security-cost experiment measures three prototype operations: full-lineage security validation, audit logging, and full Robot Gateway authorization.

Each operation is measured over 1,000 iterations.

```bash
python experiments/security_cost_evaluation.py
```

The script reports the mean, median, standard deviation, and 95th-percentile latency in milliseconds.

Performance measurements are environment-dependent and may vary across hardware, operating systems, background workloads, and repeated executions.

### Workload Scalability Evaluation

The workload-scalability experiment evaluates Robot Gateway authorization under increasing numbers of legitimate authorization requests.

The evaluated workload sizes are 100, 500, 1,000, 5,000, and 10,000 requests. Each workload is repeated across 10 batches.

```bash
python experiments/scalability_evaluation.py
```

The experiment reports mean and median authorization latency, latency standard deviation, mean throughput, and throughput standard deviation for each workload size.

Performance measurements are environment-dependent and may vary across systems and repeated executions.

### Concurrent Scalability Evaluation

The concurrent-scalability experiment evaluates legitimate Robot Gateway authorization under increasing concurrent request loads using Python threads.

The evaluated worker counts are 1, 2, 4, 8, 16, and 32. Each worker submits 100 authorization requests per batch, and each configuration is repeated across 10 batches.

```bash
python experiments/concurrent_scalability_evaluation.py
```

The experiment writes:

```text
results/concurrent_scalability_results.csv
```

The experiment reports authorization latency and wall-clock throughput statistics for each worker count.

These measurements characterize concurrent request load in the single-process Python prototype. They should not be interpreted as multicore or distributed-system scaling results, and performance is environment-dependent.

### Security-Path Performance Evaluation

The security-path performance experiment compares authorization-processing latency across one legitimate request path and seven rejected request paths:

- legitimate authorization
- cross-task misuse
- unauthorized robot identity
- unauthorized action
- unauthorized zone
- resource mismatch
- purpose mismatch
- destination mismatch

Each path is evaluated over 10 batches of 1,000 authorization calls.

```bash
python experiments/security_path_performance.py
```

The experiment writes:

```text
results/security_path_performance_results.csv
```

The experiment checks the expected authorization decision and rejection reason while measuring processing latency. The measurements show the cost of different implemented authorization paths and are environment-dependent.

### Delegation-Depth Scalability Evaluation

The delegation-depth experiment measures full-lineage validation latency as the Authority Capsule delegation chain becomes deeper.

The evaluated delegation depths are 1, 2, 5, 10, 20, and 50. For each depth, the experiment performs 10 batches of 1,000 lineage validations.

```bash
python experiments/delegation_depth_evaluation.py
```

The experiment reports the overall mean, median batch mean, standard deviation, minimum batch mean, and maximum batch mean validation latency for each delegation depth.

Performance measurements are environment-dependent and may vary across systems and repeated executions.

### Multi-Model LLM-Agent Containment Experiment

The repeated LLM evaluation uses five fixed scenarios: one legitimate scenario and four adversarial manipulation scenarios. Each scenario is executed 50 times per model.

The reported evaluation uses four local Ollama models: `qwen3:1.7b`, `llama3.2:3b`, `gemma3:4b`, and `phi4-mini:3.8b`. This produces 250 trials per model and 1,000 trials across the four-model evaluation. The reported experiments use temperature 0.7.

Make sure Ollama is running and the required models have been installed. Run each model separately from the repository root:

```bash
python experiments/llm_repeated_evaluation.py --model qwen3:1.7b
python experiments/llm_repeated_evaluation.py --model llama3.2:3b
python experiments/llm_repeated_evaluation.py --model gemma3:4b
python experiments/llm_repeated_evaluation.py --model phi4-mini:3.8b
```

The script writes model-specific checkpoint and final trial-level result files under `data/`. The final result files used by the multi-model analysis are:

```text
data/llm_repeated_results_qwen3_1.7b.csv
data/llm_repeated_results_llama3.2_3b.csv
data/llm_repeated_results_gemma3_4b.csv
data/llm_repeated_results_phi4-mini_3.8b.csv
```

After the four model runs are available, generate the multi-model summary with:

```bash
python experiments/analyze_llm_results.py
```

This writes:

```text
results/llm_multi_model_summary.csv
```

Generate the comparison figure with:

```bash
python experiments/visualize_llm_results.py
```

This writes:

```text
results/llm_multi_model_comparison.pdf
```

Across the reported 1,000 trials, the 800 adversarial prompts produced 784 observed parseable unauthorized proposals. All 784 observed unauthorized proposals were rejected by the security layer. The evaluation also contained 17 malformed model outputs, which were rejected before gateway authorization. The legitimate scenarios were accepted in 109 of 200 trials.

These results characterize containment under the tested models, prompts, scenarios, and prototype configuration; they should not be interpreted as a universal guarantee for arbitrary LLMs or prompts.

LLM generation is nondeterministic in this experiment and no model-generation seed is fixed. Therefore, rerunning the models may produce different trial-level responses from the archived reported results. The archived model-specific CSV files provide the trial-level outputs used for the reported evaluation.

### Cross-Domain Warehouse Evaluation

The warehouse experiment evaluates whether the same core TriSovereign-ZT architecture can be applied to a second controlled domain without changing its central authorization mechanisms.

The warehouse scenario models delegated authority for transferring `Package-X` from `Storage-A` to `Loading-Bay-2` using `Warehouse-R1`.

The evaluation contains one legitimate operation and eight security cases covering unauthorized zone, destination, resource, purpose, task, task-state, version, and action conditions.

```bash
python experiments/warehouse_cross_domain_evaluation.py
```

The experiment writes:

```text
results/warehouse_cross_domain_results.csv
```

In the reported evaluation, the legitimate warehouse operation was allowed and all 8 security cases were blocked with their expected rejection reasons.

This is a focused cross-domain portability evaluation rather than a second exhaustive security matrix. The current prototype evidence is therefore bounded to the implemented hospital and warehouse scenarios.

## Reproducibility Notes

The repository contains the scripts and result artifacts used for the reported prototype evaluations.

Non-LLM experiments are designed to be rerunnable from the repository root using the commands above. Performance measurements can vary across hardware, operating systems, Python runtime conditions, and background workloads.

The LLM evaluation depends on locally installed Ollama models and nondeterministic model generation. The archived model-specific trial-level CSV files should therefore be used when inspecting the exact LLM outputs underlying the reported multi-model results.

The reported security results describe the implemented test suites, attack matrices, scenarios, and threat model. They do not establish universal security against attacks outside the evaluated conditions.
