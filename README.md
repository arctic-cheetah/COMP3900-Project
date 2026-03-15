# COMP3900 Project

This is the P133 project _Systems and Methods for Phishing and Spam Detection_

### <u>Run project via docker (Most portable)</u>

#### Run entire stack

```bash
docker compose up --build
```

### Run project locally (Easiest way to debug)

#### Front end

```bash
cd frontend
npm run dev
```

# TO DEVS PLEASE RUN THE BACKEND IN TO ROOT DIRECTORY OF PROJECT!!!😡

#### Back end

```bash
python3 backend/app.py
```

#### Run database

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

# AI Documentation
Documentation about the AI is better seen in the project proposal, google docs and drive attached here:

[Drive](https://drive.google.com/drive/u/0/folders/1N3dP0OT8UrrZ0Erqoa-uDxxtts7K4beO)

[Project proposal](https://docs.google.com/document/d/1fBpHYAdUYVQCxvb3eVvccJjBpkHvOcFmu_YNtdwViTw/edit?usp=drive_link)

[Ai Model Information](https://docs.google.com/document/d/18d1kwb2hCRl2MtNw0yuYHhzIhPl3S8mXL4isAkQN7-4/edit?usp=sharing)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.



## License

[MIT](https://choosealicense.com/licenses/mit/)
```

## Authors

Joules, Ray, Kelly, Lara, Shadab, Caitlin
