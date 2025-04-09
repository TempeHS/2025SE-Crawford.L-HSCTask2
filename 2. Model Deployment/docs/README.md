# Flask PWA - API Extension Task

This task is to build a safe API that extends the [Flask PWA - Programming for the Web Task](https://github.com/TempeHS/Flask_PWA_Programming_For_The_Web_Task_Template). From the parent task, students will abstract the database and management to an API with key authentication. The PWA will then be retooled to GET request the data from the API and POST request data to the API. The PWA UI for the API will be rapidly prototyped using the [Bootstrap](https://getbootstrap.com/) frontend framework.

The API instructions focus on modelling how to build and test an API incrementally. The PWA instructions focus on using the [Bootstrap](https://getbootstrap.com/) frontend framework to prototype an enhanced UI/UX frontend rapidly using [Bootstrap](https://getbootstrap.com/) components and classes.

> [!note]
> The template for this project has been pre-populated with assets from the Flask PWA task, including the logo, icons and .database. Students can migrate their own assets if they wish.

> [!Important]
> Some aspects of the code _require_ certain extensions to be installed so it is highly advised to run and edit code inside of a container so that extensions don't conflict and proper requirements are installed.

## Dependencies

## Requirements

1. [VSCode](https://code.visualstudio.com/download) or [GitHub Codespaces](https://github.com/features/codespaces)
2. [Python 3.x](https://www.python.org/downloads/)
3. [GIT 2.x.x +](https://git-scm.com/downloads)
4. [SQLite3 Editor](https://marketplace.visualstudio.com/items?itemName=yy0931.vscode-sqlite3-editor)
5. [Start git-bash](https://marketplace.visualstudio.com/items?itemName=McCarter.start-git-bash) 6.[Thunder Client](https://marketplace.visualstudio.com/items?itemName=rangav.vscode-thunder-client)
6. pip/pip3 installs

```bash
    pip install Flask
    pip install flask_wtf
    pip install flask_csp
    pip install jsonschema
    pip install requests
```

> [!Important]
> MacOS and Linux users may have a `pip3` soft link instead of `pip`, run the below commands to see what path your system is configured with and use that command through the project. If neither command returns a version, then likely [Python 3.x](https://www.python.org/downloads/) needs to be installed.
>
> ```bash
> pip show pip
> pip3 show pip
> ```

## Instructions for building the API

> [!Warning]
> These instructions are less verbose than the parent task because students are expected to be now familiar with Bash, Flask & SQLite3.

### Step 1: Learn the basics of implementing an API in Flask

Watch: [Build a Flask API in 12 Minutes](https://www.youtube.com/watch?v=zsYIw6RXjfM)

> [!Note]
> The video uses [Postman](https://www.postman.com/), this tutorial uses [Thunder Client](https://www.thunderclient.com/) a VS Code extension that has similar functionality.

### Step 2: Create the Directory Structure

Students can create files as they are needed. This structure defines the correct directory structure for all files. As students `touch` each file, they should refer to this structure to ensure the file path is correct.

```text
├── .database
│   └─── data_source.db
├── static
│   ├── css
│   │   ├──bootstrap.min.css
│   │   └──style.css
│   ├── icons
│   │   ├──desktop_screenshot.png
│   │   ├──icon-128x128.png
│   │   ├──icon-192x192.png
│   │   ├──icon-384x384.png
│   │   ├──icon-512x512.png
│   │   └──mobile_screenshot.png
│   ├── images
│   │   ├──favicon.png
│   │   └──logo.png
│   ├─── js
│   │   ├──app.js
│   │   ├──bootstrap.bundle.min.js
│   │   └──serviceWorker.js
│   └── manifest.json
├── templates
│   ├── partials
│   │   ├──footer.html
│   │   └──menu.html
│   ├──index.html
│   ├──layout.html
│   └──privacy.html
├── api.py
├── database_manager.py
├── LICENSE
└── main.py
```

### Step 3: Setup a basic API in api.py

This Python implementation in 'api.py':

1. Imports all the required dependencies for the whole project.
2. Configure the 'Cross Origin Request' policy.
3. Configure the rate limiter.
4. Configure a route for the root `/` with a GET method to return stub data and a 200 response.
5. Configure a route to /add_extension with a POST method to return stub data and a 201 response.

```python
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

import database_manager as dbHandler


api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


@api.route("/", methods=["GET"])
@limiter.limit("3/second", override_defaults=False)
def get():
    return ("API Works"), 200


@api.route("/add_extension", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def post():
    data = request.get_json()
    return data, 201


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)
```

### Step 3: Test your basic API with Thunder Client

![Screen recording testing an API with Thunder Client](/docs/README_resources/test_basic_API.gif "Follow these steps to test your basic API")

### Step 4: Build a basic GET response

Extend the `get():` method in `api.py` to get data from the database via the `dbHandler` and return it to the request with a status `200`.

```python
def get():
    content = dbHandler.extension_get("%")
    return (content), 200
```

This Python implementation in 'database_manager.py'

1. Imports all the required dependencies for the project
2. Connects to the SQLite3 database
3. Executes a query
4. Converts the query data to a JSON structure
5. Returns the JSON data

```python
from flask import jsonify
import sqlite3 as sql
from jsonschema import validate
from flask import current_app


def extension_get(lang):
    con = sql.connect(".database/data_source.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM extension")
    migrate_data = [
        dict(
            extID=row[0],
            name=row[1],
            hyperlink=row[2],
            about=row[3],
            image=row[4],
            language=row[5],
        )
        for row in cur.fetchall()
    ]
    return jsonify(migrate_data)
```

### Step 5: Test your basic GET Response

![Screen recording testing a API GET with Thunder Client](/docs/README_resources/test_basic_GET_API.gif "Follow these steps to test your basic GET API")

### Step 6 Add a GET request argument to filter extensions by language

Extend the `get():` method in `api.py` to either get all data or data that matches a language parameter from the database by

1. Validating the argument is "lang" and that the "lang" is only alpha characters for security.
2. Passing the language request to the dbHandler.
3. If no language is specified, the wildcard `%` will be passed.
4. Return the data from dbHandler to the request.
5. Return a status `200`.

```python
def get():
    # For security data is validated on entry
    if request.args.get("lang") and request.args.get("lang").isalpha():
        lang = request.args.get("lang")
        lang = lang.upper()*
        content = dbHandler.extension_get(lang)
    else:
        content = dbHandler.extension_get("%")
    return (content), 200
```

Extend the database query in the `extension_get():` method in the `database_manager.py` to filter the SQL query based on the argument parameter and return it as JSON data where:

1. If no valid parameter is passed, the function will return the entire database in a JSON format because of the `%` wildcard.
2. If a valid parameter is passed, the database will be queried with a `WHERE language LIKE' SQL query, and all matching languages (if any) will be returned in JSON format.

```python
def extension_get(lang):
    con = sql.connect(".database/data_source.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM extension WHERE language LIKE ?;", [lang])
    migrate_data = [
        dict(
            extID=row[0],
            name=row[1],
            hyperlink=row[2],
            about=row[3],
            image=row[4],
            language=row[5],
        )
        for row in cur.fetchall()
    ]
    return jsonify(migrate_data)
```

### Step 7: Test your GET Response

![Screen recording testing a API GET with Thunder Client](/docs/README_resources/test_GET_API.gif "Follow these steps to test your GET API")

### Step 8: Setup your basic POST response

Extend the `/add_extension` route in api.py to pass the POST data to the 'dbHandler' and set up a driver to return the response with a 201 status code.

```python
def post():
    data = request.get_json()
    response = dbHandler.extension_add(data)
    return response
```

Extend the `extension_add():` method in the `database_manager.py` to be a driver that returns the received data to the POST request.

```python
def extension_add(response):
    data = response
    return data, 200
```

### Step 9: Test your basic POST response

![Screen recording testing a API basic POST with Thunder Client](/docs/README_resources/test_basic_POST_API.gif "Follow these steps to test your basic POST API")

### Step 10: Extend the dbHandler to validate the JSON

Update the `extension_add():` method in `database_manager.py` to validate the JSON and return a message and response code. The schema provided validates the JSON with the following rules:

1. All 5 properties are required.
2. No extra properties are allowed.
3. The data type for all 5 properties is string.
4. The hyperlink pattern enforces the URL to start with `https://marketplace.visualstudio.com/items?itemName=`, and the characters `<` and `>` are not allowed to prevent XXS attacks.
5. The image pattern requires https:// but `<` and `>` are not allowed to prevent XXS attacks.
6. Languages must be enumerated with the list of languages.

> [!Important]
> You can use [https://regex101.com/](https://regex101.com/) to design and test patterns for your database design. It is important to understand a regular expression may look slightly different between languages due to the way characters need to be escaped.

```python
    if validate_json(data):
        return {"message": "Extension added successfully"}, 201
    else:
        return {"error": "Invalid JSON"}, 400


schema = {
    "type": "object",
    "validationLevel": "strict",
    "required": [
        "name",
        "hyperlink",
        "about",
        "image",
        "language",
    ],
    "properties": {
        "name": {"type": "string"},
        "hyperlink": {
            "type": "string",
            "pattern": "^https:\\/\\/marketplace\\.visualstudio\\.com\\/items\\?itemName=(?!.*[<>])[a-zA-Z0-9-._~:\/?#\\[\\]@!$&'()*\\+,;=]*$",
        },
        "about": {"type": "string"},
        "image": {
            "type": "string",
            "pattern": "^https:\\/\\/(?!.*[<>])[a-zA-Z0-9-._~:\/?#\\[\\]@!$&'()*\\+,;=]*$",
        },
        "language": {
            "type": "string",
            "enum": ["PYTHON", "CPP", "BASH", "SQL", "HTML", "CSS", "JAVASCRIPT"],
        },
    },
    "additionalProperties": False,
}

def validate_json(json_data):
    try:
        validate(instance=json_data, schema=schema)
        return True
    except:
        return False
```

Sample JSON data for you to test the API:

```text
{"name": "test", "hyperlink": "https://marketplace.visualstudio.com/items?itemName=123.html", "about": "This is a test", "image": "https://test.jpg", "language": "BASH"}
```

### Step 10: Test your validation POST response

![Screen recording testing a API basic POST with Thunder Client](/docs/README_resources/test_POST_API_Auth.gif "Follow these steps to test your basic POST API")

### Step 11: Insert the POST data into the database

Update the `extension_add():` method in database_manager.py`to INSERT the JSON data into the database. The`extID` is not required as it has been configured to auto increment in the database table.

```python
def extension_add(data):
    if validate_json(data):
        con = sql.connect(".database/data_source.db")
        cur = con.cursor()
        cur.execute(
            "INSERT INTO extension (name, hyperlink, about, image, language) VALUES (?, ?, ?, ?, ?);",
            [
                data["name"],
                data["hyperlink"],
                data["about"],
                data["image"],
                data["language"],
            ],
        )
        con.commit()
        con.close()
        return {"message": "Extension added successfully"}, 201
    else:
        return {"error": "Invalid JSON"}, 400
```

### Step 12: Implement POST Authorisation

[API Key Authorisation](https://cloud.google.com/endpoints/docs/openapi/when-why-api-key) is a common method for authorising an application, site, or project. In this scenario, the API is not authorising a specific user. This is a very simple implementation of API Key Authorisation.

Extend the `api.py` to store the key as a variable. Students will need to generate a unique basic 16 secret key with [https://acte.ltd/utils/randomkeygen](https://acte.ltd/utils/randomkeygen).

```python
auth_key = "4L50v92nOgcDCYUM"
```

Extend the `def post():` method in `api.py` to request the `authorisation` attribute from the post head, compare it to the `auth_key,` and process the appropriate response.

```python
def post():
    if request.headers.get("Authorisation") == auth_key:
        data = request.get_json()
        response = dbHandler.extension_add(data)
        return response
    else:
        return {"error": "Unauthorised"}, 401
```

### Step 13: Test your authorisation for a POST response

![Screen recording testing a API basic POST with Thunder Client](/docs/README_resources/test_POST_API_Auth.gif "Follow these steps to test your POST API Authorisation")

### 14: Configure the logger to log to api_security_log.log

Extend the `api.py` with the implementation below, which should be inserted directly below the `imports`. This will configure the logger to log to a file for security analysis.

```python
api_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="api_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)
```

## Instructions for building the PWA user interface to the API.

> [!Note]
> This implementation uses the [Bootstrap](https://getbootstrap.com/) frontend CSS & JS design framework. Version 5.3.3 has been included in the static files.

### Step 1: Setup the Jinga2 template engine file structure

```text
├── templates
│   ├── partials
│   │   ├──footer.html
│   │   └──menu.html
│   ├──index.html
│   ├──layout.html
│   └──privacy.html
```

### Step 2: Setup the Jinga2 template

This Jinga2/HTML implementation in layout.html:

1. Security features are defined in the head.
2. The menu and footer are defined in a partial for easy maintenance.
3. The body will be defined by the block content when the `layout.html` is inherited.
4. Bootstrap components (CSS & JavaScript) are linked.
5. JS Components, including the PWA service worker, are linked.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta
      http-equiv="Content-Security-Policy"
      content="base-uri 'self'; default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' *; media-src 'self'; font-src 'self'; connect-src 'self'; object-src 'self'; worker-src 'self'; frame-src 'none'; form-action 'self'; manifest-src 'self'"
    />
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link rel="stylesheet" type="text/css" href="static/css/style.css" />
    <title>VS Code Extensions for Software Engineering</title>
    <link rel="manifest" href="static/manifest.json" />
    <link rel="icon" type="image/x-icon" href="static/images/favicon.png" />
    <meta name="theme-color" content="" />
    <link href="static/css/bootstrap.min.css" rel="stylesheet" />
  </head>
  <body>
    {% include "partials/menu.html" %}
    <main>{% block content %}{% endblock %}</main>
    {% include "partials/footer.html" %}
    <script src="static/js/bootstrap.bundle.min.js"></script>
    <script src="static/js/serviceWorker.js"></script>
    <script src="static/js/app.js"></script>
  </body>
</html>
```

### Step 3: Setup the footer.html

This HTML implementation provides a full-width horizontal rule and a Bootstrap column containing a link to the privacy page.

```html
<div class="container-fluid">
  <hr />
</div>
<div class="container">
  <div class="row">
    <div class="col-12">
      <a href="privacy.html">Privacy Policy</a>
    </div>
  </div>
</div>
```

### Step 4: Setup the menu.html and add some UX/accessibility advanced features using JS.

This HTML implementation is an adaption of the basic [Bootstrap Navbar](https://getbootstrap.com/docs/5.3/components/navbar/).

```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">
      <img src="static/images/logo.png" alt="logo" height="80" />
    </a>
    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent"
      aria-expanded="false"
      aria-label="Toggle navigation"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" href="/" aria-current="page">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/add.html">Add Extension</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/privacy.html">Privacy</a>
        </li>
      </ul>
      <form class="d-flex" role="search" id="search-form">
        <input
          class="form-control me-2"
          type="search"
          placeholder="Search"
          aria-label="Search"
          id="search-input"
        />
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>
```

Extend the `app.js` with this script that toggles the active class and the `aria-current="page"` attribute for the current page menu item. The `active` class improves UX by styling the current page in the menu differently and adding the [`aria-current` attribute](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-current) to the current page which improves the context understanding of screen readers for enhanced accessibility.

```js
document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll(".nav-link");
  const currentUrl = window.location.pathname;

  navLinks.forEach((link) => {
    const linkUrl = link.getAttribute("href");
    if (linkUrl === currentUrl) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  });
});
```

Extend the `app.js` with this script that adds basic search functionality to the search button in the menu by searching the current page and highlighting matching words.

```js
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("search-form");
  const input = document.getElementById("search-input");

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const searchTerm = input.value.trim().toLowerCase();
    if (searchTerm) {
      highlightText(searchTerm);
    }
  });

  function highlightText(searchTerm) {
    const mainContent = document.querySelector("main");
    removeHighlights(mainContent);
    highlightTextNodes(mainContent, searchTerm);
  }

  function removeHighlights(element) {
    const highlightedElements = element.querySelectorAll("span.highlight");
    highlightedElements.forEach((el) => {
      el.replaceWith(el.textContent);
    });
  }

  function highlightTextNodes(element, searchTerm) {
    const regex = new RegExp(`(${searchTerm})`, "gi");
    const walker = document.createTreeWalker(
      element,
      NodeFilter.SHOW_TEXT,
      null,
      false
    );
    let node;
    while ((node = walker.nextNode())) {
      const parent = node.parentNode;
      if (
        parent &&
        parent.nodeName !== "SCRIPT" &&
        parent.nodeName !== "STYLE"
      ) {
        const text = node.nodeValue;
        const highlightedText = text.replace(
          regex,
          '<span class="highlight">$1</span>'
        );
        if (highlightedText !== text) {
          const tempDiv = document.createElement("div");
          tempDiv.innerHTML = highlightedText;
          while (tempDiv.firstChild) {
            parent.insertBefore(tempDiv.firstChild, node);
          }
          parent.removeChild(node);
        }
      }
    }
  }
});
```

Extend style.css to add the class required by the search script.

```css
.highlight {
  background-color: yellow;
  border-radius: 20px;
  border: 1px yellow solid;
}
```

### Step 5: Inherit the layout to the /index.html and set up the app route.

Insert the basic HTML into index.html.

```html
{% extends 'layout.html' %} {% block content %}
<div class="container">
  <div class="row"></div>
  <div class="row"></div>
</div>
{% endblock %}
```

This Python Flask implementation in `main.py`

1. Imports all dependencies required for the whole project.
2. Set up CSRFProtect to provide asynchronous keys that protect the app from a CSRF attack. Students will need to generate a unique basic 16 secret key with [https://acte.ltd/utils/randomkeygen](https://acte.ltd/utils/randomkeygen).
3. Defines the head attribute for authorising a POST request to the API.
4. Define a secure Content Secure Policy (CSP) head.
5. Configures the Flask app.
6. Redirect /index.html to the domain root for a consistent user experience.
7. Renders the index.html for a GET app route.
8. Provide an endpoint to log CSP violations for security analysis.

```python
from flask import Flask
from flask import redirect
from flask import render_template
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging


# Generate a unique basic 16 key: https://acte.ltd/utils/randomkeygen
app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b"6HlQfWhu03PttohW;apl"

app_header = {"Authorisation": "4L50v92nOgcDCYUM"}


@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["GET"])
@csp_header(
        {
        "base-uri": "self",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "*",
        "media-src": "'self'",
        "font-src": "self",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
        }
)
def index():
    return render_template("/index.html")


@app.route("/csp_report", methods=["POST"])
@csrf.exempt
def csp_report():
    app.logger.critical(request.data.decode())
    return "done"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

```

### Step 7: Test the basic index.html

```bash
python main.py
```

![A render of the basic index.html](README_resources\basic_index.png "The basic index.html should load like this")

### Step 8: Setup the Privacy Policy

```html
{% extends 'layout.html' %} {% block content %}
<div class="container">
  <div class="row">
    <h1 class="display-1">Privacy Policy</h1>
    <p>Policy here...</p>
  </div>
  <div class="row"></div>
</div>
{% endblock %}
```

Extend `main.py` to include an app route to privacy.html

```python
@app.route("/privacy.html", methods=["GET"])
def privacy():
    return render_template("/privacy.html")
```

### Step 9: Test privacy.html and search functionality.

![A render of the privacy.html](README_resources\privacy_search.png "The privacy index.html should load like this")

Ensure your page renders correctly with the test cases:

1. The page renders correctly
2. The privacy menu item is darker than the other menu items
3. A search for "priv" highlights the correct letters in the main body.

### Step 10: Setup the cards and request the data from the API

Extend the `index():` method in `main.py` so it requests data from the API and handles the exception that the API did not respond with an error message.

```python
def index():
    url = "http://127.0.0.1:3000"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        data = {"error": "Failed to retrieve data from the API"}
    return render_template("index.html", data=data)
```

Replace the test html in 'index.html` template that:

1. Implements a [Bootstrap jumbotron heading](https://getbootstrap.com/docs/5.3/examples/jumbotron/).
2. Implements a [Bootstrap button group](https://getbootstrap.com/docs/5.3/components/button-group/) that will later allow users to filter the extensions by language.
3. Implements the database items as [Bootstrap cards](https://getbootstrap.com/docs/5.3/components/card/) in a responsive[Bootstrap Column Layout](https://getbootstrap.com/docs/5.3/layout/columns/).
4. Provides API error feedback to the user that is styled by the [Bootstrap color utility](https://getbootstrap.com/docs/5.3/utilities/colors/).

```html
{% extends 'layout.html' %} {% block content %}
<div class="container py-4"">
  <div class="p-4 bg-body-tertiary rounded-3">
    <div class="container-fluid py-2">
      <h1 class="display-4">VS Code Extensions for Software Engineering</h1>
      <p class="lead">
        This is a collection of Visual Studio Code extensions that are useful
        for software engineering.
      </p>
    </div>
  </div>
</div>
<div class="container">
  <div class="row">
    <div class="btn-group" role="group" aria-label="Filter by language">
      <button type="button" class="btn btn-primary" id="all">All</button>
      <button type="button" class="btn btn-primary" id="python">Python</button>
      <button type="button" class="btn btn-primary" id="c++">C++</button>
      <button type="button" class="btn btn-primary" id="bash">BASH</button>
      <button type="button" class="btn btn-primary" id="sql">SQL</button>
      <button type="button" class="btn btn-primary" id="html">HTML</button>
      <button type="button" class="btn btn-primary" id="css">CSS</button>
      <button type="button" class="btn btn-primary" id="js">JAVASCRIPT</button>
    </div>
  </div>
</div>
<div class="container p-4">
  <div class="row">
    <div class="error"><h2 class="text-danger">{{ data.error }}</h2></div>
    {% if data.error is not defined %}
      {% for row in data %}
      <div class="col-sm-12 col-lg-4">
        <div class="card" style="width: 18rem">
          <img
            src="{{ row.image }}"
            class="card-img-top"
            alt="Product image for the {{ row.name }} VSCode extension."
          />
          <div class="card-body">
            <h5 class="card-title">{{ row.name }}</h5>
            <p class="card-text">{{ row.about }}</p>
            <a href="{{ row.hyperlink }}" class="btn btn-primary">Read More</a>
          </div>
        </div>
      </div>
      {% endfor %}
    {% endif %}
  </div>
</div>
{% endblock %}
```

### Step 11: Test the index.html and API integration

![Screen recording testing a the index and the API integration](/docs/README_resources/test_index_and_API.gif "Follow these steps to test your index.html and API")

### Step 12: Implement a form with attribute controls to POST a new extension to API.

The HTML Implementation in `add.html`

1. Provides error and message feedback to the user that is styled by the [Bootstrap color utility](https://getbootstrap.com/docs/5.3/utilities/colors/).
2. Uses [Bootstrap Forms](https://getbootstrap.com/docs/5.3/forms/form-control/) to layout a data entry form.
3. Uses Form attributes type, place holder & pattern to improve user experience in entering the correct data.

```html
{% extends 'layout.html' %} {% block content %}
<div class="container">
  <div class="row">
    <h1>Add an Extension</h1>
    <div class="error">
      <h2>
        <span class="text-danger">{{ data.error }}</span
        ><span class="text-success">{{ data.message }}</span>
      </h2>
    </div>
  </div>
</div>
<div class="container">
  <div class="row">
    <form action="/add.html" method="POST" class="box">
      <div class="col-auto">
        <label for="name" class="form-label">Extension name</label>
        <textarea
          id="name"
          name="name"
          class="form-control"
          rows="1"
          autocomplete="off"
        ></textarea>
      </div>
      <div class="col-auto">
        <label for="hyperlink" name="hyperlink" class="form-label"
          >Hyperlink to extension</label
        >
        <input
          id="hyperlink"
          name="hyperlink"
          type="url"
          class="form-control"
          placeholder="https://marketplace.visualstudio.com/items?itemName="
          pattern="^https:\/\/marketplace\.visualstudio\.com\/items\?itemName=(?!.*[<>])[a-zA-Z0-9\-._~:\/?#\[\]@!$&'()*+,;=]*$"
        />
      </div>
      <div class="col-auto">
        <label for="about" class="form-label">About</label>
        <textarea
          id="about"
          name="about"
          class="form-control"
          rows="3"
          placeholder="A brief description of the extension"
        ></textarea>
      </div>
      <div class="col-auto">
        <label for="name" name="image" class="form-label">URL to Icon</label>
        <input
          id="image"
          name="image"
          type="url"
          class="form-control"
          pattern="^https:\/\/(?!.*[<>])[a-zA-Z0-9\-._~:\/?#\[\]@!$&'()*+,;=]*$"
          placeholder="https://"
        />
      </div>
      <div class="col-auto">
        <label for="language" name="language" class="form-label"
          >Programming language</label
        >
        <select
          id="language"
          name="language"
          class="form-select"
          aria-label="Default select language"
        >
          <option selected>Select a language from this menu</option>
          <option value="PYTHON">PYTHON</option>
          <option value="CPP">CPP</option>
          <option value="BASH">BASH</option>
          <option value="SQL">SQL</option>
          <option value="HTML">HTML</option>
          <option value="CSS">CSS</option>
          <option value="JAVASCRIPT">JAVASCRIPT</option>
        </select>
      </div>
      <br />
      <div class="col-auto">
        <button type="submit" class="btn btn-primary mb-3">Submit</button>
      </div>
      <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
    </form>
  </div>
</div>
{% endblock %}
```

Extend `main.py' to provide a route with POST and GET methods for `add.html` that

1. Renders `add.html` on GET requests.
2. On a POST method, read the form in add.html and construct a JSON.
3. Then, POST the JSON with the header that includes the Authentication key to the API.
4. Render `add.html` with any errors or messages from the API.

```python
@app.route("/add.html", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        hyperlink = request.form["hyperlink"]
        about = request.form["about"]
        image = request.form["image"]
        language = request.form["language"]
        data = {
            "name": name,
            "hyperlink": hyperlink,
            "about": about,
            "image": image,
            "language": language,
        }
        app.logger.critical(data)
        try:
            response = requests.post(
                "http://127.0.0.1:3000/add_extension",
                json=data,
                headers=app_header,
            )
            data = response.json()
        except requests.exceptions.RequestException as e:
            data = {"error": "Failed to retrieve data from the API"}
        return render_template("/add.html", data=data)
    else:
        return render_template("/add.html", data={})
```

### Step 13: Add event listeners to the `/` page for the buttons to filter the extensions by language.

Extend `app.js` with a script to provide functionality to the home page buttons.

```js
document.addEventListener("DOMContentLoaded", function () {
  if (window.location.pathname === "/") {
    const buttons = [
      { id: "all", url: "/" },
      { id: "python", url: "?lang=python" },
      { id: "cpp", url: "?lang=cpp" },
      { id: "bash", url: "?lang=bash" },
      { id: "sql", url: "?lang=sql" },
      { id: "html", url: "?lang=html" },
      { id: "css", url: "?lang=css" },
      { id: "js", url: "?lang=javascript" },
    ];

    buttons.forEach((button) => {
      const element = document.getElementById(button.id);
      if (element) {
        element.addEventListener("click", function () {
          window.location.href = button.url;
        });
      }
    });
  }
});
```

### Step 14: Forward the GET request argument to the API to filter extensions by language.

```python
    url = "http://127.0.0.1:3000"
    if request.args.get("lang") and request.args.get("lang").isalpha():
        lang = request.args.get("lang")
        url += f"?lang={lang}"
```

### 15: Configure the logger to log to main_security_log.log

Extend the `main.py` with the implementation below, which should be inserted directly below the `imports`. This will configure the logger to log to a file for security analysis.

```python
app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="main_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)
```

## Extension activities to improve the API and PWA.

1. Create a get_languages method that returns all the languages in the database.
2. Improve exception handling of the `add_extension` endpoint to give more detailed feedback to the user.
3. Use the new get-languages method to define the content that renders in the PWA.
4. Implement a sort extension by function

```

```
