def foo(a):
    if a < 5:
        return a


if __name__ == '__main__':
    s = []

    for i in range(10):
        if foo(i):
            s.append(foo(i))

    print(s)