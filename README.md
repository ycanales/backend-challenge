# Challenge Solution

I've implemented the challenge in Python, the project setup and dependency management is done with [poetry](https://python-poetry.org/) and I've added a `.python-version` file which works with the [pyenv](https://github.com/pyenv/pyenv) utility to automatically set the `python` version to use when available.

## Requirements Summary Table

Bonus
-----------
Tests | ✅
--------------------
Money as integers | ✅
-----------------------

## How to run

### Manually
0. `cd` into `challenge` directory.
1. Install dependencies with poetry.
2. Activate virtual environment shell with `poetry shell`
3. Enter `FLASK_APP=challenge/lana.py FLASK_ENV=development python -m flask run`

## Libraries Used

- [flask](https://flask.palletsprojects.com/en/1.1.x/) Flask is a micro framework for developing web apps in Python. Being micro means that you can start your application with a simple core and then add features as you like, using the python libraries that you choose, opposed to a batteries-included approach like the one followed by Django. 

## Will this scale to production?

I chose Flask it because it's a great fit for a small proof-of-concept application but that doesn't mean it can't grow into a proper production-grade application. I see at least three ways in which that transition can be achieved:

- Migrate the business logic to Django and make use of all the great features that come in included in the framework like the ORM, admin interface, forms validation, Class Based Views, authentication and security features, database migrations and lots of other goodies.

- Migrate the business logic to FastAPI, which is a modern and fast framework for building APIs. It relies on standard Python hints (3.6+ required) to provide validation and serialization.

- Keep Flask and add libraries as needed. This would be more work but might be better to keep a tight control on every design decision if it provides a considerable benefit in performance, features or developer experience.

## Database integration

I've chosen [SQLAlchemy](https://www.sqlalchemy.org) as an ORM (Object Relational Mapper) and SQL toolkit for this project. Flask offers integration to it via the [Flask-SQLAlchemy](https://github.com/pallets/flask-sqlalchemy) extension.


## Requirements

Lana has come to conclusion that users are very likely to buy awesome Lana merchandising from a physical store that sells the following 3 products:

```
Code         | Name              |  Price
-----------------------------------------------
PEN          | Lana Pen          |   5.00€
TSHIRT       | Lana T-Shirt      |  20.00€
MUG          | Lana Coffee Mug   |   7.50€
```

Various departments have insisted on the following discounts:

 * The sales department thinks a buy 2 get 1 free promotion will work best (buy two of the same product, get one free), and would like this to only apply to `PEN` items.

 * The CFO insists that the best way to increase sales is with discounts on bulk purchases (buying x or more of a product, the price of that product is reduced), and requests that if you buy 3 or more `TSHIRT` items, the price per unit should be reduced by 25%.

Your task is to implement a simple checkout server and client that communicate over the network.

We'd expect the server to expose the following independent operations:

- Create a new checkout basket
- Add a product to a basket
- Get the total amount in a basket
- Remove the basket

The server must support concurrent invocations of those operations: any of them may be invoked at any time, while other operations are still being performed, even for the same basket.

At this stage, the service shouldn't use any external databases of any kind, but it should be possible to add one easily in the future.

Implement a checkout service and its client that fulfills these requirements.

Examples:

    Items: PEN, TSHIRT, MUG
    Total: 32.50€

    Items: PEN, TSHIRT, PEN
    Total: 25.00€

    Items: TSHIRT, TSHIRT, TSHIRT, PEN, TSHIRT
    Total: 65.00€

    Items: PEN, TSHIRT, PEN, PEN, MUG, TSHIRT, TSHIRT
    Total: 62.50€

**The solution should:**

- Build and execute in a Unix operating system.
- Focus on solving the business problem (less boilerplate!)
- Have a clear structure.
- Be easy to grow with new functionality.
- Don't include binaries, and use a dependency management tool.

**Bonus Points For:**

- Be written in Go (let us know if this is your first time!)
- Unit/Functional tests
- Dealing with money as integers
- Formatting money output
- Useful comments
- Documentation
- Docker images / CI
- Commit messages (include .git in zip)
- Thread-safety
- Clear scalability
