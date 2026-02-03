from sqlalchemy.ext.asyncio import AsyncSession
from core.models.product import Product
from sqlalchemy.engine import Result
from sqlalchemy import select
from api_v1.products.schemas import (
    ProductCreateSchema,
    ProductSchema,
    ProductUpdateSchema,
    ProductUpdatePartialSchema,
)


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(product_id: int, session: AsyncSession) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(
    product_in: ProductCreateSchema,
    session: AsyncSession,
):
    new_product = Product(**product_in.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdateSchema | ProductUpdatePartialSchema,
    partial: bool = False,
) -> ProductSchema:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product


async def delete_product(
    session: AsyncSession,
    product: Product,
) -> None:
    await session.delete(product)
    await session.commit()
