import os
import json
import time
import requests
from io import BytesIO

input_dir = './'
output_dir = './output'
api_url = 'http://tinypng.org/api/shrink'
tinypng_api_minimum_request_interval = 0.6

image_file_extensions = ['.jpg','.jpeg','.gif','.bmp','.tiff','.tga']

def output_path_for_dirpath(dirpath):
	output_path = os.path.join(output_dir,dirpath.replace('./',''))
	if (not os.path.isdir(output_path)):
		os.makedirs(output_path)
	return output_path

def filename_has_image_file_extension(filename):
	for ext in image_file_extensions:
		if (filename.endswith(ext)):
			return True
	return False

def log_warning(message_string,message_param):
	if (message_string == 'spacer'):
		print '[-]--------------------------------------------------------------------------[-]'
		return
	print '[!] %s %s' % (message_string,message_param)

def log_error(error_string,error_param,error_details):
	print '[E] %s %s Details: %s' % (error_string,error_param,error_details)

log_warning('Processing Images','')

os.system("rm -rf %s" % output_dir)
os.system("mkdir %s" % output_dir)

for dirpath, dirnames, files in os.walk(input_dir):		
	for f in files:
		if (dirpath.startswith(output_dir)): continue
		if f.startswith('.') or not f.endswith('.png'):
			if (filename_has_image_file_extension(f)):
				source_path = os.path.join(dirpath, f)
				output_path = os.path.join(output_path_for_dirpath(dirpath), f)
				os.system("cp %s %s" % (source_path,output_path))
				log_warning('spacer','')
				log_warning('Copied',f)
			continue
		
		foldername = os.path.basename(os.path.dirname(dirpath))
		source_path = os.path.join(dirpath, f)
		
		fh = open(source_path,'rb')
		filecontent = fh.read()
		
		log_warning('spacer','')
		log_warning('Compressing',f)

		r = requests.post(
			api_url,
			data=filecontent,
			headers={'Content-Type': 'image/png'})
		
		request_response = json.loads(r.content)
		try:
			request_response['output']['url']
		except:
			log_error('Error Compressing',f,request_response)
			continue
		compressed_image_url = request_response['output']['url']
		log_warning('Finished compressing','')
		time.sleep(tinypng_api_minimum_request_interval)
		log_warning('Downloading from',compressed_image_url)
		download_request = requests.get(compressed_image_url)
		log_warning('Finished downloading','')
		log_warning('Saving','')
		image_content = BytesIO(download_request.content).read()
		file_location = os.path.join(output_path_for_dirpath(dirpath),f)
		f = open(file_location,'wb')
		f.write(image_content)
		f.close()
		time.sleep(tinypng_api_minimum_request_interval)
log_warning('spacer','')