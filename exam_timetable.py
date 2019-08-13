class Exam:
    def __init__(self, line):
        """Creates atrributes based off the line given from the file in the
        construction of the main class"""
        attributes = line.split(",")    # Splits the line into a list
        # Setting the attributes
        self.__subject = attributes[0]
        self.__time = attributes[1]
        self.__date = attributes[2]
        self.__location = attributes[3]

    def get_subject(self):
        """allow other processes to access the subject name"""
        return self.__subject

    def get_time(self):
        """allow other processes to access the time"""
        return self.__time

    def get_date(self):
        """allow other processes to access the date"""
        return self.__date
      
    def get_location(self):
        """allow other processes to access the location"""
        return self.__location

    def change_subject(self, change):
        """allow other processes to change the subject"""
        self.__subject = change

    def change_time(self, change):
        """allow other processes to change the time"""
        self.__time = change

    def change_date(self, change):
        """allow other processes to change the date"""
        self.__date = change
        
    def change_location(self, change):
        """allow other processes to change the location"""
        self.__location = change
