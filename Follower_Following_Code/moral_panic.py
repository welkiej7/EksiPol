from mp_tools import MorPan
import logging
import json
from tqdm import tqdm
import os 
import time 

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG)

if __name__ == '__main__':
    pan = MorPan()
    login_bool = input('Do you want to Login first? Y / N \n')
    if login_bool not in ['Y', 'N']:
        raise ValueError('You must answer with Y (yes) or N (no).\n')

    logging.info(f'Establishing the Connection')
    if login_bool == 'Y':
        try:
            pan.login()
        except Exception as e:
            logging.error(f'An Error Occurred: {e}')

    # Get the User Names from a File Named users.json
    file_name_to_save = input('Please give the file name to save.\n')

    with open('users.json', 'r') as file:
        users = json.load(file)['users']

    return_data = {}  # Initialize return_data outside the loop

    for i in tqdm(users, desc='Scraping the Info'):
        try:
            user_basic_info = pan.get_user_info_basic(i)
            time.sleep(3)
            user_followers = pan.get_user_followers(i)
            time.sleep(3)
            user_following = pan.get_user_following(i)
            time.sleep(3)

            logging.info(f'Finished the Author {i}')
            return_data[i] = {}  # Initialize the dictionary for user i
            return_data[i]['basic_infos'] = user_basic_info
            return_data[i]['followers'] = user_followers
            return_data[i]['following'] = user_following

            with open(file_name_to_save, 'w') as file:
                json.dump(return_data, file, indent=2)

        except Exception as e:
            logging.warning(f'An exception occurred: {e}, username {i}')
            
            
