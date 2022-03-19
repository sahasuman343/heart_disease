import os
import sys
import time

class Run_manager:
    def __init__(self,run_name) -> None:
        self.run_name=run_name
        self.dir_name=os.path.join("data/output/",self.run_name+str(time.time()))
        
        


    def create_output(self):
        if not os.path.exists("data/output"):
            os.makedirs("data/output")

        os.mkdir(self.dir_name)