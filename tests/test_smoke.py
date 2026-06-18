from agent_cascade import __version__
from agent_cascade.config import Settings


def test_version():
    assert __version__ == "0.1.0"


def test_default_flags_conservative():
    """Connectors are off by default until staging deploys are green."""
    s = Settings()
    assert s.flags.salesforce_connector is False
    assert s.flags.zendesk_connector is False
