# Improvements

## Exception handlers

- Sadly proper exception handler is missing in this project, since I tried to complete this project as fast as I could. But if I had more time, perhaps I would make similar handler I perviously made in [this](https://github.com/ArataKido/kotlin/blob/main/src/main/kotlin/middleware/ExceptionHandler.kt) project.

## Tests

- This project lacks tests, functionality is slightly big, and it takes time to test everything. Basic unit tests would help this project a lot. Would suggest too make tests, and then start integrating exception handler, and refactor code base.

## Security

- I was not focused hardly on the security, but I do have a concern regarding placing route for getting all users from database in '/users' since it is easy to mess up. I would prefer making separate router for admin usage.  I would like to note that in update method for users, I left access for field `is_admin`, but this was only for test purposes, and if it is planed to launch it in the production, I would advice to remove it, unless you want users to make admin accounts.

- Additionally, the way how user account is gets confirmed need improvement, what code does is, it turn user data into base64, which is unsafe and can be decoded by anyone. what should be done instead is, either make stateless code, like right now, but hash it, so only our backend could decode it and active the user. There is also way of doing the activation by storing some code in database, but I think stateless way would fit better, because it decreases requests to database.

## Bugs

- [Order router](../app/routers/orders.py) and [Service](../app/services/order_service.py) have a bug, which has not been fixed yet. Response and Request schemas must be refactored to not accept the user id, and instead they should grab it from token and verify if the order belongs to the user from token.

- [Logging Middleware](../app/middleware/logging_middleware.py) is turned off due to malfunctioning. It cannot process the data from body, which is needed for authentication. The issue is withing how ASGI works, and the body is being consumed. I tried to fix this issue, but could not find solution and need to dive a bit into how to handle streams. Might as well fix it later.
If you want to see the logger in action, you can turn on in [main.py](../app/main.py), it should work for routes where authentication is not needed.

- One more thing which i did not think of is, to create a cart right after the user is registered. Right now, cart entity gets created only when user tries to add an item into it for the first time, which i think is not what supposed to happen...
