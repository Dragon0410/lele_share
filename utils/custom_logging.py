# /usr/bin python3
# -*- encoding:utf-8 -*-
# create date: 2023/8/27
# create time: 13:21
# create author: 93207
# desc: 基于系统 logging 的log方法

import sys
import traceback


def main():
    try:
        pass
    except Exception as e:
        traceback.print_exc()
    finally:
        print("程序结束")
        sys.exit()


if __name__ == "__main__":
    main()
