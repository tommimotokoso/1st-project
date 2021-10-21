money = input("введите сумму вашего депозита:")
money = int(money)

per_cent = {'TKB': 5.6, 'SKB': 5.9, 'VTB': 4.28, 'SBER': 4.0}

TKB1 = per_cent['TKB'] * money / 100
SKB1 = per_cent['SKB'] * money / 100
VTB1 = per_cent['VTB'] * money / 100
SBER1 = per_cent['SBER'] * money / 100

list_1year = [TKB1, SKB1, VTB1, SBER1]

deposit = max(list_1year)

print("Накопленные денежные средства за год в TKB:", TKB1)
print("Накопленные денежные средства за год в SKB:", SKB1)
print("Накопленные денежные средства за год в VTB:", VTB1)
print("Накопленные денежные средства за год в SBER:", SBER1)

print ("Максимальный годовой заработок:", deposit)
