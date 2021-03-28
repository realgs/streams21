

def purchase_selling_diff(purchase_cost, selling_cost):
    result = round((1 - (selling_cost - purchase_cost) / purchase_cost), 3)
    return '{}{}'.format(result, " %")


print(purchase_selling_diff(2, 1))
