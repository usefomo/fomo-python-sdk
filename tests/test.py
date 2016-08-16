import unittest

import Fomo


class TestFomo(unittest.TestCase):
    def test_example(self):
        client = Fomo.FomoClient('<token>')

        # Delete all events
        events = client.get_events()
        for event in events:
            client.delete_event(event.id)

        # Check if there is now events
        events = client.get_events()
        self.assertEqual(0, len(events))

        # Create event
        new_event = Fomo.FomoEventBasic()
        new_event.event_type_id = '183'
        new_event.title = 'Test event'
        new_event.city = 'San Francisco'
        new_event.url = 'https://www.usefomo.com'
        created_event = client.create_event(new_event)
        self.assertIsNotNone(created_event)
        self.assertIsNotNone(created_event.id)

        # Get created event
        event = client.get_event(created_event.id)
        self.assertEqual(created_event.__str__(), event.__str__())

        # List events
        events = client.get_events()
        self.assertEqual(1, len(events))

        # Update event
        event.first_name = 'John'
        updated_event = client.update_event(event)
        self.assertEqual(updated_event.first_name, event.first_name)

        # Delete event
        event_delete_response = client.delete_event(event.id)
        self.assertEqual('Event successfully deleted', event_delete_response.message)


if __name__ == '__main__':
    unittest.main()
