# LinkedIn Automater AI 🤖✨

Welcome to **LinkedIn Automater AI**, your new best friend for automating LinkedIn job applications. Ever dreamt of having a robot do your job hunting? Well, now you have one. Just hope it doesn’t start applying for jobs on Mars. 🚀

## Table of Contents

- [Introduction](#introduction)
- [Setup](#setup)
- [Configuration](#configuration)
- [Shoutouts](#shoutouts)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Are you tired of endlessly copying and pasting your resume into job applications? Do you wish you had a personal assistant that actually does something useful? Look no further! **LinkedIn Automater AI** is here to take over your LinkedIn job applications with style and efficiency. 🌟

## Setup

To get started, you’ll need to set up a Python virtual environment to keep things tidy. If you’re not familiar with virtual environments, don’t worry—it's like a sandbox for your Python projects. 🏖️

1. **Clone the repository and open its folder:**

    ```bash
    git clone https://github.com/akshay-k-a-dev/LinkedIn_Automater_AI
    cd LinkedIn_Automater_AI
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the application:**

    ```bash
    python3 main.py
    ```

## Configuration

Before you start automating your job applications, you need to configure a few things. Don’t worry, it’s easier than making a cup of coffee. ☕

1. **Create and configure the YAML files in the `data_folder`:**

    - `config.yaml`: This is where you configure the automation parameters. Think of it as your personal job application settings menu.

    - `plain_text_resume.yaml`: Your resume in plain text. If you don’t have one, it’s time to dust off that old resume and give it a makeover.

    - `secrets.yaml`: This file contains sensitive information like your LinkedIn email, password, and Gemini API credentials. Make sure to keep it safe and secure. 🛡️

## Shoutouts

A huge shoutout to the awesome folks who inspire us:

- [LinkedIn Auto Jobs Applier with AI](https://github.com/feder-cr/linkedIn_auto_jobs_applier_with_AI): They’ve set the bar high by using the OpenAI API. Kudos to them! 🌟

- Libraries we use (and couldn’t live without):
    - `langchain`, `langchain-community`, `langchain-core`, `langsmith`
    - `Levenshtein`, `regex`, `reportlab`, `selenium`, `webdriver-manager`
    - And many more in `requirements.txt`!

    Special thanks to `lib_resume_builder_AIHawk` for their incredible resume-building library. 🙌

## Contributing

Found a bug? Have an idea for a cool feature? We welcome contributions! Feel free to open an issue or submit a pull request. Help us make this project even better, and let’s automate the world together. 🌍💡

## License

Distributed under the GLP3 license. See [LICENSE](LICENSE) for more information.

Happy automating! 🚀
