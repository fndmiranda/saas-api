import pytest
from typer.testing import CliRunner

from app.cli import cli

runner = CliRunner()


@pytest.mark.asyncio
async def test_cli_should_show_routes():
    """Test cli should show routes."""

    result = runner.invoke(cli, ["route", "show"])
    assert result.exit_code == 0
