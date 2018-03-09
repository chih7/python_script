import chrome_driver
from multiprocessing import Pool

p = Pool()
p.apply_async(chrome_driver.chrome_driver, args=("https://s.taobao.com/search?q=%E6%96%B0%E5%93%81",))
p.apply_async(chrome_driver.chrome_driver, args=("https://s.taobao.com/search?q=%E6%AF%9B%E8%A1%A3",))

p.close()
p.join()
