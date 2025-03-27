#!/usr/bin/env python3
# Copyright 2025 Canonical
"""Charmed Gubernator."""
import json
import logging

import ops

# NOTE: adjust to your local environment
# the ip address is what process in a pod can use to access the vm
URL="http://192.168.107.3:4318/v1/traces"


class HexanatorHelperCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, framework: ops.Framework):
        super().__init__(framework)
        self.framework.observe(self.on.charm_tracing_relation_created, self._on_charm_tracing_changed)
        self.framework.observe(self.on.send_ca_cert_relation_created, self._on_send_ca_cert_changed)

    def _on_charm_tracing_changed(self, event: ops.RelationCreatedEvent):
        if not self.unit.is_leader():
            return
        relation = event.relation
        relation.data[self.app]["receivers"] = json.dumps([
            {
                "protocol": {"name": "otlp_http", "type": "http"},
                "url": URL,
            }
        ])
        logging.info("Set tracing destination data on relation %s", relation.id)

    def _on_send_ca_cert_changed(self, event: ops.RelationCreatedEvent):
        if not self.unit.is_leader():
            return
        relation = event.relation
        relation.data[self.app]["certificates"] = json.dumps(["FIXME--CERT", "FIXME--CERT"])
        logging.info("Set CA certificates on relation %s", relation.id)


if __name__ == "__main__":  # pragma: nocover
    ops.main(HexanatorHelperCharm)  # type: ignore
