# Web scrapper tool

This repo contains tool that can parse website and get needed text fields from it.

## Run directly

```shell
pip install -r requirements.txt
```
To run scrapper (by default you it will create two files `output.csv` and `db.sqlite3`:
```shell
python3 main.py
```
To run test of scrapper methods:
```shell
pytest test_main.py
```
## Run using Docker

Make sure that docker is running on your machine.

Build image:
```shell
docker build --tag coxit-test .
```

To run image as a container:
```shell
docker run -d coxit-test
```

Get container id from and copy it:
```shell
docker ps
```

Enter container files:
```shell
docker exec -it <container-id> bash
```

You should see created sqlite and csv files for main program and test one. 






