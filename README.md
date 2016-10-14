# Kyrkosok.se API

## Requirements

 - Python 3.5+
 - Flask(`pip install flask`)
 - Flask RESTful(`pip install flask-restful`)
 - SQLAlchemy(`pip install sqlalchemy`)

## Database

The SQLite database provided within this repository is created in another repository.

## Usage

### Get single church by Wikidata ID(exclude `Q`):

```
/churches/<string:wikidata>
```

### Search by label:

```
/churches/label?text=<string:value>
```

### Search within bounding box:

```
/churches/bbox?south=<float>&east=<float>&north=<float>&west=<float>
```