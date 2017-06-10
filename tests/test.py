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
        new_event.event_type_tag = 'new_order'  # Event type tag is found on Fomo dashboard (Templates -> Template name)
        new_event.title = 'Test event'
        new_event.first_name = 'Ryan'
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
        new_event2 = Fomo.FomoEventBasic()
        new_event2.event_type_id = '1894'  # Event type ID is found on Fomo dashboard (Templates -> Template ID)
        new_event2.title = 'Test event'
        new_event2.city = 'San Francisco'
        new_event2.url = 'https://www.usefomo.com'
        # Add event custom attribute value
        new_event2.add_custom_event_field('variable_name', 'value')
        created_event = client.create_event(new_event2)
        self.assertIsNotNone(created_event)
        self.assertIsNotNone(created_event.id)
        self.assertEqual('variable_name', created_event.custom_event_fields_attributes[0]['key'])
        self.assertEqual('value', created_event.custom_event_fields_attributes[0]['value'])

        # Get created event
        event = client.get_event(created_event.id)
        self.assertEqual(created_event.__str__(), event.__str__())

        # List events
        events = client.get_events()
        self.assertEqual(2, len(events))

        # List events with meta data
        events_with_meta = client.get_events_with_meta(30, 1)
        self.assertEqual(2, len(events_with_meta.events))
        self.assertEqual(2, events_with_meta.meta.total_count)
        self.assertEqual(30, events_with_meta.meta.per_page)
        self.assertEqual(1, events_with_meta.meta.page)
        self.assertEqual(1, events_with_meta.meta.total_pages)

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
