# fe16-tools

A python web-based application with various tools to
help with gameplay in Fire Emblem: Three Houses

Current tools:
- **Meal Finder**: Find shared liked meals between two characters.
- **Tea Helper**: Get favorite teas, liked topics, and correct responses.
- **Item Helper**: Help return lost items and deliver liked gifts.
- **Seed Calculator**: Simulate seed combinations at the Greenhouse.

# Usage

## Local

Run the app locally to use incomplete
features or if the website is down.

### Docker

You can build and run the app locally through docker.

A [dockerized image](https://hub.docker.com/r/brufinus/fe16-tools)
can be pulled from the docker hub and ran using this command:

```bash
docker run --name fe16-tools -p 5000:5000 --rm docker.io/brufinus/fe16-tools:latest
```

Once it is running, you can access the tool at http://localhost:5000.

### Python

You can also use Python to run the app.

1. Clone the repository or download source code from the
   [latest release](https://github.com/brufinus/fe16-tools/releases).
2. Install requirements using pip.
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app using flask.
   ```bash
   flask run
   ```

Once again, you can access the tool at http://localhost:5000.

## Website

You can access the app online at
[fe16-tools.web.app](https://fe16-tools.web.app/).

# Issues

If you run into any problems or wish for certain
features or improvements, please open an Issue.

The project is also open to contribution through PR.
