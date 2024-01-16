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


def test_list_todos(session, client, user, token):
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert len(response.json()["todos"]) == 5
