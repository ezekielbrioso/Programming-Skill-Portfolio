# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 09:05:57 2024

@author: Ezekiel
"""

import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu, ttk

class StudentManager: #Responsible for Initializing the main interface, sets up the window properties, and loads student data
    def __init__(self, master):
        self.master = master
        self.master.title("Student Manager")
        self.master.geometry("520x450")
        self.master.configure(bg="#FFE5EC")

        #This loads students data
        self.students = []
        self.load_data("studentMarks.txt")

        #For the title label
        title_label = tk.Label(master, text="Student Manager", font=("Times New Roman", 16, "bold"), bg="#FFE5EC", fg="#FB6F92")
        title_label.pack(pady=10)

        #For the button frame
        button_frame = tk.Frame(master, bg="#FFE5EC")
        button_frame.pack(pady=10)

        #Style for Buttons
        style = ttk.Style()
        style.configure("TButton",
                        font=("Times New Roman", 10),
                        padding=6,
                        relief="flat",
                        background="#FF8FAB",
                        foreground="#3D3D3D")  
        style.map("TButton",
                  background=[("active", "#FB6F92")])

        #This is for creating buttons
        ttk.Button(button_frame, text="View All Student Records", command=self.view_all_records).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Show Highest Score", command=self.show_highest_score).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Show Lowest Score", command=self.show_lowest_score).grid(row=0, column=2, padx=5)

        #Dropdown that shows individual record selection
        selection_frame = tk.Frame(master, bg="#FFE5EC")
        selection_frame.pack(pady=10)

        tk.Label(selection_frame, text="View Individual Student Record:", font=("Times New Roman", 10), bg="#FFE5EC", fg="#FB6F92").grid(row=0, column=0, padx=5)

        #For selecting and updating student list
        self.selected_student = StringVar(master)
        self.selected_student.set("          ")  
        self.update_student_list()

        #Creates the OptionMenu for students with an empty first option
        student_menu = ttk.OptionMenu(selection_frame, self.selected_student, "", *self.student_names)
        student_menu.grid(row=0, column=1, padx=5)

        ttk.Button(selection_frame, text="View Record", command=self.view_individual_record).grid(row=0, column=2, padx=5)

        #This is the result text area (starts empty)
        self.result_text = tk.Text(master, wrap="word", font=("Times New Roman", 10), height=12, width=50, bg="#FFC2D1", fg="#000000")
        self.result_text.delete(1.0, tk.END)  
        self.result_text.pack(pady=10)

    def load_data(self, filename): #These loads student data from a file, calculates coursework totals, percentages, and grades, then appends each student’s data to self.students
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                self.num_students = int(lines[0].strip())

                for line in lines[1:]:
                    student_data = line.strip().split(",")
                    student_id = int(student_data[0])
                    name = student_data[1]
                    coursework_marks = list(map(int, student_data[2:5]))
                    exam_mark = int(student_data[5])
                    total_coursework = sum(coursework_marks)
                    overall_percentage = (total_coursework + exam_mark) / 160 * 100
                    grade = self.get_grade(overall_percentage)

                    student = {
                        "id": student_id,
                        "name": name,
                        "coursework_total": total_coursework,
                        "exam_mark": exam_mark,
                        "overall_percentage": overall_percentage,
                        "grade": grade
                    }

                    self.students.append(student)

            #This code calculates average percentage
            self.average_percentage = sum(s['overall_percentage'] for s in self.students) / self.num_students

        except FileNotFoundError:
            messagebox.showerror("Error", "The file studentMarks.txt was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def get_grade(self, percentage): #Determines and returns a letter grade based on the student’s overall percentage
        if percentage >= 70:
            return "A"
        elif percentage >= 60:
            return "B"
        elif percentage >= 50:
            return "C"
        elif percentage >= 40:
            return "D"
        else:
            return "F"

    def update_student_list(self): #Updates self.student_names with the names of all students for use in the dropdown menu
        self.student_names = [student["name"] for student in self.students]

    def view_all_records(self): #This clears and displays all student records in self.result_text, along with the total number of students and average percentage
        self.result_text.delete(1.0, tk.END)

        for student in self.students:
            self.result_text.insert(tk.END, self.format_student_record(student))
            self.result_text.insert(tk.END, "\n\n")

        self.result_text.insert(tk.END, f"Total Students: {self.num_students}\n")
        self.result_text.insert(tk.END, f"Average Percentage: {self.average_percentage:.2f}%")

    def view_individual_record(self): #This displays the selected student’s record from self.students based on the dropdown selection
        selected_name = self.selected_student.get()
        student = next((s for s in self.students if s["name"] == selected_name), None)

        if student:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.format_student_record(student))
        else:
            messagebox.showwarning("Warning", "Student not found.")

    def show_highest_score(self): #Displays the record of the student with the highest score
        if self.students:
            highest_student = max(self.students, key=lambda s: s["overall_percentage"])
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.format_student_record(highest_student))
        else:
            messagebox.showwarning("Warning", "No student data available.")

    def show_lowest_score(self): #Displays the record of the student with the lowest score
        if self.students:
            lowest_student = min(self.students, key=lambda s: s["overall_percentage"])
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.format_student_record(lowest_student))
        else:
            messagebox.showwarning("Warning", "No student data available.")

    def format_student_record(self, student): #Formats a student's information into a structured string for display in the result text area
        return (f"Name: {student['name']}\n"
                f"Number: {student['id']}\n"
                f"Coursework Total: {student['coursework_total']}\n"
                f"Exam Mark: {student['exam_mark']}\n"
                f"Overall Percentage: {student['overall_percentage']:.2f}%\n"
                f"Grade: {student['grade']}")

#Runs the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()
