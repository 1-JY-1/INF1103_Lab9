from product import Product, physicalProduct, digitalProduct


class ProductFactory:

    @staticmethod
    def create(product_type: str, *args, **kwargs) -> Product:

        if product_type.lower() == "physical":
            return physicalProduct(*args, **kwargs)

        elif product_type.lower() == "digital":
            return digitalProduct(*args, **kwargs)

        else:
            raise ValueError(f"Unknown product type: {product_type}")