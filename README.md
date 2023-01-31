# Athletics results scrapper

A PDF scrapper for RFEA format athletics results documents with Python and FastAPI.

## How to make it work

The project was made on a Windows computer, so I don't think it will work on Unix systems.
For linux or mac os, it would be necessary to adapt the paths in the computer to '/' instead of
'\', so the system processes it correctly.

Before starting the web app, it is necessary to init the virtual environment using `.\venv\Scripts\activate`
as the dependencies are installed on it.

To start the web server, the comand to input is `uvicorn main:app --reload`.
It will start a development server, which will be enough to try the app.
After that, open your web browser and navigate to `localhost:8000` or `http://127.0.0.1:8000`. The URL will be showed in the command line.

It is important to run the project from the folder where the `main.py` file is located.
The same applies for the example code folder.

## How it works

The principal URL is `/` (index), which includes a form and processes the pdf sent by the user. It will show an error if you send a non pdf file. If the pdf is not in RFEA results format (see example in the `/pdf`) folder, it will probably return a 0 element list (`[]`) as a response, which indiceates that there was no information scrapped.

The rest of the URLs available are in the `routes.py` file.

## Contact

Remember that this is still a new project, so there will be many bugs and errors, but I'll be working to fix them if the project goes ahead.

If you have any questions or suggestions feel free to ask me by email (emagodev@gmail.com) or social media ([Instagram](https://www.instagram.com/3rnestomartinez/) or [Twitter](https://twitter.com/3rnestomartinez): @3rnestomartinez).
