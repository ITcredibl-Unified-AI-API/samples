from itcredibl_enterprise.health import ProviderHealth
from itcredibl_enterprise.policies import CostPolicy, RoutingPolicy


def test_routing_pick():
    p = RoutingPolicy(allow=["a", "b", "c"])
    chosen = p.pick(["a", "b", "c"], ProviderHealth())
    assert chosen in {"a", "b", "c"}


def test_cost_policy_allows_unknown():
    assert CostPolicy(max_cost=0.01).allow({}) is True
