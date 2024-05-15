import base64


def encode(path):
	filetype = path.split(".")[-1].lower()
	if filetype == "jpg": 
		filetype = "jpeg"
	elif filetype == "svg": 
		filetype = "svg+xml"
	with open(path, "rb") as file: 
		raw = file.read()
	encoded = base64.b64encode(raw).decode("utf-8", "surrogateescape")
	encoded = f"data:image/{filetype};base64," + encoded
	return encoded


if __name__ == "__main__":
	in_path = input()
	print(encode(in_path))
