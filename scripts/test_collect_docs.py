from __future__ import annotations

import unittest

from collect_docs import (
    SLMP_PYTHON_API_OPERATION_INDEX,
    public_api_table_symbols,
    validate_operation_index,
)


class SlmpOperationIndexTests(unittest.TestCase):
    def test_current_index_has_no_deleted_queued_client(self) -> None:
        symbols = public_api_table_symbols(SLMP_PYTHON_API_OPERATION_INDEX)

        self.assertNotIn("QueuedAsyncSlmpClient", symbols)
        self.assertIn("open_and_connect", symbols)
        self.assertIn("open_and_connect_sync", symbols)

    def test_synthetic_stale_class_is_rejected(self) -> None:
        index = "| Operation | Public API |\n| --- | --- |\n| Connect | `DeletedClient` |"
        reference = "| Operation | Public API |\n| --- | --- |\n| Connect | `CurrentClient` |"

        with self.assertRaisesRegex(RuntimeError, "DeletedClient"):
            validate_operation_index(index, reference)

    def test_synthetic_stale_method_is_rejected(self) -> None:
        index = "| Operation | Public API |\n| --- | --- |\n| Read | `removed_read` |"
        reference = "| Operation | Public API |\n| --- | --- |\n| Read | `read_devices` |"

        with self.assertRaisesRegex(RuntimeError, "removed_read"):
            validate_operation_index(index, reference)


if __name__ == "__main__":
    unittest.main()
