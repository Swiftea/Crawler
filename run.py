from crawler.main import main


if __name__ == '__main__':
    crawler = main(url="https://github.io/", target_level=1)
    # crawler = main(l1=2, l2=3, dir_data='data1')
    crawler.start()
