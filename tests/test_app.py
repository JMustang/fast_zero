def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')  # Act

    assert response.status_code == 200  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


# def test_delete_user_invalid_id(client, user):
#     # Escolha um ID que você sabe que não existe no seu sistema
#     invalid_user_id = 9999

#     response = client.delete(f'/users/{invalid_user_id}')

#     assert response.status_code == 404
#     assert response.json() == {'detail': 'User not found'}
