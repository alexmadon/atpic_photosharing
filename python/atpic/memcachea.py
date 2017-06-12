import pylibmc
mc = pylibmc.Client(["127.0.0.1"], binary=True)
mc.behaviors = {"tcp_nodelay": True, "ketama": True}
mc.set("key1", "1")
