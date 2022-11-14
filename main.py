from model.account import Account
from managers.accounts_manager import AccountManager
from services.mail_sender import MailSender
from services.transactions_importer import TransactionsImporter


def run():
    print(
        'Select an option:',
        '1 - Check Balance',
        '2 - Delete an Account',
        '3 - Import Transactions and Send Notification',
        sep='\n'
    )
    option = input().strip()
    if option not in ['1', '2', '3']:
        print('Invalid action!')
        run()

    print('Insert account id:')
    account_id = input()
    if option == '1':
        get_account(account_id)
    elif option == '2':
        account = get_account(account_id)
        if account:
            print('Confirm deletion of account [Y/n]:')
            confirmation = input().lower()
            if confirmation == '' or confirmation == 'y':
                accounts_manager.delete(account)
    elif option == '3':
        account = get_or_create_account(account_id)
        print('Select file name to import:')
        file_name = input()
        try:
            TransactionsImporter(account, accounts_manager).process(file_name)
            print(f'Transactions imported satisfactorily\nCurrent balance: {account.balance()}')
            send_email(account)
        except FileNotFoundError:
            print('The selected file does not exists')

    print('Do you wish to perform another action? [Y/n]')
    confirmation = input().lower()
    if confirmation == '' or confirmation == 'y':
        run()
    else:
        print('Thank you!\nPowered by Stori ©')


def get_account(account_id):
    account = accounts_manager.get(account_id)
    if account:
        print(f'Found account with ID {account_id}: {account.description} - Balance: {account.balance()}')
        return account
    else:
        print(f'Account with ID {account_id} does not exists')


def get_or_create_account(account_id):
    account = accounts_manager.get(account_id)
    if account:
        print(f'Found account with ID {account_id}: {account.description} - Balance: {account.balance()}')
        return account
    else:
        print(f'Account with ID {account_id} does not exists, select account name:')
        account_description = input()
        return Account(account_id, account_description)


def send_email(account):
    print(f'Select address to send email:')
    to = input()
    print(f'Sending mail to "{to}"')
    MailSender().send_balance_email(account, to)


if __name__ == '__main__':
    accounts_manager = AccountManager()
    try:
        run()
    except Exception as error:
        print('An unexpected error happened, please try again')
        print(error)
        run()
