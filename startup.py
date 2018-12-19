
## Migraion file to create tables ##

from cyclonecrawler.database.connection import *
from cyclonecrawler.database.models import *


Base.metadata.create_all(engine)