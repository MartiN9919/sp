# -*- coding: utf-8 -*-

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR  = BASE_DIR+'/../log/'
sys.path.append(BASE_DIR+'/')  # +'/../'
sys.path.append(BASE_DIR+'/web/')
