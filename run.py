import sys
import gspread

from cardHolder import cardHolder

from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("client_database")


# client = SHEET.worksheet('client')

# cardNumber = client.col_values(1)
# print(cardNumber)
# pin = client.col_values(2)
# print(pin)
# name = client.col_values(3)
# print(name)
# surename = client.col_values(4)
# print(surename)
# balance = client.col_values(5)
# print(balance)


print(
    """
                    ░█████╗░████████╗███╗░░░███╗
                    ██╔══██╗╚══██╔══╝████╗░████║
                    ███████║░░░██║░░░██╔████╔██║
                    ██╔══██║░░░██║░░░██║╚██╔╝██║
                    ██║░░██║░░░██║░░░██║░╚═╝░██║
                    ╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░░░░╚═╝
                   """
)



def print_menu():
  # Print options to the user
  print("Please chose from one of the follewing options...")
  print("1. Deposit")
  print("2. Withdraw")
  print("3. Show Balance")
  print("4. Exit")

 
  while True:
    try:
      option = input("Enter option: ")
      if not option:
        raise ValueError("Enter a value")
      if not option.isnumeric() or not option in [1, 2, 3, 4]:
        raise ValueError("Invalid input")
      if option in ['1', '2', '3', '4']:
        break
    except ValueError as e_r:
      print(f"{e_r}")
  return option

# print("Your current balance is: €", current_user[-1])

# if __name__ == "__main__":
#   current_user = cardHolder("","","","","")

def validate_card_Num():
    list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
    while True:
      card_num = input("\nEnter card number: ")
      user = [ holder for holder in list_of_cardHolders if card_num == holder[0]]
      if card_num and len(user) > 0:
        break
      elif not card_num:
        print("Please enter card number")
      else:
        print("Card number not recognized")
    return cardHolder(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4])

def validate_user(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  tries = 0
  while tries < 3:
    tries += 1
    pin_code = input("\nEnter PIN: ")
    if not pin_code:
      print("please enter pin, try again")
      status = False
    elif not pin_code.isnumeric():
      print("Only numbers allowed")
      status = False
    elif pin_code.isnumeric() and pin_code == user[0][1]:
      status = True
      break
    elif tries == 3:
      print("Sorry you've exceede you trial limit")
      status = False
      break
    else:
      print("Incorrect pin.")
      status = False
    
  return status


def deposit(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  while True:
    amount = input("Enter amount: ")
    if not amount:
      print("Please enter an amount, try again.")
      status = False
    elif not amount.isnumeric():
      print("Enter only amount in figures.")
      status = False
    else:
      status = True
      new_balance = float(cardHolder.get_balance()) + float(amount)
      cardHolder.set_balance(new_balance)
      cur_user = SHEET.worksheet('client').find(user[0][0])
      SHEET.worksheet('client').update_cell(cur_user.row, 5, new_balance)
      print("Successfully deposited to account.")
      break
  return True

def withdraw(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  while True:
    amount = input("Enter amount: ")
    if not amount:
      print("Please enter an amount you would like to withdraw, try again.")
      status = False
    elif not amount.isnumeric():
      print("Enter only amount in figures.")
      status = False
    elif float(cardHolder.get_balance()) < float(amount):
      print("Insoffician balance. Try again.")
      status = False

    else:
      status = True
      new_balance = float(cardHolder.get_balance()) - float(amount)
      cardHolder.set_balance(new_balance)
      cur_user = SHEET.worksheet('client').find(user[0][0])
      SHEET.worksheet('client').update_cell(cur_user.row, 5, new_balance)
      print("Successfully withdraw from your account.")
      break
  return True


def show_balance(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  return user[0][-1]

def show_user_name(cardHolder):
  list_of_cardHolders = SHEET.worksheet("client").get_all_values()[1:]
  user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
  return user[0][2]
  

# def withdraw(cardHolder):
#   try:
#     withdraw = float(input("How much € would you like to withdraw:\n "))
#     #Chkesk if user has enough mony
#     if(cardHolder.get_balance() < withdraw):
#       print("Insufficient balance :(")
#     else:
#       cardHolder.set_balance(cardHolder.get_balance() - withdraw)
#       print("You're good to go! Thank you :)")
#   except:
#     print("Invalit input")

# def check_balance(cardHolder):
#   list_of_cardHolders = SHEET.worksheet('client').get_all_values()[1:]
#   current_user = [holder for holder in list_of_cardHolders if cardHolder.get_cardNum() == holder[0]]
#   print(f"Your balance is {current_user[-1]}")
# # get data fro spreadsheet
# data = client.worksheet('client').get_all_values()[1:]
# print(data)
#   #Prompt user for debit card number
#   # debitCardNum = ""
current_user = validate_card_Num()
# print(current_user)
print(validate_user(current_user))
print(show_balance(current_user))


print("Welcome", show_user_name(current_user), ":)")
while True:
  p = int(print_menu())
  if p == 1:
    deposit(current_user)
  if p == 2:
    withdraw(current_user)
  if p == 3:
    show_balance(current_user)
  if p == 4:
    sys.exit()




# while True:
#   print_menu()
#   try:
#     option = int(input())
#   except ValueError:
#     print("Invalid input. Please try again.")
#   if option == 1:
#     deposit(current_user)
#   elif option == 2:
#     withdraw(current_user)
#   elif option == 3:
#     show_balance(current_user)
#   elif option == 4:
#     break
#   else:
#     option = 0
# print("\nThank you. Have a nice day :)")

# deposit(current_user)
# withdraw(current_user)
# option = 0
# while True:
#   print_menu()
#   try:
#     option = int(input())
#   except:
#     print("Invalid input. Please try again.")

#     if (option == 1):
#       deposit(current_user)
#     elif (option == 2):
#       withdraw(current_user)
#     elif (option == 3):
#       check_balance(current_user)
#     elif (option == 4):
#       break
#     else:
#       option = 0

# print("\nThank you. Have a nice day :)")

# data = SHEET.worksheet('client').get_all_values()[1:]
# print(data)
