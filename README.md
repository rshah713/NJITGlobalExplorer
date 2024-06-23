# NJIT Global Explorer
Welcome to the [NJIT Global Explorer](https://github.com/yourusername/NJITGlobalExplorer), a comprehensive, full-stack interactive dashboard designed specifically for the analysis and visualization of NJIT's Study Abroad Program data. This tool is intended for use by the NJIT Office of Global Initiatives, providing them with a powerful resource to draw meaningful insights from the program's data.

The NJIT Global Explorer is built on [Flask](https://flask.palletsprojects.com/), a robust Python web framework, and utilizes [Firebase](https://firebase.google.com/) for secure data storage and user authentication. A unique feature of this project is its LLM-powered backend, which is capable of analyzing data and drawing significant conclusions.

## Project Funding and Accolades
The NJIT Global Explorer is a product of the NJIT Honors Summer Research Institute, where it was developed as a paid research project. The project's primary focus is to analyze the impact of the NJIT Study Abroad Program. The project has been recognized and presented at the NJIT Undergraduate Summer Research Symposium.

## Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Ensure you have the following installed on your system:
- [Python 3.6 or higher](https://www.python.org/downloads/)
- [pip (Python package installer)](https://pip.pypa.io/en/stable/installation/)
- A [Firebase account](https://firebase.google.com/) and a new project for testing

### Installation
Follow these steps to set up the project:
1. Clone the repository to your local machine using `git clone https://github.com/yourusername/NJITGlobalExplorer.git`
2. Navigate to the project directory using `cd NJITGlobalExplorer`
3. Install the required Python packages using `pip install -r requirements.txt`
4. Create a `.env` file in the root directory and populate it with your Firebase project credentials (API key, database URL, etc.)
5. Register for the [meta-llama/Llama-3-8b-chat-hf LLM model](https://together.ai/) and obtain your API key.
6. Add the together.ai API key to your `.env` file.
7. Start the Flask server using `python main.py`, and visit `http://127.0.0.1:5000` to view the project.

