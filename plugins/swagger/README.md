# mkdocs-zerto-swagger-plugin
This is the [Mkdocs](https://www.mkdocs.org) plugin for rendering swagger &amp; openapi schemas using [Swagger UI](https://swagger.io/tools/swagger-ui/). It is written in Python.

## Usage
Install the plugin using `pip install mkdocs-zerto-swagger-plugin`.

Add the following lines to your mkdocs.yml:

    plugins:
      - zerto_swagger

### Referencing a local json

Place an OpenAPI json in the same folder as the the `.md` file.

Enter `!!zswagger FILENAME!!` at the appropriate location inside the markdown file.

### Referencing an external json

You may reference an external OpenAPI json using the following syntax: `!!zswagger-http URL!!`.

## Explicit declaration of the Swagger JS library

You can explicitly specify the swagger-ui css and js dependencies if you wish to not use the unpkg CDN.

Keep in mind, the filename has to be `swagger-ui.css` for the CSS and `swagger-ui-bundle.js` for the JS.

To specify this use `extra_javascript` and `extra_css` in your mkdocs.yaml:
``` yaml
--- 
extra_css: 
  - assets/css/swagger-ui.css
extra_javascript: 
  - assets/js/swagger-ui-bundle.js
```

## Contributing & Developing Locally

After downloading and extracting the `.tar.gz`, install this package locally using `pip` and the `--editable` flag:

``` bash
pip install --editable .
```

You'll then have the `zerto-swagger` package available to use in Mkdocs and `pip` will point the dependency to this folder. You are then able to run the docs using `mkdocs serve`. Make sure you restart the process between code changes as the plugin is loaded on startup.

## MkDocs plugins and Swagger api

The Zerto Swagger MkDocs plugin uses a set of extensions and plugin APIs that MkDocs and Swagger UI supports.
You can find more info about MkDocks plugins and Swagger UI  on the official website of [MkDocks](https://www.mkdocs.org/user-guide/plugins/) and [SwaggerUI](https://github.com/swagger-api/swagger-ui/blob/master/docs/customization/plugin-api.md).

The input OpenAPI files processed by the plugin should conform to the [OpenAPI specification](https://swagger.io/specification/).

</br>
<small>
Disclaimer: This plugin is unofficial, and is not sponsored, owned or endorsed by mkdocs, swagger, or any other 3rd party.</br>
Credits to @aviramha for starting this project.
</small>
