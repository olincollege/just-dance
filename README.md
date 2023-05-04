# just-dance

Sparsh Gupta, Chang Jun Park and Akshat Jain

## Project Description

Visit our game's website at https://just-dance.netlify.app

‘Just Dance’ is a motion-based dance video game. 
The objective of the game is to follow the on-screen dance moves and score points by mimicking the dance moves with your body. 
The game uses pose-estimation techniques to detect player’s movements and then uses that to give them a score. 
We also utilize OpenCV and Tensorflow for carrying out computations on the video feed obtained from the user’s webcam video. 

Explore the real Just Dance Game at https://justdancenow.com

## Dependencies

| Package    | Uses                    |
|------------|-------------------------|
| NumPy      | Array Operations        |
| OpenCV     | Computer Vision         |
| Playsound  | Plays sound file        |
| TensorFlow | Machine Learning        |
| Mutagen    | Audio Length Extraction |
| Pytest     | Testing functions       |


 The dependencies are present in `requirements.txt` and can be installed using the following in terminal/command prompt (make sure to have your present working directory as this repo):
 
 ```
 pip install -r requirements.txt
 ```


## Computational Requirements

To have the best performance for this project, your machine must meet the following minimum requirements:

- **RAM:** At least 16GB of RAM is required to ensure smooth performance without lagging of video frames. We recommend using a machine with 32GB of RAM.

- **Camera:** A camera of at least 1080p resolution is recommended, although not required.

- **Processor:** We recommend using a multi-core processor with a clock speed of at least 2GHz to ensure fast computation times.

- **Graphics Card:** A dedicated graphics card with at least 2GB of memory is highly recommended to accelerate rendering and visualization tasks.


## Code Execution

To run the code in this repo, please clone this repo to your local machine and run `just_dance_gui.py` in either a Python-compatible IDE or if using a terminal/command prompt (make sure to have your present working directory as this repo):

```
python3 just_dance_gui.py
```

Executing `just_dance_gui.py` using python will automatically open the GUI window to start the game and play it. 

If you want to exit the game anytime during its execution, just press the 'q' key and it will kill the program.


## Song Credits

**Disclaimer**: We hereby declare that we do not own the rights to any music/song/video used in this project.
All rights belong to the owner.
No copyright infringement intended.

[1] [Dance Workout] Sia - Cheap Thrills | MYLEE Cardio Dance Workout, Dance Fitness (https://www.youtube.com/watch?v=_LMpUDvHq1Q)

[2] Call Me Maybe - Carly Rae Jepsen - Just Dance 4 (https://www.youtube.com/watch?v=wcWntZ1e1ns)

[3] Bruno Mars - Uptown Funk Dance Tutorial (https://www.youtube.com/watch?v=U9Zj1BaH01c)

[4] Dance on: Ghungroo | WAR (https://www.youtube.com/watch?v=v0JKF8S8ehc)

[5] Don't Start Now by Dua Lipa - Follow Along Dance Tutorial For Beginners (https://www.youtube.com/watch?v=p-CHsUqjnOA)

## Unit Tests

We test the functionality of our code by running pytest test cases. 
We mainly test whether the score calculated lies between 0-100, the top 5 leaderboard scores obtained are sorted in descending order, and the angles for the video and user's joints lies between 0-180.
The test files are present in the `test` directory. You can test the code by running the following in terminal/command prompt (make sure to have your present working directory as this repo):

```
pytest test_just_dance.py
```
