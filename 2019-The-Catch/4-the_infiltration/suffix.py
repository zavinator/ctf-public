
def main():
	if sys.version_info[0] < 3:
		print("ERROR: Python3 required.")
		exit(1)
	init_number = get_args()
	print("Your B-code: {}".format(convert(init_number)))

main()
