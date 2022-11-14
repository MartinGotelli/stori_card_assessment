import smtplib
from datetime import date
from email.mime.text import MIMEText


class MailSender:
    def send_balance_email(self, account, to_address):
        mail = MIMEText(self._mail_body(account), 'html')
        mail['Subject'] = f'Account #{account.id} Balance from Stori ©'
        mail['To'] = to_address
        from_address = 'noreply@storicard.com'
        mail['From'] = from_address
        # SMTP Configuration could be configurable (this is clearly unsecure!)
        with smtplib.SMTP_SSL('smtp.gmail.com') as server:
            server.login('integrationsmartingotelli@gmail.com', 'xymrnmwwuiqqoieq')
            server.sendmail(from_address, [to_address], mail.as_string())

    def _mail_body(self, account):
        monthly_details = [self._row_by_month(month, account) for month in range(1, 13)]
        return f'Dear {account.description},<br><br>' + \
               f'Detail of the transactions of your account with ID {account.id}:<br>' + \
               ''.join(
                   [
                       '<table border="1" style="table-layout: fixed; border-collapse: collapse;">',
                       '<colgroup><col width="100"><col width="100"><col width="100"><col width="100">',
                       '</colgroup><tbody>',
                       self._row('', '#Transactions', 'Average Debit', 'Average Credit'),
                       *monthly_details,
                       '</tbody></table>',
                       self._stori_logo()
                   ]
               )

    def _row_by_month(self, month_number, account):
        month_name = date(2022, month_number, 1).strftime('%B')
        return self._row(
            month_name,
            account.transactions_amount_on(month_number),
            account.average_debit_on(month_number),
            account.average_credit_on(month_number)
        )

    def _row(self, *values):
        tds = [self._td(value) for value in values]
        return '<tr>' + ''.join(tds) + '</tr>'

    def _td(self, text):
        return f'<td style="padding: 2px 3px; font-weight: bold; text-align: center; border: 1px solid black;">' \
               f'{text}</td>'

    def _stori_logo(self):
        return '<img src="https://ci6.googleusercontent.com/proxy' \
               '/ZkSCAaQwakssssdgazyVddAtAprCjy59z5dwW8tUBDwyxz9aVs2y6zGd4DIi44g7eURWrezsO90zPdzh4tvZpRzXggUWj1' \
               'hkqvElZ4EO7tcqN0AZt6zEuD3e2XxlPF3vKQArVraUhrutLNNuDQi6VnrXdB4m9wnJEkozvbCh4q2su8ge_fHKXfO3FI-WH86' \
               '6UrJ9_zMKeLUevLQiZtagnhXwoYHmDTGGMQ=s0-d-e1-ft#' \
               'https://s4-recruiting.cdn.greenhouse.io/external_greenhouse_job_boards/logos/400/560/600/original/' \
               'LogoStori-azul_Horizontal_-_Copy_(2).png?1634748631" width="562" height="231">'
