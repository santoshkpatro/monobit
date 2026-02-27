from django.db import models

from monobit.models.base import BaseUUIDTimestampModel
from monobit.models.choices import IssueStatusChoices


class Issue(BaseUUIDTimestampModel):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="issues"
    )
    first_seen = models.DateTimeField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    times_seen = models.IntegerField(default=1)
    title = models.CharField(max_length=256)
    status = models.CharField(
        max_length=32,
        choices=IssueStatusChoices.choices,
        default=IssueStatusChoices.OPEN,
    )

    class Meta:
        db_table = "issues"


class IssueFingerprint(BaseUUIDTimestampModel):
    issue = models.ForeignKey(
        "Issue", on_delete=models.CASCADE, related_name="fingerprints"
    )
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="project_fingerprints"
    )
    hash = models.CharField(max_length=128)

    class Meta:
        db_table = "issue_fingerprints"
        constraints = [
            models.UniqueConstraint(
                fields=["issue", "project"], name="unique_issue_project_fingerprint"
            )
        ]
