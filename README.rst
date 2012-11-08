sd-proxy
========

Intelligent HTTP proxy for proxying Server Density sd-agent payloads from within a private network

What?
-----

``sd-proxy`` is an HTTP proxy designed purely for forwarding JSON payloads from
the `Server Density <http://www.serverdensity.com/>`_ monitoring `agent
<https://github.com/serverdensity/sd-agent>`_, with optional validation of the
request, the payload and upstream request (e.g. checking the IP address that is
being eventually POSTed to is a known *Server Density* IP).

Why?
----

The main use-case for ``sd-proxy`` is to forward connections for multiple
monitored nodes inside a private network via a single known and
authorized-for-external-access node and thus avoiding giving port 80/443 access
to all your monitored nodes.

It has the secondary function of verifying payloads are correct before they
leave the network and don't contain any unwanted info-leaks.

How?
----

Install sd-proxy and run it on port ``80`` on the server you wish to proxy out
from.
Then on each server with an instance of `sd-agent` running that you wish to
proxy change your SD account host name (e.g. ``youraccount.serverdensity.com``) to point to the
IP of the proxy server, e.g. in ``/etc/hosts``::

    10.0.0.2 youraccount.serverdensity.com

And ensure that you are sending payloads to this address on HTTP not HTTPS in
your sd-agent config::

    [Main]
    sd_url: http://youraccount.serverdensity.com
    agent_key: foobarbaz

Restart the agent(s) and view the output from ``sd-proxy`` to verify that payload
requests are hitting the proxy node instead of serverdensity.com directly.

Installing sd-proxy
-------------------

You can either install PyPI::

    pip install sd-proxy
    sd-proxy path/to/your/config.json

Or from GitHub::

    git clone git://github.com/1stvamp/sd-proxy.git
    cd sd-proxy
    # you probably want to create a virtualenv here
    pip install -r requirements.txt
    python serverdensity/proxy/runserver.py path/to/your/config.json

y u no HTTPS?
-----------

.. image:: http://i0.kym-cdn.com/entries/icons/original/000/004/006/y-u-no-guy.jpg

As we're acting as a Man-In-The-Middle for agent
postbacks in order to allow the agents to postback over SSL to the proxy we
would have to spoof the SSL certificate in some way, whcih apart from being a
non-trivial problem is both bad juju and beyond the remit of the proxy.

So yeah, it's plain-jane HTTP I'm afraid, however if you use the
``use_outbound_ssl`` config directive all requests to serverdensity.com from the
proxy will be made over HTTPS.

As a workaround you could also possibly tunnel your HTTP requests to the proxy
over an SSH tunnel, but that's for you to figure out if you're really deadset
on it.

Configuration
-------------

Descriptions for all the values you can override in your ``config.json`` are
described in the `settings module <https://github.com/serverdensity/sd-proxy/blob/master/serverdensity/proxy/settings.py#L8>`_,
and there is also an `example config file <https://github.com/serverdensity/sd-proxy/blob/master/example-config.json>`_.

Swig me some WSGI
-----------------

As well as using the `gevent <http://www.gevent.org/>`_ co-operative asynchronous
runner for ``sd-proxy`` you can alternatively run the proxy as a normal Python
WSGI app using an application server like `uWSGI <http://projects.unbit.it/uwsgi/>`_
or `Gunicorn <http://gunicorn.org/>`_, just import the ``app`` instance from
``serverdensity.proxy.app`` and set the ``SD_PROXY_CONFIG`` environment
variable in ``os.environ``.
