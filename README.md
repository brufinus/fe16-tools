# fe16-tools

A python web application with various tools to
help with gameplay in Fire Emblem: Three Houses

The app currently has only one tool, but I
plan to implement more if the need arises.

Current tools:
- **Meal Finder**: Find shared liked meals between two characters.

# Local

You can build and run the app locally through docker.

A [dockerized image](https://hub.docker.com/r/brufinus/fe16-tools)
can be pulled from the docker hub and run like so:

```bash
docker run --name fe16-tools -p 5000:5000 --rm docker.io/brufinus/fe16-tools:latest
```

Once it is running you can access the tool at http://localhost:5000.

# Issues

If you run into any problems or wish for certain
features or improvements, please open an Issue.

The project is also open to contribution through PR.

