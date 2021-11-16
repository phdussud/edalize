# Copyright edalize contributors
# Licensed under the 2-Clause BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-2-Clause

import os.path

from edalize.flows.edaflow import Edaflow


class Lint(Edaflow):
    """Run a linter tool on the design"""

    argtypes = ["vlogdefine", "vlogparam"]

    FLOW = [
        ("verilator", [], {"mode": "lint-only", "exe": "false", "make_options": []}),
        # verible, spyglass, ascentlint, slang...
    ]

    FLOW_OPTIONS = {
        "frontends": {
            "type": "String",
            "desc": "Tools to run before linter (e.g. sv2v)",
            "list": True,
        },
        "tool": {
            "type": "String",
            "desc": "Select Lint tool",
        },
    }

    def build_tool_graph(self):
        # FIXME: Handle empty tool
        tmp = [x for x in self.FLOW if x[0] == self.flow_options.get("tool", "")]
        self.FLOW = tmp

        # FIXME: This makes an assumption that the first tool in self.FLOW is
        # a single entry point to the flow
        next_tool = self.FLOW[0][0]

        for frontend in reversed(self.flow_options.get("frontends", [])):
            self.FLOW[0:0] = [(frontend, [next_tool], {})]
            next_tool = frontend
        return super().build_tool_graph()

    def configure_tools(self, nodes, edam):
        super().configure_tools(nodes, edam)

        self.commands.default_target = nodes[
            self.flow_options.get("tool")
        ].default_target
