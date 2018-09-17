import os

class ChineseN:
	CN = ['零','一','二','三','四','五','六','七','八','九']
	N = {ch:i for ch, i in zip(CN, range(10))}


def sort_and_rename(path_in):
	count = 0
	files = os.listdir(path_in)
	for file in files:
		if file[0] == '第':
			count += 1
			if ' ' in file:
				chapter_i, chapter_name = file.split(' ', 1)
			else:
				chapter_i, chapter_name = os.path.splitext(file)
			chapter_i_new = ""
			for c in chapter_i:
				if c in ChineseN.N:
					chapter_i_new += str(ChineseN.N[c])
			new_name = chapter_i_new.zfill(3) + ' ' + chapter_name
			os.rename(os.path.join(path_in, file), os.path.join(path_in, new_name))
	print("number of files:", count)

if __name__ == "__main__":
	path_in = "../res/佛本是道"
	sort_and_rename(path_in)