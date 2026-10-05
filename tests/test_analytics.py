import importlib.util
from pathlib import Path
import unittest

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


prepare = load_module("prepare_data", "python/01_prepare_data.py")
eda = load_module("eda_rfm", "python/02_eda_rfm.py")


class DataPreparationTests(unittest.TestCase):
    def test_clean_types_preserves_ids_and_derives_revenue(self):
        raw = pd.DataFrame(
            [
                ["2021-01-01 12:00:00 UTC", "10001", "20001", "1", "", "jewelry.ring", "7", "99.99", "30001", "", "red", "gold", "diamond"],
                ["2021-01-02 12:00:00 UTC", "10002", "20002", "1", "", "electronics.clocks", "8", "250.00", "30002", "f", "black", "silver", ""],
            ],
            columns=prepare.SOURCE_COLUMNS,
        )
        out = prepare.clean_types(raw)
        self.assertEqual(out["order_id"].tolist(), ["10001", "10002"])
        self.assertTrue(np.allclose(out["line_revenue"], [99.99, 250.00]))
        self.assertEqual(out["category_name"].tolist(), ["Ring", "Clocks"])
        self.assertEqual(out["price_band"].astype(str).tolist(), ["Under $100", "$250-$499"])

    def test_duplicate_rows_are_flagged_not_deleted(self):
        row = ["2021-01-01 12:00:00 UTC", "10001", "20001", "1", "", "jewelry.ring", "7", "99.99", "30001", "", "red", "gold", "diamond"]
        raw = pd.DataFrame([row, row], columns=prepare.SOURCE_COLUMNS)
        out = prepare.clean_types(raw)
        self.assertEqual(len(out), 2)
        self.assertTrue(out["is_exact_duplicate"].all())

    def test_invalid_quantity_is_rejected(self):
        row = ["2021-01-01 12:00:00 UTC", "10001", "20001", "0", "", "jewelry.ring", "7", "99.99", "30001", "", "red", "gold", "diamond"]
        raw = pd.DataFrame([row], columns=prepare.SOURCE_COLUMNS)
        with self.assertRaises(ValueError):
            prepare.clean_types(raw)


class AnalyticsTests(unittest.TestCase):
    def test_segment_mapping(self):
        cases = [
            (5, 5, "Champions"),
            (3, 5, "Loyal Customers"),
            (5, 2, "Recent Customers"),
            (2, 5, "At Risk"),
            (1, 2, "Hibernating"),
            (3, 3, "Potential Loyalists"),
        ]
        for r_score, fm_score, expected in cases:
            row = pd.Series({"r_score": r_score, "fm_score": fm_score})
            self.assertEqual(eda.assign_rfm_segment(row), expected)

    def test_kpis_use_distinct_orders_for_repeat_rate(self):
        df = pd.DataFrame(
            {
                "user_id": ["u1", "u1", "u1", "u2"],
                "order_id": ["o1", "o1", "o2", "o3"],
                "product_id": ["p1", "p2", "p3", "p4"],
                "quantity": [1, 1, 1, 1],
                "price": [10.0, 20.0, 30.0, 40.0],
                "line_revenue": [10.0, 20.0, 30.0, 40.0],
            }
        )
        kpis = eda.create_kpi_summary(df).set_index("metric")["value"]
        self.assertEqual(int(kpis["orders"]), 3)
        self.assertEqual(int(kpis["repeat_customers"]), 1)
        self.assertAlmostEqual(float(kpis["repeat_customer_rate_pct"]), 50.0)

    def test_customer_rfm_reconciles_revenue(self):
        rows = []
        base = pd.Timestamp("2021-01-01", tz="UTC")
        for i in range(10):
            rows.append(
                {
                    "user_id": f"u{i:02d}",
                    "order_id": f"o{i:02d}",
                    "product_id": f"p{i:02d}",
                    "quantity": 1,
                    "line_revenue": float((i + 1) * 10),
                    "event_time": base + pd.Timedelta(days=i),
                }
            )
        df = pd.DataFrame(rows)
        customer, summary, _ = eda.create_customer_outputs(df)
        self.assertEqual(len(customer), 10)
        self.assertTrue(customer["user_id"].is_unique)
        self.assertAlmostEqual(customer["monetary"].sum(), df["line_revenue"].sum())
        self.assertAlmostEqual(summary["revenue"].sum(), df["line_revenue"].sum())
        self.assertEqual(set(customer["r_score"]), {1, 2, 3, 4, 5})
        self.assertEqual(set(customer["m_score"]), {1, 2, 3, 4, 5})


if __name__ == "__main__":
    unittest.main()
