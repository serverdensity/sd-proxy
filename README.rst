sd-proxy
========

Intelligent HTTP proxy for proxying Server Density sd-agent payloads from within a private network

What?
-----

`sd-proxy` is an HTTP proxy designed purely for forwarding JSON payloads from
the `Server Density <http://www.serverdensity.com/>`_ monitoring `agent
<https://github.com/serverdensity/sd-agent>`_, with optional validation of the
request, the payload and upstream request (e.g. checking the IP address that is
being eventually POSTed to is a known *Server Density* IP).

Why?
----

The main use-case for `sd-proxy` is to forward connections for multiple
monitored nodes inside a private network via a single known and
authorized-for-external-access node and thus avoiding giving port 80/443 access
to all your monitored nodes.

It has the secondary function of verifying payloads are correct before they
leave the network and don't contain any unwanted info-leaks.

How?
----

`Install sd-proxy`_ and run it on port `80` on the server you wish to proxy out
from.
Then on each server with an instance of `sd-agent` running that you wish to
proxy change your SD account URI (e.g. `youraccount.serverdensity.com`) to the
IP of the proxy server, e.g.::

    10.0.0.2 youraccount.serverdensity.com

And ensure that you are sending payloads to this address on HTTP not HTTPS in
your sd-agent config::

    [Main]
    sd_url: http://youraccount.serverdensity.com
    agent_key: foobarbaz

Restart the agent(s) and view the output from `sd-proxy` to verify that payload
requests are hitting the proxy node instead of serverdensity.com directly.

_Install
--------
