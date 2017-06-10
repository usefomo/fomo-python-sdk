Fomo Python SDK
===============

*Fomo Python SDK* is the official SDK wrapper for the `Fomo API service <https://www.usefomo.com>`_

API docs: `http://docs.usefomo.com/reference <http://docs.usefomo.com/reference>`_

Requirements
------------

- Python version [2.7+, 3.x+]
- pyOpenSSL / OpenSSL with SNI support
- Python module `requests <http://python-requests.org>`_

Installation
------------

Install the latest version with

.. code-block:: bash

    $ pip install fomo


Manual User Installation
------------------------

Download `Fomo/fomo.py <https://github.com/usefomo/fomo-python-sdk/blob/master/Fomo/fomo.py>`_ and include the file in your Python project.

Check out our examples in `tests/test.py <https://github.com/usefomo/fomo-python-sdk/blob/master/tests/test.py>`_, quick usage examples:

Basic Usage
-----------

Initialize Fomo client:

.. code-block:: python

    import Fomo
    client = Fomo.FomoClient('<token>')  # Auth token can be found Fomo application admin dashboard (App -> API Access)


Create a new event with template name:

.. code-block:: python

    event = Fomo.FomoEventBasic()
    event.event_type_tag = 'new_order'  # Event type tag is found on Fomo dashboard (Templates -> Template name)
    event.email_address = 'ryan.kulp@usefomo.com' # used to fetch Gravatar for notification image
    event.title = 'Test event'
    event.city = 'San Francisco'
    event.url = 'https://www.usefomo.com'

    # Add event custom attribute value
    event.add_custom_event_field('variable_name', 'value')

    created_event = client.create_event(event)
    print(created_event)

or with template ID:

.. code-block:: python

    event = Fomo.FomoEventBasic()
    event.event_type_id = '183'  # Event type ID is found on Fomo dashboard (Templates -> Template ID)
    event.title = 'Test event'
    event.city = 'San Francisco'
    event.url = 'https://www.usefomo.com'

    # Add event custom attribute value
    event.add_custom_event_field('variable_name', 'value')

    created_event = client.create_event(event)
    print(created_event)


Fetch an event:

.. code-block:: python

    event = client.get_event('<event ID>')
    print(event)


Get events:

.. code-block:: python

    events = client.get_events(30, 1)
    print(events)


Get events with meta data:

.. code-block:: python

    data = client.get_events_with_meta(30, 1)
    print(data.events)
    print(data.meta.per_page)
    print(data.meta.page)
    print(data.meta.total_count)
    print(data.meta.total_pages)


Delete an event:

.. code-block:: python

    client.delete_event('<event ID>')


Update an event:

.. code-block:: python

    event = client.get_event('<event ID>')
    event.first_name = 'John'
    updated_event = client.update_event(event)
    print(updated_event)

Support
-------

If you have questions, email us at `hello@usefomo.com <mailto:hello@usefomo.com>`_.
