import json
from pathlib import Path

def export_report(final_state: dict, output_path: str = "audit_report.json"):
    report_data = {
        "target_dir": final_state.get("target_dir"),
        "total_findings": len(final_state.get("findings", [])),
        "findings": final_state.get("findings", [])
    }
    Path(output_path).write_text(json.dumps(report_data, indent=2))
    print(f"Report successfully exported to {output_path}")