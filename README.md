Magnetron
=========

Introduction
------------
Magnetron is a Python script to remove unwanted trackers from a magnet link.

Usage
-----
There is 2 possible arguments, one of them is mandatory:

- '--uri URI' or '-u URI' is the mandatory argument, it's the magnet link to be cleaned up,

- '--redirect-to PROG' or '-r PROG' is an optional argument that is used to open the link. This option works with 'transmission-gtk' or 'firefox' or whatever that can handle the magnet link.

The URI must be put into quotation marks and must be a magnet link like this :

magnet:?xt=urn:btih:AE3FA25614B753118931373F8FEAE64F3C75F5CD&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80/announce&tr=http://bigfoot1942.sektori.org:6969/announce&tr=http://tracker.trackerfix.com/announce&tr=http://torrent.ubuntu.com:6969/announce&tr=udp://tracker.coppersurfer.tk:80/announce
