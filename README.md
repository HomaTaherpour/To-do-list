# To-do-list

This project is a to-do list application built using Python and Tkinter. It includes features for task management, theme customization, scheduling, and integration with ChatGPT for task-related assistance.

## Prerequisites

To run this application, you need the following libraries:

1. `tkinter` – for creating the graphical user interface
2. `Pillow` – for handling images (icons)
3. `openai` – for integrating with the OpenAI API (ChatGPT)
4. `tkcalendar` – for date selection
5. `json` – for saving and loading data
6. `subprocess` – for running system commands
7. `datetime` – for working with dates

### Installing Dependencies

To install the required libraries, you can use the following command:

pip install pillow openai tkcalendar


## Setting Up the Project

1. Download the code from the repository or extract the files.
2. Make sure you have Python 3.x and pip installed on your system.
3. Check the `requirements.txt` file to ensure all dependencies are installed.
4. Configure the `apichatgpt.py` file with your OpenAI API key.

### Setting Up ChatGPT API

To use the ChatGPT feature, you need an API key from OpenAI, which should be placed in the following line of code:

api_key = "YOUR_API_KEY"


You can get your API key from [OpenAI](https://platform.openai.com/signup).

### Running the Application

To run the application, execute the main file (usually `main.py` or a similarly named file):

python main.py

After running the program, a login window will appear. From there, you can log in or sign up as a new user.

### Features

- **User Login and Registration**: Users can log in or create a new account.
- **Task Management**: You can add, edit, delete, and reorder tasks.
- **Theme Customization**: The app allows you to change the theme color.
- **Random Tasks**: You can get a random task suggestion from a list of pre-defined tasks.
- **ChatGPT Assistance**: You can get help from ChatGPT for task descriptions.

