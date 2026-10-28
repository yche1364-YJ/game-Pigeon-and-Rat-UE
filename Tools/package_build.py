import unreal, subprocess, os, shutil, glob
P = unreal.Paths
root = os.path.dirname(P.convert_relative_path_to_full(P.get_project_file_path()))
eng = P.convert_relative_path_to_full(P.engine_dir())
d = os.path.join(root, 'Content', 'NYCrossing', '_dump')
for f in glob.glob(os.path.join(d, 'shots_*.zip')): os.remove(f)
shutil.rmtree(os.path.join(d, 'shots'), ignore_errors=True)
for f in glob.glob(os.path.join(root, 'Saved', 'Screenshots', '*', '*.png')): os.remove(f)
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
out = os.path.join(root, 'Build_Package')
uat = os.path.join(eng, 'Build', 'BatchFiles', 'RunUAT.bat')
args = [uat, 'BuildCookRun', '-project=' + os.path.join(root, 'MyProject.uproject'), '-noP4',
        '-platform=Win64', '-clientconfig=Shipping', '-serverconfig=Shipping', '-installed',
        '-nocompile', '-nocompileuat', '-nocompileeditor', '-skipbuildeditor', '-cook',
        '-stage', '-package', '-pak', '-iostore', '-compressed', '-prereqs', '-nodebuginfo',
        '-archive', '-archivedirectory=' + out, '-utf8output', '-unattended']
import json, threading
pf = os.path.join(root, 'MyProject.uproject')
orig = open(pf).read()
open(os.path.join(root, 'Saved', 'MyProject.uproject.bak'), 'w').write(orig)
j = json.loads(orig)
j['Plugins'] = [p for p in j.get('Plugins', []) if p['Name'] not in ('ModelContextProtocol', 'AllToolsets', 'Terminal', 'GameplayStateTree')]
open(pf, 'w').write(json.dumps(j, indent='\t'))
for sub in [('Intermediate', 'Source'), ('Binaries',)]:
    shutil.rmtree(os.path.join(root, *sub), ignore_errors=True)
log = open(os.path.join(root, 'Saved', 'package_log.txt'), 'w')
proc = subprocess.Popen(args, stdout=log, stderr=subprocess.STDOUT, cwd=os.path.join(eng, 'Build', 'BatchFiles'),
                 creationflags=0x08000000)

def _restore():
    proc.wait()
    open(pf, 'w').write(orig)
    open(os.path.join(root, 'Saved', 'package_done.txt'), 'w').write(str(proc.returncode))
try: os.remove(os.path.join(root, 'Saved', 'package_done.txt'))
except Exception: pass
threading.Thread(target=_restore, daemon=True).start()
