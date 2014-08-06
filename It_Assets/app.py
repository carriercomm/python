#!/usr/bin/env python

import web

from config.url import app
from controls.base import return500, return404

# Run
app.internalerror = return500
app.notfound = return404
application = app.run()

    
