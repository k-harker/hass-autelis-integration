This is the beginnings of an [Autelis Pool Controller](http://autelis.com/) integration for [Home Assistant](https://www.home-assistant.io/).

# Currently this integration supports

* A config UI that allows you to enter the host and password of your Autelis controller
* Switches (allows you to turn these items on and off)
  * for the Pumps
    * Pool
    * Spa (this is the same as putting it in Spa mode)
    * Solar Heat
  * for the Aux (e.g. lights) 
    * It will use the names configured in the Autelis controller.  IIf the name starts with "AUX" or if the name is empty, it will not be included in Home Assistant
  * for the Macros
    * The names of the Macros will be pulled from the Autelis controller.  If the name starts with "MACRO" or if the name is empty, it will not be included in Home Assistant
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

* The values for the temps don't change unless the pump is running.  For pool and spa temps, they only update when in that mode.  The air temp always updates.  This means that the spa temp will continue to report whatever temp the spa was the last time you had the spa pump running.  This is the way my Autelis works.  I could add some logic to set the temps to unknown when the pumps are not running if that is desired but I haven't had a need yet.  I'm using the Pentair Intellitouch version so if you have a different version of Autelis, maybe yours won't do this.


# Installation

1. Install manually by copying all files in this folder folder into `<config_dir>/custom_components/autelis_pool`
2. Restart Home Assistant.
3. In the Home Assistant UI, navigate to `Configuration` then `Integrations`. Click on the add integration button at the bottom right and select `Autelis Pool Control`. Fill out the options and save.
   - Host - Should be either the hostname or IP address of your Autelis device. 
     - If you are using a different port append `:<port>` to the hostname.  (Example `192.168.1.5:8080`)
   - Password - The Autelis controller password you use to login to the controller