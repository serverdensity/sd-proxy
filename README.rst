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

Requirements:

 * CPython >= 2.5 (should work on PyPy but untested and won't work with gevent)

If using the gevent runner you'll need  platform that
`supports gevent <http://www.gevent.org/intro.html>`_, otherwise you'll need
to run the WSGI app with something like uWSGI or Gunicon,
see the WSGI section below.

You can either install the egg from PyPI::

    pip install sd-proxy

    # If you're binding against port 80 you'll probably want to sudo the next line
    sd-proxy path/to/your/config.json

Or source from GitHub::

    git clone git://github.com/1stvamp/sd-proxy.git
    cd sd-proxy
    # you probably want to create a virtualenv here
    pip install -r requirements.txt

    # If you're binding against port 80 you'll probably want to sudo the next line
    python serverdensity/proxy/runserver.py path/to/your/config.json

As we bind against port ``80`` by default you'll either need to run
``sd-proxy`` as a priveleged process (e.g. as root) or run it on a different
port and forward to it from port ``80`` with a reverse proxy/load balancer of
some kind.
The other alternative is to hack ``sd-agent`` on your monitored nodes to post
back to a different port, but then you're maintaining your own port, things get
messy, and ``sd-proxy`` is designed to avoid that messyness.

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
or `Gunicorn <http://gunicorn.org/>`_, just set the ``SD_PROXY_CONFIG`` environment
variable in ``os.environ`` and import the ``app`` instance from
``serverdensity.proxy.app``.

Single threaded?
----------------

Yup, 1 process, 1 thread, multiple
`greenlets <http://codespeak.net/py/0.9.2/greenlet.html>`_,
and it's still pretty fast.

If you worry about wasting those precious CPU cores then you can you use
the provided ``sd-proxy-multi`` entrypoint or the ``multirunserver.py`` script
directly to run multiple forked processes attached to the same inbound port.

If you set the ``processes`` configuration value it will spawn that many,
otherwise it will spawn 1 process per detected CPU core.

Logging, yo?
------------

.. image:: http://cdn.memegenerator.net/instances/250x250/21226875.jpg

Logging in sd-proxy is admittedly pretty dumb right now, request logs (ala
Apache access logs) are spewed to the ``STDOUT`` of the main process while
warnings and errors get barfed to ``STDERR``.
Every rejection based on a directive (e.g. MD5 checksum if enabled, JSON schema
check if enabled, IP checks etc.) is logged as a warning, and application
errors get logged as errors.

This means if you want to log any of this to files for an audit trail you'll
have to redirect the output from the ``sd-proxy`` process using
tubes^W**pipes**, and optionally use something ``logrotate`` to keep the log
files from piling up too much.
