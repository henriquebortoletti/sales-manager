import re
import uuid
import csv

registered_sellers = {"seller_1": [],
                      "seller_2": [],
                      "seller_3": [],
                      "seller_4": [],
                      "seller_5": []}
DATE_PATTERN = r"^\d\d-\d\d-\d\d\d\d"
SALE_PATTERN = "Seller name | Customer name | Date of sale (mm-dd-yyy) | Sale item name | Sale value in dollar"
ID = 0
SELLER_NAME = 1
CUSTOMER_NAME = 2
SALE_DATE = 3
SALE_ITEM_NAME = 4
SALE_VALUE = 5


def execute_option(option):
    if option not in options:
        print("Not in the option's list :(")
    else:
        options[option][0]()


def register_sale():
    sale = input("Let's register a sale! Example of sale input:\n"
                 "seller_1 | customer_1 | 01-01-2021 | mask | 10\n"
                 "Sale input pattern:\n" + SALE_PATTERN + "\n")
    if sale_validate_and_save([x.strip() for x in sale.split('|')]):
        list_sales()
    else:
        again = input("The input is not in the sale's pattern\n"
                      "Do you want to try again? (Yes/No)\n").strip().lower()[0]
        if again == 'y':
            register_sale()


def sale_validate_and_save(sale, id=None):
    if id is None:
        id = uuid.uuid4().hex[0:8]
    sale.insert(ID, id)
    if validate_sale(sale):
        save_sale(sale)
        return True
    else:
        return False


def validate_sale(sale):
    return len(sale) == 6 and sale[SELLER_NAME] in registered_sellers.keys() and re.match(DATE_PATTERN, sale[SALE_DATE]) \
           and is_float(sale[SALE_VALUE])


def save_sale(sale):
    registered_sellers[sale[SELLER_NAME]].append(sale)


def is_float(str):
    try:
        float(str)
        return True
    except:
        return False


def register_sales_from_csv():
    csv_files_path = input("Register sales from csv files.\n"
                           "The csv files must have the \\t as delimiter and must follow the sale pattern:\n" + SALE_PATTERN + "\n" +
                           "The first line of the csv file is the header with the identification of the columns.\n"
                           "Enter the csv file paths separated by comma, for example: filepath1, filepath2, filepath3\n"
                           "Enter here:")
    for csv_file in csv_files_path.split(','):
        save_rows(csv_file)


def save_rows(csv_file_path):
    try:
        with open(csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    sale_validate_and_save(row)
                line_count += 1
                list_sales()
    except FileNotFoundError:
        print("File not found exception: " + csv_file_path)
        print("Please enter a valid file path!")



def edit_sale():
    sale_id = input("What is the sale ID to edit?")
    seller, index = sale_index(sale_id)
    if index != -1:
        print("Edit sale:")
        sale_row_presentation(registered_sellers[seller][index])
        sale = input("Re-enter the sale with the edits according to the sale's pattern:\n" + SALE_PATTERN + "\n")
        sale_validate_and_save([x.strip() for x in sale.split('|')], sale_id)
        list_sales()
    else:
        print("Sale with ID " + sale_id + " not registered")


def remove_sale():
    sale_id = input("What is the sale ID to remove?")
    seller, index = sale_index(sale_id)
    if index != -1:
        del registered_sellers[seller][index]


def sale_index(sale_id):
    for seller in registered_sellers:
        i = 0
        for sale in registered_sellers[seller]:
            if sale_id in sale[ID]:
                return seller, i
            i += 1
    return -1, -1


def list_sales():
    print("Sales list ranked by sellers with the highest amount sold.\n"
          "Sale ID  |  Seller Name  |  Customer Name  |  Sale Date  |  Sale Item Name  |  Sale Value\n"
          "==========================================================================================")
    for seller in sorted_sellers():
        for sale in registered_sellers[seller[0]]:
            sale_row_presentation(sale)


def sorted_sellers():
    sellers_sell_amount = {}
    for seller in registered_sellers:
        sellers_sell_amount.update({seller: 0})
        for sale in registered_sellers[seller]:
            sellers_sell_amount[seller] += float(sale[SALE_VALUE])
    return sorted(sellers_sell_amount.items(), key=lambda x: x[1], reverse=True)


def sale_row_presentation(sale):
    sale_presentation = adjust_str_size(sale[ID], 9) + '|'
    sale_presentation += adjust_str_size(sale[SELLER_NAME], 15) + '|'
    sale_presentation += adjust_str_size(sale[CUSTOMER_NAME], 17) + '|'
    sale_presentation += adjust_str_size(sale[SALE_DATE], 13) + '|'
    sale_presentation += adjust_str_size(sale[SALE_ITEM_NAME], 18) + '|'
    sale_presentation += '$ ' + sale[SALE_VALUE]
    print(sale_presentation)


def adjust_str_size(str, size):
    if len(str) < size:
        return '{message: <{width}}'.format(message=str, width=size)
    if len(str) > size:
        return str[:size]
    return str


def export_to_csv():
    csv_filename = input("Whats the csv filename?")
    with open(csv_filename, mode='w') as employee_file:
        writer = csv.writer(employee_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Seller Name', 'Customer Name', 'Sale Date', 'Sale Item Name', 'Sale Value'])
        for seller in sorted_sellers():
            for sale in registered_sellers[seller[0]]:
                writer.writerow(sale[1:])


def manager_exit():
    print("We hope to see you soon ;)\n"
          "Bye Bye!")
    exit()


options = {'1': [register_sale, "Register a sale."],
           '2': [edit_sale, "Edit a Sale."],
           '3': [remove_sale, "Remove a Sale."],
           '4': [list_sales, "List the sales ranked by sellers with the highest amount sold."],
           '5': [register_sales_from_csv, "Register sales which are already registered in csv files."],
           '6': [export_to_csv, "Export sales to csv."],
           '7': [manager_exit, "Exit."], }


def welcome():
    print("******************************************\n"
          "* Welcome to the shopee's sales manager! *\n"
          "******************************************\n")


def user_input():
    print("How should we help you?")
    for i in options:
        print(i + " - " + options[i][1])
    option = input("Please select an option number presented above: ").strip()
    print()
    execute_option(option)
    print()
    user_input()


if __name__ == '__main__':
    welcome()
    user_input()
