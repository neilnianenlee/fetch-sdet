# fetch-sdet
## Setup
Download the code and unzip it into a directory that you can easily access.

Please make sure that you have Python 3.12.4 installed which can be installed from [here](https://www.python.org/downloads/release/python-3124/).

The test also requires Python packages selenium version 4.22.0 and webdriver_manager version 4.0.1. If you feel comfortable, please install them yourself.

Otherwise, please run the provided setup.py file by opening up a terminal inside of the unzipped folder directory and typing the following command:
> python setup.py

In order to run the test:
> python fake-bar-finder.py (number_of_iterations: optional)

It will print out to stdout the alert message, number of weighing, and the list of weighing made.

## Overall
Initial playing around resulted in the following algorithm:
First, split the input into two equal buckets:
1. 0-3
2. 4-7

If both buckets are equal weight, we found the fake which is #8.
However, if one bucket is lighter, we split that bucket into 2 again and repeat until bucket is size of 1.
Runtime results in :
>O(log_2(n))

Referencing the below discussion on stackoverflow, it can be improved into 3 buckets as there are 9 gold bars.
Runtime results in :
>O(log_3(n))

I looked it up to ensure my initial algorithm was correct, but could be improved.
However, the overall improvement I would consider insignificant, but something I pursued out of self-interest.
Because the website uses 'coins' instead of 'gold bars', the program was written in context of 'coins'.

## References:
- https://stackoverflow.com/questions/6683485/fake-coin-problem
- https://www.browserstack.com/guide/get-current-url-in-selenium-and-python
- https://www.browserstack.com/guide/ui-automation-using-python-and-selenium#:~:text=A%20Detailed%20Guide-,UI%20Testing%20with%20Selenium%20and%20Python%3A%20Example,%2Dto%2Dend%20user%20process.
- https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python