'''
Yitong Sun Nov 2021
Class to store bee_event
'''

class bee_event:

    # class initialization 
    def __init__(self, eventID, time_stamp, tag):  
        self.eventID = eventID  
        self.time_stamp = time_stamp  # "YYYY-MM-DD_HH-MM-MM"
        self.tag = -1                 # tag number
    
    # add top image dir to class
    def add_top_image(self, top_dir):
        self.top_dir = top_dir

    # add side image dir to class
    def add_side_image(self, side_dir):
        self.side_dir = side_dir

    # retrive top image dir
    def get_top_dir(self):
        return self.top_dir
    
    # retrive side image dir
    def get_side_dir(self):
        return self.side_dir