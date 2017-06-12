import ogg.vorbis
import ao

filename = 'cmn-c0aeffc6.ogg'

class OggSample(object):
	def __init__(self, filename):
		id = ao.driver_id('alsa')
		self.vf = ogg.vorbis.VorbisFile(filename)
		self.device = ao.AudioDevice(id)

	def play(self):
		while 1:
			buff, bytes, _ = self.vf.read(4096)
			if bytes != 0:
				self.device.play(buff, bytes)
			else:
				self.vf.time_seek(0)
				return

sample = OggSample(filename)
sample.play()
# sample.play()
