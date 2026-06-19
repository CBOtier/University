def backtrack(candidates, target, start, current_sum):
    if current_sum == target:
        return True
    
    if current_sum > target or start == len(candidates):
        return False
    
    for i in range(start, len(candidates)):
        if backtrack(candidates, target, i + 1, current_sum + candidates[i]):
            return True
    
    return False


n, k = map(int, input().split())
a = list(map(int, input().split()))

if backtrack(a, k, 0, 0):
    print("Да")
else:
    print("Нет")


# Пример:
# 4 10
# 1 2 3 4
# Ответ: Да 
