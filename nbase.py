def nbase(x: str | int | float, ibase=10, obase=10, accuracy=10, point="."):

    def get_fraction(x): return x - int(x)

    alphabet = [chr(c) for c in range(0x30, 0x3a)] + \
        [chr(c)for c in range(0x41, 0x5b)] + \
        [chr(c) for c in range(0x61, 0x7b)]

    if ibase > 62 or ibase < 1:
        raise ValueError("input base in disallowed range")
    if obase > 62 or obase < 1:
        raise ValueError("output base in disallowed range")
    if accuracy < 0:
        raise ValueError("accuracy less then zero")

    num = 0
    fraction = 0
    sign = 1
    match x:
        case float() | int():
            num = x
            sign = 1 if num > 0 else -1
        case str():
            if x[0] == "-":
                sign = -1
                x = x[1:]
            if ibase <= 36:
                x = x.lower()
            if point in x:
                x, fraction = x.split(point, 1)
            i = 0
            for c in x[::-1]:
                num += alphabet.index(c) * ibase**i
                i += 1
            if fraction:
                i = -1
                for c in fraction:
                    num += alphabet.index(c) * ibase**i
                    i -= 1
            num *= sign
        case _:
            raise TypeError("x argument type is not allowed")

    num = abs(num)
    s = ""
    if obase == 10:
        return num*sign
    integer = int(num)
    fraction = get_fraction(num)
    if integer == 0:
        s = "0"
    while integer:
        s += alphabet[integer % obase]
        integer //= obase
    if fraction:
        s += point
        i = 0
        while i < accuracy:
            fraction *= obase
            s += alphabet[int(fraction)]
            fraction = get_fraction(fraction)
            i += 1
    if sign == -1:
        s = "-" + s
    s = s.rstrip("0")
    return s


if __name__ == "__main__":
    nums = [173,16.7,329,71.2,629,]
    obases = [2,8,16]
    print(f"{"dec":<10}{"bin":<15}{"oct":<10}{"hex":<10}")
    for num in nums:
        print(f"{num:<10}{nbase(num,obase=2,accuracy=4):<15}{nbase(num,obase=8,accuracy=4):<10}{nbase(num,obase=16,accuracy=4):<10}")
