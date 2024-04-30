import shutil

def delete_acc(number):
	shutil.rmtree(f'.\acc{number}_completed')