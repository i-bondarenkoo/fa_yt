from pydantic import BaseModel, ConfigDict


class ProductBaseSchema(BaseModel):
    name: str
    description: str
    price: int


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductSchema(ProductBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductUpdateSchema(ProductCreateSchema):
    pass


class ProductUpdatePartialSchema(ProductCreateSchema):
    name: str | None = None
    description: str | None = None
    price: int | None = None
