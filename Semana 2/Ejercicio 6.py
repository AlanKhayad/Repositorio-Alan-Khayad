option=int(input("Please enter a valid option: \n1- Vegetarian\n2- Non vegetarian\n->"))

if option==1:
    ingredient=int(input("Please enter a valid option: \n1- Pimiento\n2- Tofu\n->"))
    if ingredient==1:
        ingredient="Pimiento"
    else:
        ingredient="Tofu"

if option==2:
    ingrediente=int(input("Please enter a valid option: \n1- Pepperoni\n2- Jamon\n->"))

else:
    print("Invalid option")