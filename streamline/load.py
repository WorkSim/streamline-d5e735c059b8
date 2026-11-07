# """Idempotent load: upsert rows into an in-memory "target table" by natural key.

# A "table" here is just a `list[dict]` — no database involved. Re-running a
# load for the same source data must be idempotent: rows sharing a key with an
# existing row replace it in place, and genuinely new rows are appended. Rows
# with other keys are left completely untouched (including their position).
# """
# """Return a new table with `new_rows` upserted into `table` by `key`.

#     Each row in `new_rows` replaces any existing row in `table` that shares
#     the same value for `key`; a row whose key value isn't already present is
#     appended. Existing rows in `table` whose key doesn't match any row in
#     `new_rows` are left untouched, in their original position.

#     Args:
#         table: The existing rows (each a dict containing `key`).
#         new_rows: Rows to upsert into `table`, keyed the same way.
#         key: The field name that uniquely identifies a row.

#     Returns:
#         A new list of dicts — `table` and `new_rows` are not mutated.
# """

from __future__ import annotations


def upsert_rows(
    table: list[dict],
    new_rows: list[dict],
    key: str = "id",
) -> list[dict]:

    result = list(table)

    for new_row in new_rows:
        existing_row = next(
            (r for r in result if r[key] == new_row[key]),
            None
        )

        if existing_row is not None:
            result[result.index(existing_row)] = new_row
        else:
            result.append(new_row)

    return result