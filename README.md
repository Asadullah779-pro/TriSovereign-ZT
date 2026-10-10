# TriSovereign-ZT

**TriSovereign-ZT: A Cross-Domain Zero-Trust Security Framework for Human–AI-Agent–Robot Workforces in Future Enterprises and Autonomous Cities**

## Overview

TriSovereign-ZT is a research prototype for enforcing bounded authority across workflows involving human principals, AI agents, digital resources, and robotic actuators.

The framework uses task-scoped Authority Capsules, a Transitive Authority Firewall (TAF), trusted task state, full-lineage validation, and execution-boundary gateways to prevent delegated authority from expanding beyond its authorized scope.

The prototype is evaluated using a hospital logistics scenario in which AI agents delegate authority for medicine delivery and a simulated robot performs physical actions. The repository includes controlled legitimate and adversarial experiments, a Signed Local Authorization baseline, component-ablation experiments, LLM-agent containment experiments, and performance/scalability evaluation.

## Repository Structure

```text
TriSovereign-ZT/
├── ablations/      # Security-component ablation implementations
├── agents/         # Agent-related prototype components
├── attacks/        # Controlled adversarial test cases
├── baselines/      # Signed Local Authorization baseline
├── data/           # Data used by experiments, where applicable
├── experiments/    # Experimental and evaluation scripts
├── gateways/       # Tool/Data and Robot Gateway enforcement
├── results/        # Experimental result CSV files
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

The LLM-agent experiment uses Ollama with the `qwen3:1.7b` model through Ollama's local HTTP API.

Install Ollama separately and download the model:

```bash
ollama pull qwen3:1.7b
```

Make sure Ollama is running before executing the LLM experiments. The prototype expects the Ollama API at:

```text
http://localhost:11434
```

The core authorization, baseline, ablation, and non-LLM experiments do not require Ollama.

## Running the Experiments

Run commands from the repository root directory.

### Baseline Comparison

The baseline experiment compares TriSovereign-ZT with the Signed Local Authorization baseline across nine controlled authority-drift cases.

```bash
python experiments/baseline_comparison.py
```

The experiment writes its detailed results to:

```text
results/baseline_comparison_results.csv
```

### Component Ablation Experiments

The four component-ablation experiments can be executed separately.

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

### LLM-Agent Containment Experiment

The repeated LLM evaluation uses five fixed scenarios: one legitimate scenario and four adversarial manipulation scenarios. Each scenario is executed 50 times, producing 250 trials in total.

The experiment uses the local `qwen3:1.7b` model through Ollama with temperature 0.7.

Make sure Ollama is running and the model has been installed before executing:

```bash
python experiments/llm_repeated_evaluation.py
```

The experiment writes a checkpoint during execution and saves the final trial-level results to:

```text
data/llm_repeated_results.csv
```

Because LLM generation may be nondeterministic and the current experiment does not fix a model-generation seed, reproduced LLM outputs may differ from the reported trial-level outputs.

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

### Delegation-Depth Scalability Evaluation

The delegation-depth experiment measures full-lineage validation latency as the Authority Capsule delegation chain becomes deeper.

The evaluated delegation depths are 1, 2, 5, 10, 20, and 50. For each depth, the experiment performs 10 batches of 1,000 lineage validations.

```bash
python experiments/delegation_depth_evaluation.py
```

The experiment reports the overall mean, median batch mean, standard deviation, minimum batch mean, and maximum batch mean validation latency for each delegation depth.

Performance measurements are environment-dependent and may vary across systems and repeated executions.

### Legitimate Request Evaluation

The legitimate-request suite evaluates eight authorized operations across the prototype workflow, including inventory access, door access, delivery-information access and update, and robot pickup, movement, and delivery operations.

```bash
python experiments/legitimate_request_suite.py
```

The suite reports the number of legitimate requests correctly allowed and the resulting false-block rate.

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

The reported prototype evaluation blocked all 25 controlled attacks. These results apply to the implemented attack cases and stated threat model and should not be interpreted as a general security guarantee.