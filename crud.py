import asyncio
from core.models.db_helper import db_helper
from core.models.user import User
from core.models.profile import Profile
from core.models.post import Post
from core.models.order import Order
from core.models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import selectinload, joinedload


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user", user)
    return user


async def get_usr_by_username(session: AsyncSession, username: str) -> User | None:
    query = select(User).where(User.username == username)
    result: Result = await session.execute(query)
    user: User | None = result.scalar_one_or_none()
    # user : User | None = await session.scalar(stmt)
    print("current user", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    query = select(User).options(joinedload(User.profile)).order_by(User.id)
    result: Result = await session.execute(query)
    users = result.scalars().all()
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *posts_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(
    session: AsyncSession,
):
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    users = result.scalars()
    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print("post", post)
        print("author", post.user)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):

    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(
            joinedload(Profile.user).selectinload(User.posts),
        )
        .where(User.username == "john")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)

async def create_order(session: AsyncSession, promocode: str | None = None):
    order = Order(
        promocode=promocode,
    )
    session.add(order)
    await session.commit()
    return order    

async def main_relations(session: AsyncSession):
    #     user_john = await create_user(session=session, username="john")
    #     user_stepa = await create_user(session=session, username="stepa")
    #     user_alice = await create_user(session=session, username="alice")
    # await get_usr_by_username(session=session, username="123")
    # user_stepa = await get_usr_by_username(session=session, username="stepa")
    # await create_user_profile(
    #     session=session,
    #     user_id=user_stepa.id,
    #     first_name="Stepa",
    # )
    # await create_user_profile(
    #     session=session,
    #     user_id=user_john.id,
    #     first_name="john",
    # )
    # await show_users_with_profiles(session=session)
    # await create_posts(
    #     session,
    #     user_john.id,
    #     "SQLA 2.0",
    #     "SQLA Joins",
    # )
    # await create_posts(
    #     session,
    #     user_stepa.id,
    #     "FastAPI intro",
    # )
    # await get_users_with_posts(session=session)
    # await get_posts_with_authors(session=session)
    # await get_users_with_posts_and_profiles(session=session)
    # await get_profiles_with_users_and_users_with_posts(session=session)


async def demo_m2m(session: AsyncSession):
    order = await create_order(session)
    order2 = await create_order(session=session, promocode='promo')
    


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session)
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
