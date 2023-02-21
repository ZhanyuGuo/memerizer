# Memerizer
This is a simple software to help you memorize words.

## How to use
1. Create an environment. (Conda is recommended.)
   ```sh
   conda create -n memerizer python=3.9
   conda activate memerizer
   ```
2. Install the requirements using pip.
   ```sh
   pip install -r requirements.txt
   ```
3. Done!
   ```sh
   python memerizer_<VERSION>.py
   ```

## Features
1. The Memerizer will show you an English word, you need to choose the right Chinese meaning for it. Then, the correct answer will be painted green, and incorrect choice will be painted red.
2. The Memerizer will automatically jump to the next word when you complete answering a word. The time is adjustable, and its range is 1~9s.
3. The Memerizer will record and load the wrong words, which will be focus on.
