import lob
import pandas as pd
import numpy as np

def template_to_lob_postcard(row, front, back):
    if np.isnan(row['street_address_line_2']):
        row['street_address_line_2'] = ''
    print('running function...')
    to_address = {
    'name' : '{} {}'.format(row['first_name'], row['last_name']),
    'address_line1' : '{} {}'.format(row['street_address_line_1'], row['street_address_line_2']),
    'address_city' : row['city'],
    'address_state' : row['state'],
    'address_zip' : row['zipcode'],
    'address_country' : 'US',
    }
        
    front = front
    back = back
    try:
        test_lob = lob.Postcard.create(
            metadata= {'campaign':'chrissy_2414creekmanordrive_mailer'},
            to_address = to_address,
            front = front,
            back = back,
            size='6x9',
        )
        print('to address: {} '.format(to_address))
    except Exception as e:
        print('Mailing flyer for address: {} has failed! Exception: {}'.format(row['street_address_line_1'], e))
        
    
    return test_lob