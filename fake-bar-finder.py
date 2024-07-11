from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import sys

class FakeCoinFinderTest:
    # creates a test class with all relevant webelements and test variables
    def __init__(self, driver=None, wait=None, coin_elements_dict=None, gb_left=None, 
                 gb_right=None, reset_btn=None, result_btn=None, weigh_btn=None, game_info=None) -> None:
        # test variables
        self.driver = driver
        self.wait = wait
        self.coin_elements_dict = coin_elements_dict
        self.gb_left = gb_left
        self.gb_right = gb_right
        self.reset_btn = reset_btn
        self.result_btn = result_btn
        self.weigh_btn = weigh_btn
        self.game_info = game_info
        self.buckets = []
        # output variables
        self.weighed_times = 0
        self.weighed_history = []
        self.alert = None
        pass

    # inputs the numbers into the gameboard elements
    def input_coins(self, coins:list[str], bowl_boxes:list[object]):
        # check if # coins > # gameboard boxes?
        for i in range(len(coins)):
            bowl_boxes[i].send_keys(coins[i])

    # resets the gameboards (using reset_btn)
    # extend to setting all gameboard values to None if wanted
    def reset_gameboards(self, use_btn:bool=True):
        # use the reset button
        if use_btn:
            self.reset_btn.click()
        # extend to setting all values in gameboards to None if wanted

    # algorithm to solve for the fake coin/bar
    def run(self):
        # split the coins into buckets
        coins_keys = list(self.coin_elements_dict.keys())
        for i in range(0, len(coins_keys), 3):
            self.buckets.append([coins_keys[i], coins_keys[i+1], coins_keys[i+2]])
        # loop this until bucket size = 1
        while len(self.buckets) > 1:
            # input 3 elements into left (can randomize board elements)
            test.input_coins(self.buckets[0], test.gb_left)
            # input 3 elements into right (can randomize board elements)
            test.input_coins(self.buckets[1], test.gb_right)
            # get number of li's in game-info
            pre = len(self.game_info.find_elements(By.TAG_NAME, 'li'))
            # press weigh
            self.weigh_btn.click()
            self.weighed_times += 1
            # test.wait until li populates
            self.wait.until(lambda d: len(self.game_info.find_elements(By.TAG_NAME, 'li')) > pre)
            output = self.game_info.find_elements(By.TAG_NAME, 'li')[-1].text
            self.weighed_history.append(output)
            # handle these cases:
            # l == r
            if '=' in output:
                self.buckets = self.buckets[2]
            # l > r
            # r contains the fake
            elif '>' in output:
                self.buckets = self.buckets[1]
            # l < r
            # l contains the fake
            elif '<' in output:
                self.buckets = self.buckets[0]
            if len(self.buckets) == 1:
                self.coin_elements_dict[self.buckets[0]].click()
                print(f'Alert message: {self.driver.switch_to.alert.text}')
                print(f'Number of times weighed: {self.weighed_times}')
                print(f'List of weighing made: {self.weighed_history}')
            else:
                pre = self.gb_left[0].get_attribute('value')
                self.reset_btn.click()
                # test.wait until grid empties, check one only, can check all
                self.wait.until(lambda d: self.gb_left[0].get_attribute('value') != pre)
        # done
    
    # close out the test, ready for another iteration
    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    iterations = 1
    if len(sys.argv) > 1:
        # assume the first given arg is number of iterations
        iterations = int(float(sys.argv[1]))
    for i in range(iterations):
        # first get the website contents
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # make this optional

        driver.maximize_window()

        wait = WebDriverWait(driver, 60)

        driver.get('http://sdetchallenge.fetch.com/')

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'game-board')))

        coin_elements = driver.find_element(By.CLASS_NAME, 'coins').find_elements(By.CLASS_NAME, 'square')
        # create a dict for associating coin number with element
        coins_elements_dict = { coin.text:coin for coin in coin_elements }
        gameboards = driver.find_elements(By.CLASS_NAME, 'game-board')
        gb_left, gb_right = [], []
        for gameboard in gameboards:
            for box in gameboard.find_elements(By.TAG_NAME, 'input'):
                if box.get_attribute('data-side') == 'left':
                    gb_left.append(box)
                elif box.get_attribute('data-side') == 'right':
                    gb_right.append(box)
                else:
                    pass # handle however
        gb_left.sort(key=lambda element: element.get_attribute('data-index'))
        gb_right.sort(key=lambda element: element.get_attribute('data-index'))
        result_grp = driver.find_element(By.CLASS_NAME, 'result')
        result_btn = result_grp.find_element(By.XPATH, '//button[@id="reset"]')
        reset_btn = None
        for btn in driver.find_elements(By.ID, 'reset'):
            if btn != result_btn:
                reset_btn = btn
                break # this is not ideal if there is another 'reset_btn' introduced
        # check if reset_btn is None?
        weigh_btn = driver.find_element(By.ID, 'weigh')
        game_info = driver.find_element(By.CLASS_NAME, 'game-info') # get the weighings from li elements inside
        test = FakeCoinFinderTest(driver=driver, wait=wait, coin_elements_dict=coins_elements_dict,
                                gb_left=gb_left, gb_right=gb_right, reset_btn=reset_btn, 
                                result_btn=result_btn, weigh_btn=weigh_btn, game_info=game_info)
        # run actual program
        test.run()
        # close
        test.close()
