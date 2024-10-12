from utils import utils

def read_data(pages):
    # for CIN Number
    print('*********** CIN **********')
    cin = []
    for page in pages:
        cin = utils.find_cin(cin, page)

    print(f'CIN Count: {len(cin)}')

    # for mail id 
    print('*********** Mail ID **********')
    mail_id = []
    for page in pages:
        mail_id = utils.find_mailid(mail_id, page)

    print(f"Mail Count: {len(mail_id)}")

    #for Pan card
    print('*********** Pan Card **********')
    pan = []
    for page in pages:
        pan = utils.find_PAN(pan, page)
    print(f"PAN Count: {len(pan)}")

    #for Date
    print('*********** Dates **********')
    date = []
    for page in pages:
        date = utils.find_date(date,page)

    print(f"Dates Count: {len(date)}")

    #for  websites
    print('*********** Website **********')
    website = []
    for page in pages:
        website = utils.find_website(website,page)

    print(f"Website Count: {len(website)}")

    #for Phone no
    print('*********** Phone No. **********')
    phone = []
    for page in pages:
        website = utils.find_phone(phone,page)

    print(f"Phone Count: {len(phone)}")


     