# NJITGlobalExplorer
NJIT Global Explorer is a full-stack interactive dashboard for NJIT Study Abroad Analytics. It is designed to be used by the NJIT Office of Global Initiatives to analyze and visualize the data from the Study Abroad program. This project is built using Flask, a Python web framework, and Firebase for data storage and user authentication. Additionally, it features an LLM-powered backend to analyze and draw conclusions on the data.

## Project Funding and Recognition
This project is funded and conducted through the NJIT Honors Summer Research Institute as a paid research project analyzing the impact of the NJIT Study Abroad Program. This project was presented at the NJIT Undergraduate Summer Research Symposium.

## Getting Started
These instructions will provide you with a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)
- A Firebase account and a new project for testing

### Installation
1. Clone the repository to your local machine using `git clone https://github.com/yourusername/NJITGlobalExplorer.git`
2. Navigate to the project directory using `cd NJITGlobalExplorer`
3. Install the required Python packages using `pip install -r requirements.txt`
4. Create a `.env` file in the root directory and fill it with your Firebase project credentials (API key, database URL, etc.)
5. Register for the meta-llama/Llama-3-8b-chat-hf LLM model using together.ai and obtain your API key.
6. Add the together.ai API key to your `.env` file.
7. Start the Flask server using `python main.py`, and visit `http://127.0.0.1:5000`
