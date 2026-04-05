# COMP3900 Project

This is the P133 project _Systems and Methods for Phishing and Spam Detection_

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
cd backend
python3 app.py
```

#### Run test cases

```bash
docker compose -f 'docker-compose.yml' up -d --build 'test'
```

#### Run test cases

```bash
    cd ~/capstone-project-26t1-3900-m18b-date
    pytest
```

## Usage

### Routes

```python
POST /scan
```

Accepts a POST request with JSON as the payload, and the only valid key is:

```
{"url": "website_here"}
```

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

Joules, Ray, Kelly, Lara, Shadab, Caitlin
```
