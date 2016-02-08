# Taemin
A beautiful IRC bot

##Setup

The usual way:

    cd taemin
    python setup.py install
 
Now just run the bot with

    /usr/local/bin/taemin

Or if /usr/local/bin is in your path:

    taemin
 
## Run taemin as a service
If you're running on debian, just copy the file located in the inid.d folder in /etc/init.d/taemin

Then run:

    service taemin start
    
##Configuration

To adjust the configuration of taemin, just edit the configuration file:

    vim /etc/taemin/taemin.yml

##Contribute

To add a plugin, just copy the example folder:

    cp -r taemin/plugins/example taemin/plugins/yourplugin

Change the class TaeminExample to YourPluginClass in the file:

    taemin/plugins/yourplugin/plugin.py

You can now add the functions of your choice in the different handlers (on_pubmsg, on_join, on_privmsg, on_quit, on_part)

To enable your plugin just add in the plugins section on your configuration file:

    plugins.yourplugin.plugin: "YourPluginClass"

