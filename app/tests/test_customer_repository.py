from app.repositories import customer_repository


class EmptyMaybeSingleQuery:
    def select(self, *_columns):
        return self

    def eq(self, *_args):
        return self

    def maybe_single(self):
        return self

    def execute(self):
        return None


class EmptySupabase:
    def table(self, _table_name):
        return EmptyMaybeSingleQuery()


def test_get_customer_by_phone_returns_none_for_missing_customer(monkeypatch):
    monkeypatch.setattr(
        customer_repository,
        "supabase",
        EmptySupabase(),
    )

    assert customer_repository.get_customer_by_phone("+77000000000") is None


def test_get_customer_by_id_returns_none_for_missing_customer(monkeypatch):
    monkeypatch.setattr(
        customer_repository,
        "supabase",
        EmptySupabase(),
    )

    assert customer_repository.get_customer_by_id(999999) is None
