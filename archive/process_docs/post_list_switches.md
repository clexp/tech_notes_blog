1. The excitement of a new switch: learning old commands and new tricks

(unboxing, shiny ports, CLI expectations vs reality)

2. Access, it always starts here: web, serial, telnet, ssh
   (the four doors into the switch; pros/cons of each)

3. Serial cables and COM ports: retro tech in a modern rack
   (bios settings, tty struggles, why ssh-over-serial is tricky)

4. Web management panels: when convenience meets security
   (http vs https, certs, TLS/SSL choices, access lockdown)

5. Fighting ‘sensible defaults’ on an immutable distro
   (Bluefin toolbox, ostree, NetworkManager battles, tiny telnet at huge cost)

6. Telnet, nostalgia or nightmare?
   (commands that work, commands that don’t, living without backspace)

7. The serial console: slow, stubborn, and still essential
   (direct head works, ssh fails, alternatives like ser2net)

8. Towards a management strategy
   (locking down telnet, deciding between web/ssh/serial, documenting the journey)

9. The excitement of a new switch, learning old commands and new methods

- unboxing that new smell, shiny fingerprint less cables
- examining imports and sfp sockets
- Learning from online courses, cisco switches and familiar unixy commands the historical commands and the new practices

2. Access, it always starts here.

- web, serial, telnet and ssh
- web, getting to the default ip
- serial :theres a cable but what do I do with it, which goes where, and then what
- telnet: sounds easy, and secure?
- ssh: that was very easy and fast (see serial cable conflicts)

3. Serial cables and com ports from the server

- getting it with a direct head is easy and responsive, but having a head on a server isn't
- accessing tty/screen over ssh: cannot see the com port in screen. then what?
- checkeing enabled in the bios - it was trying the other port? user in dialout group?
- screen over ssh works but unusable, loss of chars both ways, and breaks the direct head
- is this a no buffer problem or 2 users acessing the same ttyS0?
- screen no better, minicom no better, picocom no beter, with or without screen-tty over ssh

4. webmin panels, http/https, tls and ssl from the framework, direct link only

- can access the panel, nicely laid out and complete
- security settings for access, http/s
-

5. fighting 'sensible defaults' on bluefin

- immutble distro and installing telnet
- toolbox versus ostree, a 230mb 'not-vm' user land for a tiny telnet program
- ostree, mutating the immutable? - a whole reboot for tiny telnet?
- nmcli dropping the ip endless resetting defaults

6. working telnet (little material yet)

- the manual is massive,
- what are the most used commands
- command line 'state' for 'menus' as setting

7. working serial cable (little material yet)
