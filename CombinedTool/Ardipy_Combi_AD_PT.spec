# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Ardipy_Combi_AD_PT.py'],
             pathex=['C:\\msys64\\home\\nomis\\Ardipy\\CombinedTool',
                     'C:\\msys64\\home\\nomis\\Ardipy',
                     'C:\\msys64\\home\\nomis\\Ardipy\\Tool',   
                     'C:\\msys64\\home\\nomis\\Ardipy\\ADGraph',
                     'C:\\msys64\\home\\nomis\\Ardipy\\PortControler',                     
                     ],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Ardipy_Combi_AD_PT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )