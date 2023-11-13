""" __init__: Initializes the ReservationManager with configuration settings read from a .ini file. It sets up two APIs for hotel and band reservations.

_handle_error: A helper method that logs exceptions and returns an error response and HTTP status code as a tuple.

get_slots_available: This method uses the get_slots_available method from the ReservationApi to retrieve available slots.

reserve_slot: Reserves a slot using the reserve_slot method from ReservationApi. It checks if the user has already made two reservations before making a new one.

release_slot: Releases a reserved slot using the release_slot method from ReservationApi. It checks if the slot is already reserved before attempting to release it.

get_slots_held: Retrieves the slots reserved by a user using the get_slots_held method from ReservationApi.

_send_request: A method that wraps the other methods for sending requests to the ReservationApi and handles exceptions.

clear_all_booked_slots: This method releases all slots held by a user.

book_first_available_slot: This method reserves the first available slot. It was used for testing purposes however now it is useless. 

    The script employs time.sleep() to introduce delays after API calls,
    mitigating API rate limiting. It also uses comprehensive exception
    handling, where all API interactions are wrapped in try-except
    blocks. Errors are processed by the _handle_error method,
    which maps exceptions to error messages and HTTP status 
    codes. This ensures a controlled flow and meaningful error reporting.

 """


import configparser
import time
import logging
import json

from typing import Tuple
from typing import Optional

import requests

from exceptions import (BadRequestError, InvalidTokenError, BadSlotError, NotProcessedError, SlotUnavailableError, ReservationLimitError, MaxRetriesExceededError)
from reservationapi import ReservationApi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


"""  
    ∗ get_slots_available method: this method should be used to check for free slots
    ∗ reserve_slot method: this method should be used to reserve a slot
    ∗ release_slot method: this method should be used to cancel a reserved slot
    ∗ get_slots_held method : this method should be used to retrieve booked slot(s)
    ∗ _send_request method: this method should be used by the above-mentioned methods to send requests and also to handle errors and failures from the API sensibly
"""


class ReservationManager:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('api.ini')

        self.hotel = ReservationApi(config['hotel']['url'], config['hotel']['key'], int(config['global']['retries']), float(config['global']['delay']))
        self.band = ReservationApi(config['band']['url'], config['band']['key'], int(config['global']['retries']), float(config['global']['delay']))


    """ Helper functions """

    


    def _handle_error(self, e: Exception) -> Tuple[str, int]:
        # Define a dictionary of error
        error_dict = {
            BadRequestError: ('A 400 Bad Request error occurred.', 400),
            InvalidTokenError: ('The API token was invalid or missing.', 401),
            BadSlotError: ('The requested slot does not exist.', 403),
            NotProcessedError: ('The request has not been processed.', 404),
            SlotUnavailableError: ('The requested slot is not available.', 409),
            ReservationLimitError: ('The client already holds the maximum number of reservations', 451)
        }

        # Return the error, if not found return a generic error message
        error_msg, status_code = error_dict.get(type(e), ('An unknown error occurred...', 500))


        # Uncomment this block if you want to see the traceback
        # 
        tb = e.__traceback__
        line_num = tb.tb_lineno
        logger.error(f"{error_msg} at line {line_num}: {e}")
        # 

        response = {'error': error_msg}

        return json.dumps(response), status_code



    def get_slots_available(self, reservation_api: ReservationApi):
        try:
            available_slots = reservation_api.get_slots_available()
            # Add a small delay after an API call to prevent API rate limiting
            time.sleep(1)
            if len(available_slots) == 0:
                logger.info('Its official: the slots are all occupied, go grab a coffee and come back later')
            else:
                # logger.info(available_slots)
                return available_slots
        except Exception as e:
            response, status_code = self._handle_error(e)
            logger.error(f" An error occurred while getting slots available: {response}")
            return response, status_code
    

    """ This functon does not check if the user has more than 2 reservations, make sure to check if the user has more than 2 bookings """
    def reserve_slot(self, reservation_api: ReservationApi, slot_id: int):
            try:
                number_of_reservations = len(self.get_slots_held(reservation_api))
                if number_of_reservations == 2:
                    raise ReservationLimitError("You have reached the limit of reservations")  # Raise an exception

                else:
                    response = reservation_api.reserve_slot(slot_id)
                    if response.get('id') == slot_id:
                        logger.info(f" Successfully reserved slot {slot_id}")
                        return 200
            except Exception as e:
                logger.info(f" An error occurred while trying to reserve a slot look below for details:")
                response, status_code = self._handle_error(e)
                return response, status_code
        

    def release_slot(self, reservation_api: ReservationApi, slot_id: int):
        slot_held = reservation_api.get_slots_held()
        time.sleep(1)
        if slot_id not in [slot['id'] for slot in slot_held]:
            message = f" Error: Slot {slot_id} is not reserved."
            logger.info(message)
            return message
        else:
            try:
                reservation_api.release_slot(slot_id)
                logger.info(f" Successfully cancelled reservation for slot {slot_id}")
            except Exception as e:
                response, status_code = self._handle_error(e)
                logger.error(f" An error occurred while trying to release this {slot_id} slot\n. {response}")
                return response, status_code


    def get_slots_held(self, reservation_api: ReservationApi):
        try:
            slot_held = reservation_api.get_slots_held()
            # We need to add a small delay after an API call to prevent API rate limiting
            time.sleep(1)
            if len(slot_held) == 0:
                # logger.info('User has no bookings')
                return slot_held
            else:
                logger.info(f" Returning slots held by the user...")
                return slot_held
        except Exception as e:
                response, status_code = self._handle_error(e)
                logger.error(f" An error occurred while trying to get slots held by the user\n: {response}")
                return response, status_code
        
    """ Using this function definetly makes the code much more consice however i have implemented the 4 functionalities 
     above before making this one so it is really not needed... """
    def _send_request(self, reservation_api: ReservationApi, action: str, slot_id: Optional[int] = None) -> requests.Response:
        for attempt in range(reservation_api.retries):
            try:
                if action == "reserve":
                    response = self.reserve_slot(reservation_api, slot_id)
                elif action == "release":
                    response = self.release_slot(reservation_api, slot_id)
                elif action == "getHeld":
                    response = self.get_slots_held(reservation_api)
                elif action == "getAvailable":
                    response = self.get_slots_available(reservation_api)
                elif action == "clearAll":
                    response = self.clear_all_booked_slots(reservation_api)
                else:
                    return f" Invalid action: {action}"
                return response
            except Exception as e:
                response, status_code = self._handle_error(e)
                logger.error(f" An error occurred while trying to process your action: {response}")
                return response, status_code
        raise MaxRetriesExceededError("Max retries exceeded.")




    def clear_all_booked_slots(self, reservation_api: ReservationApi):
        slots = reservation_api.get_slots_held()
        time.sleep(1)
        if len(slots) == 0:
            print('Every booking has been released')
            return
        else:
            for slot in slots:
                try:
                    reservation_api.release_slot(slot['id'])
                    print(f"Slot {slot['id']} released.")
                except Exception as e:
                    response, status_code = self._handle_error(e)
                    logger.error(f" An error occurred while trying to clear all bookings: {response}")
                    return response, status_code


    """ This function was used just to test the functionality of the mysession1"""
    def book_first_available_slot(self, reservation_api: ReservationApi):
        available_slots = self.get_slots_available(reservation_api)
        if not available_slots:
            logger.info("Oh my! It appears that all the slots are booked up")
            return
        first_slot_id = available_slots[0]['id']
        logger.info(f" Let's give it a shot and try to book slot {first_slot_id}. Fingers crossed!")
        try:
            reservation_response = self.reserve_slot(reservation_api, first_slot_id)
            logger.info(f" Huzzah! We've successfully booked slot {first_slot_id}. The universe is in harmony once again.")
            logger.info(f" Here are the reservation details: {reservation_response}")
        except MaxRetriesExceededError as e:
            logger.error("Oh no! We tried our best, but couldn't book the slot after multiple attempts. Maybe we'll have better luck next time.")
            logger.error(str(e))




