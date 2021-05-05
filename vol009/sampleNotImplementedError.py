# -*- coding: utf-8 -*-

# カスタムの親クラス
class NotImplementedErrorTest(object):
    def hogehoge(self):
        raise NotImplementedError()

# カスタムの子クラスその１
class Test1(NotImplementedErrorTest):
    def hogehoge(self):
        print('hogehoge')

# カスタムの子クラスその２
class Test2(NotImplementedErrorTest):
    pass


if __name__ == "__main__":
    test1 = Test1()
    test1.hogehoge()

    test2 = Test2()
    test2.hogehoge()