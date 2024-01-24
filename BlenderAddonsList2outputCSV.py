
import bpy
import addon_utils
import csv
from bpy.props import StringProperty

from datetime import datetime



def export_addons_to_csv(file_path):
	
    # アドオン情報を取得
    prefs = bpy.context.preferences
    used_ext = {ext.module for ext in prefs.addons}
    addons = [
        (mod, addon_utils.module_bl_info(mod))
        for mod in addon_utils.modules(refresh=False)
    ]
    # 現在の日付と時刻を取得 csv出力時に差分を把握しやすいように
    now = datetime.now()
    
    # 日付と時刻を文字列に変換
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # CSVファイルに書き込み
    with open(file_path, 'w', newline='') as csv_file:
	
        fieldnames = ['Addon Name', 'Version', 'Name+Ver', bpy.app.version_string, now_str]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # 冗長なヘッダーを書き込む
        writer.writeheader()

        # アドオン情報をCSVに書き込む エクセルにコピペして比較するなどする用途
        for mod, info in addons:
            modname = mod.__name__
            if modname in used_ext:
                addonVersionTupl = info['version'] if info['version'] else "N/A"
                
                addonVersion = 'N/A' if addonVersionTupl == 'N/A' else ','.join(map(str, addonVersionTupl))

                writer.writerow({'Addon Name': modname, 'Version': addonVersion , 'Name+Ver': modname + ' ' + addonVersion})



class ShowFileBrowser(bpy.types.Operator):

    bl_idname = "object.show_file_browser"
    bl_label = "Save CSV"
    bl_description = "output CSV File_Browser"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: StringProperty(subtype="FILE_PATH")


    def execute(self, context):

        print(self.filepath)
        export_addons_to_csv(self.filepath)
		
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager

        #デフォルトファイル名（Blenderのバージョンを入れておく、
        ver_str = ",".join(map(str, bpy.app.version))
        self.filepath = "InstalledAddonList(" + ver_str + ").csv"

        # ファイルダイアログ(ブラウザ)表示
        wm.fileselect_add(self)

        return {'RUNNING_MODAL'}



# オペレータを登録
bpy.utils.register_class(ShowFileBrowser)

# オペレータを呼び出し
bpy.ops.object.show_file_browser('INVOKE_DEFAULT')