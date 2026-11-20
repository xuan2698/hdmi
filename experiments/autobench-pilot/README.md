# AutoBench S1 pilot

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
