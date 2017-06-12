#!/usr/bin/python3
import configparser
import atpic.log
xx=atpic.log.setmod("INFO","getconfig")


def parse_config():
    yy=atpic.log.setname(xx,'parse_config')
    
    config=configparser.ConfigParser()
    config.read('config.ini')
    config_array=config.defaults()
    atpic.log.debug(yy,config_array)
    return config_array



if __name__ == "__main__":
    config_array=parse_config()
    print(config_array)
