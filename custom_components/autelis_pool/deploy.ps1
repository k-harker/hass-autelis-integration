# docker pull homeassistant/home-assistant:stable
# docker run --volume=/host_mnt/d/HomeAssistant/config:/config --workdir=/config -p 8123:8123 --name home-assistant homeassistant/home-assistant:stable
& robocopy ./ "D:\HomeAssistant\config\custom_components\autelis_pool\" /MIR
& docker restart home-assistant