# CS7IS2: Artificial Intelligence
TCD Group Project for AI

We are using Python 3.6 in this project.

Create a python3 virutal environment and activate it.

If you use ```venv```, follow as below to create a virtual environment.

```
python -m venv <Virtual Env Name>
source <Virtual Env Name>/bin/activate
```
If you use ```conda```, follow as below to create the virtual environment.
```
conda create -n <Virtual Env Name> python=3.6
```

Activate and Deactivate before and after working with the project.
```
conda activate <Virtual Env Name>
conda deactivate
```

After that install the required packages using pip,
```
pip install -r requirements.txt
```


## TO PLAY GAME

Checkout this repository to your local machine

Change the current working directory to the path where you have cloned or downloaded the repository.

Once in project directory 
```
cd OthelloWithAI
```
To start playing
```
python play.py
```
You will be opted to choose both players from "human,random,alphabeta,expectimax,minimax"

If you want to play manually, enter "human".

If you want to choose AI, choose one of four agents presented to you.

To select the difficulty level, please select
- '1' for Easy
- '2' for Medium
- '3' for Hard

*Enjoy the game.*

   
## For people working on this project,

### Travis-CI

* We use Travis-CI for continuous integration in this project.

### git-latexdiff

* We use ``` git-latexdiff ``` to track the changes made in the latex version of the final report.

To install ``` git-latexdiff ``` follow the below instructions,

1. Extract the zip file, *"git-latexdiff-master.zip"* from this repository outside of the repository folder.

2. We need to install ``` git-latexdiff ``` in Git's exec-path using the make file.
   We need ``` asciidoc ``` to create the make file. Run the below commands to install the same.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Linux Users (Also make sure gcc is installed):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``` sudo apt-get install -y asciidoc ```
  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Mac Users (Make sure Homebrew is installed):
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;``` brew install asciidoc ```

3. ```cd``` into the extracted folder and do,
```make install```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If git was installed on root, follow this,
```sudo make install```

4. You can verify the installation as following, ```cd``` into the path given by ```git --exec-path``` and ```ls```. The output of this should show you ``` git-latexdiff ```, if installed successfully.
