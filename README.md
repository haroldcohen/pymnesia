# Pymnesia

Pymnesia provides with a real in memory database and ORM to be used in unit tests and in staging environment when
persistence adapters are not available yet.
This tool is likely to be used within decoupled architecture projects.

## Overview

The current version is beta, but the project is stable and offers a wide range of features that can already be used in
your projects :

- Declare entities with various field types (int, str, float, bool, date, one to one relation, one to many relation)
- Save entities in an in memory database
- Commit and rollback
- Query stored entities using a very lightweight api and intuitive syntax

## Basic user documentation

Until a more detailed documentation is released, please refer to the examples below for usage.

### Entities

#### Declaring a simple entity

```python
from uuid import UUID

from pymnesia.api.entities.base import declarative_base


class CarEngine(declarative_base()):
    __tablename__ = "car_engines"

    id: UUID

    horsepower: int
```

#### Declaring an entity with a 'one to one' relation

```python
from uuid import UUID

from pymnesia.api.entities.base import declarative_base


class CarModel(declarative_base()):
    __tablename__ = "car_models"

    id: UUID

    name: str

    engine: CarEngine
```

#### Declaring an entity with a 'one to many' relation

The relation api can be used to specify custom options (for now the reverse name and whether the relation is optional or
not).

```python
from uuid import UUID

from pymnesia.api.entities.base import declarative_base
from pymnesia.api.entities.fields import field, relation


class Car(declarative_base()):
    __tablename__ = "cars"

    id: UUID

    name: str = field(default="Peugeot 3008")

    drivers: List[Driver] = relation(reverse="car_foo")
```

### Command

#### Save and commit

```python
from uuid import uuid4

from pymnesia.api.unit_of_work import uow
from pymnesia.api.command import transaction

unit_of_work = uow()
new_transaction = transaction(unit_of_work=unit_of_work)

v12_engine = CarEngine(id=uuid4(), horsepower=400)
aston_martin = CarModel(id=uuid4(), engine_id=v12_engine.id)

unit_of_work.save_entity(entity=v12_engine)
unit_of_work.save_entity(entity=aston_martin)
new_transaction.commit()
```

Querying the database for car models will return one car model (The output will be 400).

```python
for car in unit_of_work.query().cars().fetch():
    print(car.engine.horsepower)
```

#### Rollback

```python
from uuid import uuid4

from pymnesia.api.unit_of_work import uow
from pymnesia.api.command import transaction

unit_of_work = uow()
new_transaction = transaction(unit_of_work=unit_of_work)

v12_engine = CarEngine(id=uuid4(), horsepower=400)
unit_of_work.save_entity(entity=v12_engine)
new_transaction.rollback()

v8_engine = CarEngine(id=uuid4(), horsepower=300)
unit_of_work.save_entity(entity=v8_engine)
new_transaction.commit()
```

Querying the database for car engines will return the v8 engine alone (The output will be 300).

```python
for engine in unit_of_work.query().car_engines().fetch():
    print(engine.horsepower)
```

### Query

#### Fetch

Fetch allows to retrieve multiple results of a query.
To query an entity model, call query() in the unit of work instance containing your entities.
Then simply call a method using the tablename you declared for said entity.

For instance, if you declare the entity below:

```python
from uuid import UUID

from pymnesia.api.entities.base import declarative_base


class Address(declarative_base()):
    __tablename__ = "addresses"

    id: UUID

    street_name: str
```

You will query addresses as follows:

```python
for car in unit_of_work.query().addresses().fetch():
    # whatever you need to do
    pass
```

#### Fetch one

Fetch allows to retrieve the first result of a query.

Given you have two cars in your in memory database, fetch_one() will return the entity that was saved first.

```python
car = unit_of_work.query().addresses().fetch_one()
```

#### Where Or clauses

One of the great features of Pymnesia is how you can add where or clauses to you queries.

<b><i>Where clause</i></b>

To add a where clause use the where method when querying an entity.

<i> 'Equal' operator </i>

The query below will return every car engine that has a 400 horsepower:

```python
for car in unit_of_work.query().car_engines().where({"horsepower": 400}).fetch():
    # whatever you need to do
    pass
```

<i> 'Not equal' operator </i>

The query below will return every car engine that doesn't have a 400 horsepower:

```python
for car in unit_of_work.query().car_engines().where({"horsepower::not": 400}).fetch():
    # whatever you need to do
    pass
```

<i> 'Greater than' operator </i>

The query below will return every car engine that have horsepower greater than 400:

```python
for car in unit_of_work.query().car_engines().where({"horsepower::gt": 400}).fetch():
    # whatever you need to do
    pass
```

<i> 'Greater than or equal to' operator </i>

The query below will return every car engine that have horsepower greater than or equal to 400:

```python
for car in unit_of_work.query().car_engines().where({"horsepower::gte": 400}).fetch():
    # whatever you need to do
    pass
```

<i> 'Less than' operator </i>

The query below will return every car engine that have horsepower lesser than 400:

```python
for car in unit_of_work.query().car_engines().where({"horsepower::lt": 400}).fetch():
    # whatever you need to do
    pass
```

<i> 'Less than or equal to' operator </i>

The query below will return every car engine that have horsepower lesser than or equal to 400:

```python
for car in unit_of_work.query().car_engines().where({"horsepower::lte": 400}).fetch():
    # whatever you need to do
    pass
```

<i> 'Match' operator </i>

The query below will return every car that have a name matching the provided regex:

```python
for car in unit_of_work.query().cars().where({"name::match": r'^Peugeot .*$'}).fetch():
    # whatever you need to do
    pass
```

<i> 'In' operator </i>

The query below will return every car that have a value included in the provided list:

```python
for car in unit_of_work.query().cars().where({"name::in": ["Aston Martin Valkyrie", "Porsche GT3"]}).fetch():
    # whatever you need to do
    pass
```

<i> Relational queries </i>

Every operator documented above can be used to make relational queries:

```python
for car in unit_of_work.query().cars().where({"engine.horsepower::gt": 400}).fetch():
    # whatever you need to do
    pass
```

<b><i>Or clauses</i></b>

You can add one or more 'or clauses' to a query.
Every condition in a 'or clause' is evaluated as OR AND.

For instance the query below:

```python
query = unit_of_work.query().cars().where({"name": "Peugeot 3008"})
query.or_({"name::match": r'^Peugeot .*$', "engine.horsepower::gt": 100})
```

Is the equivalent of an SQL query:

```sql
SELECT *
FROM cars
         JOIN car_engines ON car_engines.id = cars.engine_id
WHERE cars.name = 'Peugeot 3008'
   OR (cars.name LIKE '^Peugeot .*$' AND car_engines.horsepower > 100)
```

Multiple 'or clauses' remain independent of one another:

```python
query = unit_of_work.query().cars().where({"name": "Peugeot 3008"})
query.or_({"name::match": r'^Peugeot .*$', "engine.horsepower::gt": 100})
query.or_({"engine.horsepower::gte": 200})
```

Is the equivalent of an SQL query:

```sql
SELECT *
FROM cars
         JOIN car_engines ON car_engines.id = cars.engine_id
WHERE cars.name = 'Peugeot 3008'
   OR (cars.name LIKE '^Peugeot .*$' AND car_engines.horsepower > 100)
   OR (car_engines.horsepower >= 200)
```

<b><i>Where clause using composition</i></b>

The entities can be queried using composition rather than declarative conditions.
<b>The example below makes little sense</b>, but this feature can be powerful to make complex queries when operator
functions
are not available to perform the requested
operation.

```python
from typing import Iterable
from functools import partial


def car_name_func(entities_: Iterable, field: str, value: str, *args, **kwargs) -> filter:
    return filter(lambda e: getattr(e, field) == value, entities_)


partial_k2000_func = partial(
    car_name_func,
    field="name",
    value="K2000",
)

partial_gran_torino_func = partial(
    car_name_func,
    field="name",
    value="Gran Torino",
)

query = unit_of_work.query().cars().where_with_composition([
    partial_k2000_func,
    partial_gran_torino_func,
])
```

#### Limit

You can limit the number of result using the limit() method.

The query below will limit the number of results to 5 car engines:

```python
for car in unit_of_work.query().car_engines().limit(5).fetch():
    # whatever you need to do
    pass
```

#### Order by

You can order by your results by specifying a direction and a key.

The query below will order the results on the field 'name' in descending order.

```python
for car in unit_of_work.query().cars().order_by(direction="desc", key="name").fetch():
    # whatever you need to do
    pass
```