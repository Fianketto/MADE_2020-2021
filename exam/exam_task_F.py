set_count = int(input())

for set_n in range(set_count):
    needed_meal = {}
    ing_cnt_for_meals = {}
    recipe = {}
    fridge_has = {}

    needed_ing = {}
    needed_ing_final = {}

    N, K, F = list(map(int, input().split(" ")))
    for i in range(N):
        a = input().split(" ")
        needed_meal[a[0]] = needed_meal.get(a[0], 0) + int(a[1])

    for i in range(K):
        a = input().split(" ")
        meal_name = a[0]
        ing_cnt_for_meal = int(a[1])
        ing_cnt_for_meals[a[0]] = ing_cnt_for_meals.get(a[0], 0) + ing_cnt_for_meal
        recipe[a[0]] = {}

        for j in range(ing_cnt_for_meal):
            b = input().split(" ")
            recipe[a[0]][b[0]] = int(b[1])

    for i in range(F):
        c = input().split(" ")
        fridge_has[c[0]] = int(c[1])


    # print("needed meal: ", needed_meal)
    # print("ing for meals: ", ing_cnt_for_meals)
    # print("recipe: ", recipe)
    # print("fridge: ", fridge_has)

    def calc_ing_count_for(Tmeal, Tcnt):
        for ing in recipe[Tmeal].keys():
            if ing not in recipe.keys():
                needed_ing[ing] = needed_ing.get(ing, 0) + Tcnt * recipe[Tmeal][ing]
            else:
                calc_ing_count_for(ing, Tcnt * recipe[Tmeal][ing])


    for meal in needed_meal.keys():
        needed_meal_count = needed_meal[meal]
        calc_ing_count_for(meal, needed_meal_count)

    for ing in needed_ing.keys():
        if ing in fridge_has.keys():
            real_needed_ing = max(0, needed_ing.get(ing) - fridge_has.get(ing))
            if real_needed_ing > 0:
                needed_ing_final[ing] = real_needed_ing
        else:
            needed_ing_final[ing] = needed_ing[ing]

    # print("needed_ing: ", needed_ing)
    # print("real needed: ", needed_ing_final)

    for i, j in sorted(needed_ing_final.items()):
        print(i, j)
