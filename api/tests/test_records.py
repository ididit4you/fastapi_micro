def test_records(cli):
    """Records enpoint is alive."""
    resp = cli.get(cli.app.url_path_for('records'))
    assert resp.status_code == 200
