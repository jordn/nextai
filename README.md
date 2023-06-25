## AutoCode 

_**Real time programming with your AI assistant.**_

This is a demonstration of a new way of developing software. 

##### **What it's not** 

It's not a big questionnaire (gpt-engineer) or upfront essay (smol developer)
 about how you want your system to behave. Let's be honest, you don't know that yet!

 ##### The core idea

Instead, the core idea is to make the iteration loop as tight as possible, so
that you can quickly respond, correct and improve as you develop your thoughts and your software.

### How it works

This is a demonstration of AutoCode for building a NextJS web app.


1. AutoCode is given a set of tools for exploring the code base, installing packages and editing files
2. You ask it to do stuff in chat
3. The dev server is hot-reloaded so you can see the effect immediately
4. Any errors are piped back into the the chat so the AI can fix them automatically


> “There is no failure. Only feedback.”
> 
>  – Robert Allen

The tools are simple Python functions converted into OpenAI function specs. It's a chat so you can underspecify and correct as you go.


### Getting Started

To develop using AutoCode this is what you do:

1. Install the dependencies by running `npm install`.
2. Start the development server by running `npm run dev 2> >(tee stderr.log >&2) | tee stdout.log`
3. Open your browser and navigate to `http://localhost:3000` to see the application.
4. Start the AI assistant by running `python nextai`.

