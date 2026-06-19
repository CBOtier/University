def count_ways(m, coins):
    dp = [0] * (m + 1)
    dp[0] = 1
    for coin in coins:
        for amount in range(coin, m + 1):
            dp[amount] += dp[amount - coin]
    
    return dp[m]



m = int(input())  
n = int(input())  
coins = list(map(int, input().split())) 

result = count_ways(m, coins)
print(result)


# Примеры для проверки:
# Пример 1: m=5, n=3, coins=[3,2,1] → ответ 5
# Пример 2: m=3, n=2, coins=[2,1] → ответ 2
# Пример 3: m=8, n=1, coins=[5] → ответ 0
