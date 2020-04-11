# unifier
Series of tools for interacting with a Ubiquiti Unifi Controller.

This was inspired by [Art-of-Wifi](https://github.com/Art-of-WiFi)'s 
[Unifi-API-client library](https://github.com/Art-of-WiFi/UniFi-API-client).

I was also inspired by [finish06](https://github.com/finish06)'s [Unifi library](https://github.com/finish06/pyunifi).

## History
I really just wanted a set of quick and dirty command-line scripts to scrape out my
bandwidth usage and I was struggling to do that. The Ubuquiti Unifi Controller does
give you stats of WAN traffic on a day-by-day basis, but they give you no sum of all TX
and all RX or a sum of TX and RX (since that's what your ISP bills you on).

I had just recently upgraded my controller to 5.11 and dragged all my devices to new firmware
and was disappointed I couldn't get a summary. :unamused:

So, I did what I always do, I started searching for existing tools, then ended up rolling my own.

However, I struggled to get finish06's to report any statistics out of my controller and I wanted
this to by in Python 3. I couldn't figure out why it was only returning empty OIDs from the
Controller API's stats URLs.

So, looking into the tools put together by Art-of-Wifi, finish06's tools, and digging on
the Uniquiti Community Wiki for the Controller API, I came up with some scripts of my own.