################################################################################
# Copyright IBM Corporation 2021, 2022
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

"""
Test cases for C2G CLI
"""
import os
import logging
import unittest
from click.testing import CliRunner
from dgi.cli import cli
from py2neo import Graph

######################################################################
#  C 2 G   C L I   T E S T   C A S E S
######################################################################


NEO4J_BOLT_URL = os.getenv(
    "NEO4J_BOLT_URL", "neo4j://neo4j:konveyor@neo4j:7687")


class TestS2GCLI(unittest.TestCase):
    """Test Cases for c2g command"""

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self) -> None:
        pass

    def test_help(self):
        """Test help command"""
        result = self.runner.invoke(cli, ["c2g", "--help"])
        self.assertEqual(result.exit_code, 0)

    def test_missing_input(self):
        """Test --input with no filename"""
        result = self.runner.invoke(cli, ["c2g", "--input"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Option '--input' requires an argument.", result.output)

    def test_not_found_output(self):
        """Test --input directory not found"""
        result = self.runner.invoke(cli, ["c2g", "--input", "foo"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Directory 'foo' does not exist.", result.output)

    def test_abstraction_level_is_class(self):
        """Test --abstraction set to 'class'"""
        result = self.runner.invoke(
            cli,
            [
                "--validate",
                "c2g",
                "--abstraction=class",
                "--input=tests/fixtures/doop_out",
            ],
        )
        self.assertIn("abstraction level is class", result.output)
        self.assertEqual(result.exit_code, 0)

    def test_abstraction_level_is_method(self):
        """Test --abstraction set to 'method'"""
        result = self.runner.invoke(
            cli,
            [
                "--validate",
                "c2g",
                "--abstraction=method",
                "--input=tests/fixtures/doop_out",
            ],
        )
        self.assertIn("abstraction level is method", result.output)
        self.assertEqual(result.exit_code, 0)

    def test_abstraction_level_is_full(self):
        """Test --abstraction set to 'full'"""
        result = self.runner.invoke(
            cli,
            [
                "--validate",
                "c2g",
                "--abstraction=full",
                "--input=tests/fixtures/doop_out",
            ],
        )
        self.assertIn("abstraction level is full", result.output)
        self.assertEqual(result.exit_code, 0)

    def test_abstraction_level_is_wrong(self):
        """Test raise exception when --abstraction set to 'unknown'"""
        result = self.runner.invoke(
            cli,
            [
                "--validate",
                "c2g",
                "--abstraction=unknown",
                "--input=tests/fixtures/doop_out",
            ],
        )
        self.assertIn(
            "Invalid value for '--abstraction' / '-a': 'unknown' is not one of 'class', 'method', 'full'.",
            result.output
        )
        self.assertEqual(result.exit_code, 2)
