from tkinter import *
from tkinter.scrolledtext import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter import ttk


class Timetable:
    def __init__(self, __parent):
        # Set up intial variables
        self.__parent = __parent
        self.__exams = []
        self.__editing = False
        self.__deleteing = False
        self.__edited = True
        self.__deleted = True

        # Setting the exams from a user given file
        try:
            for line in self.__read_from_file():
                self.__exams.append(Exam(line))
        except:
            self.__exams = []
            error = Tk()
            text_thing = "You have imported a incorrectly formatted file"
            error_label = Label(error,
                                text=text_thing)
            error_label.pack()
        self.__parent.deiconify()
        buttons = ["Enter new exam", "Find exam name",
                   "View all exams", "Edit a exam", "Delete a exam", "Quit"]
        button_functions = [self.__enter, self.__find_name,
                            self.__view_all,
                            self.__edit, self.__delete, self.quit]
        self.__buttons = []

        # Create the buttons
        for i in range(7):
            self.__buttons.append(Button(self.__parent,
                                         text=buttons[i],
                                         command=button_functions[i]))

        # Pack the buttons
        for i in range(6):
            self.__buttons[i].grid(column=i % 3, row=(i//3)+1, sticky="WE")
        self.__buttons[6].grid(column=0, row=3, columnspan=3, sticky="WE")

    def __enter(self):
        self.__clear()
        # Creating the frame for the method
        self.__enter_frame = Frame(self.__parent)
        self.__enter_frame.grid(column=0, row=0,
                                columnspan=3, sticky="WE")

        # Creating the entry variables
        self.__name_entry = StringVar()
        self.__date_entry = StringVar()
        self.__time_entry = StringVar()
        self.__location_entry = StringVar()

        # Creating the labels
        name_label = Label(self.__enter_frame,
                              text="Enter the exam name")
        name_label.grid(row=0, column=0)
        date_label = Label(self.__enter_frame,
                            text="Enter the date")
        date_label.grid(row=0, column=1)
        time_label = Label(self.__enter_frame,
                                  text="Enter the time")
        time_label.grid(row=0, column=2)
        location_label = Label(self.__enter_frame,
                                  text="Enter the location")
        location_label.grid(row=0, column=3)

        # Creating the entries
        name_entry = Entry(self.__enter_frame,
                              textvariable=self.__name_entry)
        name_entry.grid(row=1, column=0)
        date_entry = Entry(self.__enter_frame,
                            textvariable=self.__date_entry)
        date_entry.grid(row=1, column=1)
        time_entry = Entry(self.__enter_frame,
                                  textvariable=self.__time_entry)
        time_entry.grid(row=1, column=2)
        location_entry = Entry(self.__enter_frame,
                                  textvariable=self.__location_entry)
        location_entry.grid(row=1, column=3)

        # Creating the confirmation button
        confirm_button = Button(self.__enter_frame, text="Confirm!!!",
                                command=self.__enter_final)
        confirm_button.grid(column=0, row=2, columnspan=4, sticky="WE")

        # Creating a empty label for single sided padding
        padding = Label(self.__enter_frame, text="")
        padding.grid(column=0, row=3)

    def __enter_final(self):
        # Set the line in which the exam can be derived
        check_1 = "," in self.__name_entry.get()
        check_2 = "," in self.__date_entry.get()
        check_3 = "," in self.__time_entry.get()
        check_4 = "," in self.__location_entry.get()
        check_5 = "\n" in self.__name_entry.get()
        check_6 = "\n" in self.__date_entry.get()
        check_7 = "\n" in self.__time_entry.get()
        check_8 = "\n" in self.__location_entry.get()
        if check_1 or check_2 or check_3 or check_4 or check_5 or check_6 or check_7 or check_8:
            error_label = Label(self.__enter_frame,
                                text="Please do not use ',' or '\n'")
            error_label.grid(row=3, column=0, columnspan=3)
        else:
            exam_line = self.__name_entry.get() + ","
            exam_line += self.__date_entry.get() + ","
            exam_line += self.__time_entry.get() + ","
            exam_line += self.__location_entry.get() + "\n"
            # Add the exam
            self.__exams.append(exam(exam_line))
            self.__clear()

    def __find_name(self):
        # Exiting mid function, it won't edit or delete unexpectedly
        if self.__edited:
            self.__edited = False
        else:
            self.__edited = True
            self.__editing = False

        if self.__deleted:
            self.__deleted = False
        else:
            self.__deleted = True
            self.__deleting = False

        # This is to make sure there is something displayed
        self.__shown = False
        self.__clear()
        self.__find_list = []
        # Creating the frame for the method
        self.__find_name_frame = Frame(self.__parent)
        self.__find_name_frame.grid(column=0, row=0,
                                     columnspan=3, sticky="WE")

        # Creating the entry variable
        self.__name_find = StringVar()

        # Creating the label
        find_name_label = Label(self.__find_name_frame,
                                 text="Enter the exam name",
                                 height=2)
        find_name_label.grid(row=0, column=0)

        # Creating the entry
        find_name_entry = Entry(self.__find_name_frame,
                                 textvariable=self.__name_find)
        find_name_entry.grid(row=0, column=1)

        # Creating the confirmation button
        find_name_confirm_button = Button(self.__find_name_frame,
                                           text="Confirm!!!",
                                           command=self.__find_name_final)
        find_name_confirm_button.grid(column=2, row=0,
                                       columnspan=3, sticky="WE")

        # Creating a empty label for single sided padding
        find_name_padding = Label(self.__find_name_frame, text="")
        find_name_padding.grid(column=0, row=6)

    def __find_name_final(self):
        display_text = ""
        for exam in self.__exams:
            # Check if the given name matches any exam name
            if self.__name_find.get().upper() in exam.get_name().upper():
                self.__find_list.append(exam)

        if len(self.__find_list) > 0:
            self.__shown = True

        if self.__shown:
            max_name = 4    # The 7 is from the length of the word "English"
            max_date = 4
            max_time = 4
            max_location = 8
            for exam in self.__find_list:
                if len(exam.get_name()) > max_name:
                    max_name = len(exam.get_name())
                if len(exam.get_date()) > max_date:
                    max_date = len(exam.get_date())
                if len(exam.get_time()) > max_time:
                    max_time = len(exam.get_time())
                if len(exam.get_location()) > max_location:
                    max_location = len(exam.get_location())

            scrolled_width = max_name + max_date + max_time + max_location + 6
            self.__view_scrolled = ScrolledText(self.__find_name_frame,
                                                width=scrolled_width,
                                                height=5, wrap="word")

            # Inserting the formatted lines
            for exam in self.__find_list:
                output_string = exam.get_name()
                output_string += " "*(max_name-len(exam.get_name()))
                output_string += " |" + exam.get_date()
                output_string += " "*(max_date-len(exam.get_date()))
                output_string += " |" + exam.get_time()
                output_string += " "*(max_time-len(exam.get_time()))
                output_string += " |" + exam.get_location()
                str_index = str(float(self.__exams.index(exam)+1))
                self.__view_scrolled.insert(str_index, output_string)

            # Inserting the intial column headers
            # the max - len("Name") or 4 to add the correct whitespace
            output_string = "Name" + " "*(max_name-4)+" |Date"
            output_string += " "*(max_date - 4) + " |Time"
            output_string += " "*(max_time - 4) + " |Location\n"
            self.__view_scrolled.insert("0.0", output_string)

            self.__view_scrolled.grid(row=1, column=0, columnspan=3)

        else:
            # If there is nothing matching the given name, inform the user
            display_text = self.__name_find.get()
            display_text += " does not exsist in our database."
            display_label = Label(self.__find_name_frame, text=display_text)
            display_label.grid(column=0, row=1, columnspan=3, sticky="WE")

        if self.__editing:
            self.__exams_edit = []
            # Put the exam names as things to select form
            for exam in self.__find_list:
                self.__exams_edit.append(exam.get_name())
            # Set up the comboboxes and entry
            self.__editing_exam = StringVar()
            self.__editing_attributes = ["Name", "Date", "Time", "Location"]
            self.__attribute = StringVar()
            self.__attribute_edit = StringVar()
            self.__attribute_menu = ttk.Combobox(self.__find_name_frame,
                                                 textvariable=self.__attribute,
                                                 state="readonly")
            self.__attribute_menu["values"] = self.__editing_attributes
            self.__attribute_menu.grid(row=4, column=1)

            self.__exam_menu = ttk.Combobox(self.__find_name_frame,
                                             textvariable=self.__editing_exam,
                                             state="readonly")
            self.__exam_menu["values"] = self.__exams_edit
            self.__exam_menu.grid(row=4, column=0)

            self.__attribute_entry = Entry(self.__find_name_frame,
                                           textvariable=self.__attribute_edit)
            self.__attribute_entry.grid(row=4, column=2)

            # Set up the respective labels
            self.__exam_label = Label(self.__find_name_frame,
                                       text="Exam to edit")
            self.__exam_label.grid(column=0, row=3)

            self.__attribute_label = Label(self.__find_name_frame,
                                           text="Attribute to edit")
            self.__attribute_label.grid(column=1, row=3)

            self.__attribute_entry_label = Label(self.__find_name_frame,
                                                 text="Enter the change")
            self.__attribute_entry_label.grid(column=2, row=3)

            # Confirm button
            self.__confirm_button = Button(self.__find_name_frame,
                                           command=self.__final_name_edit,
                                           text="Confirm!")
            self.__confirm_button.grid(row=5, column=1)

        if self.__deleteing:
            self.__exams_edit = []
            # Put the exam names as things to select form
            for exam in self.__find_list:
                self.__exams_edit.append(exam.get_name())

            # Set up the combo box to delete a user, the button and the label
            self.__delete_exam = StringVar()
            self.__exam_menu = ttk.Combobox(self.__find_name_frame,
                                             textvariable=self.__delete_exam,
                                             state="readonly")
            self.__exam_menu["values"] = self.__exams_edit
            self.__exam_menu.grid(row=3, column=1)

            self.__exam_label = Label(self.__find_name_frame,
                                       text="Exam to delete")
            self.__exam_label.grid(column=0, row=3)

            self.__confirm_button = Button(self.__find_name_frame,
                                           command=self.__final_name_delete,
                                           text="Confirm!")
            self.__confirm_button.grid(row=3, column=2)

    def __final_name_edit(self):
        error_label = Label(self.__find_name_frame,
                            text="Please do not use ',' or '\n'")
        for i in range(len(self.__exams)):
            if self.__exams[i].get_name() == self.__editing_exam.get():
                if "\n" in self.__attribute.get():
                    error_label.grid(column=0, row=6, columnspan=3)
                elif self.__attribute.get() == "English":
                    if "," in self.__attribute_edit.get():
                        error_label.grid(column=0, row=6, columnspan=3)
                    else:
                        attribute = self.__attribute_edit.get()
                        self.__places[i].change_english(attribute)
                        self.__clear()
                        self.__edited = True
                        self.__shown = False
                elif self.__attribute.get() == "Maori":
                    if "," in self.__attribute_edit.get():
                        error_label.grid(column=0, row=6, columnspan=3)
                    else:
                        attribute = self.__attribute_edit.get()
                        self.__places[i].change_maori(attribute)
                        self.__clear()
                        self.__edited = True
                        self.__shown = False
                elif self.__attribute.get() == "Description":
                    attribute = self.__attribute_edit.get()+"\n"
                    self.__places[i].change_description(attribute)
                    self.__clear()
                    self.__edited = True
                    self.__shown = False

    def __final_maori_delete(self):
        for i in range(len(self.__places)):
            if self.__places[i].get_maori() == self.__delete_place.get():
                self.__places.pop(i)
        self.__clear()
        self.__deleted = True

    def __places_sort(self, places):
        sorted_places = []
        for place in places:
            sorted_places.append(place.get_english().lower())
        sorted_places.sort()
        final_sort = []
        for sorted_place in sorted_places:
            placed = False
            for place in places:
                if sorted_place == place.get_english().lower() and not placed:
                    placed = True
                    final_sort.append(place)
        return final_sort

    def __view(self, parent, places):
        self.__clear()
        # Finding the max length of each of the variables
        max_english = 7    # The 7 is from the length of the word "English"
        max_maori = 5
        max_description = 11
        for place in places:
            if len(place.get_english()) > max_english:
                max_english = len(place.get_english())
            if len(place.get_maori()) > max_maori:
                max_maori = len(place.get_maori())
            if len(place.get_description()) > max_description:
                max_description = len(place.get_description())

        # Putting the formatted text into the scrolled text
        scrolled_width = max_description + max_english + max_maori + 4
        self.__view_scrolled = ScrolledText(parent,
                                            width=scrolled_width,
                                            height=10, wrap="word")

        # Inserting the formatted lines
        for place in self.__places_sort(self.__places):
            output_string = place.get_english()
            output_string += " "*(max_english-len(place.get_english()))
            output_string += " |" + place.get_maori()
            output_string += " "*(max_maori-len(place.get_maori()))
            output_string += " |" + place.get_description()
            str_index = str(float(self.__places.index(place)+len(places)))
            self.__view_scrolled.insert(str_index, output_string)

        # Inserting the intial column headers
        # the max - len("English") or 7 to add the correct amount of whitespace
        output_string = "English" + " "*(max_english-7)+" |Maori"
        output_string += " "*(max_maori - 5) + " |Description\n"
        self.__view_scrolled.insert("0.0", output_string)

    def __view_all(self):
        self.__clear()
        self.__view_all_frame = Frame(self.__parent)
        # Finding the max length of each of the variables
        max_english = 7    # The 7 is from the length of the word "English"
        max_maori = 5
        max_description = 11
        for place in self.__places:
            if len(place.get_english()) > max_english:
                max_english = len(place.get_english())
            if len(place.get_maori()) > max_maori:
                max_maori = len(place.get_maori())
            if len(place.get_description()) > max_description:
                max_description = len(place.get_description())

        # Putting the formatted text into the scrolled text
        scrolled_width = max_description + max_english + max_maori + 4
        self.__view_scrolled = ScrolledText(self.__view_all_frame,
                                            width=scrolled_width,
                                            height=10, wrap="word")

        # Inserting the formatted lines
        for place in self.__places_sort(self.__places):
            output_string = place.get_english()
            output_string += " "*(max_english-len(place.get_english()))
            output_string += " |" + place.get_maori()
            output_string += " "*(max_maori-len(place.get_maori()))
            output_string += " |" + place.get_description()
            str_index = self.__places.index(place)+len(self.__places)
            str_index = str(float(str_index))
            self.__view_scrolled.insert(str_index, output_string)

        # Inserting the intial column headers
        # the max - len("English") or 7 to add the correct amount of whitespace
        output_string = "English" + " "*(max_english-7)+" |Maori"
        output_string += " "*(max_maori - 5) + " |Description\n"
        self.__view_scrolled.insert("0.0", output_string)
        self.__view_all_frame.grid(column=0, row=0, columnspan=3, sticky="WE")
        self.__view_scrolled.grid(row=0, column=0, columnspan=3)

    def __edit(self):
        # Let the find method know they are editing too
        self.__editing = True
        self.__edited = True
        self.__clear()
        self.__edit_frame = Frame(self.__parent)
        self.__edit_frame.grid(row=0, column=0)

        # select the language to search with
        self.__question_label = Label(self.__edit_frame, text="Search with?")

        # buttons go to the respective search function
        self.__english_button = Button(self.__edit_frame,
                                       text="English",
                                       command=self.__find_english)
        self.__maori_button = Button(self.__edit_frame,
                                     text="Maori", command=self.__find_maori)
        self.__english_button.grid(row=0, column=1)
        self.__maori_button.grid(row=0, column=2)
        self.__question_label.grid(row=0, column=0)

    def __delete(self):
        # Let the find method know they are editing too
        self.__deleteing = True
        self.__clear()
        self.__delete_frame = Frame(self.__parent)
        self.__delete_frame.grid(row=0, column=0)

        # select the language to search with
        question_label = Label(self.__delete_frame,
                               text="Search with?")

        # buttons go to the respective search function
        english_button = Button(self.__delete_frame,
                                text="English",
                                command=self.__find_english)
        maori_button = Button(self.__delete_frame,
                              text="Maori", command=self.__find_maori)
        english_button.grid(row=0, column=1)
        maori_button.grid(row=0, column=2)
        question_label.grid(row=0, column=0)

    def __clear(self):
        try:
            self.__find_maori_frame.destroy()
        except:
            pass

        try:
            self.__find_english_frame.destroy()
        except:
            pass

        try:
            self.__view_all_frame.destroy()
        except:
            pass

        try:
            self.__edit_frame.destroy()
        except:
            pass

        try:
            self.__delete_frame.destroy()
        except:
            pass

        try:
            self.__enter_frame.destroy()
        except:
            pass

    def quit(self):
        # Write the file to save the data, then close the window
        self.__write_to_file()
        self.__parent.destroy()

    def __read_from_file(self):
        """This allows the user to select a file
        to gather the input data from."""
        self.__parent.withdraw()
        try:
            filename = askopenfilename()

            file = open(filename, "r")
            lines = file.readlines()
            return lines
        except:
            return []

    def __write_to_file(self):
        filename = asksaveasfile(mode="w", defaultextension=".txt")
        self.__parent.withdraw()
        if filename is None:
            return

        # Writes the attributes of the places to the file
        for place in self.__places:
            write_string = place.get_english() + "," + place.get_maori() + ","
            write_string += place.get_description()
            filename.write(write_string)
        filename.close()


class Exam:
    def __init__(self, line):
        """Creates atrributes based off the line given from the file in the
        construction of the main class"""
        attributes = line.split(",")    # Splits the line into a list
        # Setting the attributes
        self.__name = attributes[0]
        self.__date = attributes[1]
        self.__time = attributes[2]
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
 
if __name__ == "__main__":
    root = Tk()
    Timetable(root)
    root.mainloop()
