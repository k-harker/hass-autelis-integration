This is an [Autelis Pool Controller](https://web.archive.org/web/20211218192955/http://autelis.com/) integration for [Home Assistant](https://www.home-assistant.io/).  Since the Autelis Pool Controller is no longer being sold, this is only for those with this device for their pool.  I will continue to update this until I no longer have a working Autelis.  Mine has been working fine since 2013 and I don't currently have plans to replace it with anything different.

If the functionality you want is not available, feel free to send me a PR or put in an issue and I'll respond as I have time.  

# Currently this integration supports

* The only version of the Autelis I have tested to work is mine.
  * Autelis Pool Control for Jandy/Zodiac (for Jandy Aqualink RS)
* A config UI that allows you to enter the host and password of your Autelis controller
* Switches (allows you to turn these items on and off)
  * for the Pumps
    * Pool
    * Spa (this is the same as putting it in Spa mode)
    * Solar Heat
    * Cleaner
  * for the Aux (e.g. lights)
    * It will use the names configured in the Autelis controller.
    * If the name starts with "AUX" or if the name is empty, it will not be included in Home Assistant.
    * If the aux name starts with "Cleaner" it will not be included so that you don't have two "Cleaner" switches
  * for the Macros
    * It will use the names configured in the Autelis controller.
    * If the name starts with "MACRO" or if the name is empty, it will not be included in Home Assistant.
* Sensors for (support both )
    * Air Temp
    * Solar Temp
    * Spa Temp
    * Pool Temp
* Climate for
  * Pool Heat
  * Spa Heat

# Not Currently Supported

* Variable Speed Pumps
* Chemistry
* Color Lights
* Battery Voltage & lowbat (Aqualink only?) 
* Freeze Protect
* Pentair Intellitouch Version - [See Issue](issues/5)

# Known Issues

* The values for some temps don't change unless the pump is running.  This looks like it's a limitation of my Aqualink RS8.
  * For pool and spa temps, they only update when in that mode. 
    * This means that the spa temp will continue to report whatever temp the spa was the last time you had the spa pump running.  I'm using the Aqualink RS8 version so if you have a different version of pool controller/Autelis, maybe yours won't do this. 
  * Solar Temp only updates when the pump is running.  
  * The air temp always updates.  

# Installation

1. Configure your Autelis
   1. Give names to any Aux or Macros you plan to use in Home Assistant, leave all the others as the defaults.
   2. If you have a dedicated Cleaner aux setup in your controller, name the Aux that is taken up `Cleaner`.
   3. Test that your Autelis works by using the local Autelis website.
   4. Make sure everything looks correct also (e.g. temps are correct), since this information is pulled from your pool controller/Autelis, if it doesn't look correct there, it will be wrong in Home Assistant.
2. Install this integration using HACS.  Follow the [HACS instructions for manually adding a custom repo](https://www.hacs.xyz/docs/faq/custom_repositories/).
3. In the Home Assistant UI, navigate to `Configuration` then `Integrations`. 
4. Click on the add integration button at the bottom right 
5. Select `Autelis Pool Control`. 
6. Fill out the options and save.
   - Host - Should be either the hostname or IP address of your Autelis device.
     - If you are using a different port append `:<port>` to the hostname.  (Example `192.168.1.5:8080`)
   - Password - The Autelis controller password you use to login to the controller