import platform
import subprocess
import os
class mocha_locator_dialog(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, "Choose mocha executable location", "uk.co.thefoundry.FramePanel")
        self.path = nuke.File_Knob("path", "Path:")
        self.addKnob(self.path)
    def showDialog(self):
        result = nukescripts.PythonPanel.showModalDialog(self)
        if result:
            return (self.path.value())
class send_to_mocha():
    def getUpFr(self, node):
    #node['selected'].setValue(True)
        if node.input(0).Class()=='FrameRange':#selects framerange node, connected to the selected node
            node.input(0)['selected'].setValue(True)
        elif node.input(0) == None:
            node['selected'].setValue(True)
        else:
            self.getUpFr(node.input(0))
    #finds roto or rotopaint node, connected to the selected node
    def getUpRoto(self, node):
        index = 0
        if node.input(0) == None:
            return index
        elif node.input(0).Class()=='Roto' or node.input(0).Class()=='RotoPaint':
            index = 1
            return index
        else:
            self.getUpRoto(node.input(0))
    def getUpNode(self, node):
        if node.input(0) == None:#selects read node, connected to the selected node
            node['selected'].setValue(True)
        else:
            self.getUpNode(node.input(0))
    def __init__(self):
        self.mocha_path = self.get_mocha_path()
        if self.mocha_path != 'None':
            self.load_mocha_with_clip()
    def get_mocha_path(self):
        sys = platform.system()
        default_path = r'C:\Program Files\Imagineer Systems Ltd\mocha Pro V4\bin\mochapro.exe'
        return default_path        
    def get_readnode(self):
        try:# check if 
            selected_node = nuke.selectedNode()
        except:
            nuke.message('Please select a node')
            return 0
        if selected_node.Class() == 'Read': #checks if selected Node is "Read"
            footage_path = nuke.filename(selected_node, nuke.REPLACE)
            return footage_path
        else:
            self.getUpNode(selected_node)
            selected_node['selected'].setValue(False)
            footage_path = nuke.filename(nuke.selectedNode(), nuke.REPLACE)
            re=nuke.selectedNode()
            re['selected'].setValue(False)
            selected_node['selected'].setValue(True)
            return footage_path 
    def open_mocha_with_file(self,filepath):
        files=['mov','mp4','avi','mxf','m4a','mpvg','mpg']
        first=nuke.selectedNode().firstFrame()
        last=nuke.selectedNode().lastFrame()
        selected_node=nuke.selectedNode()
        name=str(filepath)
        
        isThereRoto = 0
        if selected_node.Class() == 'Roto' or selected_node.Class() == 'RotoPaint':
            isThereRoto = 1
            print 'We are on Roto'
        else:    
            isThereRoto = self.getUpRoto(selected_node)
            
        movFileOrNot = 0
        if name.split(".")[1] == "mov":
            movFileOrNot = 1;
            
        isRotoUpper = 0
        if isThereRoto == 1:
                isRotoUpper = 1
                
        if selected_node.Class() == 'Read':
            rin=nuke.selectedNode().firstFrame()#first frame of node, selected by user
            in_point = str(first-rin)
            out_point = str(last-rin)
        else:
            self.getUpNode(selected_node)#select read node
            selected_node['selected'].setValue(False)#unselect node selected by user
            re=nuke.selectedNode()
            rin=nuke.selectedNode().firstFrame()#read node first frame
            rout=nuke.selectedNode().lastFrame()#read node last frame
            re['selected'].setValue(False)#unselect read node
            selected_node['selected'].setValue(True)#select node, selected by user
            if first<=rin and last<rout:#frame range was edited by TimeOffset node in - direction
                self.getUpFr(selected_node)
                selected_node['selected'].setValue(False)
                fr=nuke.selectedNode()
                if fr.Class()=='FrameRange':
                    fr1=fr.firstFrame()
                    fr2=fr.lastFrame()
                    diffir=fr1-first
                    diflas=fr2-last
                    if name.split('.')[1] not in files:
                        in_point = str(first+diffir-1-rin)
                        out_point = str(rout-last+diflas-1)
                        print out_point, '1'
                    else:
                        in_point = str(first+diffir-1)
                        out_point = str(last+diflas-1)
                        print out_point, '2'
                    fr['selected'].setValue(False)
                    selected_node['selected'].setValue(True)
                else:
                    fr['selected'].setValue(False)
                    selected_node['selected'].setValue(True)
                    diffir=rin-first
                    diflas=rout-last
                    if name.split('.')[1] not in files:
                        in_point = str(first+diffir-1-rin)
                        out_point = str(rout-last+diflas-1)
                        print out_point, '3'
                    else:
                        in_point = str(first+diffir-1)
                        out_point = str(last+diflas-1)
                        print out_point, '4'
            elif first>rin and last>rout:#frame range was edited by TimeOffset node in + direction
                self.getUpFr(selected_node)
                selected_node['selected'].setValue(False)
                fr=nuke.selectedNode()
                fr['selected'].setValue(False)
                selected_node['selected'].setValue(True)
                if fr.Class()=='FrameRange':
                    fr1=fr.firstFrame()
                    fr2=fr.lastFrame()
                    diffir=first-fr1
                    diflas=last-fr2
                    if name.split('.')[1] not in files:
                        in_point = str(first-diffir-1-rin)
                        out_point = str(rout-last-diflas-1)
                        print out_point, '5'
                    else:
                        in_point = str(first-diffir-1)
                        out_point = str(last-diflas-1)
                        print out_point, '6'
                else:
                    diffir=first-rin
                    diflas=last-rout
                    if name.split('.')[1] not in files:
                        in_point = str(first-rin-diffir-1)
                        out_point = str(rout-last-diflas-1)
                        print out_point, '7'
                    else:
                        in_point = str(first-diffir-1)
                        out_point = str(last-diflas-1)
                        print out_point, '8'
            elif first>rin and last<rout:#frame range was edited by FrameRange node only
                if name.split('.')[1] not in files:
                    in_point = str(first-rin)
                    out_point = str(rout-first-1)
                    print out_point, '9'
                else:
                    in_point = str(first)
                    out_point = str(last)
                    print out_point, '10'
            elif first==rin and last==rout:#users node is directly connected to read node
                if name.split('.')[1] not in files:
                    in_point = str(first-rin-1)
                    out_point = str(rout-last-1)
                    print out_point, '11'
                else:
                    in_point = str(first-1)
                    out_point = str(last-1)
                    print in_point, out_point, '12'
        frame_rate = str(nuke.Root().fps())
        if movFileOrNot == 1:
            if isRotoUpper == 1:
                cmd = [self.mocha_path, '--in', in_point, '--out', out_point, '--frame-rate', frame_rate, filepath]
            else:
                in_point = int(in_point) - 1
                out_point = int(out_point) - 1
                in_point = str(in_point)
                out_point = str(out_point)
                cmd = [self.mocha_path, '--in', in_point, '--out', out_point, '--frame-rate', frame_rate, filepath]
        else:
            cmd = [self.mocha_path, '--in', in_point, '--out', out_point, '--frame-rate', frame_rate, filepath]
        try:
            err = subprocess.Popen(cmd) #open mocha with the project file as a separate process
        except subprocess.CalledProcessError, e:
            print "Ping stdout output:\n", e.output
        return err
    def load_mocha_with_clip(self):
        filepath = self.get_readnode()
        if filepath:
            self.open_mocha_with_file(filepath)
nuke.menu('Nodes').addCommand('CustomCommands/NukeToMocha', send_to_mocha)