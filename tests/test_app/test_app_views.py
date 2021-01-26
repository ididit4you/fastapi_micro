def test_healthcheck(cli):
    """Healthcheck is alive."""
    resp = cli.get(cli.app.url_path_for('healthcheck'))
    resp_json = resp.json()
    assert resp.status_code == 200
    assert resp_json == {'message': 'OK'}
