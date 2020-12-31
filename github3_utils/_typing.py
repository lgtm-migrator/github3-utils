# stdlib
import sys

# 3rd party
from typing_extensions import _TypedDictMeta

__all__ = ["make_typed_dict"]


def make_typed_dict(typename, *args, total=True, **kwargs):
	# Temporary fix until https://github.com/python/typing/issues/761 is merged
	# From CPython
	# PSF Licensed
	# Copyright Python Software Foundation

	if not args:
		raise TypeError("TypedDict.__new__(): not enough arguments")

	if args:
		try:
			fields, = args  # allow the "_fields" keyword be passed
		except ValueError:
			raise TypeError(
					f'TypedDict.__new__() takes from 2 to 3 positional arguments but {len(args) + 2} were given'
					)
	else:
		fields = None

	if fields is None:
		fields = kwargs
	elif kwargs:
		raise TypeError("TypedDict takes either a dict or keyword arguments, but not both")

	ns = {"__annotations__": dict(fields), "__total__": total}
	try:
		# Setting correct module is necessary to make typed dict classes pickleable.
		ns["__module__"] = sys._getframe(1).f_globals.get("__name__", "__main__")
	except (AttributeError, ValueError):
		pass

	return _TypedDictMeta(typename, (), ns, total=total)