import os
from slack_bolt import App
from . import config
app = App(
    token=config.tester["auth"],
    
)