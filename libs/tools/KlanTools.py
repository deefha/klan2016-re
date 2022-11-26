import hashlib, json, requests
from objdict import ObjDict
from tqdm import tqdm
from yaml import unsafe_load as yaml_load
from bs4 import BeautifulSoup


def config_load(config_path):
	with open(config_path) as f:
		config_yaml = yaml_load(f)

	config = ObjDict(json.dumps(config_yaml))

	return config


def issue_download(config, issue, issue_path):
	session = requests.Session()
	response = session.get(config.origin.main % issue.origin.key, stream = True)

	soup = BeautifulSoup(response.text, features="html.parser")
	download_url = soup.select(config.origin.download_element)[0][config.origin.download_attribute]
	response_download = session.get(download_url, stream = True)

	with open(issue_path, "wb") as f:
		with tqdm(total=issue.origin.size_packed, unit="B", unit_scale=True, ascii=True, leave=False) as pbar: 
			for chunk in response_download.iter_content(32 * 1024):
				if chunk:
					f.write(chunk)
					pbar.update(len(chunk))


# TODO unify functions
def issue_packed_md5(config, issue, file_issue_packed):
	hash_md5 = hashlib.md5()

	with tqdm(total=issue.origin.size_packed, unit="B", unit_scale=True, ascii=True, leave=False) as pbar:
		with open(file_issue_packed, "rb") as f:
			for chunk in iter(lambda: f.read(4 * 1024), b""):
				hash_md5.update(chunk)
				pbar.update(len(chunk))

		pbar.update(abs(issue.origin.size_packed - pbar.n))

	return hash_md5.hexdigest()


# TODO unify functions
def issue_iso_md5(config, issue, file_issue_iso):
	hash_md5 = hashlib.md5()

	with tqdm(total=issue.origin.size, unit="B", unit_scale=True, ascii=True, leave=False) as pbar:
		with open(file_issue_iso, "rb") as f:
			for chunk in iter(lambda: f.read(4 * 1024), b""):
				hash_md5.update(chunk)
				pbar.update(len(chunk))

		pbar.update(abs(issue.origin.size - pbar.n))

	return hash_md5.hexdigest()
