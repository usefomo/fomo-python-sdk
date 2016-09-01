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

        # Create event with template name
        new_event = Fomo.FomoEventBasic()
        new_event.event_type_tag = 'new-order'  # Event type tag is found on Fomo dashboard (Templates -> Template name)
        new_event.title = 'Test event'
        new_event.city = 'San Francisco'
        new_event.url = 'https://www.usefomo.com'
        # Add event custom attribute value
        new_event.add_custom_event_field('variable_name', 'value')
        created_event = client.create_event(new_event)
        self.assertIsNotNone(created_event)
        self.assertIsNotNone(created_event.id)
        self.assertEqual('variable_name', created_event.custom_event_fields_attributes[0]['key'])
        self.assertEqual('value', created_event.custom_event_fields_attributes[0]['value'])

        # Create event with template ID
        new_event = Fomo.FomoEventBasic()
        new_event.event_type_id = '183'  # Event type ID is found on Fomo dashboard (Templates -> Template ID)
        new_event.title = 'Test event'
        new_event.city = 'San Francisco'
        new_event.url = 'https://www.usefomo.com'
        # Add event custom attribute value
        new_event.add_custom_event_field('variable_name', 'value')
        created_event = client.create_event(new_event)
        self.assertIsNotNone(created_event)
        self.assertIsNotNone(created_event.id)
        self.assertEqual('variable_name', created_event.custom_event_fields_attributes[0]['key'])
        self.assertEqual('value', created_event.custom_event_fields_attributes[0]['value'])

        # Get created event
        event = client.get_event(created_event.id)
        self.assertEqual(created_event.__str__(), event.__str__())

        # List events
        events = client.get_events()
        self.assertEqual(1, len(events))

        # Update event
        event.first_name = 'John'
        event.custom_event_fields_attributes[0]['value'] = 'changed_value'
        updated_event = client.update_event(event)
        self.assertEqual(updated_event.first_name, event.first_name)
        self.assertEqual('variable_name', updated_event.custom_event_fields_attributes[0]['key'])
        self.assertEqual('changed_value', updated_event.custom_event_fields_attributes[0]['value'])

        # Delete event
        event_delete_response = client.delete_event(event.id)
        self.assertEqual('Event successfully deleted', event_delete_response.message)


if __name__ == '__main__':
    unittest.main()
