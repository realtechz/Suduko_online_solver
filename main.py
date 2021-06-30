from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import numpy as np
import time

global driver
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 0,
    "profile.default_content_setting_values.notifications": 1
})
grid = []
mat = []
row = [0, 0, 0, 0, 0, 0, 0, 0, 0]

URL = "https://www.soduko-online.com/"
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt, service_log_path='Nul')
driver.get(URL)

def possible(y, x, n):
    for i in range(0, 9):
        if grid[i][x] == n and i != y:
            return False
    for i in range(0, 9):
        if grid[y][i] == n and i != x:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for X in range(x0, x0 + 3):
        for Y in range(y0, y0 + 3):
            if grid[Y][X] == n:
                return False
    return True


def solve():
    global grid
    global mat
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0
                return
    print(np.matrix(grid))
    for x in range(9):
        for y in range(9):
            id_mat = "vc_" + str(y) + "_" + str(x)
            id_2 = "c_" + str(y) + "_" + str(x)
            value = driver.find_element_by_id(id_mat)
            if driver.find_element_by_id(id_mat).text == '':
                driver.execute_script('arguments[0].innerText = "%s"' % (grid[x][y]), value)
                click_number = grid[x][y]
                id = "M" + str(click_number)


while True:

    for x in range(9):
        for y in range(9):
            id_mat = "c_" + str(y) + "_" + str(x)
            if driver.find_element_by_id(id_mat).text != '':
                row[y] = int(driver.find_element_by_id(id_mat).text)

        grid.append(row)

        row = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # print(np.matrix(grid))
    solve()
    time.sleep(15)
    grid = []
    driver.get(URL)
