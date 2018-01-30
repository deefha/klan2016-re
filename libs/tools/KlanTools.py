import requests, hashlib
from objdict import ObjDict
from tqdm import tqdm
from yaml import load as yaml_load



def config_load(config_path):
	with open(config_path) as f:
		config_yaml = yaml_load(f)

	config = ObjDict(ObjDict(config_yaml).dumps())

	return config



def issue_download(config, issue, issue_path):
	session = requests.Session()
	response = session.get(config.origin.main % issue.origin.key, stream = True)

	for key, value in response.cookies.items():
		if key.startswith(config.origin.confirm_key):
			response = session.get(config.origin.confirm % (issue.origin.key, value), stream = True)

	with open(issue_path, "wb") as f:
		with tqdm(total=issue.origin.size, unit="B", unit_scale=True, ascii=True, leave=False) as pbar: 
			for chunk in response.iter_content(32 * 1024):
				if chunk:
					f.write(chunk)
					pbar.update(len(chunk))



def issue_md5(config, issue, issue_path):
	hash_md5 = hashlib.md5()

	with tqdm(total=issue.origin.size, unit="B", unit_scale=True, ascii=True, leave=False) as pbar:
		with open(issue_path, "rb") as f:
			for chunk in iter(lambda: f.read(4 * 1024), b""):
				hash_md5.update(chunk)
				pbar.update(len(chunk))

		pbar.update(abs(issue.origin.size - pbar.n))

	return hash_md5.hexdigest()



