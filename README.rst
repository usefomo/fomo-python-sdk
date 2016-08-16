Fomo Python SDK
================

*Fomo Python SDK* is the official SDK wrapper for the `Fomo API service <https://www.usefomo.com>`_

API docs: `http://docs.usefomo.com/reference <http://docs.usefomo.com/reference>`_

Requirements
------------

- PHP Version 2.7+
- pyOpenSSL / OpenSSL with SNI support
- Python module `requests <http://python-requests.org>`_

Installation
------------

Install the latest version with

.. code-block:: bash

    $ pip install fomo


Manual User Installation
------------------------

Download `Fomo/fomo.py <Fomo/fomo.py>`_ and include the file in your Python project.

Check out our examples in `tests/test.py <tests/test.py>`_, quick usage examples:

Basic Usage
-----------

Initialize Fomo client via:

.. code-block:: python

    import Fomo
    client = Fomo.FomoClient('<token>') # Auth token can be found Fomo application admin dashboard (App -> API Access)


To create a new event:

.. code-block:: python

    event = Fomo.FomoEventBasic()
    event.event_type_id = '183' # Event type ID is found on Fomo dashboard (Templates -> Template ID)
    event.title = 'Test event'
    event.city = 'San Francisco'
    event.url = 'https://www.usefomo.com'
    created_event = client.create_event(event)
    print(created_event)


To get an event:

.. code-block:: python

    event = client.get_event('<event ID>')
    print(event)


To get all events:

.. code-block:: python

    events = client.get_events()
    print(events)


To delete an event:

.. code-block:: python

    client.delete_event('<event ID>')


To update an event:

.. code-block:: python

    event = client.get_event('<event ID>')
    event.first_name = 'John'
    updated_event = client.update_event(event)
    print(updated_event)

Support
-------

If you have questions, email us at `hello@usefomo.com <mailto:hello@usefomo.com>`_.