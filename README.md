WL_DOE
======

The DOE project of Wikkit Labs

======

classifier.py : classification module

student_recommend.py : recommendation either based on hmm or rule

generate_exercise.py : Randomly generate exercise problem for test and also updating rules 


1. To run the code first install hmmlearn package:

git clone git://github.com/hmmlearn/hmmlearn.git
cd hmmlearn
sudo python setup.py install


2. go into ipython
run student_recommend.py

== 
Package Wrapping - Flask/Django

Dependency
1. python-dev
2. python-setuptools
3. numpy
sudo pip install numpy 
4. scipy
sudo apt-get install liblapack-dev libatlas-dev gfortran
TODO: check how to import the above libraries in Flask 
sudo pip install scipy
5. sklearn (>1.6)
sudo pip install sklearn
6. matplotlib (1.4.3)
sudo apt-get install libfreetype6-dev libpng12-dev
TODO: check how to import the above libraries in Flask 
sudo pip install matplotlib 
7. hmmlearn
TODO: Import the egg into flask project
8. flask (0.10.1) 

# old dependency
9. cython (0.22.1)

== 
generate_exercise.py
