import os
from datetime import datetime
from pathlib import Path

import click
from loguru import logger

from second_brain.app import configure_logging

_DEFAULT_DIR = "~/second_brain"


@click.group()
def main():
    """Second Brain — capture quick thoughts from the command line."""
    configure_logging()


@main.command()
@click.argument("thought")
def new(thought):
    """Save THOUGHT as a timestamped markdown file."""
    storage_dir = Path(os.environ.get("SECOND_BRAIN_DIR", _DEFAULT_DIR)).expanduser()
    storage_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    filename = now.strftime("%Y-%m-%dT%H-%M-%S") + ".md"
    filepath = storage_dir / filename

    filepath.write_text(f"# {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n{thought}\n")

    click.echo(f"Saved: {filepath}")
    logger.debug("Saved thought to {}", filepath)


@main.command(name="list")
def list_notes():
    """List all saved notes."""
    storage_dir = Path(os.environ.get("SECOND_BRAIN_DIR", _DEFAULT_DIR)).expanduser()
    click.echo(str(storage_dir))

    if not storage_dir.exists():
        click.echo("(no notes yet)")
        return

    files = sorted(storage_dir.glob("*.md"))
    if not files:
        click.echo("(no notes yet)")
        return

    for i, f in enumerate(files, 1):
        click.echo(f"  {i}. {f.name}")


@main.command()
@click.argument("number", type=int)
def show(number):
    """Print the contents of note NUMBER."""
    storage_dir = Path(os.environ.get("SECOND_BRAIN_DIR", _DEFAULT_DIR)).expanduser()
    files = sorted(storage_dir.glob("*.md"))

    if not files:
        click.echo("No notes found.")
        return

    if number < 1 or number > len(files):
        raise click.BadParameter(
            f"must be between 1 and {len(files)}", param_hint="NUMBER"
        )

    click.echo(files[number - 1].read_text())
