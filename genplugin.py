#!/usr/bin/env  python
#coding=utf-8
import os,sys,re
import shutil

def createDIR(dirs=None):
    for xdir in dirs:
        os.system("rm -rf  %s"%xdir )

    for xdir in dirs:
        os.system("mkdir -p  %s"%xdir)


def getPlugin(nspace, mclass,opath):
    lowerclass = mclass.lower()
    tpl="""<?xml version="1.0" encoding="UTF-8"?>
<plugin xmlns="http://apache.org/cordova/ns/plugins/1.0"
    id="{nspace}.{mclass}"
    version="0.0.1">
    <name>{mclass}</name>
    <engines>
        <engine name="cordova" version=">=3.7.1"/>
    </engines>

    <js-module src="www/{lowerclass}.js" name="{lowerclass}">
        <clobbers target="{lowerclass}" />
    </js-module>

    <!-- android -->
    <platform name="android">
        <config-file target="res/xml/config.xml" parent="/*">
            <feature name="{mclass}">
                <param name="android-package" value="{nspace}.{mclass}" />
            </feature>
        </config-file>
        <source-file src="src/android/{mclass}.java" target-dir="src/{opath}" />
	<hook type="after_plugin_install" src="scripts/afterBuild.js" />
    </platform>

</plugin>
""".format(**locals())
    return tpl


def getBuidJScript():
    tpl ="""#!/usr/bin/env node
module.exports = function(context) {
	console.log("plugin install");
};
"""
    return tpl


def getWebJS(mclass, mfunc):
    tpl="""var exec = require('cordova/exec');
    var channel = require('cordova/channel');

    channel.createSticky('onCordovaInfoReady');
    channel.waitForInitialization('onCordovaInfoReady');
    
    var {mclass} = function() {{}};
    {mclass}.prototype.{mfunc} = function (arg0 ,arg1 ,successCallback, errorCallback) {{
        //對應javascript  cordova.exec(SuccessFn,  FailFn , Device , Fn , [ ]) //Fn即為發佈的function
        cordova.exec(successCallback, errorCallback, "{mclass}", "{mfunc}", [arg0 , arg1]);
    }}

    module.exports = new {mclass}();
""".format(**locals())
    return tpl


def getClass(nspace,mclass,mfunc):
    tpl="""package {nspace};
import org.apache.cordova.CallbackContext;
import org.apache.cordova.CordovaPlugin;
import org.apache.cordova.PluginResult;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class {mclass} extends CordovaPlugin{{
    @Override
    public boolean execute(String action, final JSONArray args, final CallbackContext callbackContext) throws JSONException {{
        //return super.execute(action, args, callbackContext);

        if (action.equalsIgnoreCase("{mfunc}")){{
            JSONObject jobj = args.getJSONObject(0);
            //callbackContext.success("my call back");
            //callbackContext.error("erorr");

            //PluginResult result = new PluginResult(PluginResult.Status.OK);
            //PluginResult result = new PluginResult(PluginResult.Status.ERROR);
            //PluginResult result = new PluginResult(PluginResult.Status.NO_RESULT);
            //callbackContext.sendPluginResult( result);
            return true;
        }}
        return false;
    }}
}}
""".format(**locals())
    return tpl

def getHTML(mclass,mfunc):
    tpl="""<!DOCTYPE html>
<html>
    <head>
    <title>Hello World</title>
        <script type="text/javascript" src="cordova.js"></script>
        <script type="text/javascript" src="js/index.js"></script>
        <script>
             function test(){{
                var conf = {{
                    "name": "alex",
                    "mobile": "09138"
                }}

                {mclass}.{mfunc}( conf ,false,
                    function(message){{
                        alert(message);
                    }},
                    function(){{
                        alert("Error calling Hello Plugin");
                    }}
                );
            }}

        </script>    
    </head>
    <body>
        <button type="button" onclick="test()" >Click me </button>
    </body>
</html>
""".format(**locals())
    return tpl

def getTest():
    print ""

def main():
    if len(sys.argv ) <= 2:
        print "genplugin.py Namespace.Class Fn\ngenplugin.py com.axsoho.hello.Hello greet"
        sys.exit(-1)

    #params
    f = sys.argv[1].split(".")
    fn = sys.argv[2]
    

    mClass = f[-1]
    f.remove( mClass )
    oPath = "/".join(f)
    nSpace = ".".join(f)
    
    #create dir
    root = "myplugin"
    srccode = root + "/src/android"
    www = root + "/www"
    scripts = root + "/scripts"
    test = root + "/test"
    xdir = [  root  , srccode , www ,  scripts ,  test]
    createDIR(xdir)    

    mplugin = getPlugin(nSpace, mClass, oPath)
    open(root + "/plugin.xml"  , "w+").write(mplugin)
    
    mscript = getBuidJScript()
    open(scripts + "/afterBuild.js" , "w+").write(mscript)
    
    mclass = getClass(nSpace,mClass,fn)
    open(srccode  + "/" + mClass + ".java", "w+").write(mclass)
    
    mwebjs=getWebJS( mClass,  fn)
    open(www + "/" +  mClass.lower() + ".js", "w+").write(mwebjs)
    
    mhtml=getHTML(mClass,fn)
    open(root + "/index.html" , "w+").write(mhtml )
    print "finish"

if __name__ == '__main__':
    main()
