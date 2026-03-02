"""
Pydantic models for all IIPS data structures.
Defines schemas for context packets, extracted invoices, findings,
match results, approval packets, posting payloads, and metrics.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────────────

class DocumentType(str, Enum):
    INVOICE = "invoice"
    PURCHASE_ORDER = "purchase_order"
    GRN = "goods_receipt_note"
    CREDIT_NOTE = "credit_note"
    VENDOR_MASTER = "vendor_master"
    TAX_RULES = "tax_rules"
    APPROVAL_POLICY = "approval_policy"
    UNKNOWN = "unknown"


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class MatchType(str, Enum):
    TWO_WAY = "2-way"
    THREE_WAY = "3-way"
    NO_MATCH = "no_match"


class MatchStatus(str, Enum):
    MATCHED = "matched"
    PARTIAL = "partial_match"
    MISMATCHED = "mismatched"
    UNMATCHED = "unmatched"


class DecisionAction(str, Enum):
    AUTO_POST = "auto_post"
    APPROVE_AND_POST = "approve_and_post"
    ROUTE_FOR_APPROVAL = "route_for_approval"
    HOLD = "hold"
    REJECT = "reject"
    MANUAL_REVIEW = "manual_review"


class ExceptionCategory(str, Enum):
    QUANTITY_VARIANCE = "quantity_variance"
    PRICE_VARIANCE = "price_variance"
    TOTAL_MISMATCH = "total_mismatch"
    MISSING_GRN = "missing_grn"
    MISSING_PO = "missing_po"
    DUPLICATE = "duplicate"
    TAX_MISMATCH = "tax_mismatch"
    VENDOR_MISMATCH = "vendor_mismatch"
    NEW_VENDOR = "new_vendor"
    BANK_CHANGE = "bank_change"
    LOW_CONFIDENCE = "low_confidence"
    COMPLIANCE = "compliance"
    ANOMALY = "anomaly"
    VALIDATION_ERROR = "validation_error"


# ── Evidence & Findings ────────────────────────────────────────────────

class EvidencePointer(BaseModel):
    """Points to a specific location in a source document."""
    source_file: str
    page: Optional[int] = None
    field: Optional[str] = None
    bbox: Optional[list[float]] = None  # [x0, y0, x1, y1]
    text_snippet: Optional[str] = None


class Finding(BaseModel):
    """Unified finding schema used by all agents."""
    finding_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    agent: str
    category: ExceptionCategory
    severity: Severity
    confidence: float = Field(ge=0.0, le=1.0)
    title: str
    description: str
    evidence: list[EvidencePointer] = Field(default_factory=list)
    recommendation: Optional[str] = None
    open_questions: list[str] = Field(default_factory=list)
    data: dict[str, Any] = Field(default_factory=dict)


# ── Line Items ─────────────────────────────────────────────────────────

class LineItem(BaseModel):
    """A single invoice line item."""
    line_number: int
    description: str
    quantity: float
    unit: Optional[str] = None
    unit_price: float
    amount: float
    tax_rate: Optional[float] = None
    tax_amount: Optional[float] = None
    po_line_ref: Optional[str] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class POLineItem(BaseModel):
    """A single purchase order line item."""
    line_number: int
    description: str
    quantity: float
    unit: Optional[str] = None
    unit_price: float
    amount: float


class GRNLineItem(BaseModel):
    """A single goods receipt note line item."""
    line_number: int
    description: str
    quantity_received: float
    unit: Optional[str] = None
    po_line_ref: Optional[str] = None
    received_date: Optional[str] = None


# ── Context Packet ─────────────────────────────────────────────────────

class DocumentEntry(BaseModel):
    """A classified document within the bundle."""
    file_path: str
    document_type: DocumentType
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContextPacket(BaseModel):
    """Built by Agent A – the full context for a processing run."""
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    bundle_path: str
    documents: list[DocumentEntry] = Field(default_factory=list)
    vendor_candidates: list[str] = Field(default_factory=list)
    po_references: list[str] = Field(default_factory=list)
    grn_references: list[str] = Field(default_factory=list)
    risk_indicators: list[str] = Field(default_factory=list)
    evidence_index: list[EvidencePointer] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


# ── Extracted Invoice ──────────────────────────────────────────────────

class ExtractedInvoice(BaseModel):
    """Output of Agent B – structured invoice data."""
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    vendor_name: Optional[str] = None
    vendor_id: Optional[str] = None
    vendor_address: Optional[str] = None
    vendor_tax_id: Optional[str] = None
    vendor_bank_account: Optional[str] = None
    buyer_name: Optional[str] = None
    buyer_address: Optional[str] = None
    buyer_tax_id: Optional[str] = None
    po_number: Optional[str] = None
    currency: Optional[str] = "USD"
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    line_items: list[LineItem] = Field(default_factory=list)
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    confidence_scores: dict[str, float] = Field(default_factory=dict)
    evidence: list[EvidencePointer] = Field(default_factory=list)


# ── Purchase Order ─────────────────────────────────────────────────────

class PurchaseOrder(BaseModel):
    """Structured purchase order data."""
    po_number: str
    vendor_name: Optional[str] = None
    vendor_id: Optional[str] = None
    order_date: Optional[str] = None
    currency: str = "USD"
    total_amount: Optional[float] = None
    line_items: list[POLineItem] = Field(default_factory=list)
    payment_terms: Optional[str] = None


# ── Goods Receipt Note ─────────────────────────────────────────────────

class GoodsReceiptNote(BaseModel):
    """Structured GRN data."""
    grn_number: str
    po_number: Optional[str] = None
    vendor_name: Optional[str] = None
    receipt_date: Optional[str] = None
    line_items: list[GRNLineItem] = Field(default_factory=list)


# ── Vendor Master ──────────────────────────────────────────────────────

class VendorRecord(BaseModel):
    """A vendor from the master data."""
    vendor_id: str
    vendor_name: str
    tax_id: Optional[str] = None
    address: Optional[str] = None
    bank_account: Optional[str] = None
    bank_account_last_changed: Optional[str] = None
    payment_terms: Optional[str] = None
    status: str = "active"


# ── Match Result ───────────────────────────────────────────────────────

class LineMatchResult(BaseModel):
    """Match result for a single line item."""
    invoice_line: int
    po_line: Optional[int] = None
    grn_line: Optional[int] = None
    quantity_match: bool = False
    price_match: bool = False
    quantity_variance_pct: Optional[float] = None
    price_variance_pct: Optional[float] = None
    quantity_invoice: Optional[float] = None
    quantity_po: Optional[float] = None
    quantity_grn: Optional[float] = None
    price_invoice: Optional[float] = None
    price_po: Optional[float] = None
    status: MatchStatus = MatchStatus.UNMATCHED
    notes: list[str] = Field(default_factory=list)


class MatchResult(BaseModel):
    """Output of Agent E – matching result."""
    match_type: MatchType
    overall_status: MatchStatus
    invoice_number: Optional[str] = None
    po_number: Optional[str] = None
    grn_numbers: list[str] = Field(default_factory=list)
    line_matches: list[LineMatchResult] = Field(default_factory=list)
    total_invoice: Optional[float] = None
    total_po: Optional[float] = None
    total_variance: Optional[float] = None
    total_variance_pct: Optional[float] = None
    within_tolerance: bool = False
    findings: list[Finding] = Field(default_factory=list)
    summary: str = ""


# ── Approval Packet ────────────────────────────────────────────────────

class ApprovalPacket(BaseModel):
    """Output of Agent H – routing information for exceptions."""
    invoice_number: Optional[str] = None
    vendor_name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: str = "USD"
    exceptions: list[Finding] = Field(default_factory=list)
    approval_required: bool = False
    approver_role: Optional[str] = None
    approver_reason: str = ""
    priority: str = "normal"
    recommended_action: DecisionAction = DecisionAction.MANUAL_REVIEW
    follow_up_actions: list[str] = Field(default_factory=list)
    evidence_summary: list[str] = Field(default_factory=list)


# ── Posting Payload ────────────────────────────────────────────────────

class PostingLineItem(BaseModel):
    """A line item for ERP posting."""
    gl_account: str = ""
    cost_center: str = ""
    description: str
    amount: float
    tax_code: str = ""
    po_line_ref: Optional[str] = None


class PostingPayload(BaseModel):
    """ERP-ready posting payload."""
    document_type: str = "invoice"
    invoice_number: Optional[str] = None
    vendor_id: Optional[str] = None
    posting_date: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    currency: str = "USD"
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    po_number: Optional[str] = None
    payment_terms: Optional[str] = None
    line_items: list[PostingLineItem] = Field(default_factory=list)
    status: str = "ready"
    decision: DecisionAction = DecisionAction.AUTO_POST


# ── Final Decision ─────────────────────────────────────────────────────

class FinalDecision(BaseModel):
    """Output of Agent I – the orchestrator's final decision."""
    run_id: str
    invoice_number: Optional[str] = None
    vendor_name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: str = "USD"
    decision: DecisionAction
    reason: str
    all_findings: list[Finding] = Field(default_factory=list)
    critical_findings: list[Finding] = Field(default_factory=list)
    risk_score: float = 0.0
    confidence: float = 1.0
    approval_packet: Optional[ApprovalPacket] = None
    posting_payload: Optional[PostingPayload] = None
    audit_trail: list[str] = Field(default_factory=list)


# ── Metrics ────────────────────────────────────────────────────────────

class RunMetrics(BaseModel):
    """Processing metrics for a run."""
    run_id: str
    start_time: str = ""
    end_time: str = ""
    duration_seconds: float = 0.0
    documents_processed: int = 0
    line_items_extracted: int = 0
    extraction_confidence_avg: float = 0.0
    extraction_confidence_min: float = 0.0
    findings_total: int = 0
    findings_by_severity: dict[str, int] = Field(default_factory=dict)
    findings_by_category: dict[str, int] = Field(default_factory=dict)
    match_status: str = ""
    decision: str = ""
    exceptions_count: int = 0
    auto_posted: bool = False
