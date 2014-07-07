from flask.ext.peewee_swagger.swagger import Swagger, SwaggerUI

from gistsurfr.app import app
from gistsurfr.api import api


# swagger
swagger = Swagger(api)
swagger.setup()

# create the Swagger user interface endpoint
swaggerUI = SwaggerUI(app)
swaggerUI.setup()
