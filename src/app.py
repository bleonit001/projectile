"""
IIPS – Streamlit Dashboard
Interactive web UI for the Intelligent Invoice Processing System.
Run with: streamlit run src/app.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

# Ensure project root is on sys.path and is the working directory
import os
_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
os.chdir(_project_root)

import pandas as pd
import streamlit as st
import yaml

from src.pipeline import Pipeline
from src.schemas.models import (
    DecisionAction,
    Finding,
    MatchStatus,
    MatchType,
    Severity,
)
from src.utils.file_utils import load_json

# ── Constants ──────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUNDLES_DIR = PROJECT_ROOT / "tests" / "bundles"
DEFAULT_POLICY = PROJECT_ROOT / "config" / "policy.yaml"

DECISION_COLORS = {
    "auto_post": "#28a745",
    "approve_and_post": "#17a2b8",
    "route_for_approval": "#ffc107",
    "hold": "#dc3545",
    "reject": "#dc3545",
    "manual_review": "#fd7e14",
}

DECISION_LABELS = {
    "auto_post": "AUTO POST",
    "approve_and_post": "APPROVE & POST",
    "route_for_approval": "ROUTE FOR APPROVAL",
    "hold": "HOLD",
    "reject": "REJECT",
    "manual_review": "MANUAL REVIEW",
}

SEVERITY_ICONS = {
    "critical": "\U0001f534",  # red circle
    "error": "\U0001f7e0",     # orange circle
    "warning": "\U0001f7e1",   # yellow circle
    "info": "\U0001f535",      # blue circle
}

# ── Page Config ────────────────────────────────────────────────────────

st.set_page_config(
    page_title="IIPS – Invoice Processing",
    page_icon="\U0001f4c4",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Helpers ────────────────────────────────────────────────────────────

def get_available_bundles() -> list[str]:
    """List test bundles available for processing."""
    if not BUNDLES_DIR.exists():
        return []
    return sorted([d.name for d in BUNDLES_DIR.iterdir() if d.is_dir()])


def run_pipeline(bundle_path: str, policy_overrides: dict | None = None) -> dict[str, Any]:
    """Run the IIPS pipeline and return the context."""
    # Apply policy overrides by writing a temp policy file
    policy_path = None
    if policy_overrides:
        base_policy = yaml.safe_load(open(DEFAULT_POLICY))
        for key, value in policy_overrides.items():
            keys = key.split(".")
            d = base_policy
            for k in keys[:-1]:
                d = d.setdefault(k, {})
            d[keys[-1]] = value
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False)
        yaml.dump(base_policy, tmp)
        tmp.close()
        policy_path = tmp.name

    pipeline = Pipeline(
        bundle_path=bundle_path,
        output_dir=str(PROJECT_ROOT / "runs"),
        policy_path=policy_path,
    )
    return pipeline.run(), pipeline.run_dir


def decision_badge(decision_value: str) -> str:
    """Return styled HTML badge for a decision."""
    color = DECISION_COLORS.get(decision_value, "#6c757d")
    label = DECISION_LABELS.get(decision_value, decision_value.upper())
    return (
        f'<div style="display:inline-block;background:{color};color:white;'
        f'padding:8px 20px;border-radius:8px;font-size:1.3em;font-weight:bold;'
        f'letter-spacing:1px;">{label}</div>'
    )


def severity_badge(severity: str) -> str:
    """Return colored severity text."""
    colors = {"critical": "#dc3545", "error": "#fd7e14", "warning": "#ffc107", "info": "#17a2b8"}
    color = colors.get(severity, "#6c757d")
    icon = SEVERITY_ICONS.get(severity, "")
    return f"{icon} :{severity.upper()}"


# ── Sidebar ────────────────────────────────────────────────────────────

def render_sidebar() -> tuple[str | None, dict]:
    """Render the sidebar and return (bundle_path, policy_overrides)."""
    st.sidebar.title("\U0001f4c4 IIPS")
    st.sidebar.caption("Intelligent Invoice Processing System")
    st.sidebar.divider()

    # Bundle selection
    st.sidebar.subheader("Invoice Bundle")
    bundles = get_available_bundles()
    if not bundles:
        st.sidebar.warning("No test bundles found.")
        return None, {}

    selected = st.sidebar.selectbox(
        "Select a test scenario",
        bundles,
        format_func=lambda x: x.replace("_", " ").title(),
    )

    # Show scenario description
    manifest_path = BUNDLES_DIR / selected / "manifest.yaml"
    if manifest_path.exists():
        manifest = yaml.safe_load(open(manifest_path))
        scenario = manifest.get("metadata", {}).get("scenario", "")
        if scenario:
            st.sidebar.info(f"**Scenario:** {scenario}")

    st.sidebar.divider()

    # Policy overrides
    overrides = {}
    with st.sidebar.expander("\u2699\ufe0f Policy Overrides", expanded=False):
        auto_approve = st.number_input(
            "Auto-approve threshold ($)",
            value=5000.0, min_value=0.0, max_value=1000000.0, step=500.0,
        )
        if auto_approve != 5000.0:
            overrides["approval_thresholds.auto_approve_max"] = auto_approve

        qty_tol = st.slider("Quantity tolerance (%)", 0.0, 20.0, 5.0, 0.5)
        if qty_tol != 5.0:
            overrides["tolerance.quantity_percent"] = qty_tol

        price_tol = st.slider("Price tolerance (%)", 0.0, 20.0, 2.0, 0.5)
        if price_tol != 2.0:
            overrides["tolerance.price_percent"] = price_tol

        tax_rate = st.number_input("Expected tax rate (%)", value=18.0, min_value=0.0, max_value=50.0, step=0.5)
        if tax_rate != 18.0:
            overrides["compliance.default_tax_rate"] = tax_rate

    st.sidebar.divider()

    # Process button
    bundle_path = str(BUNDLES_DIR / selected) if selected else None
    return bundle_path, overrides


# ── Tab: Dashboard ─────────────────────────────────────────────────────

def render_dashboard(ctx: dict, run_dir: Path) -> None:
    """Render the overview dashboard tab."""
    decision = ctx["final_decision"]

    # Decision badge
    st.markdown(decision_badge(decision.decision.value), unsafe_allow_html=True)
    st.markdown(f"> {decision.reason}")
    st.divider()

    # KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Risk Score", f"{decision.risk_score}/10")
    col2.metric("Confidence", f"{decision.confidence:.0%}")
    col3.metric("Total Findings", len(decision.all_findings))
    col4.metric("Critical", len(decision.critical_findings))

    invoice = ctx.get("extracted_invoice")
    line_count = len(invoice.line_items) if invoice else 0
    col5.metric("Line Items", line_count)

    st.divider()

    # Quick summary cards
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Invoice Details**")
        if invoice:
            st.markdown(f"- **Number:** {invoice.invoice_number or 'N/A'}")
            st.markdown(f"- **Vendor:** {invoice.vendor_name or 'N/A'}")
            st.markdown(f"- **Amount:** {invoice.currency or 'USD'} {invoice.total_amount or 'N/A':,.2f}")
            st.markdown(f"- **Date:** {invoice.invoice_date or 'N/A'}")
            st.markdown(f"- **PO Ref:** {invoice.po_number or 'None'}")

    with c2:
        match = ctx.get("match_result")
        st.markdown("**Matching Summary**")
        if match:
            st.markdown(f"- **Match Type:** {match.match_type.value}")
            st.markdown(f"- **Status:** {match.overall_status.value}")
            st.markdown(f"- **Within Tolerance:** {'Yes' if match.within_tolerance else 'No'}")
            if match.total_variance is not None:
                st.markdown(f"- **Total Variance:** {match.total_variance:,.2f} ({match.total_variance_pct}%)")
        else:
            st.markdown("No matching data available.")


# ── Tab: Invoice Details ───────────────────────────────────────────────

def render_invoice_details(ctx: dict) -> None:
    """Render the extracted invoice details tab."""
    invoice = ctx.get("extracted_invoice")
    if not invoice:
        st.warning("No invoice data extracted.")
        return

    # Header fields
    st.subheader("Header Fields")
    fields = {
        "Invoice Number": invoice.invoice_number,
        "Invoice Date": invoice.invoice_date,
        "Due Date": invoice.due_date,
        "Vendor Name": invoice.vendor_name,
        "Vendor ID": invoice.vendor_id,
        "Vendor Tax ID": invoice.vendor_tax_id,
        "PO Number": invoice.po_number,
        "Currency": invoice.currency,
        "Subtotal": f"{invoice.subtotal:,.2f}" if invoice.subtotal is not None else None,
        "Tax Amount": f"{invoice.tax_amount:,.2f}" if invoice.tax_amount is not None else None,
        "Total Amount": f"{invoice.total_amount:,.2f}" if invoice.total_amount is not None else None,
        "Payment Terms": invoice.payment_terms,
    }

    cols = st.columns(3)
    for i, (label, value) in enumerate(fields.items()):
        with cols[i % 3]:
            display = value if value is not None else "N/A"
            st.markdown(f"**{label}:** {display}")

    st.divider()

    # Confidence scores
    if invoice.confidence_scores:
        st.subheader("Field Confidence Scores")
        conf_data = []
        for field, score in invoice.confidence_scores.items():
            conf_data.append({
                "Field": field.replace("_", " ").title(),
                "Confidence": score,
                "Status": "Good" if score >= 0.7 else ("Low" if score >= 0.4 else "Very Low"),
            })
        conf_df = pd.DataFrame(conf_data)
        st.dataframe(
            conf_df.style.background_gradient(subset=["Confidence"], cmap="RdYlGn", vmin=0, vmax=1),
            use_container_width=True,
            hide_index=True,
        )
        st.divider()

    # Line items table
    if invoice.line_items:
        st.subheader(f"Line Items ({len(invoice.line_items)})")
        rows = []
        for item in invoice.line_items:
            rows.append({
                "Line": item.line_number,
                "Description": item.description,
                "Qty": item.quantity,
                "Unit": item.unit or "",
                "Unit Price": item.unit_price,
                "Amount": item.amount,
                "Tax Rate": f"{item.tax_rate}%" if item.tax_rate is not None else "",
                "Tax Amount": item.tax_amount if item.tax_amount is not None else "",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ── Tab: Matching ──────────────────────────────────────────────────────

def render_matching(ctx: dict) -> None:
    """Render the matching results tab."""
    match = ctx.get("match_result")
    if not match:
        st.warning("No matching data available.")
        return

    # Match summary
    col1, col2, col3 = st.columns(3)
    type_color = {"2-way": "blue", "3-way": "green", "no_match": "red"}.get(match.match_type.value, "gray")
    col1.markdown(f"**Match Type:** :{type_color}[{match.match_type.value}]")

    status_color = {
        "matched": "green", "partial_match": "orange",
        "mismatched": "red", "unmatched": "gray",
    }.get(match.overall_status.value, "gray")
    col2.markdown(f"**Status:** :{status_color}[{match.overall_status.value}]")
    col3.markdown(f"**Within Tolerance:** {'Yes' if match.within_tolerance else 'No'}")

    st.divider()

    # Totals comparison
    if match.total_invoice is not None:
        st.subheader("Total Comparison")
        tc1, tc2, tc3, tc4 = st.columns(4)
        tc1.metric("Invoice Total", f"${match.total_invoice:,.2f}")
        tc2.metric("PO Total", f"${match.total_po:,.2f}" if match.total_po else "N/A")
        tc3.metric("Variance", f"${match.total_variance:,.2f}" if match.total_variance is not None else "N/A")
        tc4.metric("Variance %", f"{match.total_variance_pct}%" if match.total_variance_pct is not None else "N/A")
        st.divider()

    # Line-level matches
    if match.line_matches:
        st.subheader("Line-by-Line Match")
        rows = []
        for lm in match.line_matches:
            status_icon = {
                "matched": "\u2705", "partial_match": "\U0001f7e1",
                "mismatched": "\u274c", "unmatched": "\u2b1c",
            }.get(lm.status.value, "")

            rows.append({
                "Status": f"{status_icon} {lm.status.value}",
                "Inv Line": lm.invoice_line,
                "PO Line": lm.po_line if lm.po_line is not None else "-",
                "GRN Line": lm.grn_line if lm.grn_line is not None else "-",
                "Qty (Inv)": lm.quantity_invoice,
                "Qty (PO)": lm.quantity_po if lm.quantity_po is not None else "-",
                "Qty (GRN)": lm.quantity_grn if lm.quantity_grn is not None else "-",
                "Qty Var %": f"{lm.quantity_variance_pct}%" if lm.quantity_variance_pct else "-",
                "Price (Inv)": lm.price_invoice,
                "Price (PO)": lm.price_po if lm.price_po is not None else "-",
                "Price Var %": f"{lm.price_variance_pct}%" if lm.price_variance_pct else "-",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # GRN references
    if match.grn_numbers:
        st.markdown(f"**GRN References:** {', '.join(match.grn_numbers)}")


# ── Tab: Findings & Exceptions ─────────────────────────────────────────

def render_findings(ctx: dict) -> None:
    """Render findings and exception triage tab."""
    decision = ctx["final_decision"]
    findings = decision.all_findings
    approval = ctx.get("approval_packet")

    if not findings:
        st.success("No findings or exceptions. Invoice is clean.")
        return

    # Summary counts
    counts = {"critical": 0, "error": 0, "warning": 0, "info": 0}
    for f in findings:
        counts[f.severity.value] = counts.get(f.severity.value, 0) + 1

    cols = st.columns(4)
    cols[0].metric("\U0001f534 Critical", counts["critical"])
    cols[1].metric("\U0001f7e0 Error", counts["error"])
    cols[2].metric("\U0001f7e1 Warning", counts["warning"])
    cols[3].metric("\U0001f535 Info", counts["info"])

    st.divider()

    # Findings list
    for severity in ["critical", "error", "warning", "info"]:
        group = [f for f in findings if f.severity.value == severity]
        if not group:
            continue

        icon = SEVERITY_ICONS.get(severity, "")
        st.subheader(f"{icon} {severity.upper()} ({len(group)})")

        for f in group:
            with st.expander(f"**{f.title}** — {f.category.value} (agent: {f.agent})"):
                st.markdown(f"**Description:** {f.description}")
                st.markdown(f"**Confidence:** {f.confidence:.0%}")
                if f.recommendation:
                    st.markdown(f"**Recommendation:** {f.recommendation}")
                if f.evidence:
                    st.markdown("**Evidence:**")
                    for e in f.evidence:
                        parts = [e.source_file]
                        if e.field:
                            parts.append(f"field: {e.field}")
                        if e.text_snippet:
                            parts.append(f'"{e.text_snippet}"')
                        st.markdown(f"- {' | '.join(parts)}")
                if f.data:
                    st.json(f.data)

    # Approval routing
    if approval and approval.approval_required:
        st.divider()
        st.subheader("Approval Routing")
        st.markdown(f"- **Approver:** {approval.approver_role or 'N/A'}")
        st.markdown(f"- **Priority:** {approval.priority}")
        st.markdown(f"- **Reason:** {approval.approver_reason}")
        if approval.follow_up_actions:
            st.markdown("**Follow-up Actions:**")
            for i, action in enumerate(approval.follow_up_actions, 1):
                st.markdown(f"{i}. {action}")


# ── Tab: Audit Trail ──────────────────────────────────────────────────

def render_audit_trail(ctx: dict, run_dir: Path) -> None:
    """Render the audit trail tab."""
    # Try to load the audit log markdown
    audit_path = run_dir / "audit_log.md"
    if audit_path.exists():
        content = audit_path.read_text()
        st.markdown(content)
    else:
        # Fallback to audit entries from context
        decision = ctx.get("final_decision")
        if decision and decision.audit_trail:
            st.subheader("Processing Trail")
            for entry in decision.audit_trail:
                st.markdown(f"- `{entry}`")
        else:
            st.info("No audit trail available.")


# ── Tab: Artifacts ─────────────────────────────────────────────────────

def render_artifacts(ctx: dict, run_dir: Path) -> None:
    """Render the artifacts browser tab."""
    st.markdown(f"**Run Directory:** `{run_dir}`")
    st.divider()

    if not run_dir or not run_dir.exists():
        st.warning("Run directory not found.")
        return

    artifacts = sorted(run_dir.glob("*"))
    if not artifacts:
        st.warning("No artifacts found.")
        return

    for artifact in artifacts:
        col1, col2 = st.columns([4, 1])
        size_kb = artifact.stat().st_size / 1024
        col1.markdown(f"**{artifact.name}** ({size_kb:.1f} KB)")

        # Download button
        content = artifact.read_bytes()
        col2.download_button(
            label="Download",
            data=content,
            file_name=artifact.name,
            key=f"dl_{artifact.name}",
        )

    st.divider()

    # JSON viewer
    st.subheader("Artifact Viewer")
    json_artifacts = [a for a in artifacts if a.suffix == ".json"]
    if json_artifacts:
        selected_file = st.selectbox(
            "Select artifact to inspect",
            json_artifacts,
            format_func=lambda x: x.name,
        )
        if selected_file:
            data = json.loads(selected_file.read_text())
            st.json(data)


# ── Main App ───────────────────────────────────────────────────────────

def main():
    bundle_path, policy_overrides = render_sidebar()

    # Header
    st.title("\U0001f4c4 Intelligent Invoice Processing System")

    if not bundle_path:
        st.info("Select an invoice bundle from the sidebar to begin processing.")
        return

    # Process button in sidebar
    process_clicked = st.sidebar.button(
        "\u25b6\ufe0f Process Invoice",
        type="primary",
        use_container_width=True,
    )

    # Run pipeline
    if process_clicked:
        with st.spinner("Running invoice processing pipeline..."):
            try:
                ctx, run_dir = run_pipeline(bundle_path, policy_overrides or None)
                st.session_state["ctx"] = ctx
                st.session_state["run_dir"] = run_dir
            except Exception as e:
                st.error(f"Pipeline failed: {e}")
                return

    # Display results if available
    if "ctx" not in st.session_state:
        st.info("Click **Process Invoice** in the sidebar to start.")

        # Show available scenarios
        st.subheader("Available Test Scenarios")
        bundles = get_available_bundles()
        scenarios_data = []
        for b in bundles:
            manifest_path = BUNDLES_DIR / b / "manifest.yaml"
            scenario = ""
            if manifest_path.exists():
                manifest = yaml.safe_load(open(manifest_path))
                scenario = manifest.get("metadata", {}).get("scenario", "")
            scenarios_data.append({"Bundle": b.replace("_", " ").title(), "Scenario": scenario})
        if scenarios_data:
            st.dataframe(pd.DataFrame(scenarios_data), use_container_width=True, hide_index=True)
        return

    ctx = st.session_state["ctx"]
    run_dir = st.session_state["run_dir"]

    # Tabs
    tabs = st.tabs([
        "\U0001f4ca Dashboard",
        "\U0001f4c4 Invoice",
        "\U0001f517 Matching",
        "\u26a0\ufe0f Findings",
        "\U0001f4dd Audit Trail",
        "\U0001f4c1 Artifacts",
    ])

    with tabs[0]:
        render_dashboard(ctx, run_dir)

    with tabs[1]:
        render_invoice_details(ctx)

    with tabs[2]:
        render_matching(ctx)

    with tabs[3]:
        render_findings(ctx)

    with tabs[4]:
        render_audit_trail(ctx, run_dir)

    with tabs[5]:
        render_artifacts(ctx, run_dir)


if __name__ == "__main__":
    main()
