# HASH CHECKER
# VERSION 1.0
# CREATED BY PAUL IZZI
# DATE: 5 NOVEMBER, 2024

# IMPORT LIBRARIES
from tkinter import *

# VARIABLES
BACKGROUND_COLOR = "white"
hash1_characters = []
hash2_characters = []


# ______________________________ GET HASH -------------------------------- #

# Gets the hash value from the Entry box and places the hash in an array
def get_hashes():
    # Turn button back on to check hashes
    window.after(5000, lambda: check_btn.config(state="normal"))
    window.after(5000, lambda: different_btn.config(state="normal"))
    hash1_difference_label.delete(1.0, "end")
    hash2_difference_label.delete(1.0, "end")

    # Clear the hashes from original hash
    reset_hash(hash1_characters, hash2_characters)

    # Get data from the Entry box
    get_hash1 = hash1_input.get()
    get_hash2 = hash2_input.get()

    # Traverse through the lists for both hash1 and hash2 and add the letters to the appropriate lists
    for hash1letters in get_hash1:
        hash1_characters.append(hash1letters)

    for hash2letters in get_hash2:
        hash2_characters.append(hash2letters)

    # Check each letter within the hash against the letter in the same position from the opposite hash
    check_hashes(hash1_characters, hash2_characters)


# Compares each value within the hash to check if they are equal
def check_hashes(hash1, hash2):
    # Disables check button to prevent users from spamming the check button
    check_btn.config(state="disabled")

    # Checks to see if the length of the two lists are not equal and outputs message accordingly
    if len(hash1) != len(hash2):
        info_label.config(text="[i] The hashes are not equal. The file may have been modified.")
        hash1_input.config(bg="#FFCCCB")
        hash2_input.config(bg="#FFCCCB")
        reset_labels()
        return

    # If list lengths are equal, traverse through each character to see if all the characters are the same
    else:
        for i in range(len(hash1)):
            if hash1[i] != hash2[i]:
                info_label.config(
                    text=f"[{hashing_algorithm_type(hash1_characters, hash2_characters)}] The hashes are not equal. "
                         f"The file may have been modified.")
                hash1_input.config(bg="#FFCCCB")
                hash2_input.config(bg="#FFCCCB")
                reset_labels()
                return
            else:
                info_label.config(
                    text=f"[{hashing_algorithm_type(hash1_characters, hash2_characters)}] The hashes are equal. The "
                         f"file is secure.")
                hash1_input.config(bg="#90EE90")
                hash2_input.config(bg="#90EE90")
                reset_labels()


def reset_labels():
    window.after(5000, lambda: (
        info_label.config(text=""),
        hash1_input.config(bg=BACKGROUND_COLOR),
        hash2_input.config(bg=BACKGROUND_COLOR)
    ))


# Deletes all the elements in the array from the previous hash
def reset_hash(list1, list2):
    del list1[:]
    del list2[:]


def hashing_algorithm_type(hash1, hash2):
    if len(hash1) == len(hash2):
        if len(hash1) == 32:
            return "MD5"
        elif len(hash1) == 40:
            return "SHA-1"
        elif len(hash1) == 56:
            return "SHA-224"
        elif len(hash1) == 64:
            return "SHA-256"
        elif len(hash1) == 96:
            return "SHA-384"
        elif len(hash1) == 128:
            return "SHA-512"
        else:
            return "Not Found"


# -------------------------- SHOW DIFFERENCES ---------------------------- #

def show_differences():
    different_btn.config(state="disabled")

    hash1_difference_label.tag_configure("red", foreground="red")
    hash2_difference_label.tag_configure("red", foreground="red")

    def update_label(index, current_text1, current_text2):
        # For hash1 (length-based loop)
        if index < len(hash1_characters):
            char1 = hash1_characters[index]
            current_text1 += char1

            # Check if the character is different from hash2
            if index < len(hash2_characters):
                if char1 != hash2_characters[index]:
                    # Highlight in red if characters differ
                    hash1_difference_label.insert("end", char1, "red")
                else:
                    # Print normally if characters are the same
                    hash1_difference_label.insert("end", char1)
            else:
                # If hash2 is shorter, treat the missing character as different
                hash1_difference_label.insert("end", char1, "red")
        else:
            # If hash1 is shorter, insert a placeholder "-" and highlight in red
            current_text1 += "-"
            hash1_difference_label.insert("end", "-", "red")

        # For hash2 (length-based loop)
        if index < len(hash2_characters):
            char2 = hash2_characters[index]
            current_text2 += char2

            # Check if the character is different from hash1
            if index < len(hash1_characters):
                if char2 != hash1_characters[index]:
                    # Highlight in red if characters differ
                    hash2_difference_label.insert("end", char2, "red")
                else:
                    # Print normally if characters are the same
                    hash2_difference_label.insert("end", char2)
            else:
                # If hash1 is shorter, treat the missing character as different
                hash2_difference_label.insert("end", char2, "red")
        else:
            # If hash2 is shorter, insert a placeholder "-" and highlight in red
            current_text2 += "-"
            hash2_difference_label.insert("end", "-", "red")

        # Schedule the next character to be displayed after 100ms
        if index < max(len(hash1_characters), len(hash2_characters)) - 1:
            window.after(100, update_label, index + 1, current_text1, current_text2)

    # Start the process from the first character with empty strings for both hashes
    update_label(0, "", "")


# ------------------------------ CREATE GUI ------------------------------ #
window = Tk()
window.title("Hash Checker")
window.geometry("900x800")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.resizable(False, False)

# Create a frame to hold the logo and title together for easier alignment
frame = Frame(window, bg=BACKGROUND_COLOR)
frame.grid(row=0, column=0, columnspan=3, pady=(0, 20))  # This will take up the full width of the window

# Logo canvas
logo_canvas = Canvas(frame, width=200, height=200, highlightthickness=0, bg=BACKGROUND_COLOR)
logo_image = PhotoImage(file="hash_logo.png")

logo_canvas.create_image(100, 100, image=logo_image)
logo_canvas.grid(row=0, column=0, columnspan=3)

# Create a different logo image when program runs
window.iconphoto(True, logo_image)

# Title label directly beneath the logo
hash_checker_title = Label(frame, text="Hash Checker", font=("Courier", 20, "bold", "italic"), bg=BACKGROUND_COLOR)
hash_checker_title.grid(row=1, column=0, columnspan=3)

# Add hash labels inside the main canvas, properly positioned in its grid
hash1_label = Label(text="Hash 1: ", font=("Courier", 14, "bold"), pady=15, bg=BACKGROUND_COLOR, width=10)
hash1_label.grid(column=0, row=2)

hash2_label = Label(text="Hash 2: ", font=("Courier", 14, "bold"), pady=15, bg=BACKGROUND_COLOR, width=10)
hash2_label.grid(column=0, row=3)

# Create the information label that tells user if hash works checks out
info_label = Label(text="", font=("Courier", 14, "bold"), pady=10, bg=BACKGROUND_COLOR, width=64)
info_label.grid(column=0, row=4, columnspan=3)

# Generate the hash inputs
hash1_input = Entry(bg=BACKGROUND_COLOR, font=16, highlightthickness=1, width=64)
hash1_input.grid(column=1, row=2, columnspan=2)

hash2_input = Entry(bg=BACKGROUND_COLOR, font=16, highlightthickness=1, width=64)
hash2_input.grid(column=1, row=3, columnspan=2)

# Add a check button to compare hashes
check_btn = Button(text="Check", font=16, width=74, command=get_hashes)
check_btn.grid(column=0, row=5, columnspan=3, pady=15)

# Button to check where hash is different
different_btn = Button(text="Differences", font=16, width=74, state="disabled", command=show_differences)
different_btn.grid(column=0, row=6, columnspan=3, pady=10)

hash1_difference_label = Text(
    font=("Courier", 14, "bold"),
    pady=15,
    bg=BACKGROUND_COLOR,
    width=74,
    height=1,
    wrap=NONE,
)
hash1_difference_label.grid(column=0, row=7, columnspan=3)

scrollbar_hash1 = Scrollbar(window, orient=HORIZONTAL, command=hash1_difference_label.xview)
scrollbar_hash1.grid(row=8, column=0, columnspan=3, sticky="ew")  # Scrollbar placed below the label

# Attach the scrollbar to the label
hash1_difference_label.config(xscrollcommand=scrollbar_hash1.set)

hash2_difference_label = Text(
    font=("Courier", 14, "bold"),
    pady=15,
    bg=BACKGROUND_COLOR,
    width=74,
    height=1,
    wrap=NONE,
)
hash2_difference_label.grid(column=0, row=9, columnspan=3)

scrollbar_hash2 = Scrollbar(window, orient=HORIZONTAL, command=hash2_difference_label.xview)
scrollbar_hash2.grid(row=10, column=0, columnspan=3, sticky="ew")  # Scrollbar placed below the label

# Attach the scrollbar to the label
hash2_difference_label.config(xscrollcommand=scrollbar_hash2.set)

window.mainloop()
