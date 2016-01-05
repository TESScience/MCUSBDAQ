from distutils.core import setup, Extension

module1 = Extension('mcusbdaq', 
		sources = ['mcusbdaqmodule.c', 'find_usb_daqs.c'],
		libraries = ['usb'])

setup (name = 'PackageName',
        version = '1.0',
        description = 'This is a demo package',
        ext_modules = [module1])
