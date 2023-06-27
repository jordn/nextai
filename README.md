## AutoCode 🤖

_**Real time programming with your AI assistant.**_

This is a demonstration of a new way of developing software.

#### **What it's not** 

It's not a big questionnaire (gpt-engineer) or upfront essay (smol developer) about how you want your system to behave. Let's be honest, you don't know that yet!

 #### The core idea

Instead, the core idea is to make the iteration loop as tight as possible, so
that you can quickly respond, correct and improve as you develop your thoughts and your software.

#### Philosophy

- Simplicity
- Speed and fast iterations
- No need to specify everything upfront
- Try, look, improve
- Use AI but feel free to code too 

### How it works

This is a demonstration of AutoCode for building a NextJS web app.

1. AutoCode is given tools for exploring the code base, installing packages and editing files
2. You ask it to do stuff in chat
3. The app is hot-reloaded so you can see the effect immediately
4. Errors are piped back into the the chat so the AI can fix them automatically


> “There is no failure. Only feedback.”
> 
>  – Robert Allen

The tools are simple Python functions converted into OpenAI function specs. It's a chat so you can underspecify and correct as you go. 

**Note:** We used GPT-4, like smol-developer and gpt-engineer do, and this will not work as well with GPT 3.5

### Getting Started

To develop using AutoCode this is what you do:

1. Install the dependencies: `brew install ripgrep tree` and `npm install`
2. Rename `.env.sample` to `.env` and add your OpenAI API key
3. Start the development server by running `npm run dev 2> >(tee stderr.log >&2) | tee stdout.log`
4. Open your browser and navigate to `http://localhost:3000` to see the application
5. Start the AI assistant by running `python nextai`

