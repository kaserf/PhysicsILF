import tools
import olpcgames
import pygame
from sugar.graphics.radiotoolbutton import RadioToolButton
from sugar.activity import activity
from gettext import gettext as _
import gtk

class PhysicsActivity(olpcgames.PyGameActivity):
    game_name = 'physics'
    game_title = 'Physics'
    game_size = None # olpcgame will choose size

    # setup the toolbar
    def build_toolbar(self):        
        # make a toolbox
        toolbox = activity.ActivityToolbox(self)
         
        # modify the Activity tab
        activity_toolbar = toolbox.get_activity_toolbar()
        activity_toolbar.share.props.visible = False
        self.blocklist = [] 
        # make a 'create' toolbar
        create_toolbar = gtk.Toolbar()
        
        # make + add the component buttons
        self.radioList = {}
        for c in tools.allTools:                             
            button = RadioToolButton(named_icon=c.icon)
            button.set_tooltip(_(c.toolTip))
            button.connect('clicked',self.radioClicked)
            create_toolbar.insert(button,-1)    
            button.show()
            self.radioList[button] = c.name

        # add the toolbars to the toolbox
        toolbox.add_toolbar("Create",create_toolbar)
        create_toolbar.show()

        # add a ILF specific toolbar which gives feedback about problems
        #ilf_toolbar = gtk.Toolbar()
        #self.ilf_label = gtk.Label("test")
        #ilf_toolbar.insert_widget(self.ilf_label, "testlabel", None, -1)
        #self.ilf_label.show()
        #toolbox.add_toolbar("ILF", ilf_toolbar)
        #ilf_toolbar.show()
       
        
        toolbox.show()
        self.set_toolbox(toolbox)
        toolbox.set_current_toolbar(1)
        return activity_toolbar

    def radioClicked(self,button):
        pygame.event.post(olpcgames.eventwrap.Event(pygame.USEREVENT, action=self.radioList[button]))

    def updateILFLabel(self, text):
        self.statusbar.push(0, text)
