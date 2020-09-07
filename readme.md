This is the beginnings of an [Autelis Pool Controller](http://autelis.com/) integration for [Home Assistant](https://www.home-assistant.io/).

Currently this integration supports:

* A config UI that allows you to enter the host and password of your Autelis controller
* Switches for the Pumps/Aux allowing you to turn them On and Off
  * They are currently set for my aux names.  Will work on pulling the names from the autelis controller soon
* Sensors for 
    * Air Temp
    * Solar Temp
    * Spa Temp
    * Pool Temp
* Unable to turn on pool or spa heat or solar heat yet and unable to set goal temp
  * (Currently working on this)

#Not Currently Supported
* Variable Speed Pumps
* "Chemistry" pages
* Color Lights
