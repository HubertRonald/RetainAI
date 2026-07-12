"""Build RetainAI RAG evidence documents from local model artifacts.

Inputs are local artifacts produced by existing RetainAI modeling, survival and
explainability workflows. Outputs are markdown documents and a JSON manifest.

This module does not call cloud services, Bedrock, Gemini, FAISS or S3.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from modules.rag.manifest import build_manifest, write_manifest
from modules.rag.schemas import RagDocument, RagDocumentMetadata, slugify

DEFAULT_DOCUMENTS_PATH = Path("artifacts/rag/documents")
DEFAULT_MANIFEST_PATH = Path("artifacts/rag/manifest.json")
DEFAULT_S3_DOCUMENTS_PREFIX = "s3://retainai-dev-data/model-artifacts/rag/documents/"


def _read_json(path: Path) -> dict[str, Any] | list[Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def _safe_preview(value: Any, max_chars: int = 3000) -> str:
    text = json.dumps(value, indent=2, sort_keys=True, default=str)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n... truncated ..."


def _infer_top_drivers(payload: dict[str, Any]) -> list[str]:
    for key in ("top_drivers", "drivers", "features", "top_features"):
        value = payload.get(key)
        if isinstance(value, list):
            return [str(item) for item in value[:10]]
    return []


def _document(
    *,
    document_id: str,
    document_type: str,
    title: str,
    source_artifact: Path,
    output_path: Path,
    s3_documents_prefix: str,
    body: str,
    model_name: str | None = None,
    employee_segment: str | None = None,
    risk_level: str | None = None,
    top_drivers: list[str] | None = None,
    tags: list[str] | None = None,
) -> RagDocument:
    metadata = RagDocumentMetadata(
        document_id=document_id,
        document_type=document_type,
        title=title,
        source_artifact=str(source_artifact),
        local_output_path=str(output_path / f"{slugify(document_id)}.md"),
        s3_target_prefix=s3_documents_prefix.rstrip("/") + "/",
        model_name=model_name,
        employee_segment=employee_segment,
        risk_level=risk_level,
        top_drivers=top_drivers or [],
        tags=tags or [],
    )
    return RagDocument(metadata=metadata, body=body)


def build_responsible_use_document(
    *,
    output_path: Path,
    s3_documents_prefix: str,
) -> RagDocument:
    """Create the mandatory responsible-use document."""
    body = """
# Responsible Use Policy for RetainAI RAG

RetainAI provides decision-support evidence for employee retention analysis. It
must not be used as an automated employment decision system.

## Intended Use

- summarize model evidence;
- explain attrition-risk drivers;
- support HR analytics conversations;
- provide traceable context from model reports and SHAP artifacts.

## Non-Goals

- do not make employment decisions automatically;
- do not rank employees for termination;
- do not expose sensitive employee records to public clients;
- do not call external AI providers before quota, auth and redaction controls.

## Required Controls

- AI provider mode remains disabled by default;
- backend quota must run before any AI call;
- generated advice must reference model evidence and responsible-use notes;
- raw sensitive data should be redacted before provider calls;
- all generated outputs must be treated as advisory, not authoritative.
""".strip()

    return _document(
        document_id="responsible_use_policy",
        document_type="responsible_use",
        title="Responsible Use Policy",
        source_artifact=Path("docs/multicloud/sprint7_multicloud_deployment_plan.md"),
        output_path=output_path,
        s3_documents_prefix=s3_documents_prefix,
        body=body,
        tags=["responsible-use", "governance", "ai-disabled-by-default"],
    )


def build_model_registry_document(
    *,
    output_path: Path,
    s3_documents_prefix: str,
    registry_path: Path = Path("artifacts/models/model_registry.json"),
) -> RagDocument | None:
    """Build a document from the model registry manifest if available."""
    payload = _read_json(registry_path)
    if payload is None:
        return None

    body = f"""
# Model Registry Evidence

This document summarizes the local RetainAI model registry artifact.

## Source Artifact

```text
{registry_path}
```

## Registry Payload Preview

```json
{_safe_preview(payload)}
```
""".strip()

    return _document(
        document_id="model_registry_evidence",
        document_type="model_registry",
        title="Model Registry Evidence",
        source_artifact=registry_path,
        output_path=output_path,
        s3_documents_prefix=s3_documents_prefix,
        body=body,
        tags=["model-registry", "model-artifacts"],
    )


def build_report_documents(
    *,
    output_path: Path,
    s3_documents_prefix: str,
    reports_dir: Path = Path("artifacts/reports"),
) -> list[RagDocument]:
    """Convert markdown/text reports into RAG evidence documents."""
    documents: list[RagDocument] = []

    if not reports_dir.exists():
        return documents

    for report_path in sorted(
        list(reports_dir.glob("*.md")) + list(reports_dir.glob("*.txt"))
    ):
        text = _read_text(report_path)
        if not text:
            continue

        report_slug = slugify(report_path.stem)
        title = report_path.stem.replace("_", " ").replace("-", " ").title()
        body = f"""
# {title}

This document was generated from a RetainAI report artifact.

## Source Artifact

```text
{report_path}
```

## Report Content

{text}
""".strip()

        documents.append(
            _document(
                document_id=f"report_{report_slug}",
                document_type="report",
                title=title,
                source_artifact=report_path,
                output_path=output_path,
                s3_documents_prefix=s3_documents_prefix,
                body=body,
                tags=["report", "model-evidence"],
            )
        )

    return documents


def build_explanation_json_documents(
    *,
    output_path: Path,
    s3_documents_prefix: str,
    explanations_dir: Path = Path("artifacts/explanations"),
) -> list[RagDocument]:
    """Convert JSON explanation artifacts into RAG evidence documents."""
    documents: list[RagDocument] = []

    if not explanations_dir.exists():
        return documents

    for json_path in sorted(explanations_dir.rglob("*.json")):
        payload = _read_json(json_path)
        if not isinstance(payload, dict):
            continue

        model_name = str(payload.get("model_name") or json_path.parent.name)
        risk_level = payload.get("risk_level")
        employee_segment = payload.get("employee_segment") or payload.get("segment")
        top_drivers = _infer_top_drivers(payload)

        document_id = f"explanation_{json_path.stem}"
        title = f"Explanation Evidence — {json_path.stem}"

        body = f"""
# {title}

This document summarizes a RetainAI explainability artifact.

## Source Artifact

```text
{json_path}
```

## Model

```text
{model_name}
```

## Top Drivers

{chr(10).join(f"- {driver}" for driver in top_drivers) if top_drivers else "- Not available in source artifact."}

## Payload Preview

```json
{_safe_preview(payload)}
```
""".strip()

        documents.append(
            _document(
                document_id=document_id,
                document_type="explanation",
                title=title,
                source_artifact=json_path,
                output_path=output_path,
                s3_documents_prefix=s3_documents_prefix,
                body=body,
                model_name=model_name,
                employee_segment=str(employee_segment) if employee_segment else None,
                risk_level=str(risk_level) if risk_level else None,
                top_drivers=top_drivers,
                tags=["explainability", "shap", "model-evidence"],
            )
        )

    return documents


def build_feature_importance_documents(
    *,
    output_path: Path,
    s3_documents_prefix: str,
    explanations_dir: Path = Path("artifacts/explanations"),
) -> list[RagDocument]:
    """Convert feature-importance parquet/csv artifacts into document summaries."""
    documents: list[RagDocument] = []

    if not explanations_dir.exists():
        return documents

    candidate_paths = sorted(explanations_dir.rglob("feature_importance.*"))

    for artifact_path in candidate_paths:
        preview = None

        try:
            if artifact_path.suffix == ".csv":
                import pandas as pd  # type: ignore

                preview = pd.read_csv(artifact_path).head(15).to_markdown(index=False)
            elif artifact_path.suffix == ".parquet":
                import pandas as pd  # type: ignore

                preview = pd.read_parquet(artifact_path).head(15).to_markdown(index=False)
        except Exception as exc:
            preview = f"Unable to preview artifact locally: {exc}"

        if preview is None:
            continue

        model_name = artifact_path.parent.name
        title = f"Global Driver Summary — {model_name}"

        body = f"""
# {title}

This document summarizes global feature-importance evidence for RetainAI.

## Source Artifact

```text
{artifact_path}
```

## Preview

{preview}
""".strip()

        documents.append(
            _document(
                document_id=f"global_drivers_{model_name}",
                document_type="global_drivers",
                title=title,
                source_artifact=artifact_path,
                output_path=output_path,
                s3_documents_prefix=s3_documents_prefix,
                body=body,
                model_name=model_name,
                tags=["global-drivers", "feature-importance", "shap"],
            )
        )

    return documents


def build_rag_documents(
    *,
    output_path: Path = DEFAULT_DOCUMENTS_PATH,
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    s3_documents_prefix: str = DEFAULT_S3_DOCUMENTS_PREFIX,
) -> list[RagDocument]:
    """Build and write all available RAG evidence documents."""
    output_path.mkdir(parents=True, exist_ok=True)

    documents: list[RagDocument] = [
        build_responsible_use_document(
            output_path=output_path,
            s3_documents_prefix=s3_documents_prefix,
        )
    ]

    registry_document = build_model_registry_document(
        output_path=output_path,
        s3_documents_prefix=s3_documents_prefix,
    )
    if registry_document is not None:
        documents.append(registry_document)

    documents.extend(
        build_report_documents(
            output_path=output_path,
            s3_documents_prefix=s3_documents_prefix,
        )
    )
    documents.extend(
        build_explanation_json_documents(
            output_path=output_path,
            s3_documents_prefix=s3_documents_prefix,
        )
    )
    documents.extend(
        build_feature_importance_documents(
            output_path=output_path,
            s3_documents_prefix=s3_documents_prefix,
        )
    )

    for document in documents:
        target_path = output_path / document.filename
        target_path.write_text(document.to_markdown(), encoding="utf-8")

    manifest = build_manifest(
        documents=documents,
        local_documents_path=output_path,
        s3_documents_prefix=s3_documents_prefix,
    )
    write_manifest(manifest, manifest_path)

    return documents


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build RetainAI RAG evidence documents.")
    parser.add_argument("--output-path", default=str(DEFAULT_DOCUMENTS_PATH))
    parser.add_argument("--manifest-path", default=str(DEFAULT_MANIFEST_PATH))
    parser.add_argument("--s3-documents-prefix", default=DEFAULT_S3_DOCUMENTS_PREFIX)
    return parser.parse_args()


def main() -> None:
    """CLI entrypoint."""
    args = _parse_args()
    documents = build_rag_documents(
        output_path=Path(args.output_path),
        manifest_path=Path(args.manifest_path),
        s3_documents_prefix=args.s3_documents_prefix,
    )
    print(f"Generated {len(documents)} RAG evidence documents.")
    print(f"Output path: {args.output_path}")
    print(f"Manifest path: {args.manifest_path}")


if __name__ == "__main__":
    main()
