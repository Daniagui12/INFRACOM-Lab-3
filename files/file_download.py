import gdown

url = "https://drive.google.com/uc?id=1hUhwMC2iWWTP-Yil0wNrnpfMRZA33Ci2"
output = "files/files_server.zip"

gdown.download(url, output, quiet=False)

