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
from core.models.order_product_association import OrderProductAssociation
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
    pass


async def get_orders_with_products(
    session: AsyncSession,
) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def create_orders_and_products(session: AsyncSession):
    order1 = await create_order(session)
    order2 = await create_order(
        session=session,
        promocode="promo",
    )
    mouse = await create_product(
        session,
        name="Mouse",
        description="Gaming mouse",
        price=123,
    )
    keyboard = await create_product(
        session,
        name="Keyboard",
        description="Keyboard mouse",
        price=533,
    )
    display = await create_product(
        session,
        name="display 24f",
        description="super monitor",
        price=666,
    )
    order1 = await session.scalar(
        select(Order)
        .where(Order.id == order1.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order2 = await session.scalar(
        select(Order)
        .where(Order.id == order2.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order1.products.append(mouse)
    order1.products.append(display)
    # order2.products.append(keyboard)
    # order2.products.append(display)
    # можно добавить в список присваиванием
    order2.products = [keyboard, display]
    await session.commit()


async def create_order(session: AsyncSession, promocode: str | None = None):
    order = Order(
        promocode=promocode,
    )
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
):
    product = Product(
        name=name,
        description=description,
        price=price,
    )
    session.add(product)
    await session.commit()
    return product


async def demo_get_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for product in order.products:
            print("-", product.id, product.name, product.price)


async def demo_get_orders_with_products_with_assoc(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)

    for order in orders:
        print(order.id, order.promocode, order.created_at, "products:")
        for order_product_details in order.products_details:
            print(
                "-",
                order_product_details.product.id,
                order_product_details.product.name,
                order_product_details.product.price,
                "qty:",
                order_product_details.count,
            )


async def get_orders_with_products_assoc(
    session: AsyncSession,
) -> list[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            ),
        )
        .order_by(Order.id)
    )
    orders = await session.scalars(stmt)
    return list(orders)


async def create_gift_product_for_existing_orders(session: AsyncSession):
    orders = await get_orders_with_products_assoc(session)
    gift_product = await create_product(
        session,
        name="Gift",
        description="Gift for u",
        price=0,
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(
                count=1,
                unit_price=0,
                product=gift_product,
            )
        )
    await session.commit()


async def demo_m2m(session: AsyncSession):
    # await create_orders_and_products(session)
    # await demo_get_orders_with_products_through_secondary(session)
    await demo_get_orders_with_products_with_assoc(session)
    # await create_gift_product_for_existing_orders(session)


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session)
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
