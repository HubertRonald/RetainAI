from modules.security.usage_quota import InMemoryUsageQuota


def test_allows_three_requests_and_rejects_the_fourth() -> None:
    quota = InMemoryUsageQuota(limit=3, window_seconds=86_400)

    decisions = [
        quota.consume("203.0.113.10", "advisor", provider="mock")
        for _ in range(4)
    ]

    assert [decision.allowed for decision in decisions] == [True, True, True, False]
    assert decisions[2].remaining == 0
    assert decisions[3].request_count == 3
    assert decisions[3].remaining == 0


def test_raw_client_identifier_is_not_used_as_quota_key() -> None:
    quota = InMemoryUsageQuota(limit=3, window_seconds=86_400)

    decision = quota.consume("203.0.113.10", "advisor", provider="mock")

    assert decision.quota_key != "203.0.113.10"
    assert len(decision.quota_key) == 64
