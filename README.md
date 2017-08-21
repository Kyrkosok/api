# Kyrkosok.se API

## Requirements

 - Python 3.5+

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

### Search within bounding box (returns a subset of fields):

```
/churches/bbox?south=<float>&east=<float>&north=<float>&west=<float>
```

### Get a set of random churches:

```
/churches/random?limit=1
```

### Get all churches (returns a subset of fields):

```
/churches
```
