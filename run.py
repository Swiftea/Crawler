from crawler.main import main


if __name__ == '__main__':
    c = main(url="https://github.io/", target_level=1)
    c.start()
