import factory.fuzzy

from fast_zero.models import Todo, TodoState, User


def test_create_todo(client, token):
    response = client.post(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "state": "draft",
        },
    )
    assert response.json() == {
        "id": 1,
        "title": "Test Todo",
        "description": "This is a test todo",
        "state": "draft",
    }


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker("text")
    description = factory.Faker("text")
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1
