import os

# 1st function.
def welcome():
    """
    Prints welcome message and purpose of the program for the user
    """
    
    print("Welcome to the Caesar Cipher")
    print("This program encrypts and decrypts text with Caesar Cipher.")
    
# 2nd function
def enter_message():
    """
    Asks user to choose either encryption or decryption, the message they'd like to 
    process, and the shift value.
    
    Returns a tuple that contains mode, message and shift.
    """

# asking user to input until value is d or e.
    while True:
        mode = input("Would you like to encrypt (e) or decrypt (d): ").lower()
        if mode in ['e']:
            break
# asking user input until alphabet in entered.
    while True:
        message = input(f"What message would you like to {'encrypt' if mode=='e' else 'decrypt'}?").upper()
        if message.isalpha():
            break
# asking user input until shift is within range of 0-26.
    while True:
        try:
            shift = int(input("What is the shift number: "))
            if 0 <= shift <= 25:
                break
        except ValueError:
            print("Invalid Shift. Please enter a number.")
# returning values as tuple
    return mode, message, shift


# 3rd function
def encrypt(message, shift):
    """
    Encrypts the message given by user.
    Returns the encrypted message.
    """
    res = ""
    
# iterates over each character in user input
    for x in message:
        if x.isalpha():
            
# if a character in x is lower character, setting value to ASCII value of 'a'
# else to the value of 'A'
            if x.islower():
                base = ord('a')
            else:
                base = ord('A')
# ord gets ASCII value of x, '+shift' gets the new position in alphabet
# -base to subtract the ASCII value and calculate in terms of actual alphabets.
            
            shifted_char = chr((ord(x) - base + shift) % 26 + base)
            res = res + shifted_char
            
# if character is not alphabet it is directly appended to the result.
        else:
            res = res + x
    return res


# 4th function
def decrypt(message, shift):
    """ 
    Decrypts the given message.
    Returns the decrypted message.
    """
    return encrypt(message, -shift)


# 5th function
def process_file(filename, mode1, shift):
    """ 
    Opens given file with read mode, encrypts or decrypts them and returns the result.
    """
    msgs = []
    try:
# opening a file, reading it's content line by line and 
# append each line to msgs by removing starting and ending while spaces.
        with open(filename, 'r') as f:
            for line in f:
                msgs.append(line.strip())

# error handling if file is not found
    except FileNotFoundError:
        print("File not found")
        return []
    print(msgs)
    
    return [encrypt(message, shift) if mode1 == 'e' else decrypt(message, shift) for message in msgs]


# 6th function
def is_file(filename):
    """ 
    Checks if the file given by user exists or not.
    """
    return os.path.isfile(filename)


# 7th function
def write_messages(msgs):
    """ 
    Writes messages to results.txt file
    """
    with open('results.txt', 'w') as f:
        for message in msgs:
            f.write(message + '\n')
        
            
# 8th function
def message_or_file():
    """ 
    Asks the user to select either encrypt or decrypt,
    select whether to take input from a file or console, 
    Returns the output.
    """
    while True:
        mode1 = input("Would you like to encrypt (e) or decrypt (d): ").lower()
        if mode1 in ['e', 'd']:
            break
        else:
            print("Invalid Mode")

    while True:
        check = input("Would you like to read from a file (f) or the console (c): ").lower()
        if check in ['f', 'c']:
            break
        else:
            print("Invalid Choice")

    if check == 'c':
        while True:
            message = input(f"What message would you like to {'encrypt' if mode1=='e' else 'decrypt'}? ")
            message = message.upper()
            if any(c.isalpha() for c in message):
                break
            else:
                print("Invalid Message")
        return mode1, message, None
    else:
        while True:
            filename = input("Enter a filename: ")
            if is_file(filename):
                break
            else:
                print("Invalid Filename")
        return mode1, None, filename
    
    
# 9th function

def main():
    """ 
    Main function that organizes the code.
    """
    
# welcome function call
    welcome()
    
# keep asking until user decides to exit
    while True:
        mode1, message, filename = message_or_file()
        shift = 0
        while True:
            try:
                shift = int(input("What is the shift number: "))
                if 1 <= shift <= 26:
                    break
                else:
                    print("Invalid Shift")
            except ValueError:
                print("Invalid Shift. Please enter a number.")

        if filename:
# processing file based on selected mode and shift value
            message = process_file(filename, mode1, shift)
# checking if the message list is not empty
            if message:
                write_messages(message)
                print(message)
                print("Output written to results.txt")
            else:
                print("No messages to process.")
        else:
            result = encrypt(message, shift) if mode1 == 'e' else decrypt(message, shift)
            print(result)

        next_msg = input("Would you like to encrypt or decrypt another message? (y/n): ")
        next_msg = next_msg.lower()
        if next_msg != 'y':
            print("Thanks for using the program, goodbye!")

if __name__ == "__main__":
    main()