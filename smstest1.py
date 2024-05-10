#testing the email alert

import yagmail
password = "mqahcvnfosaeoxpi"
yag = yagmail.SMTP('antitheft61@gmail.com', password)
yag.send(to = 'ginikannaobi@gmail.com',
         subject = "INTRUDER",
         contents = "Intruder alert, please check your dashboard")
print("Email sent")