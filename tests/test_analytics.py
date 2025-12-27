def test_profitability_expectations_returns_list():
    from app.analytics.handlers import profitability_expectations

    class DummyEngine:
        def begin(self):
            class Conn:
                def execute(self, *_):
                    return []

                def __enter__(self):
                    return self

                def __exit__(self, *args):
                    pass

            return Conn()

    result = profitability_expectations(DummyEngine())
    assert isinstance(result, list)
