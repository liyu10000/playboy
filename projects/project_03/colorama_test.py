from colorama import init, Fore, Back, Style

# for windows os
init(convert=True)
# # for ubuntu os
# init()

a = [1, 23, 23.5]
print(Fore.GREEN + "some green text")
print(Fore.BLUE + "some blue text" + Fore.WHITE)
print("some red text", a)