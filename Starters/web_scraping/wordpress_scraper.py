'''
This script requires python >= 3.4.
It has two non-default python modules, so you can install them with pip.
pip install requests
pip install aiohttp
You will need to modify the endpoints at the beginning of this script.
'''

ENDPOINT = 'https://SOMEWORDPRESSENDPOINT'

import aiohttp
import requests

import asyncio
import json
import os
from os import path

import glob

def get_all_from_endpoint(endpoint):

	i = 1
	totalpages = 1

	all_results = []

	while i <= totalpages:
		payload = {'page': i}

		r = requests.get(endpoint, params=payload, timeout=10.0)

		totalpages = int(r.headers['X-WP-TotalPages'])

		if r.status_code != 200:
			# todo: do something
			pass

		j = r.json()
		all_results += j

		i += 1

	return all_results

results = get_all_from_endpoint(ENDPOINT)

with open('results.json', 'w') as f:
	json.dump(results, f, ensure_ascii=False)

asset_urls = []
for a in results:

	try:
		# todo: put your own logic here for getting asset urls from the object.
		# "acf" is just a wordpress thing.
		acf = a['acf']
		if 'image' in acf and acf['image']:
			asset_urls.append(acf['image'])
		elif 'video' in acf and acf['video']:
			asset_urls.append(acf['video'])
	except Exception as e:
		pass

# print(asset_urls)

SAVE_PATH = 'saved' # note, this directory must exist!

def get_savepath(asset_url):

	head, tail = path.split(asset_url)  # 'some_folder', 'foo.mp4'
	savepath = path.join(SAVE_PATH, tail)
	return savepath

all_savepaths = [get_savepath(asset_url) for asset_url in asset_urls]

all_data = zip(asset_urls, all_savepaths)

# delete the superfluous files in the SAVE_PATH folder
files_to_delete = set([get_savepath(a) for a in glob.glob(SAVE_PATH+'/*')]) - set(all_savepaths)

# OPTIONAL: delete files that are in the local filesystem but weren't recently listed by the server
# for file_to_delete in list(files_to_delete):
# 	print('deleting file: ' + str(file_to_delete))
# 	os.remove(file_to_delete)

async def download_asset(data):

	asset_url = data[0]
	savepath = data[1]

	if path.isfile(savepath):
		# the file already exists so don't redownload it
		return

	async with aiohttp.ClientSession() as session:
		print('downloading: ' + str(asset_url))
		# https://docs.aiohttp.org/en/stable/client.html
		async with sem, session.get(asset_url) as resp:
			with open(savepath, 'wb') as fd:
				chunk_size = 1024 * 64
				while True:
					chunk = await resp.content.read(chunk_size)
					if not chunk:
						break
					fd.write(chunk)

if all_data:
	NUM_SIMULTANEOUS_DOWNLOADS = 5
	sem = asyncio.Semaphore(NUM_SIMULTANEOUS_DOWNLOADS)
	loop = asyncio.get_event_loop()
	f = asyncio.wait([download_asset(data) for data in all_data])
	loop.run_until_complete(f)
	print('downloaded all assets')
else:
	print('Skipped downloading assets.')
