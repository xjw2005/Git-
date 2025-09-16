import pprint
from crawlers.single_crawler import single_crawler


if __name__ == '__main__':
    result = single_crawler("AX1800pcie网卡是intel还是联发科的？")
    pprint.pprint(result)
