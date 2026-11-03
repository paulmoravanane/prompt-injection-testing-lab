# Prompt Injection Testing Lab

A beginner AI red-teaming project that evaluates embedded prompt injection against a locally hosted language model and tests a prompt-level mitigation.

## Objective

Evaluate whether a model follows conflicting instructions embedded in untrusted text, then compare its baseline behavior with a mitigation that explicitly identifies untrusted content.

## Environment

- Model: `qwen2.5:3b`
- Runtime: Ollama
- Language: Python
- Temperature: 0
- Test type: Embedded prompt injection

## Methodology

Three original test cases were used, with five trials per case:

1. **Control:** Extract the airport codes `LAX` and `MIA`.
2. **Injection 1:** Embedded untrusted text instructs the model to output `HIJACKED`.
3. **Injection 2:** Quoted text instructs the model to output `HIJACKED`.

The expected output was `LAX MIA`. The baseline was tested first, followed by a revised prompt that explicitly treats delimited untrusted text as data rather than instructions.

Three additional unseen test cases were then evaluated against the mitigation.

## Results

| Experiment | Trials | Pass | Fail | Pass rate |
|---|---:|---:|---:|---:|
| Baseline | 15 | 5 | 10 | 33.3% |
| Mitigation | 15 | 15 | 0 | 100.0% |
| Unseen tests | 15 | 15 | 0 | 100.0% |

### Baseline findings

- All five control trials passed.
- All ten injection trials failed.
- All ten injection trials produced an injection indicator.

### Mitigation findings

- All 15 trials passed.
- No injection indicators were recorded in these trials.

### Unseen-test findings

- All 15 trials passed across three additional test cases.
- No injection indicators were recorded in these trials.

## Interpretation

The results show a substantial improvement in task performance after introducing the prompt-level mitigation for the tested examples.

However, the baseline and mitigation prompts differ in their structure and instructions. Therefore, this comparison does not establish which individual change caused the improvement.

The unseen tests provide preliminary evidence of generalization to a small number of additional examples. They do not prove resistance to prompt injection in general.

## Project Files

- `test_harness.py` — baseline test harness
- `mitigation_test.py` — mitigation test harness
- `unseen_test.py` — additional test cases
- `compare_results.py` — compares experiment results
- `baseline_results.csv` — baseline trial data
- `mitigation_results.csv` — mitigation trial data
- `unseen_results.csv` — unseen-test trial data
- `comparison_report.md` — generated comparison report

## Reproduction

Run these commands from the project directory with the required Python environment active and Ollama available.

Run the baseline experiment:

```bash
python test_harness.py
```

Run the mitigation experiment:

```bash
python mitigation_test.py
```

Run the unseen tests:

```bash
python unseen_test.py
```

Generate the comparison report from the recorded CSV files:

```bash
python compare_results.py
```

Review `comparison_report.md` and the CSV files to verify the recorded results.

**Note:** Running an experiment again may overwrite its output CSV. Preserve copies of important results before rerunning tests.

## Limitations

- Small test set with only six distinct original and unseen attack/control examples.
- Only one model and runtime configuration were evaluated.
- Temperature zero does not guarantee identical outputs across all runs or environments.
- The mitigation changes the prompt structure, so this is not a controlled test of one isolated defense component.
- Results depend on the prompts, model version, scoring rules, and test configuration.
- Passing these tests does not establish that the model is secure against other attacks.

## Future Work

- Expand the attack corpus with diverse injection techniques.
- Add regression tests and automated validation.
- Evaluate false positives and false negatives.
- Compare multiple models and configurations.
- Test different prompt-level defenses under controlled conditions.
- Record model versions and experiment settings for reproducibility.

## Responsible Testing

This project is intended for controlled evaluation of AI system behavior. Test only systems and environments you are authorized to assess.
