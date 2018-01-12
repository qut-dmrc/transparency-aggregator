"""
Download and cache files from the internet
"""
import re
import urllib
import urllib.request
import os.path

class Downloader:
	def download(self, url, dst_dir):
		"""
		download a file from url, and cache it in dst_dir, unless it's already downloaded
		returns a path to the file
		"""
		dst_file = os.path.join(dst_dir, self.url_to_filename(url))
		if (os.path.isfile(dst_file)):
			return dst_file
		res = urllib.request.urlretrieve(url, dst_file)
		return res[0]

		
	def url_to_filename(self, url):
		"""
		convert a url to a string that can be used as a filename
		"""
		return re.sub("[^a-zA-Z0-9]", "_", url)

