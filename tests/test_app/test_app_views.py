def test_smoke(cli):
    """Healthcheck is alive."""
    resp = cli.get(cli.app.url_path_for('healthcheck'))
    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json == {'message': 'OK'}

    # Check is database is test database
    db = cli.app.state.db
    assert str(db.url).endswith('pytest')
