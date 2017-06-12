# https://bugzilla.mozilla.org/show_bug.cgi?id=720182
# chromium thunar drag drop:
# console.log in chromium press F12

# http://code.google.com/p/html5uploader/
# http://stackoverflow.com/questions/6513192/html5-drag-n-drop-file-upload

"""
<!DOCTYPE html>
<html>
	<head>
		<title>Drag'n'drop test</title>
		<meta charset="utf-8">
		<script type="text/javascript">
			window.ondragover = function(e) {e.preventDefault()}
			window.ondrop = function(e) {
				e.preventDefault();
				console.log(e.dataTransfer.files[0]);
			}
		</script>
	</head>
	<body>
		(drop a file here)
	</body>
</html>
"""
