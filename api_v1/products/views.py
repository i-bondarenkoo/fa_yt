from fastapi import APIRouter, status
from fastapi import Depends
from api_v1.products import crud
from core.models.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.products.schemas import (
    ProductSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductUpdatePartialSchema,
)
from api_v1.products.dependencies import product_by_id
from core.models.product import Product

router = APIRouter(
    tags=["Products"],
)


@router.get("/", response_model=list[ProductSchema])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session=session)


@router.post(
    "/",
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreateSchema,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(
        session=session,
        product_in=product_in,
    )


@router.get("/{product_id}/", response_model=ProductSchema)
async def get_product(
    product: Product = Depends(product_by_id),
):
    return product


@router.put("/{product_id}/")
async def update_product(
    product_update: ProductUpdateSchema,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{product_id}/")
async def update_product_partial(
    product_update: ProductUpdatePartialSchema,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete(
    "/{product_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(
        session=session,
        product=product,
    )
