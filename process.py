import re
import urllib.robotparser
import warcat.model
import glob
import json
f = open("disallows.txt", "a+")
for filename in glob.glob('warc_files\\*.gz'):

	warc = warcat.model.WARC()
	warc.load(filename)

	print(len(warc.records))

	for record in warc.records:
	    fields = record.header.fields

	    if fields['WARC-Type'] == 'response' and fields['WARC-Target-URI'].endswith('/robots.txt'):
	        url = fields['WARC-Target-URI']
	        content_body = record.content_block.payload.get_file().read()
	        content_text = content_body.decode('utf8', 'replace')

	        robots_parser = urllib.robotparser.RobotFileParser()
	        robots_parser.parse(content_text.split('\n'))
	        bot = 'Googlebot'
	        disallow = '/'
	        if not robots_parser.can_fetch(bot, disallow):
	            #output = url + '\n' + 'User-Agent:' + bot + '\n' + 'Disallow: ' + disallow + '\n---\n'
	            output = url + '\n'
	            print(output)
	            f.write(output)

