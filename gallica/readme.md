# Gallica

This script query the Gallica database and fetch partition. The files are stored by
default in the directory ``files/``.

## Install
```shell
$ ./setup.sh
$ docker run -d -p 3306:3306 -v db:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=changeme --name root mariadb
$ ./gallica.py --query your_search
```

## Usage manual
```
Usage: Gallica querying tool

Options:
  -h, --help            show this help message and exit
  -d DEST, --dest=DEST  destination directory
  -q QUERY, --query=QUERY
                        Query term
```

#### `--query`

Search term

#### `--dest`

Directory where the partition are stored

## Database

There are two tables in the database ``glc_metadata`` and ``glc_partition``

#### `glc_metadata`

This table contains all metadata like the title, the author, etc.


#### `glc_partition`

This table stores the file location.
