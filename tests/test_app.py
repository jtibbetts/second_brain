from click.testing import CliRunner

from second_brain.cli import main


def test_new_creates_file(tmp_path, monkeypatch):
    monkeypatch.setenv("SECOND_BRAIN_DIR", str(tmp_path))
    runner = CliRunner()
    result = runner.invoke(main, ["new", "My brilliant idea about caching"])
    assert result.exit_code == 0
    files = list(tmp_path.glob("*.md"))
    assert len(files) == 1
    assert "My brilliant idea about caching" in files[0].read_text()


def test_new_prints_saved_path(tmp_path, monkeypatch):
    monkeypatch.setenv("SECOND_BRAIN_DIR", str(tmp_path))
    runner = CliRunner()
    result = runner.invoke(main, ["new", "Another idea"])
    assert "Saved:" in result.output


def test_new_file_contains_timestamp(tmp_path, monkeypatch):
    monkeypatch.setenv("SECOND_BRAIN_DIR", str(tmp_path))
    runner = CliRunner()
    runner.invoke(main, ["new", "Time-stamped thought"])
    content = next(tmp_path.glob("*.md")).read_text()
    # File should start with a markdown h1 date header
    assert content.startswith("# 20")


def test_list_shows_path_and_files(tmp_path, monkeypatch):
    monkeypatch.setenv("SECOND_BRAIN_DIR", str(tmp_path))
    (tmp_path / "2026-03-22T09-00-00.md").write_text("# note one\n")
    (tmp_path / "2026-03-22T10-00-00.md").write_text("# note two\n")
    runner = CliRunner()
    result = runner.invoke(main, ["list"])
    assert result.exit_code == 0
    assert str(tmp_path) in result.output
    assert "1." in result.output
    assert "2." in result.output


def test_show_prints_content(tmp_path, monkeypatch):
    monkeypatch.setenv("SECOND_BRAIN_DIR", str(tmp_path))
    (tmp_path / "2026-03-22T09-00-00.md").write_text("# note one\n\nFirst thought.\n")
    (tmp_path / "2026-03-22T10-00-00.md").write_text("# note two\n\nSecond thought.\n")
    runner = CliRunner()
    result = runner.invoke(main, ["show", "2"])
    assert result.exit_code == 0
    assert "Second thought." in result.output


def test_show_out_of_range(tmp_path, monkeypatch):
    monkeypatch.setenv("SECOND_BRAIN_DIR", str(tmp_path))
    (tmp_path / "2026-03-22T09-00-00.md").write_text("# note\n")
    runner = CliRunner()
    result = runner.invoke(main, ["show", "99"])
    assert result.exit_code != 0


def test_list_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("SECOND_BRAIN_DIR", str(tmp_path))
    runner = CliRunner()
    result = runner.invoke(main, ["list"])
    assert result.exit_code == 0
    assert "(no notes yet)" in result.output
