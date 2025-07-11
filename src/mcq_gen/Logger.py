import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #strftime for formatting the way in which the output will be visible...

#path of file at which execution of differnt methods will be stored... 
log_path=os.path.join(os.getcwd(),"logs") #getcwd=get currently working directory... "logs is the folder name"...
os.makedirs(log_path,exist_ok=True)
#now inside log folder creating the file...
LOG_FILEPATH=os.path.join(log_path,LOG_FILE)

logging.basicConfig(
    level=logging.INFO, #different level of logging...
    filename=LOG_FILEPATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)
