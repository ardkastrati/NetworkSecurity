# Network security project
This repro contains all the code needed to run the project.

# Bootstrap
Before you start, make sure you have pip installed. If you are on Mac OS X, then install Python using Homebrew. That would automatically install pip for you! If you haven’t installed Python using Homebrew, you should definitely give it a try. It will save from a lot of headache everywhere in Python-land! If you are on Ubuntu, just run the following command on your terminal:

```bash
    sudo apt-get install python-pip
```
We are now ready to install Flask. Run the following command on your terminal:
```bash
    pip install flask
```
You should see the installation success message printed on your terminal.

# Run
To run the server run from your terminal and open [localhost:5000](localhost:5000 "") in your favourite browser.
```bash
    cd code
    python main.py
```

# Configuration
Currently the cookie is hardcoded in the main.py and is called terrorLoginCookie with the value 123. The steganography image is the image.jpg, but it has no content.