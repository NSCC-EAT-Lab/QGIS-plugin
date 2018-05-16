"""
This Process takes place within mainPlug
"""

# Within initGui


self.add_action(
    icon_path,
    store_val=3,
    text=self.tr(u'Calculate NDVI'),
    callback=self.run_calc_ndvi,
    dialog=ImportExportDialog()
)

"""
This function does a couple things and requires a couple things,
    icon_path is the path to the Icons within the Resources
    store_val is the Storage within the actions array, This needs to be unique and static as it's referenced within the callback

    text uses the Traslator call (self.tr) to display the Name of the function within the menu bar

    Callback requires the pointer to the function ( Basically a C level call that looks like (void callback (*f)) this basically
    allows QGIS to Call that Function, (Basically, just type the name of the Function you wish to pass without the ()

    Dialog references the Call to the UI handler. Which is mostly a copy paste job working off of either mainPlug_dialog
    for generics or file_input_dialog for Input stuff (importexport_dialog is a little more complex but can still be reworked)
"""
