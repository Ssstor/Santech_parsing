try:
    import os
    
    os.system('cd ' + os.path.realpath(__file__).split('start.py')[0] + ' && scrapy crawl santech_parser')
    print('<p align="center"><font color=green>Parsed!<font></p>')
    
except Exception as error:
    print('<p align="center"><font color=red>Error!<font></p>')
    print(f'<pre>{error}</pre>')
