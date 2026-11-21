# AutoBench S1 pilot

The [v3 protocol and replay instructions](v3/README.md) cover the 17-task experiment with gated H scoring, complete checkers, and nine-proxy O feedback.

This pilot fixes the ordering of the 75 sequential AutoBench entries by upstream task number, then draws 25 with Python's `random.Random(42).sample`. The first two entries in [selected_tasks.json](selected_tasks.json) are the pilot tasks. [plan.json](plan.json) records the run parameters.

The driver supplies nonclock input vectors. The Python reference predicts each output at the sampled rising edge. Both sources come from DeepSeek V4.1 Flash and execute in separate Bubblewrap processes with a minimal filesystem and no network. The simulator replays the resulting vectors and captures DUT outputs. G comes from deterministic single-site edits of R1. Each compilable candidate is screened on three independent 2,000-cycle runs.

The evaluator keeps the official references and H in its own directory. It records the R1–R3 verdicts independently. The checker-generation prompt receives the public spec and interface, its own previous source when applicable, and approved scenario observations. The stimulus-generation prompt may include R1 mutation lines and instrumentation observations.

For each H entry the results preserve both the raw checker failure and the count of mismatch signal/cycle pairs absent on the golden RTL. Use the separate golden verdict when interpreting detection on a configuration that also rejects the golden RTL.

Initial requests used a 4,096-token cap and the provider's default reasoning setting. The pilot retained complete artifacts from those requests. Truncated work resumed with an 8,192-token cap and low reasoning. Later connection recovery used streamed output. The final two configurations finished after resuming with the request options in [recovery.json](recovery.json). Each request log records its actual settings. The CSV includes elapsed time for successful initialization and the final run segment, and separately totals all recorded HTTP attempt durations including earlier failures.

## Resume on Linux

Use a Linux environment with Python 3, Git, a working Bubblewrap installation with user namespaces, and Icarus Verilog. Configure `OPENCODE_GO_API_KEY` through the environment's secret settings before requesting new generation.

```bash
cd experiments/autobench-pilot
./setup.sh
python3 run_pilot.py
```

The committed inputs already support pilot resume. To rebuild them from the pinned AutoBench and CorrectBench checkouts, use `python3 prepare.py` after setup. A completed task/configuration has its own commit, immutable run artifacts, and an entry in the corresponding task checkpoint. The runner skips completed entries. It checks a fingerprint of the plan before resuming.

Run `python3 report.py` after all results exist to regenerate the aggregate metrics, the ten-prompt audit, and the public Go catalog snapshot. The replay harness currently samples a single rising-edge clock. Tasks requiring other clock edges or timing patterns need separate handling before the full study.

## Second pilot protocol

The locked request configuration lives in [pilot2.json](pilot2.json). Every v2 phase uses the same model, streaming mode, thinking toggle, temperature, output limit, socket timeout and retry policy. JSONL records both truncation and retries. Completed trial checkpoints include the protocol fingerprint.

The evaluator pre-screens all official H mutants with the three configured seeds and 2,000 cycles per seed. Clocked screens sample before and after the active edge and after the opposite edge. The baseline and official sources use the same Icarus/4-state replay. Compile errors are recorded as invalid. Exact sample agreement for all seeds is evidence of suspected equivalence. The detailed classifications stay on the evaluation side and are never supplied as generation feedback.

A calibration trial is an independent A0 run using the configured calibration seed. Retain a task only when the calibrated H detection rate is below 100% and H has at least one valid retained mutant. Unscorable tasks are recorded separately. If fewer than 15 tasks qualify in the original 25, apply the same rule to all 75 sequential tasks. The second pilot comes from a deterministic draw of six eligible tasks with the configured selection seed. This is the fixed selection rule for subsequent experiments.

Stimulus revisions are append-only. The runner appends a separately generated suffix and verifies that every previous observation remains exposed. It reports both the raw rate in the currently active G set and each round's rate on the fixed final G set. The raw rate can decrease when an unsolved cohort is admitted. The fixed-set measure is the comparable nondecreasing trajectory.

Guided configurations activate a deeper screened cohort when all active mutants have been exposed. New cohorts favor multiple sites, separate state assignments and timing-sensitive edits. The runner stops at the round cap or after two consecutive newly introduced cohorts are fully exposed. A0 is a single-round control. The checker categories count each qualifying mutant/cycle/output observation and keep R1-bug findings out of revision evidence. Evaluation of H for the full round history starts after that configuration has finished generating. Detection requires a checker mismatch absent at the same cycle/output on the golden RTL.

The proxy simulator first compiles the original CorrectBench RTL. If Icarus rejects an enum assignment for requiring a cast, it retries that proxy with a width-preserving vector encoding and the same state constants. The repository retains the original sources. The evaluator compiles golden and official variants as supplied, so this proxy accommodation carries no effect into H.

Reach and infection feedback uses source-site probes. Their synthesized guards are approximate for complex nested branches and case arms. Retained G and H exposure verdicts use actual replayed outputs and remain independent of those probe labels.

Run the v2 stages from this directory after installing the tools and configuring the environment secret.

```bash
python3 pilot2_prepare.py
python3 pilot2_evaluation.py
python3 pilot2_run.py calibrate
python3 pilot2_run.py rerun
python3 pilot2_run.py second
python3 pilot2_report.py
```
