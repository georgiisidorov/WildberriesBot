import os
import glob

def recompile():
	list_accs = glob.glob(r'.\acc*_completed')
	numbers_accs = sorted([int(i[(i.index('acc')+3):i.index('_')]) for i in list_accs])
	numbers_generated = [i for i in range(1, numbers_accs[-1] + 1)]
	len_accs = len(numbers_accs)
	num = set(numbers_generated)
	num.difference_update(set(numbers_accs))
	for number in list(num):
		if number < len_accs:
			os.rename(f'.\acc{numbers_accs[-1]}_completed', f'.\acc{number}_completed')
			numbers_accs.remove(numbers_accs[-1])

def recompile_auto(number, list_accs):
	os.rename(list_accs[-1].path, list_accs[number-1].path)


