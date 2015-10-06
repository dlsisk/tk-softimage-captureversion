# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import tank
from tank import TankError
import os
import sys
import threading

# we need a couple more things for this.
import win32com
Application = win32com.client.Dispatch('XSI.Application')
        
# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog

def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system. 
    
    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Capture to Shotgun...", app_instance, AppDialog)
    


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """
    
    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)
        
        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()
        
        # via the self._app handle we can for example access:
        # - The engine, via self._app.engine
        # - A Shotgun API instance, via self._app.shotgun
        # - A tk API instance, via self._app.tk 
        
        
        # Get values from the config
        self._movie_template = self._app.get_template("movie_template")
        self._snapshot_template = self._app.get_template("current_scene_template")
        self._version_template = self._app.get_template("sg_version_name_template")
        self._height = self._app.get_setting("height")
        self._width = self._app.get_setting("width")


        # Parse templates
        name = "Quickdaily"
        
        # now try to see if we are in a normal work file
        # in that case deduce the name from it
        curr_filename = Application.ActiveProject.ActiveScene.Filename.Value #.replace("/", os.path.sep)
        version = 0
        name = "Quickdaily"
        if self._snapshot_template.validate(curr_filename):
            fields = self._snapshot_template.get_fields(curr_filename)
            name = fields.get("name")
            version = fields.get("version")

        # calculate the increment
        fields = self._app.context.as_template_fields(self._movie_template)
        if name:
            fields["name"] = name
        if version != None:
            fields["version"] = version
        fields["iteration"] = 1
        
        # get all files
        files = self._app.tank.paths_from_template(self._movie_template, fields, ["iteration"])
        
        # get all iteration numbers
        iterations = [self._movie_template.get_fields(f).get("iteration") for f in files]
        if len(iterations) == 0:
            new_iteration = 1
        else:
            new_iteration = max(iterations) + 1
        
        # compute new file path
        fields["iteration"] = new_iteration
        mov_path = self._movie_template.apply_fields(fields)
        
        # compute shotgun version name
        sg_version_name = self._version_template.apply_fields(fields)
        
        self._fields = fields
        
        # lastly, set up our UI
        self.ui.context.setText("Current Context: %s" % self._app.context)
        self.ui.filenameLabel.setText("File Name: %s" % mov_path)
        self.ui.versionName.setText("Version Name: %s" % sg_version_name)
        self.ui.startButton.clicked.connect(self._start_capture)
        self.ui.cancelButton.clicked.connect(self._exit_app)
        
    def _start_capture(self):
        
    # First, set viewport options
        
        # We start by getting all the pieces we need.
        mov_path = self._movie_template.apply_fields(self._fields)
        fps = Application.GetValue("PlayControl.Rate")
        startFrame = Application.GetValue("PlayControl.In")
        endFrame = Application.GetValue("PlayControl.Out")
        width = self._width
        height = self._height

        # Set the codec with pre-encoded values.
        # Photo-JPEG has the framerate in its codec settings, meaning we need different values
        # depending on what our framerate is. We're getting it from the scene instead of from
        # the config file.
        format = Application.GetValue("PlayControl.Format")
        if format == 13 or fps == 23.976 or fps == 23.98:
            dscodec = "AAAAFnNwdGxqcGVn/gABAAAAAAADAAAAABR0cHJsAAAAAAAX+uEAAAAAAAAAGGRyYXQAAAAAAAAAUwAAAQAAAAEAAAAACW1wc28AAAAADG1mcmEAAAAAAAAADHBzZnIAAAAAAAAACWJmcmEAAAAACm1wZXMAAAAAABxoYXJkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKc2RuZQAAAAAADGNtZnJhcHBsAAAAAA=="
        elif format == 7 or fps == 24.0:
            dscodec = "AAAAFnNwdGxqcGVn/gABAAAAAAACAAAAABR0cHJsAAAAAAAYAAAAAAAAAAAAGGRyYXQAAAAAAAAAUwAAAQAAAAEAAAAACW1wc28AAAAADG1mcmEAAAAAAAAADHBzZnIAAAAAAAAACWJmcmEAAAAACm1wZXMAAAAAABxoYXJkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKc2RuZQAAAAAADGNtZnJhcHBsAAAAAA=="
        elif format == 10 or fps == 29.97:
            dscodec = "AAAAFnNwdGxqcGVn/gABAAAAAAADAAAAABR0cHJsAAAAAAAd+FEAAAAAAAAAGGRyYXQAAAAAAAAAUwAAAQAAAAEAAAAACW1wc28AAAAADG1mcmEAAAAAAAAADHBzZnIAAAAAAAAACWJmcmEAAAAACm1wZXMAAAAAABxoYXJkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKc2RuZQAAAAAADGNtZnJhcHBsAAAAAA=="
        elif format == 19 or fps == 30.0:
            dscodec = "AAAAFnNwdGxqcGVn/gABAAAAAAADAAAAABR0cHJsAAAAAAAeAAAAAAAAAAAAGGRyYXQAAAAAAAAAUwAAAQAAAAEAAAAACW1wc28AAAAADG1mcmEAAAAAAAAADHBzZnIAAAAAAAAACWJmcmEAAAAACm1wZXMAAAAAABxoYXJkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKc2RuZQAAAAAADGNtZnJhcHBsAAAAAA=="
        elif format == 8 or fps == 25.0:
            dscodec = "AAAAFnNwdGxqcGVn/gABAAAAAAADAAAAABR0cHJsAAAAAAAZAAAAAAAAAAAAGGRyYXQAAAAAAAAAUwAAAQAAAAEAAAAACW1wc28AAAAADG1mcmEAAAAAAAAADHBzZnIAAAAAAAAACWJmcmEAAAAACm1wZXMAAAAAABxoYXJkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKc2RuZQAAAAAADGNtZnJhcHBsAAAAAA=="
        else:
            raise TankError("Unsupported Frame Rate!")
        
        Application.SetValue("ViewportCapture.Filename", mov_path, "")
        Application.SetValue("ViewportCapture.FrameRate", fps, "")
        Application.SetValue("ViewportCapture.DSCodec", dscodec, "")
        Application.SetValue("ViewportCapture.Start",startFrame, "")
        Application.SetValue("ViewportCapture.End",endFrame, "")
        Application.SetValue("ViewportCapture.ImageWidth", width, "")
        Application.SetValue("ViewportCapture.ImageHeight", height, "")

        viewport = self.ui.viewportCombo.currentIndex() + 1

        # make sure folders exist for mov
        mov_folder = os.path.dirname(mov_path)
        self._app.ensure_folder_exists(mov_folder)

        # Capture it!
        Application.CaptureViewport(viewport,False)
        
    # Now we post it to Shotgun
        sg_version_name = self._version_template.apply_fields(self._fields)
        message = self.ui.versionText.toPlainText()
        # create sg version        
        data = {
            "code": sg_version_name,
            "description": message,
            "project": self._app.context.project,
            "entity": self._app.context.entity,
            "sg_task": self._app.context.task,
            "created_by": tank.util.get_shotgun_user(self._app.tank.shotgun),
            "user": tank.util.get_shotgun_user(self._app.tank.shotgun),
            "sg_path_to_movie": mov_path,
            "sg_first_frame": int(startFrame),
            "sg_last_frame": int(endFrame),
            "frame_count": int((endFrame - startFrame) + 1),
            "frame_range": "%d-%d" % (startFrame, endFrame),
            "sg_movie_has_slate": False
        }
        
        entity = self._app.shotgun.create("Version", data)
        """
        # and thumbnail
        if thumb:
            self.shotgun.upload_thumbnail("Version", entity["id"], thumb)
        # and filmstrip
        if filmstrip:
            self.shotgun.upload_filmstrip_thumbnail("Version", entity["id"], filmstrip)
        """
        # execute post hook
        for h in self._app.get_setting("post_hooks", []):
            self._app.execute_hook_by_name(h, mov_path=mov_path, version_id=entity["id"], comments=message)
        
        # status message!
        sg_url = "%s/detail/Version/%s" % (self._app.shotgun.base_url, entity["id"]) 
        #Application.cmds.confirmDialog()("Your submission was successfully sent to review.")
        self._app.engine.execute_in_main_thread(QtGui.QMessageBox.information, None, "Send Capture to Shotgun", "Your Submission was successfully sent to review.")
        self.close()
    def _exit_app(self):
        Application.LogMessage("Exiting CaptureVersion...")
        self.close()