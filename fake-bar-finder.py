from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class FakeCoinFinderTest:
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
        # output variables
        self.weighed_times = 0
        self.weighed_history = []
        self.alert = None
        pass

    def input_coins(self, coins:list[str], bowl_boxes:list[object]):
        # check if # coins > # gameboard boxes?
        for i in range(len(coins)):
            bowl_boxes[i].send_keys(coins[i])

    def reset_gameboards(self, use_btn:bool=True):
        # use the reset button
        if use_btn:
            self.reset_btn.click()
        # extend to setting all values in gameboards to None if wanted

# handle chrome, safari, edge, etc?
if __name__ == "__main__":
    test = FakeCoinFinderTest()
    # first get the website contents
    test.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # make this optional

    test.driver.maximize_window()

    test.wait = WebDriverWait(test.driver, 60)

    test.driver.get('http://sdetchallenge.fetch.com/')

    test.wait.until(EC.url_to_be('http://sdetchallenge.fetch.com/'))

    coin_elements = test.driver.find_element(By.CLASS_NAME, "coins").find_elements(By.CLASS_NAME, "square")
    # create a dict for associating coin number with element
    coins_elements_dict = { coin.text:coin for coin in coin_elements }
    test.gameboards = test.driver.find_elements(By.CLASS_NAME, "game-board")
    test.gb_left, test.gb_right = [], []
    for gameboard in test.gameboards:
        for box in gameboard.find_elements(By.TAG_NAME, 'input'):
            if box.get_attribute('data-side') == 'left':
                test.gb_left.append(box)
            elif box.get_attribute('data-side') == 'right':
                test.gb_right.append(box)
            else:
                pass # handle however
    test.gb_left.sort(key=lambda element: element.get_attribute('data-index'))
    test.gb_right.sort(key=lambda element: element.get_attribute('data-index'))
    result_grp = test.driver.find_element(By.CLASS_NAME, 'result')
    result_btn = result_grp.find_element(By.XPATH, '//button[@id="reset"]')
    reset_btn = None
    for btn in test.driver.find_elements(By.ID, 'reset'):
        if btn != result_btn:
            reset_btn = btn
            break # this is not ideal if there is another "reset_btn" introduced
    # check if reset_btn is None?
    weigh_btn = test.driver.find_element(By.ID, 'weigh')
    game_info = test.driver.find_element(By.CLASS_NAME, 'game-info') # get the weighings from li elements inside
    # run actual program
    # split the coins into buckets
    buckets = []
    coins_keys = list(coins_elements_dict.keys())
    for i in range(0, len(coins_keys), 3):
        buckets.append([coins_keys[i], coins_keys[i+1], coins_keys[i+2]])
    # loop this until bucket size = 1
    weighed_times, weighed_history = 0, []
    while len(buckets) > 1:
        # input 3 elements into left
        test.input_coins(buckets[0], test.gb_left)
        # input 3 elements into right
        test.input_coins(buckets[1], test.gb_right)
        # get number of li's in game-info
        pre = len(game_info.find_elements(By.TAG_NAME, 'li'))
        # press weigh
        weigh_btn.click()
        weighed_times += 1
        # test.wait until li populates
        test.wait.until(lambda d: len(game_info.find_elements(By.TAG_NAME, 'li')) > pre)
        output = game_info.find_elements(By.TAG_NAME, 'li')[-1].text
        weighed_history.append(output)
        # handle these cases:
        # l == r
        if "=" in output:
            buckets = buckets[2]
        # l > r
        # r contains the fake
        elif ">" in output:
            buckets = buckets[1]
        # l < r
        # l contains the fake
        elif "<" in output:
            buckets = buckets[0]
        if len(buckets) == 1:
            coins_elements_dict[buckets[0]].click()
            print(f'Alert message: {test.driver.switch_to.alert.text}')
            print(f'Number of times weighed: {weighed_times}')
            print(f'List of weighing made: {weighed_history}')
        else:
            pre = test.gb_left[0].get_attribute('value')
            print(pre)
            reset_btn.click()
            # test.wait until grid empties
            test.wait.until(lambda d: test.gb_left[0].get_attribute('value') != pre)
    # done
