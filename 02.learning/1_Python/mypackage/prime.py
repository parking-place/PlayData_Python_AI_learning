
# 소수 리스트
prime_num = [2, 3, 5, 7]
# 체크한 수의 최대값
check_max = 4

# 에라토스테네스의 체
def eratosthenes_shecker(num : int, *, from_is_prime : bool = True) -> None:
    """
    에라토스테네스의 체를 이용하여 소수 리스트를 만드는 함수
    Args:
        num (type[int]): 이 수의 제곱근보다 작은 모든 소수를 구함
        
        from_is_prime (bool, optional): num이 is_prime 함수에서 호출되었는지 확인. Defaults to True.
    """
    global check_max
    n_min = 2
    
    # 받은 값이 체 범위내에 있을 경우
    if num <= prime_num[-1] :
        return
    
    if from_is_prime :
        # 모든 수는 자신의 제곱근보다 큰 소인수를 가지지 못함
        n_max = int(num**0.5)+1
    else :
        # 어떤 수 보다 작은 소수를 구해두는 경우
        n_max = num + 1

    
    if num > check_max :
        # 소수 리스트에 이후 숫자들을 추가
        ex_l = list(range(prime_num[-1]+1,n_max))
        ex_l = [v for v in ex_l if (v % 2 != 0) and (v % 3 != 0)]
        prime_num.extend(ex_l)
        check_max = num
    else :
        return
    
    # print(prime_num)
    
    # '소수판별 체' 알고리즘
    for i in prime_num:
        for j in prime_num:
            if i == j:
                continue
            if 0==(j%i):
                prime_num.remove(j)
    return

# 소수 판별
def is_prime(num : int) -> bool :
    """
    소수 판별 함수
    Args:
        num (type[int]): 소수인지 확인 할 숫자

    Returns:
        bool: 소수이면 True, 아니면 False
    """
    result = True
    
    # 소수 리스트에 있는지 먼저 확인
    if num <= prime_num[-1] :
        if num in prime_num :
            return True
        else :
            return False

    # 체크해본 수보다 num이 크면 에라토스테네스의 체를 이용하여 소수 리스트를 만듬
    if num > check_max :
        eratosthenes_shecker(num)
    
    # 소수 리스트중 나누어 떨어지는 수가 있으면 소수가 아님
    for v in prime_num :
        if num % v == 0 :
            result = False
            break
    
    return result
        
def prime_generator(start = 2 ,*, end = 0):
    # start ~ end 사이의 소수를 생성하는 제너레이터 함수
    # start를 생략하면 2부터 소수를 생성하는 제너레이터 함수
    # end를 생략하면 start ~ 무한대 사이의 소수를 생성하는 제너레이터 함수
    
    i = start
    while True:
        if end != 0 and i > end:
            break
        
        if is_prime(i):
            yield i
        
        i += 1
