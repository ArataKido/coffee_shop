class RepositoryException(Exception):
    """Base exception for all domain-specific exceptions."""



class EntityNotFoundException(RepositoryException):
    """Raised when an entity cannot be found."""

    def __init__(self, entity_type: str, entity_id: any):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.message = f"{entity_type} with id {entity_id} not found"
        super().__init__(self.message)


class CartItemNotFoundException(EntityNotFoundException):
    """Raised when a cart item cannot be found."""

    def __init__(self, user_id: int, product_id: int):
        self.user_id = user_id
        self.product_id = product_id
        self.message = f"Cart item for user {user_id} with product {product_id} not found"
        super().__init__("CartItem", f"user_id={user_id}, product_id={product_id}")
