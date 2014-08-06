#!/usr/bin/env python
# coding: utf-8
# Author steven
# 2012-6-27 / 2012-11-7
import web

from config.url import app
from controls.base import return500, return404

# Run
app.internalerror = return500
app.notfound = return404
application = app.run()

    
