This is the beginnings of an [Autelis Pool Controller](http://autelis.com/) integration for [Home Assistant](https://www.home-assistant.io/).

# Currently this integration supports

* A config UI that allows you to enter the host and password of your Autelis controller
* Switches for the Pumps/Aux allowing you to turn them On and Off
* Sensors for 
    * Air Temp
    * Solar Temp
    * Spa Temp
    * Pool Temp
* Climate for
  * Pool Heat
  * Spa Heat

# Not Currently Supported

* Variable Speed Pumps
* "Chemistry" pages
* Color Lights
  
# Known Issues

* Pumps and Aux names are currently set for how my pool is set
* If the pump is in service mode everything is still enabled but doesn't function
* The values for the Temps don't change unless the pump is running.  For pool and spa they only update when in that mode.  The air temp always updates.  This is the way autelis works and there is no way to "fix" this.

