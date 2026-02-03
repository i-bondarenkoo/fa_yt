from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Path
from fastapi import Depends, HTTPException, status
from core.models.db_helper import db_helper
from api_v1.products import crud
from core.models.product import Product


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    product = await crud.get_product(
        session=session,
        product_id=product_id,
    )
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Продукт с идентификатором {product_id} не найден",
    )
