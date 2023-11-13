""" Reservation API wrapper

This class implements a simple wrapper around the reservation API. It
provides automatic retries for server-side errors, delays to prevent
server overloading, and produces sensible exceptions for the different
types of client-side error that can be encountered.
"""

import requests
import simplejson
import warnings
import time



from requests.exceptions import HTTPError
from exceptions import (
    BadRequestError, InvalidTokenError, BadSlotError, NotProcessedError,
    SlotUnavailableError,ReservationLimitError)

"""
    Args:
        base_url: The URL of the reservation API to communicate with.
        token: The user's API token obtained from the control panel.
        retries: The maximum number of attempts to make for each request.
        delay: A delay to apply to each request to prevent server overload.
"""
class ReservationApi:

    def __init__(self, base_url: str, token: str, retries: int, delay: float):
        """ Create a new ReservationApi to communicate with a reservation
        server."""

        self.base_url = base_url
        self.token    = token
        self.retries  = retries
        self.delay    = delay

    def _reason(self, req: requests.Response) -> str:
        """Obtain the reason associated with a response"""
        reason = ''

        # Try to get the JSON content, if possible, as that may contain a
        # more useful message than the status line reason
        try:
            json = req.json()
            reason = json['message']

        # A problem occurred while parsing the body - possibly no message
        # in the body (which can happen if the API really does 500,
        # rather than generating a "fake" 500), so fall back on the HTTP
        # status line reason
        except simplejson.errors.JSONDecodeError:
            if isinstance(req.reason, bytes):
                try:
                    reason = req.reason.decode('utf-8')
                except UnicodeDecodeError:
                    reason = req.reason.decode('iso-8859-1')
            else:
                reason = req.reason

        return reason


    def _headers(self) -> dict:
        """Create the authorization token header needed for API requests

        * The dictionary has a single key-value pair.
        * The key is "Authorization".
        * The value is a string that includes the token associated with
        * the current instance of the class.
        
        """

        return {'Authorization': f'Bearer {self.token}'}
        



    def _send_request(self, method: str, endpoint: str) -> dict:
        """Send a request to the reservation API and convert errors to
           appropriate exceptions"""
        url = f'{self.base_url}{endpoint}'
        # Check if the Halo installed in kilburn
        # spinner = Halo(text=f'Connecting to: {url} ', spinner='dots')
        # spinner.start()


        # Allow for multiple retries if needed
        for attempt in range(self.retries):
            # Perform the request.
            response = requests.request(method, url, headers=self._headers())
            # Delay before processing the response to avoid swamping server.
            time.sleep(self.delay)
            # 200 response indicates all is well - send back the json data.
            if response.status_code == 200:
                return response.json()
            # 5xx responses indicate a server-side error, show a warning
            # (including the try number).
            elif response.status_code >= 500:
                warnings.warn(f"\n\n    | WARNING: Retry ({attempt+1}/{self.retries}): {self._reason(response)}\n")
            # 400 errors are client problems that are meaningful, so convert
            # them to separate exceptions that can be caught and handled by
            # the caller.
            elif response.status_code >=400 & response.status_code < 500:
                if response.status_code == 400:
                    raise BadRequestError(self._reason(response))
                elif response.status_code == 401:
                    raise InvalidTokenError(self._reason(response))
                elif response.status_code == 403:
                    raise NotProcessedError(self._reason(response))
                elif response.status_code == 404:
                    raise BadSlotError(self._reason(response))
                elif response.status_code == 429:
                    raise ReservationLimitError(self._reason(response))
                # Cancelling:
                elif response.status_code == 409:
                    raise SlotUnavailableError(self._reason(response))
                elif response.status_code == 403:
                    raise NotProcessedError(self._reason(response))

            # Anything else is unexpected and may need to kill the client.
            else:
                raise NotProcessedError(f'\nLooks like we have a code red:{response.status_code}: {self._reason(response)} Who let the bugs out again?')

        # Get here and retries have been exhausted, throw an appropriate
        # exception.
        raise ReservationLimitError(f'\nThat\'s a lot of responses for me, oh boy need to calm down from this many responses: {self.retries} ')






        # Add time sleep here to avoid server overload
    def get_slots_available(self):
        """Obtain the list of slots currently available in the system"""
        response = self._send_request('GET', '/reservation/available')
        time.sleep(self.delay)
        return response


    def get_slots_held(self):
        """Obtain the list of slots currently held by the client"""
        response = self._send_request('GET', '/reservation')
        time.sleep(self.delay)
        return response


    def release_slot(self, slot_id):
        """Release a slot currently held by the client"""
        response = self._send_request('DELETE', f'/reservation/{slot_id}')
        time.sleep(self.delay)
        return response


    def reserve_slot(self, slot_id):
        """Attempt to reserve a slot for the client"""
        response = self._send_request('POST', f'/reservation/{slot_id}')
        time.sleep(self.delay)
        return response





