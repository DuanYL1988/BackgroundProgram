import itertools

# 人物和礼装 cost
servant_costs = [3, 4, 7, 12, 16]   # 1星到5星人物
ce_costs = [9, 12]                  # 仅4星和5星礼装

def best_fgo_team(max_cost, max_members):
    best_team = None
    best_cost = 0
    
    # 穷举所有人物组合 (最多 max_members 人)
    for num in range(1, max_members+1):
        print(f"level1 ->{num}/{max_members}")
        for servants in itertools.combinations_with_replacement(servant_costs, num):
            print(f"level2 ->{servants}")
            return
            # 穷举礼装分配 (每人0或1个礼装)
            ce_options = ce_costs + [None]
            for ces in itertools.product(ce_options, repeat=num):
                total = sum(servants) + sum(c for c in ces if c is not None)
                if total <= max_cost:
                    # 优先级: cost利用率 → 人数 → 高星人物 → 高星礼装
                    if (best_team is None or
                        total > best_cost or
                        (total == best_cost and len(servants) > len(best_team[0])) or
                        (total == best_cost and len(servants) == len(best_team[0]) and sum(servants) > sum(best_team[0])) or
                        (total == best_cost and len(servants) == len(best_team[0]) and sum(servants) == sum(best_team[0]) and sum(c for c in ces if c) > sum(c for c in best_team[1] if c))):
                        best_team = (servants, ces)
                        best_cost = total
    
    return best_team, best_cost

# 示例：最大 cost = 115
if __name__ == "__main__":
    max_cost = 115
    # 两个5星人物礼装固定了
    max_cost = 115 - 56
    best_fgo_team(max_cost, max_members=3)
    '''
    team, total_cost = best_fgo_team(max_cost, max_members=3)
    for i, (s, ce) in enumerate(zip(team[0], team[1]), 1):
        print(f"人物{i}: cost={s}, 礼装={ce}")
    print("总cost:", total_cost)
    print("利用率:", round(total_cost/max_cost*100, 2), "%")
    '''
