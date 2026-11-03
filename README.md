# Prompt Injection Testing Lab

A Python-based AI red-teaming project for evaluating embedded prompt injection against a locally hosted language model and measuring the effect of a prompt-level mitigation.

The project compares baseline behavior, mitigation performance, and performance on additional unseen test cases using repeatable experiments and CSV-based evaluation.

## Project Overview

**Objective:** Investigate whether untrusted text containing conflicting instructions can cause a language model to deviate from its intended task.

The lab evaluates a baseline prompt, applies a mitigation that explicitly treats delimited untrusted content as data, and compares the recorded results.

### Technology Stack

- **Model:** Qwen 2.5 3B (`qwen2.5:3b`)
- **Runtime:** Ollama
- **Language:** Python
- **Temperature:** 0
- **Technique:** Embedded prompt injection testing
- **Evaluation:** Repeated trials, CSV records, and an automated comparison report

## How It Works

1. Establish a baseline using a task that extracts airport codes.
2. Introduce untrusted text containing conflicting instructions.
3. Record model responses and evaluate them against the expected output.
4. Apply a prompt-level mitigation that identifies untrusted content.
5. Evaluate the mitigation against the original cases and additional unseen cases.
6. Compare the recorded results using a Python script.

The expected task output is `LAX MIA`. Injection examples attempt to redirect the model to output `HIJACKED`.

## Experimental Results

The following results were recorded by the project's comparison script.

| Experiment | Trials | Passed | Failed | Errors | Pass rate |
|---|---:|---:|---:|---:|---:|
| Baseline | 15 | 5 | 10 | 0 | 33.3% |
| Mitigation | 15 | 15 | 0 | 0 | 100.0% |
| Unseen tests | 15 | 15 | 0 | 0 | 100.0% |

### Key Findings

- **Baseline:** All five control trials passed, while all ten injection trials failed.
- **Mitigation:** All 15 recorded trials passed, with no injection indicators reported.
- **Unseen tests:** All 15 recorded trials passed across three additional test cases, with no injection indicators reported.

These findings indicate improved task performance on the evaluated examples after introducing the mitigation.

> **Important:** These results apply only to the tested prompts, model, and configuration. They do not demonstrate universal protection against prompt injection.

## Project Structure

| File | Purpose |
|---|---|
| `test_harness.py` | Baseline evaluation harness |
| `mitigation_test.py` | Mitigation evaluation harness |
| `unseen_test.py` | Evaluation using additional test cases |
| `compare_results.py` | Summarizes and compares recorded results |
| `baseline_results.csv` | Baseline trial records |
| `mitigation_results.csv` | Mitigation trial records |
| `unseen_results.csv` | Additional test trial records |
| `automated_results.csv` | Additional automated test results |
| `automated_repeated_results.csv` | Repeated automated test results |
| `comparison_report.md` | Generated experiment comparison |
| `results.md` | Evaluation notes and results |
| `.gitignore` | Files and directories excluded from Git |

## Setup

### Prerequisites

- Python 3
- Git
- Ollama installed and running
- The `qwen2.5:3b` model available locally

Pull the model if it is not already installed:

```bash
ollama pull qwen2.5:3b
```

From the project directory, activate your existing virtual environment if you have one:

```bash
source .venv/bin/activate
```

If you do not have a virtual environment yet, create one:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Check Python and Ollama:

```bash
python --version
ollama --version
ollama list
```

Install any Python dependencies required by the scripts. Check the imports in the scripts first; this repository does not currently document a dependency lockfile or `requirements.txt`.

## Run the Experiments

Run each command from the project directory with the required environment active and Ollama available.

### 1. Baseline

```bash
python test_harness.py
```

### 2. Mitigation

```bash
python mitigation_test.py
```

### 3. Additional Unseen Tests

```bash
python unseen_test.py
```

### 4. Generate the Comparison Report

```bash
python compare_results.py
```

Inspect `comparison_report.md` and the corresponding CSV files to verify the results.

**Reproducibility note:** Experiment scripts may overwrite their output files. Back up important CSV results before rerunning experiments. The comparison script summarizes the recorded CSV data; it does not independently prove that the experiments were executed correctly.

## Methodology and Limitations

- Three original test cases were evaluated with five trials per case.
- Three additional unseen test cases were evaluated with five trials per case.
- Only one model and runtime configuration were tested.
- The baseline and mitigation prompts differ in structure and instructions, so the comparison does not isolate the effect of one defense component.
- The test corpus is small and may not represent the diversity of real-world prompt injection attacks.
- Temperature zero does not guarantee identical behavior across different model versions or environments.
- Results depend on the prompt design, model version, scoring logic, and evaluation procedure.
- Passing these tests does not establish resistance to other attacks, false-positive rates, or production readiness.

## Future Improvements

- Expand the test corpus with diverse direct and indirect injection cases.
- Add automated assertions and regression testing.
- Measure false positives and false negatives.
- Compare multiple models and defense strategies under controlled conditions.
- Record model versions, dependencies, and configuration details.
- Add reproducible test fixtures and continuous integration.

## Responsible Testing

This project is intended for controlled AI security evaluation and educational use. Test only systems you own or are explicitly authorized to assess.

## Author

**Moravanane Paul Manikanta**

GitHub: [@paulmoravanane](https://github.com/paulmoravanane)

---

*An educational AI red-teaming project exploring prompt injection, evaluation methodology, and prompt-level defenses.*
