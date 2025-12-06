import polars as pl
import pytest

from app import app as flask_app


@pytest.fixture()
def client(monkeypatch):
    flask_app.config["TESTING"] = True

    class DummyConnection:
        pass

    def dummy_get_db():
        class _DummyContext:
            def __enter__(self):
                return DummyConnection()

            def __exit__(self, exc_type, exc, tb):
                return False

        return _DummyContext()

    monkeypatch.setattr("app.get_db", dummy_get_db)
    with flask_app.test_client() as client:
        yield client


@pytest.fixture()
def mock_polars(monkeypatch):
    def factory(df: pl.DataFrame):
        def fake_read_database(query, conn, execute_options=None):
            return df

        monkeypatch.setattr("app.pl.read_database", fake_read_database)

    return factory
