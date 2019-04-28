# Sea Rescue Mission

## Description
This repo contains python code for the optimization of small autonomous rescue vessels' functions. What we are looking to optimise is the time needed to save all people in danger after a wreck nearby the port. The implementation uses Disjktra's algorithm and A-star algorithm for path planning.

***

## Dependencies
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)  
The following Python libraries are required:
1. Matplotlib
2. Numpy
3. sys
4. pyfiglet

***

## Water survival info

*__Water temperature__: 32 degrees or below  
Time until exhaustion or unconsciousness: Less than 15 minutes  
Expected time of survival in the water: Less than 15 to 45 minutes

*__Water temperature__: 32.5 to 40 degrees  
Time until exhaustion or unconsciousness: 15 to 30 minutes  
Expected time of survival in the water: 30 to 90 minutes

*__Water temperature__: 40 to 50 degrees  
Time until exhaustion or unconsciousness: 30 to 60 minutes  
Expected time of survival in the water: 1 to 3 hours

*__Water temperature__: 50 to 60 degrees  
Time until exhaustion or unconsciousness: 1 to 2 hours  
Expected time of survival in the water: 1 to 6 hours

*__Water temperature__: 60 to 70 degrees  
Time until exhaustion or unconsciousness: 2 to 7 hours  
Expected time of survival in the water: 2 to 40 hours

*__Water temperature__: 70 to 80 degrees  
Time until exhaustion or unconsciousness: 3 to 12 hours  
Expected time of survival in the water: 3 hours to indefinite

__People can survive indefinitely in water temperatures above 80 degrees.__

Source: [witn.com](https://www.witn.com/home/headlines/37639264.html?fbclid=IwAR1MX9ILbNpoEvrUhyUFarmyc0c0jeAujIL0o-s3PjkKBo_l_3_jf0T__Fs)
