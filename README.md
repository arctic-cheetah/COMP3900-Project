# COMP3900 Project

This is the P133 project _Systems and Methods for Phishing and Spam Detection_

## Installation

### <u>Run project via docker (Most portable)</u>

#### Run entire stack

```bash
docker pull nginx:alpine
docker compose up --build
```

### Run project locally (Easiest way to debug)

#### Front end

```bash
cd frontend
npm run dev
```

#### Back end

```bash
python3 backend/app.py
```

because the paths imply running from backend directory

#### Run test cases

```bash
docker compose -f 'docker-compose.yml' up -d --build 'test'
```

#### Run test cases

```bash
    cd ~/capstone-project-26t1-3900-m18b-date
    pytest
```

## Troubleshooting

If `docker compose up --build` fails, try rebuild containers:

```bash
    docker compose down
    docker compose up --build
```

If the port is in use, try to following to see what is conflicting:

```bash
    docker ps
```

If `npm run dev` fails due to missing dependencies, install them first:

```bash
    cd frontend
    npm install
```

If the backend fails due to missing Python packages, install backend dependencies using:

```bash
    cd backend
    pip install -e .
```

If the backend database schema has changed and is causing issues, try the following:

**Note**: If your database is stored in a Docker volume, the flag `-v` will **delete all database data** and reset the system.

```bash
    docker compose down -v
    docker compose up --build
```


### Manuals:
Please see the
[Operational and Installation Manual](/operational-install-manual.md)
for further information on running and installing the system

Or for using the software please see the
[Operational and Installation Manual](/frontend/User_Manual.md)


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## AI documentation

We sourced data from this dataset:
[Research paper](linkinghub.elsevier.com/retrieve/pii/S0167404823004558)

[AI dataset source](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset)

## License

[MIT](https://choosealicense.com/licenses/mit/)

```

## Authors

Caitlin, Joules, Kelly, Lara, Ray, Shadab
```
