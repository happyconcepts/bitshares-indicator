# Testing module for bitshares-indicator
# deprecated 0.6
# bitshares-indicator copyright 2018 ben bird
# https://github.com/happyconcepts/bitshares-indicator
# mit license ~ open source software 


def dump(obj):

    for attr in dir(obj):

	if hasattr(obj, attr):

            print("obj.%s = %s" % (attr, getattr(obj, attr)))



