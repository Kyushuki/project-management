import pulp

# Эксперты и задачи
experts = [1, 2, 3]
tasks = [1, 2, 3, 4, 5, 6]

# Оценки (сложность, желание) для каждого эксперта по каждой задаче
scores = {
    1: {1: (4, 9), 2: (5, 5), 3: (5, 6), 4: (6, 7), 5: (5, 8), 6: (6, 7)},
    2: {1: (2, 9), 2: (6, 4), 3: (4, 6), 4: (4, 7), 5: (3, 7), 6: (3, 8)},
    3: {1: (3, 9), 2: (7, 5), 3: (6, 4), 4: (4, 8), 5: (8, 4), 6: (3, 8)}
}

alpha = 0.5 # штраф за сложность

# Полезность u_ij = желание - alpha * сложность
utility = {}
for i in experts:
    for j in tasks:
        diff, desire = scores[i][j]
        utility[(i, j)] = desire - alpha * diff

# Модель
prob = pulp.LpProblem("Task_Assignment", pulp.LpMaximize)

# Переменные x_ij
x = pulp.LpVariable.dicts("x", (experts, tasks), cat="Binary")

# Целевая функция
prob += pulp.lpSum(utility[(i, j)] * x[i][j] for i in experts for j in tasks)

# Ограничение: каждая задача ровно одному эксперту
for j in tasks:
    prob += pulp.lpSum(x[i][j] for i in experts) == 1

# Ограничение: не более 2 задач на эксперта
for i in experts:
    prob += pulp.lpSum(x[i][j] for j in tasks) <= 2

# Решение
prob.solve(pulp.PULP_CBC_CMD(msg=False))

print("Статус:", pulp.LpStatus[prob.status])
print("\nНазначения:")
for i in experts:
    assigned = [j for j in tasks if pulp.value(x[i][j]) > 0.5]
    print(f"Эксперт {i}: задачи {assigned}")

print("\nЗначение целевой функции:", pulp.value(prob.objective))
