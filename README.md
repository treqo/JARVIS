# The JARVIS Project

**The JARVIS Project** is a Work-In-Progress Conversational AI Assistant, inspired by Iron Man's [JARVIS](https://en.wikipedia.org/wiki/J.A.R.V.I.S.). This project leverages a multimodal architecture, incpororating LLMs, speech recognition, and TTS models to create a sophisticated and interactive AI assistant.

The end goal of this project is to create a tool can be of assistance for leisure or highly demanding tasks, like assisting an engineer in designing a product. The hope is that it can provide support and increase efficiency when working on a project.

The roadmap for JARVIS will attempt to implement

- Ability to undertake subprocesses
- Computer vision support
- Custom futuristic UI for holomat, holographs and projection technology

## Installation

After cloning the repository, rename the `.example.env` file to `.env` and add the corresponding API keys.

For now, the working implementation is in the root directory, `main.py`. However, a revamp is currently in development, which would give the user freedom to customize which models they're using, as well as input parameters for each specific model. The reason for this change is because newer, more efficient models are bound to come out in the future, so having the ability to easily implement a newer model would be very beneficial.

## Config

You can fing the model configuration file under the `models` directory. Included in the same directory is a `md` file which will contain supported models and the corresponding API key needed, as well as model specs.
