#!/usr/bin/env python3
"""Insert or refresh durable RetainAI release documentation."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT_BLOCK = """<!-- retainai-delivery-safety:start -->
## Application delivery and data safety

RetainAI separates application promotion, infrastructure management, and data
processing into independent operational paths.

Dashboard and backend images are promoted manually from `main` through GitHub
Actions using short-lived cloud identity and immutable image references.
Documentation-only changes do not qualify for an application release.

Terraform remains the source of truth for cloud infrastructure, including
domains, certificates, IAM, secrets, runtime configuration, quotas, and the
future protected S3 data-lake foundation. Routine application releases do not
run Terraform or perform S3 data operations.

See:

- [Manual multi-cloud application release](./docs/multicloud/manual_application_release.md)
- [Multi-cloud architecture](./docs/multicloud/README.md)
- [Data architecture](./docs/data/README.md)
- [Architecture decisions](./docs/architecture/README.md)
<!-- retainai-delivery-safety:end -->"""


MULTICLOUD_BLOCK = """<!-- retainai-manual-release:start -->
## Manual application promotion

RetainAI uses a manually dispatched GitHub Actions workflow to promote immutable
dashboard and backend images from the protected `main` branch.

The workflow evaluates component-specific build inputs before cloud
authentication. Documentation, diagrams, Markdown, and other non-runtime changes
do not qualify by themselves.

AWS authentication uses GitHub OIDC. Google Cloud authentication uses Workload
Identity Federation. Long-lived AWS keys and Google service-account key files
are not used.

Application releases update only Cloud Run and Lambda image references. They do
not run Terraform, manage S3, or recreate infrastructure.

See
[Manual multi-cloud application release](./manual_application_release.md)
for the complete operating contract.
<!-- retainai-manual-release:end -->"""


def repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def replace_or_insert(
    text: str,
    block: str,
    start_marker: str,
    end_marker: str,
    anchors: tuple[str, ...],
) -> str:
    pattern = re.compile(
        re.escape(start_marker)
        + r".*?"
        + re.escape(end_marker),
        re.DOTALL,
    )

    if pattern.search(text):
        return pattern.sub(block, text, count=1)

    for anchor in anchors:
        if anchor in text:
            return text.replace(
                anchor,
                block.rstrip() + "\n\n" + anchor,
                1,
            )

    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def main() -> None:
    root = repository_root()

    readme = root / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    readme_text = replace_or_insert(
        readme_text,
        ROOT_BLOCK,
        "<!-- retainai-delivery-safety:start -->",
        "<!-- retainai-delivery-safety:end -->",
        (
            "## Roadmap",
            "## Documentation",
            "## License",
        ),
    )
    readme.write_text(
        readme_text.rstrip() + "\n",
        encoding="utf-8",
    )

    multicloud = root / "docs/multicloud/README.md"
    multicloud.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if multicloud.exists():
        multicloud_text = multicloud.read_text(
            encoding="utf-8"
        )
    else:
        multicloud_text = "# RetainAI multi-cloud architecture\n"

    multicloud_text = replace_or_insert(
        multicloud_text,
        MULTICLOUD_BLOCK,
        "<!-- retainai-manual-release:start -->",
        "<!-- retainai-manual-release:end -->",
        (
            "## Architectural principles",
            "## References",
        ),
    )
    multicloud.write_text(
        multicloud_text.rstrip() + "\n",
        encoding="utf-8",
    )

    print(f"Updated: {readme}")
    print(f"Updated: {multicloud}")


if __name__ == "__main__":
    main()
