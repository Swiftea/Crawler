from crawler.main import main


if __name__ == '__main__':
    c = main(url="https://swiftea.yo.fr/", target_level=2)
    c.start()
