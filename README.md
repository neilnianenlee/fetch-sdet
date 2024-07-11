# fetch-sdet
## setup
Please make sure that you have Python 3.12.4 installed which can be installed from [here](https://www.python.org/downloads/release/python-3124/).

The test also requires Python packages selenium version 4.22.0 and webdriver_manager version 4.0.1. If you feel comfortable, please install them yourself.

Otherwise, please run the provided setup.py file:
> python setup.py

In order to run the test:
> python fake-bar-finder.py (number_of_iterations: optional)

It will print out to stdout the alert message, number of weighing, and the list of weighing made.

## overall
initial playing around resulted in the following algorithm:
split the input into two equal buckets:
1. 0-3
2. 4-7

if both buckets are equal weight, we found the fake which is #8
however, if one bucket is lighter, we split that bucket into 2 again and repeat
resulting in 
>O(log_2(n))

referencing the below discussion on stackoverflow, it can be improved into 3 buckets as there are 9 gold bars,
resulting in 
>O(log_3(n))

I looked it up to ensure my initial algorithm was correct, but could be improved.
however, the overall improvement I would consider insignificant, but something i pursued out of self-interest.
because the website uses 'coins' instead of 'gold bars', the program was written in context of 'coins'

## References:
- https://stackoverflow.com/questions/6683485/fake-coin-problem
- https://www.browserstack.com/guide/get-current-url-in-selenium-and-python
- https://www.browserstack.com/guide/ui-automation-using-python-and-selenium#:~:text=A%20Detailed%20Guide-,UI%20Testing%20with%20Selenium%20and%20Python%3A%20Example,%2Dto%2Dend%20user%20process.
- https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python