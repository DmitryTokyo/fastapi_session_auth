from src.my_apps.users.crud import crud_user
from src.my_apps.users.schemas import UserRegistrate, UserUpdateDB


async def test_get_user_by_email(test_session, user_factory):
    user = await user_factory()
    exist_user = await crud_user.get_by_email(db_session=test_session, email=user.email)
    assert exist_user.email == user.email


async def test_creating_user(test_session, mocker):
    mocker.patch('src.my_apps.users.crud.get_password_hash', return_value='hashed_password')
    user_schema = UserRegistrate(username='test user', email='test@email.com', password='password')
    new_user = await crud_user.create_user(test_session, user_schema)
    assert new_user.username == 'test user'
    assert new_user.email == 'test@email.com'
    assert new_user.hashed_password == 'hashed_password'


async def test_deleting_user(test_session, user_factory):
    user = await user_factory()
    await crud_user.delete(db_session=test_session, obj_id=user.id)
    exist_user = await crud_user.get_single(db_session=test_session, obj_id=user.id)
    assert exist_user is None


async def test_get_user_by_id(test_session, user_factory):
    user = await user_factory()
    exist_user = await crud_user.get_single(db_session=test_session, obj_id=user.id)
    assert exist_user.id == user.id
    assert exist_user.email == user.email


async def test_get_all_users(test_session, clean_users, user_factory):
    await user_factory(username='first user')
    await user_factory(username='second user')
    all_users = await crud_user.get_multi(db_session=test_session)
    assert len(all_users) == 2


async def test_update_user(test_session):
    user_schema = UserRegistrate(username='before updating', email='test@email.com', password='password')
    user = await crud_user.create_user(test_session, user_schema)
    update_user_schema = UserUpdateDB(username='after updating', email='super_test@email.com')
    await crud_user.update(db_session=test_session, obj_id=user.id, schema_update=update_user_schema)
    await test_session.refresh(user)
    assert user.username == 'after updating'
    assert user.email == 'super_test@email.com'
