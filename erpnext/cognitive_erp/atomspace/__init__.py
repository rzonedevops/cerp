"""
AtomSpace Module

Manages the global atomspace instance and provides integration with ERP entities.
"""

from ..hypergraph import AtomSpace

# Global atomspace instance
_global_atomspace = None


def get_atomspace() -> AtomSpace:
	"""Get or create the global atomspace instance."""
	global _global_atomspace
	if _global_atomspace is None:
		_global_atomspace = AtomSpace()
	return _global_atomspace


def reset_atomspace():
	"""Reset the global atomspace (useful for testing)."""
	global _global_atomspace
	if _global_atomspace:
		_global_atomspace.clear()
	_global_atomspace = AtomSpace()


__all__ = ["get_atomspace", "reset_atomspace"]
