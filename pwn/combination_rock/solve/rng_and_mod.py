import random

# used to generate the source code for ropchain.c.
if __name__ == "__main__":
    cnt = 1;
    MOD = int(1e9+7);
    lst_num = []
    lst_prod = []
    for i in range(200):
        cur = random.randint(1, 1000000000)
        lst_num.append(cur)
        print(f"bool pin{i}(int attempt){{\n\tif(PIN!={cnt}&&cnt!={i})\n\t\texit(0);\n\tPIN*=attempt;\n\tPIN%=MOD;\n\tcnt++;\n}}")
        cnt *= cur
        cnt %= MOD
        lst_prod.append(cnt)

    print(lst_num)
    print(lst_prod)
