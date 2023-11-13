""" 
This script, using ReservationManager from mysession1,
manages hotel and band reservations. The Client class
has methods to get common slots (get_common_slots),
release previous bookings (release_previous_booked_slots),
book common slots (book_common_slots), check for better
slots (check_for_better_slots), and a run method tying
everything together. It books the earliest common slot,
and if a better slot becomes available, it attempts
to rebook. A Client instance is created at the end to start the process.

 """



import time
from mysession1 import ReservationManager


class Client:
    manager = ReservationManager()
    sleeping_time = 3

    def __init__(self):
        # Variables below used to check for better slots
        self.current_slot_reserved = {}
        self.check_for_better_slots_times = 3

    


    def get_common_slots(self):
        
        try:
                print(f"    |Fidning common slots...\n")

                print(f"    |Getting available slots for the hotel, please wait... \n")
                hotel_slots = self.manager._send_request(self.manager.hotel, "getAvailable")
                time.sleep(1)

                print(f"    |Getting available slots for the band, please wait... \n")
                band_slots = self.manager._send_request(self.manager.band, "getAvailable")
                time.sleep(1)

                hotel_slot_ids = set(slot['id'] for slot in hotel_slots)
                band_slot_ids = set(slot['id'] for slot in band_slots)

                # Find common slot ids
                common_slot_ids = hotel_slot_ids.intersection(band_slot_ids)
                common_slots = [slot for slot in hotel_slots if slot['id'] in common_slot_ids]
                print("    |The first 20 common available slots are:")

                slot_number = 1
                for slot in common_slots[:20]:
                    print(f"    |{slot_number}. Slot ID: {slot['id']}|")
                    slot_number += 1
                print("\n")
                return common_slots
        except Exception as e:
            print(f"    |Huston we got a problem...\n{e}\n")
            return



    def release_previous_booked_slots(self):
        print("    |Releasing previous booked slots for hotel...\n", end=' ')
        self.manager._send_request(self.manager.hotel, "clearAll")
        time.sleep(1)

        print("    |Hotel slots released, releasing previous booked slots for band...\n")
        self.manager._send_request(self.manager.band, "clearAll")
        time.sleep(1)
        print("    |Band slots released.\n")


    def book_common_slots(self):
        print("    |Welcome, to reservations manager!|\n")
        # print("    |Starting to book slots...\n")

        common_slots = self.get_common_slots()
        time.sleep(1)
        # if there are no common slots available
        if not common_slots:
            print("    |No common slots available.")
            return
        # Sort the common slots
        common_slots.sort(key=lambda x:x['id'])

        for slot in common_slots:
            # Save current slots for later use
            self.current_slot_reserved = slot

            """ !HOTEL """

            print(f"    |Booking slot {slot['id']} for the hotel. Please wait...\n")
            flag = self.manager._send_request(self.manager.hotel, "reserve", slot['id'])
            time.sleep(1)

            if flag == 200:
                print(f"    | ! Successfully booked slot {slot['id']} for the hotel !\n")   
            else:
                print(f"    |Failed to make a reservation, for hotel: {slot['id']}. Trying next slot...\n")
                continue  # Skip the rest of this iteration and try the next slot

            """ !BAND """

            print(f"    |Booking slot {slot['id']} for the band. Please wait... \n")
            flag = self.manager._send_request(self.manager.band,'reserve', slot['id'])
            time.sleep(1)

            if flag == 200:
                print(f"    | ! Successfully booked slot {slot['id']} for the band !\n ")
            else:
                print(f"    |Failed to make a reservation, for band: {slot['id']}. Releasing hotel slot and trying next slot...\n")
                self.manager._send_request(self.manager.hotel, "release", slot['id'])  # Release the hotel slot before moving to the next slot
                continue  # Skip the rest of this iteration and try the next slot

            # If we get here, it means that we successfully booked both the hotel and the band for the current slot
            break  # Exit the loop since we've successfully booked a slot

            
        # Get the booked slots
        booked_slots_hotel = self.manager._send_request(self.manager.hotel, "getHeld")
        time.sleep(1)
        booked_slots_band = self.manager._send_request(self.manager.band, "getHeld")
        time.sleep(1)



        if booked_slots_hotel ==None or booked_slots_band ==None:
            return "EXIT"
        else:
            if booked_slots_hotel[0]['id']!=booked_slots_band[0]['id']:
                return "EXIT"
            else:
                # Display the booked slots
                print("     |The booked slots are:")

                for slot in booked_slots_hotel:
                    print(f"    |Hotel - Slot ID: {slot['id']}\n")
                for slot in booked_slots_band:
                    print(f"    |Band - Slot ID: {slot['id']}\n")

                print("    |Thank you for using reservations manager!\n")




    # Before realising the slot make sure to book the better slot first
    def check_for_better_slots(self):
        print(f"    |Please wait while we check for better slots.\n")
        print(f"    |Thank you for your patience\n")

        for _ in range(self.check_for_better_slots_times):
            common_slots = self.get_common_slots()
            if common_slots:
                earliest_slot = min(common_slots, key=lambda x:x['id'])
                if self.current_slot_reserved is None or earliest_slot['id'] < self.current_slot_reserved['id']:
                    print(f"    |Better slot found: {earliest_slot['id']}\n")

                    print("    |Attempting to update the reservation...\n")

                    # Retry logic
                    retry_count = 0
                    max_retries = 1  # Adjust this to set the maximum number of retries

                    while retry_count < max_retries:
                        # Reserve new slot for hotel
                        flag_hotel = self.manager._send_request(self.manager.hotel, 'reserve', earliest_slot['id'])
                        time.sleep(1)
                        if flag_hotel == 200:
                            print(f"    |Successfully booked the better slot for the hotel: {earliest_slot['id']}\n")

                            # Reserve new slot for band
                            flag_band = self.manager._send_request(self.manager.band, 'reserve', earliest_slot['id'])
                            time.sleep(1)
                            if flag_band == 200:
                                print(f"    |Successfully booked the better slot for the band: {earliest_slot['id']}\n")

                                # If we have a previous reservation, release it
                                if self.current_slot_reserved:
                                    self.manager._send_request(self.manager.hotel, 'release', self.current_slot_reserved['id'])
                                    time.sleep(1)
                                    self.manager._send_request(self.manager.band,'release', self.current_slot_reserved['id'])
                                    time.sleep(1)
                                    print(f"    |Released previous slot: {self.current_slot_reserved['id']}\n")

                                # Update current reservation
                                self.current_slot_reserved = earliest_slot
                                break
                            else:
                                # If failed to reserve for band, release hotel and retry
                                self.manager._send_request(self.manager.hotel, 'release', earliest_slot['id'])
                                time.sleep(1)
                                print(f"    |Failed to book for the band. Released the slot for hotel: {earliest_slot['id']}\n")
                                retry_count += 1
                        else:
                            retry_count += 1
                            continue

                    if retry_count == max_retries:
                        print("    |Failed to reserve the better slot after several retries.\n")
                else:
                    print("     |No better slot found.\n")
            else:
                print(f"    |No slots available. You got the best booking\n")
        print(f"    |Finished checking for better slots.\n")
        print(f"    |Confirmed. Your reservations:{self.current_slot_reserved['id']}")



    def run(self):
        self.release_previous_booked_slots()
        self.book_common_slots()
        self.check_for_better_slots()

        


# Create the Client instance and start the GUI
client = Client()
client.run()
