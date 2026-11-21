import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import pilot3_generate as generation
from simulate import RunError


class GenerationRetryTests(unittest.TestCase):
    def test_revision_evidence_survives_a_validation_retry(self):
        for role in ("checker", "stimulus"):
            with self.subTest(role=role), tempfile.TemporaryDirectory() as directory:
                task = {"spec": "Example public spec"}
                pins = ({"data": 1}, {"value": 1}, "clk", "posedge")
                request = Mock(side_effect=["invalid first answer", "corrected answer"])
                validator = Mock(side_effect=[RunError("first answer failed validation"), ["validated"]])
                plan = {"check_regenerations": 2, "compile_repairs": 2, "append_cycles": 32}
                with patch.object(generation, "public", return_value=(task, pins)), patch.object(
                    generation, "request", request
                ):
                    result = generation.generate(
                        Path(directory), role, 2, "example", plan, 10, validator,
                        evidence="Original diagnostic from this round.",
                    )

                self.assertEqual(result, ("corrected answer", ["validated"], 1))
                initial, retry = [call.args[1] for call in request.call_args_list]
                self.assertIn("Original diagnostic from this round.", initial)
                self.assertIn("Original diagnostic from this round.", retry)
                self.assertIn("invalid first answer", retry)
                self.assertIn("first answer failed validation", retry)


if __name__ == "__main__":
    unittest.main()
