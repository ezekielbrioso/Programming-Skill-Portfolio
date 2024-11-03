# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 11:57:05 2024

@author: Ezekiel
"""
import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu, ttk, simpledialog

class StudentManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Manager")
        self.master.geometry("520x550")
        self.master.configure(bg="#FFE5EC")

        #Load students data
        self.students = []
        self.load_data("studentMarks.txt")

        #Title Label
        title_label = tk.Label(master, text="Student Manager", font=("Times New Roman", 16, "bold"), bg="#FFE5EC", fg="#FB6F92")
        title_label.pack(pady=10)

        #Button Frame
        button_frame = tk.Frame(master, bg="#FFE5EC")
        button_frame.pack(pady=10)

        #Style for Buttons
        style = ttk.Style()
        style.configure("TButton",
                        font=("Times New Roman", 10),
                        padding=6,
                        relief="flat",
                        background="#FF8FAB",
                        foreground="#3D3D3D")  #Darker font color for readability
        style.map("TButton",
                  background=[("active", "#FB6F92")])

        # Creating Buttons with Aligned Layout
        ttk.Button(button_frame, text="View All Student Records", command=self.view_all_records).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Show Highest Score", command=self.show_highest_score).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Show Lowest Score", command=self.show_lowest_score).grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        ttk.Button(button_frame, text="Sort Records", command=self.sort_records).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Add Record", command=self.add_record).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Delete Record", command=self.delete_record).grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        #Move Update Record button to the next row for alignment
        ttk.Button(button_frame, text="Update Record", command=self.update_record).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        #Dropdown for Individual Record Selection
        selection_frame = tk.Frame(master, bg="#FFE5EC")
        selection_frame.pack(pady=10)

        tk.Label(selection_frame, text="View Individual Student Record:", font=("Times New Roman", 10), bg="#FFE5EC", fg="#FB6F92").grid(row=0, column=0, padx=5)

        self.selected_student = StringVar(master)
        self.selected_student.set("          ")
        self.update_student_list()

        student_menu = ttk.OptionMenu(selection_frame, self.selected_student, "", *self.student_names)
        student_menu.grid(row=0, column=1, padx=5)

        ttk.Button(selection_frame, text="View Record", command=self.view_individual_record).grid(row=0, column=2, padx=5)

        #Result Text Area
        self.result_text = tk.Text(master, wrap="word", font=("Times New Roman", 10), height=12, width=50, bg="#FFC2D1", fg="#000000")
        self.result_text.delete(1.0, tk.END)
        self.result_text.pack(pady=10)



    def load_data(self, filename): #Loads data from the file
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

            self.average_percentage = sum(s['overall_percentage'] for s in self.students) / self.num_students

        except FileNotFoundError:
            messagebox.showerror("Error", "The file studentMarks.txt was not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def get_grade(self, percentage):
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

    def update_student_list(self): #Updates list 
        self.student_names = [student["name"] for student in self.students]

    def view_all_records(self): #Displays records of all students
        self.result_text.delete(1.0, tk.END)
        for student in self.students:
            self.result_text.insert(tk.END, self.format_student_record(student))
            self.result_text.insert(tk.END, "\n\n")
        self.result_text.insert(tk.END, f"Total Students: {self.num_students}\n")
        self.result_text.insert(tk.END, f"Average Percentage: {self.average_percentage:.2f}%")

    def view_individual_record(self): #Displays record of a selected student
        selected_name = self.selected_student.get()
        student = next((s for s in self.students if s["name"] == selected_name), None)
        if student:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.format_student_record(student))
        else:
            messagebox.showwarning("Warning", "Student not found.")

    def show_highest_score(self): #Displays the record of the student who has highest score
        if self.students:
            highest_student = max(self.students, key=lambda s: s["overall_percentage"])
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.format_student_record(highest_student))
        else:
            messagebox.showwarning("Warning", "No student data available.")

    def show_lowest_score(self): #Displays the record of the student who has lowest score
        if self.students:
            lowest_student = min(self.students, key=lambda s: s["overall_percentage"])
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.format_student_record(lowest_student))
        else:
            messagebox.showwarning("Warning", "No student data available.")

    def sort_records(self): #Displays sorted record, it can be ascending or descending
        order = simpledialog.askstring("Sort Order", "Enter 'asc' for ascending or 'desc' for descending:")
        if order in ["asc", "desc"]:
            self.students.sort(key=lambda s: s["overall_percentage"], reverse=(order == "desc"))
            self.view_all_records()
        else:
            messagebox.showwarning("Warning", "Invalid sort order. Please enter 'asc' or 'desc'.")


    def delete_record(self): #Responsible for deleting record
        selected_name = self.selected_student.get()
        self.students = [s for s in self.students if s["name"] != selected_name]
        self.update_student_list()
        self.save_data()
        messagebox.showinfo("Success", "Student deleted successfully.")
        self.view_all_records()

    def update_record(self): #Responsible for updating record
        selected_name = self.selected_student.get()
        student = next((s for s in self.students if s["name"] == selected_name), None)
        if student:
            field = simpledialog.askstring("Update Field", "Enter the field to update (name, coursework, exam):")
            if field == "name":
                new_name = simpledialog.askstring("Input", "Enter New Name:")
                student["name"] = new_name
            elif field == "coursework":
                student["coursework_total"] = sum([int(simpledialog.askstring("Input", f"Enter Coursework {i+1} Marks:")) for i in range(3)])
            elif field == "exam":
                student["exam_mark"] = int(simpledialog.askstring("Input", "Enter New Exam Mark:"))
            else:
                messagebox.showwarning("Warning", "Invalid field.")
                return
            student["overall_percentage"] = (student["coursework_total"] + student["exam_mark"]) / 160 * 100
            student["grade"] = self.get_grade(student["overall_percentage"])
            self.save_data()
            messagebox.showinfo("Success", "Student record updated successfully.")
            self.view_all_records()

    def format_student_record(self, student): #This formats and returns a string representation of a student's details, including their name, ID, coursework total, exam mark, overall percentage, and grade
        return (f"Name: {student['name']}\n"
                f"Number: {student['id']}\n"
                f"Coursework Total: {student['coursework_total']}\n"
                f"Exam Mark: {student['exam_mark']}\n"
                f"Overall Percentage: {student['overall_percentage']:.2f}%\n"
                f"Grade: {student['grade']}")
            
    def add_record(self): #This prompts the user to input a new student's ID, name, coursework marks, and exam mark, calculates their total coursework, overall percentage, and grade, adds the new student to the student list, updates the dropdown menu, and saves the data to the file
        try:
            student_id = int(simpledialog.askstring("Input", "Enter Student ID:"))
            name = simpledialog.askstring("Input", "Enter Student Name:")
            coursework_marks = [int(simpledialog.askstring("Input", f"Enter Coursework {i+1} Marks:")) for i in range(3)]
            exam_mark = int(simpledialog.askstring("Input", "Enter Exam Mark:"))

            total_coursework = sum(coursework_marks)
            overall_percentage = (total_coursework + exam_mark) / 160 * 100
            grade = self.get_grade(overall_percentage)

            new_student = {
                "id": student_id,
                "name": name,
                "coursework_total": total_coursework,
                "exam_mark": exam_mark,
                "overall_percentage": overall_percentage,
                "grade": grade
            }
        #Adds the new student to the students list
            self.students.append(new_student)
            self.num_students += 1  # Increment total student count

        #Updates the student names list
            self.update_student_list()

        #Refresh dropdown with updated student list
            self.selected_student.set("")  # Reset selection
            student_menu = self.master.nametowidget(self.selected_student._name)
            menu = student_menu.children["menu"]
            menu.delete(0, "end")
            for name in self.student_names:
                menu.add_command(label=name, command=lambda value=name: self.selected_student.set(value))

        #Saves the updated data to the file
            self.save_data()

        #Refresh the displayed student count and notify the user
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Student '{name}' added successfully.\n")
            self.result_text.insert(tk.END, f"Total Students: {self.num_students}\n")

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numeric values for marks.")
            
    def save_data(self): #This writes the current list of students, including their IDs, names, coursework averages, and exam marks, to the studentMarks.txt file, overwriting any existing data
        try:
            with open("studentMarks.txt", "w") as file:
                file.write(f"{len(self.students)}\n")
                for s in self.students:
                    coursework_marks = [str(int(s["coursework_total"] / 3))] * 3
                    file.write(f"{s['id']},{s['name']},{','.join(coursework_marks)},{s['exam_mark']}\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving data: {e}")


#Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()

