## Project Overview

The TalentScout Hiring Assistant Chatbot is a conversational app that uses AI to simplify the initial candidate screening process for a fictional recruitment agency, `TalentScout`. 

The chatbot interacts with candidates, gathers important information, and creates customized technical questions based on their tech stack. It uses AI Models (gpt-5-nano) to make sure conversations are intelligent, context aware, and responsive.

[Read docs](https://docs.google.com/document/d/e/2PACX-1vSP4tbsAIbF4pqt1gKeS2adWFtyzw-ceGEwOuxc4h_RhInFWLOZ2F6wHYKMiMf7FmUif2sDbcWxAqUW/pub) for more information.

![alt text](image.png)

## Installation

1. Clone the Repository: 
    ```bash 
    git clone https://github.com/Ankit6174/talentscout-hiring-assistant.git
    cd talentscout-hiring-assistant
    ```
    
2. Create Virtual Environment
    ```bash 
    uv venv venv
    source venv/bin/activate  # Mac/Linux
    venv\Scripts\activate     # Windows
    ```

3. Install Dependencies
    ```bash 
    uv sync
    ```

4. Set API Keys: 
    
    Create a .env file and add API_KEYS. See [.env.example](.env.example)

5. Run the Application
    ```bash 
    streamlit run main.py
    ```

## Tech Stack

| Category      | Technology                                                                                                                                                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Language** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
| **UI**         | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) |
| **AI Frameworks** | ![LangChain](https://img.shields.io/badge/LangChain-0FA958?style=for-the-badge) ![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge) ![LangSmith](https://img.shields.io/badge/LangSmith-FF6F61?style=for-the-badge)
| **Model** | ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--5%20Nano-412991?style=for-the-badge&logo=openai&logoColor=white) |
| **Database** | ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)                                                                                                                                         |
| **Deployment**| ![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Author

**Ankit Ahirwar**

* [Twitter](https://x.com/Ankit6174)
* [Medium](https://medium.com/@ankit6174)
* [LinkedIn](https://www.linkedin.com/in/Ankit6174) 