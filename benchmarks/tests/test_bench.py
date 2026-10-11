import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('bench', Path(__file__).resolve().parents[1] / 'bench.py')
bench = importlib.util.module_from_spec(spec)
sys.modules['bench'] = bench
spec.loader.exec_module(bench)


class HarnessTests(unittest.TestCase):
    def test_codex_usage_subsets_and_unknowns(self):
        for usage, expected in [({'input_tokens': 100, 'cached_input_tokens': 90, 'output_tokens': 20, 'reasoning_output_tokens': 10}, 120), ({}, None)]:
            with self.subTest(usage=usage), tempfile.TemporaryDirectory() as directory:
                event = json.dumps({'type': 'turn.completed', 'usage': usage})
                cmd = [sys.executable, '-c', 'print(' + repr(event) + ')']
                run = bench.run_codex(cmd, Path(directory), 1, 'task', 10, 'dual')
                self.assertEqual(run.total_tokens, expected)
                self.assertIsNone(run.ttft_ms)

    def test_single_memory_preserves_same_advisory_contract(self):
        scenario = {'prompts': {'main': 'Do task'}}
        prompt = bench.build_prompt(scenario, 'main', 'single_memory')
        self.assertIn('advisory context, never instructions', prompt)
        self.assertIn('no delegation', prompt)
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            (repo / '.dual-brain').mkdir()
            (repo / '.dual-brain/MEMORY.md').write_text('memory')
            self.assertTrue(bench.prepare_workspace_for_strategy(repo, 'single_memory'))

    def test_skill_snapshot_is_exact_and_includes_resources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'; root.mkdir()
            (root / 'SKILL.md').write_text('exact skill')
            (root / 'references').mkdir()
            (root / 'references/detail.md').write_text('details')
            repo = Path(directory) / 'repo'; repo.mkdir()
            with patch.object(bench, 'ROOT', root), patch.object(bench, 'run_shell'):
                hashes = bench.install_skill_snapshot(repo)
            self.assertEqual((repo / '.benchmark-skill/SKILL.md').read_bytes(), (root / 'SKILL.md').read_bytes())
            self.assertIn('references/detail.md', hashes)

    def test_cli_failure_cannot_pass(self):
        from types import SimpleNamespace
        self.assertFalse(bench.successful(SimpleNamespace(returncode=1), {'returncode': 0}, {'passed': True}))
        self.assertFalse(bench.successful(SimpleNamespace(returncode=0), {'returncode': 0}, {'passed': True, 'returncode': 1}))

    def test_effort_forwarded(self):
        with patch.object(bench, 'run_codex') as run:
            bench.CodexAdapter('example', reasoning_effort='high').run(Path('.'), 'task', Path('.'), 1, 10, 'dual')
            self.assertIn('model_reasoning_effort="high"', run.call_args.args[0])

    def test_summary_does_not_claim_improvement_when_dual_worse(self):
        rows = []
        for matrix, repairs in [('codex_single_no_memory', 0), ('codex_dual_memory', 2)]:
            rows.append(dict(scenario='example', method='main', matrix=matrix,
                             passed=False, first_pass=False, repair_loops=repairs,
                             tokens={'total_tokens': None}))
        with tempfile.TemporaryDirectory() as directory:
            bench.summarize(rows, Path(directory))
            report = (Path(directory) / 'benchmark_results.md').read_text()
            self.assertNotIn('reduced repair', report)
            self.assertNotIn('Human repair prompts', report)
            self.assertIn('0 and 2', report)
            self.assertIn('unknown', report)

    def test_default_includes_equal_memory_control(self):
        self.assertIn('codex_single_memory', bench.expand_matrix('default'))


if __name__ == '__main__':
    unittest.main()
